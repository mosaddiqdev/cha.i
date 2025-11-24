import React from "react";
import { AlertCircle, RefreshCw } from "lucide-react";
import "./ErrorMessage.css";

const ErrorMessage = ({
  message = "Something went wrong. Please try again.",
  onRetry,
  type = "inline",
}) => {
  if (type === "banner") {
    return (
      <div className="error-banner">
        <div className="error-banner-content">
          <AlertCircle size={20} />
          <span>{message}</span>
        </div>
        {onRetry && (
          <button onClick={onRetry} className="error-retry-btn">
            <RefreshCw size={16} />
            Retry
          </button>
        )}
      </div>
    );
  }

  return (
    <div className="error-inline">
      <div className="error-icon-wrapper">
        <AlertCircle size={24} />
      </div>
      <div className="error-text">
        <p className="error-title">Error</p>
        <p className="error-description">{message}</p>
      </div>
      {onRetry && (
        <button onClick={onRetry} className="error-retry-btn-inline">
          <RefreshCw size={16} />
          Try Again
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;
