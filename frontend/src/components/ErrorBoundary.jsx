import React from "react";
import "./ErrorBoundary.css";
import { AlertTriangle, RefreshCw, Home } from "lucide-react";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  handleReset = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
    window.location.href = "/";
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary-container">
          <div className="error-glass-panel">
            <div className="error-icon-wrapper">
              <AlertTriangle size={48} className="error-icon-svg" />
            </div>

            <h1 className="error-title">Something went wrong</h1>

            <p className="error-message">
              We encountered an unexpected issue. Don't worry, your data is
              safe.
            </p>

            <div className="error-actions">
              <button
                onClick={() => window.location.reload()}
                className="error-btn-primary"
              >
                <RefreshCw size={18} />
                <span>Refresh Page</span>
              </button>

              <button
                onClick={this.handleReset}
                className="error-btn-secondary"
              >
                <Home size={18} />
                <span>Go Home</span>
              </button>
            </div>

            {process.env.NODE_ENV === "development" && this.state.error && (
              <div className="error-dev-details">
                <summary className="dev-details-summary">
                  Error Details (Dev)
                </summary>
                <div className="code-block">
                  {this.state.error.toString()}
                  <br />
                  {this.state.errorInfo?.componentStack}
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
