import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Home from "./pages/Home";
import ChatInterface from "./pages/ChatInterface";
import AuthPage from "./pages/AuthPage";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./context/AuthContext";
import ServerStatusToast from "./components/ServerStatusToast";
import "./index.css";

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <>
      <ServerStatusToast />
      <div className="container">
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route
            path="/auth"
            element={isAuthenticated ? <Navigate to="/" /> : <AuthPage />}
          />
          <Route
            path="/chat/:id"
            element={
              <ProtectedRoute>
                <ChatInterface />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </>
  );
}

export default App;
