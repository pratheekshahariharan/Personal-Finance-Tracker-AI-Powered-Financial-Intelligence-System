import React from "react";

export default function Skeleton({ width = "100%", height = "20px", borderRadius = "4px", margin = "0" }) {
  const style = {
    width,
    height,
    borderRadius,
    margin,
    background: "linear-gradient(90deg, var(--surface2) 25%, var(--border) 50%, var(--surface2) 75%)",
    backgroundSize: "200% 100%",
    animation: "skeleton-loading 1.5s infinite",
  };

  return <div style={style}></div>;
}
