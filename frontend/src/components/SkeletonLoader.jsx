import React from "react";
import "./SkeletonLoader.css";

const SkeletonLoader = ({
  type = "text",
  width,
  height,
  className = "",
  style = {},
}) => {
  const customStyle = {
    width,
    height,
    ...style,
  };

  return (
    <div className={`skeleton ${type} ${className}`} style={customStyle}></div>
  );
};

export default SkeletonLoader;
