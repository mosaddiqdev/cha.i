import { useEffect, useState } from "react";
import { useServerStatus } from "../context/ServerStatusContext";
import { Loader2, Wifi, WifiOff } from "lucide-react";
import "./ServerStatusToast.css";

const ServerStatusToast = () => {
  const { isWakingUp, isOnline } = useServerStatus();
  const [visible, setVisible] = useState(false);
  const [message, setMessage] = useState("");
  const [type, setType] = useState("info"); // info, success, error

  useEffect(() => {
    if (isWakingUp) {
      setVisible(true);
      setMessage("Waking up the server... this may take up to a minute.");
      setType("info");
    } else if (isOnline && visible) {
      // If it was visible (meaning we were waking up), show success then fade out
      setMessage("Connected! 🚀");
      setType("success");
      const timer = setTimeout(() => setVisible(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [isWakingUp, isOnline]);

  if (!visible) return null;

  return (
    <div className={`server-status-toast ${type}`}>
      {type === "info" && <Loader2 className="animate-spin" size={18} />}
      {type === "success" && <Wifi size={18} />}
      {type === "error" && <WifiOff size={18} />}
      <span>{message}</span>
    </div>
  );
};

export default ServerStatusToast;
