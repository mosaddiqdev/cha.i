import HomeSkeleton from "./HomeSkeleton";
import { useAuth } from "../context/AuthContext";
import { Navigate, useLocation } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return <HomeSkeleton />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
