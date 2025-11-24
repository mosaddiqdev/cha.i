import { createContext, useContext, useState, useEffect } from "react";
import API from "../services/api";

const ServerStatusContext = createContext();

export const useServerStatus = () => useContext(ServerStatusContext);

export const ServerStatusProvider = ({ children }) => {
  const [isChecking, setIsChecking] = useState(true);
  const [isWakingUp, setIsWakingUp] = useState(false);
  const [isOnline, setIsOnline] = useState(false);

  useEffect(() => {
    let timeoutId;
    let isMounted = true;

    const checkServerStatus = async () => {
      // Set a timeout to show "Waking up" message if request takes too long
      timeoutId = setTimeout(() => {
        if (isMounted) setIsWakingUp(true);
      }, 2000); // 2 seconds threshold

      try {
        await API.health.check();
        if (isMounted) {
          setIsOnline(true);
          setIsWakingUp(false); // Hide wake-up message immediately on success
        }
      } catch (error) {
        console.error("Server health check failed:", error);
        if (isMounted) setIsOnline(false);
      } finally {
        if (isMounted) setIsChecking(false);
        clearTimeout(timeoutId);
      }
    };

    checkServerStatus();

    return () => {
      isMounted = false;
      clearTimeout(timeoutId);
    };
  }, []);

  return (
    <ServerStatusContext.Provider value={{ isChecking, isWakingUp, isOnline }}>
      {children}
    </ServerStatusContext.Provider>
  );
};
