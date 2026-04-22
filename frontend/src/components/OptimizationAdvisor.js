import React, { useState, useEffect } from "react";
import { getOptimization } from "../services/api";

export default function OptimizationAdvisor() {
  const [recs, setRecs] = useState([]);

  useEffect(() => {
    getOptimization().then(res => setRecs(res.data)).catch(() => {});
  }, []);

  if (recs.length === 0) return null;

  return (
    <div className="optimization-card">
      <div className="optimization-header">
        <span className="optimization-icon">💡</span>
        <strong className="optimization-title">Subscription Advisor</strong>
      </div>
      {recs.map((r, i) => (
        <div key={i} style={{ fontSize: "0.85rem", color: "var(--text)", marginBottom: "5px" }}>
          {r.message}
          {r.potential_monthly_savings > 0 && (
            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginTop: "2px" }}>
               Potential 5-year savings: <strong>₹{(r.potential_monthly_savings * 60).toLocaleString()}</strong>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
