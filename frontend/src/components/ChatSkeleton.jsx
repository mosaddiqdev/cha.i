import React from "react";
import SkeletonLoader from "./SkeletonLoader";
import "./ChatSkeleton.css";

const ChatSkeleton = () => {
  return (
    <div className="chat-page-container skeleton-mode">
      {/* Sidebar Skeleton */}
      <div className="profile-wrapper open">
        <aside className="character-profile">
          <div className="profile-header">
            <SkeletonLoader type="text" width="60px" height="24px" />
          </div>
          <div className="profile-content no-scrollbar">
            <div className="profile-image-container">
              <SkeletonLoader type="rect" width="100%" height="100%" />
            </div>
            <div className="profile-identity">
              <SkeletonLoader
                type="text"
                width="70%"
                height="2rem"
                style={{ marginBottom: "0.5rem" }}
              />
              <SkeletonLoader
                type="text"
                width="40%"
                height="1rem"
                style={{ marginBottom: "1rem" }}
              />
              <SkeletonLoader type="text" width="100%" height="0.9rem" />
              <SkeletonLoader type="text" width="90%" height="0.9rem" />
            </div>
            <div className="profile-details">
              <SkeletonLoader
                type="text"
                width="30%"
                height="1.2rem"
                style={{ marginBottom: "0.5rem" }}
              />
              <SkeletonLoader type="text" width="100%" height="0.9rem" />
              <SkeletonLoader
                type="text"
                width="100%"
                height="0.9rem"
                style={{ marginTop: "1rem" }}
              />
            </div>
          </div>
        </aside>
      </div>

      {/* Chat Area Skeleton */}
      <div className="chat-interface-wrapper">
        <div className="chat-interface">
          <header className="chat-header">
            <SkeletonLoader type="circle" width="40px" height="40px" />
            <div style={{ marginLeft: "1rem", flex: 1 }}>
              <SkeletonLoader type="text" width="120px" height="1.2rem" />
              <SkeletonLoader type="text" width="80px" height="0.8rem" />
            </div>
          </header>

          <div className="chat-messages">
            {/* Incoming Message Skeleton */}
            <div className="message-group ai">
              <SkeletonLoader
                type="circle"
                width="32px"
                height="32px"
                style={{ marginRight: "12px" }}
              />
              <div
                className="message-bubble-skeleton"
                style={{ width: "60%", height: "80px" }}
              >
                <SkeletonLoader
                  type="rect"
                  width="100%"
                  height="100%"
                  style={{ borderRadius: "18px" }}
                />
              </div>
            </div>

            {/* Outgoing Message Skeleton */}
            <div
              className="message-group user"
              style={{ flexDirection: "row-reverse" }}
            >
              <div
                className="message-bubble-skeleton"
                style={{ width: "40%", height: "60px" }}
              >
                <SkeletonLoader
                  type="rect"
                  width="100%"
                  height="100%"
                  style={{ borderRadius: "18px" }}
                />
              </div>
            </div>

            {/* Incoming Message Skeleton */}
            <div className="message-group ai">
              <SkeletonLoader
                type="circle"
                width="32px"
                height="32px"
                style={{ marginRight: "12px" }}
              />
              <div
                className="message-bubble-skeleton"
                style={{ width: "50%", height: "100px" }}
              >
                <SkeletonLoader
                  type="rect"
                  width="100%"
                  height="100%"
                  style={{ borderRadius: "18px" }}
                />
              </div>
            </div>
          </div>

          <div className="chat-input-area">
            <div className="input-wrapper">
              <SkeletonLoader
                type="rect"
                width="100%"
                height="50px"
                style={{ borderRadius: "25px" }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatSkeleton;
