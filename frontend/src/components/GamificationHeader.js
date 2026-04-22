import React, { useState, useEffect } from "react";
import { getGamification } from "../services/api";

export default function GamificationHeader() {
  const [data, setData] = useState({ streak_days: 0, badges: [] });

  useEffect(() => {
    getGamification().then(res => setData(res.data)).catch(() => {});
  }, []);

  return (
    <div className="gamification-bar" style={{ display: "flex", gap: "20px", alignItems: "center", marginBottom: "20px", padding: "10px 15px", background: "var(--bg-sec)", borderRadius: "12px", border: "1px solid var(--border)" }}>
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <span style={{ fontSize: "1.5rem" }}>🔥</span>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", fontWeight: "bold" }}>STREAK</span>
          <span style={{ fontSize: "1.1rem", fontWeight: "bold", color: "var(--primary)" }}>{data.streak_days} Days</span>
        </div>
      </div>
      
      <div style={{ height: "30px", width: "1px", background: "var(--border)" }} />
      
      <div style={{ display: "flex", gap: "10px", alignItems: "center", overflowX: "auto" }}>
        <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", fontWeight: "bold", marginRight: "5px" }}>BADGES:</span>
        {data.badges.map((b, i) => (
          <div key={i} title={b.description} style={{ filter: b.unlocked ? "none" : "grayscale(1) opacity(0.3)", transition: "all 0.3s ease" }}>
            <span style={{ fontSize: "1.4rem" }}>{b.icon}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
