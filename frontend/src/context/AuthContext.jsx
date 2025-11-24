import { createContext, useContext, useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import API from "../services/api";
import HomeSkeleton from "../components/HomeSkeleton";
import ChatSkeleton from "../components/ChatSkeleton";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("token")
  );
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem("token");
      if (storedToken) {
        try {
          const userData = await API.auth.getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (error) {
          console.error("Token verification failed:", error);
          logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const data = await API.auth.login(email, password);
      setToken(data.access_token);
      setUser(data.user);
      setIsAuthenticated(true);
      setLoading(false);
      return data;
    } catch (error) {
      throw error;
    }
  };

  const register = async (email, username, password) => {
    try {
      const data = await API.auth.register(email, username, password);
      setToken(data.access_token);
      setUser(data.user);
      setIsAuthenticated(true);
      setLoading(false);
      return data;
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    API.auth.logout();
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    token,
    isAuthenticated,
    loading,
    login,
    register,
    logout,
  };

  if (loading) {
    if (location.pathname.startsWith("/chat/")) {
      return <ChatSkeleton />;
    }
    return <HomeSkeleton />;
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export default AuthContext;
