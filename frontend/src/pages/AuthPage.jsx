import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Mail, Lock, ArrowRight, AlertCircle, User } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import "./AuthPage.css";

const AuthPage = () => {
  const [isSignIn, setIsSignIn] = useState(true);
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { login, register } = useAuth();

  const validateForm = () => {
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = "Required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Invalid";
    }

    if (!isSignIn && !formData.username) {
      newErrors.username = "Required";
    } else if (!isSignIn && formData.username.length < 3) {
      newErrors.username = "Min 3 chars";
    }

    if (!formData.password) {
      newErrors.password = "Required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Min 6 chars";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (validateForm()) {
      setIsLoading(true);
      try {
        if (isSignIn) {
          await login(formData.email, formData.password);
        } else {
          await register(formData.email, formData.username, formData.password);
        }
        navigate("/");
      } catch (error) {
        setErrors({
          submit: error.message || "Authentication failed. Please try again.",
        });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (errors[e.target.name]) {
      setErrors({ ...errors, [e.target.name]: "" });
    }
  };

  const toggleMode = () => {
    setIsSignIn(!isSignIn);
    setErrors({});
    setFormData({ username: "", email: "", password: "" });
  };

  return (
    <div className="auth-centered-container">
      <div className="auth-content-wrapper">
        <div className="auth-header">
          <h1>{isSignIn ? "Welcome Back" : "Create Account"}</h1>
          <p>
            {isSignIn
              ? "Enter your credentials to continue."
              : "Join us and start your journey."}
          </p>
        </div>

        {errors.submit && (
          <div className="error-banner">
            <AlertCircle size={16} />
            <span>{errors.submit}</span>
          </div>
        )}

        <form className="auth-form" onSubmit={handleSubmit}>
          {!isSignIn && (
            <div className="input-group">
              <User className="input-icon" size={20} />
              <input
                type="text"
                name="username"
                placeholder="Username"
                className="rounded-input"
                value={formData.username}
                onChange={handleChange}
                autoComplete="username"
              />
              {errors.username && (
                <div className="error-message">
                  <AlertCircle size={16} />
                </div>
              )}
            </div>
          )}

          <div className="input-group">
            <Mail className="input-icon" size={20} />
            <input
              type="email"
              name="email"
              placeholder="Email Address"
              className="rounded-input"
              value={formData.email}
              onChange={handleChange}
              autoComplete="email"
            />
            {errors.email && (
              <div className="error-message">
                <AlertCircle size={16} />
              </div>
            )}
          </div>

          <div className="input-group">
            <Lock className="input-icon" size={20} />
            <input
              type="password"
              name="password"
              placeholder="Password"
              className="rounded-input"
              value={formData.password}
              onChange={handleChange}
              autoComplete={isSignIn ? "current-password" : "new-password"}
            />
            {errors.password && (
              <div className="error-message">
                <AlertCircle size={16} />
              </div>
            )}
          </div>

          <button type="submit" className="rounded-btn" disabled={isLoading}>
            <span>
              {isLoading ? "Processing..." : isSignIn ? "Sign In" : "Sign Up"}
            </span>
            {!isLoading && <ArrowRight size={20} />}
          </button>
        </form>

        <div className="auth-toggle">
          <span>{isSignIn ? "New here?" : "Already a member?"}</span>
          <button onClick={toggleMode} className="toggle-link">
            {isSignIn ? "Create account" : "Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
