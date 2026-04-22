import React from "react";

export default function HealthGauge({ score, strokeWidth = 10, radius = 60 }) {
  const norm = Math.max(0, Math.min(100, score));
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (norm / 100) * circumference;

  let color = "var(--primary)";
  if (norm < 40) color = "var(--status-expense)";
  else if (norm < 70) color = "#FFA000"; // Amber

  return (
    <div style={{ position: "relative", width: radius * 2, height: radius * 2, margin: "0 auto" }}>
      <svg width={radius * 2} height={radius * 2} viewBox={`0 0 ${radius * 2} ${radius * 2}`}>
        <circle
          stroke="var(--border)"
          fill="transparent"
          strokeWidth={strokeWidth}
          cx={radius}
          cy={radius}
          r={radius - strokeWidth / 2}
        />
        <circle
          stroke={color}
          fill="transparent"
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          cx={radius}
          cy={radius}
          r={radius - strokeWidth / 2}
          style={{ transform: "rotate(-90deg)", transformOrigin: "50% 50%", transition: "stroke-dashoffset 1s ease-in-out" }}
        />
      </svg>
      <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
        <span style={{ fontSize: "2rem", fontWeight: "bold", lineHeight: 1 }}>{norm}</span>
        <span style={{ fontSize: "0.7rem", color: "var(--text-muted)", letterSpacing: "1px" }}>SCORE</span>
      </div>
    </div>
  );
}
