import React from "react";
import SkeletonLoader from "./SkeletonLoader";
import "./HomeSkeleton.css";

const HomeSkeleton = () => {
  return (
    <div className="home-container skeleton-mode">
      <header className="fixed-header">
        <SkeletonLoader type="text" width="120px" height="40px" />
      </header>

      <div className="horizontal-scroll-wrapper no-scrollbar">
        {[1, 2, 3].map((item) => (
          <section key={item} className="character-section">
            <div className="character-content">
              <div className="text-content">
                <SkeletonLoader
                  type="text"
                  width="60%"
                  height="3rem"
                  style={{ marginBottom: "1rem" }}
                />
                <SkeletonLoader
                  type="text"
                  width="40%"
                  height="1.5rem"
                  style={{ marginBottom: "2rem" }}
                />
                <SkeletonLoader type="text" width="100%" height="1rem" />
                <SkeletonLoader type="text" width="90%" height="1rem" />
                <SkeletonLoader
                  type="text"
                  width="80%"
                  height="1rem"
                  style={{ marginBottom: "3rem" }}
                />

                <SkeletonLoader
                  type="rect"
                  width="180px"
                  height="50px"
                  style={{ borderRadius: "25px" }}
                />
              </div>

              <div className="image-content">
                <div className="image-wrapper">
                  <SkeletonLoader type="rect" width="100%" height="100%" />
                </div>
              </div>
            </div>
          </section>
        ))}
      </div>

      <div className="scroll-indicator">
        <SkeletonLoader type="circle" width="8px" height="8px" />
        <SkeletonLoader type="circle" width="8px" height="8px" />
        <SkeletonLoader type="circle" width="8px" height="8px" />
      </div>
    </div>
  );
};

export default HomeSkeleton;
