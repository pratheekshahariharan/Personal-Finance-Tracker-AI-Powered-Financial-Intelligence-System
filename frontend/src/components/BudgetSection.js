import React, { useState } from "react";
import { setBudget } from "../services/api";

const fmt = (n) => {
  if (n === undefined || n === null) return "—";
  const absVal = Math.abs(n).toLocaleString("en-IN", { maximumFractionDigits: 0 });
  return n < 0 ? "−₹" + absVal : "₹" + absVal;
};

const CATEGORIES = [
  "Food", "Transport", "Shopping", "Housing", "Entertainment",
  "Healthcare", "Education", "Other",
];

export default function BudgetSection({ budgetStatus, onSave, showToast }) {
  const [cat, setCat] = useState("Food");
  const [limit, setLimit] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    if (!limit || isNaN(limit)) return;
    setLoading(true);
    try {
      const oldLimit = budgetStatus.find(b => b.category === cat)?.monthly_limit || 0;
      await setBudget({ category: cat, monthly_limit: parseFloat(limit) });
      setLimit("");
      onSave();
      
      if (showToast) {
        showToast(`Budget for ${cat} updated!`, "success", { 
          type: "budget", 
          data: { category: cat, oldLimit } 
        });
      }
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to save budget.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2 className="section-title">Monthly Budgets</h2>

      {/* Set budget form */}
      <div className="form-grid" style={{ marginBottom: 20 }}>
        <div className="form-group">
          <label className="form-label">Category</label>
          <select className="form-select" value={cat} onChange={(e) => setCat(e.target.value)}>
            {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Monthly Limit (₹)</label>
          <input className="form-input" type="number" placeholder="e.g. 5000" value={limit} onChange={(e) => setLimit(e.target.value)} />
        </div>
        <button className="btn-primary" onClick={handleSave} disabled={loading} style={{ marginTop: 4 }}>
          {loading ? "Saving…" : "Save Budget"}
        </button>
      </div>

      {/* Budget status bars */}
      <div className="budget-list">
        {budgetStatus.length === 0 && (
          <div style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>No budgets set yet.</div>
        )}
        {budgetStatus.map((b) => {
          const pct = Math.min((b.current_spending / b.monthly_limit) * 100, 100);
          const isProjectedOver = !b.exceeded && b.projected_spending > b.monthly_limit;
          
          return (
            <div key={b.category} className="budget-item">
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", fontWeight: 600 }}>
                <span>{b.category}</span>
                <span style={{ color: b.exceeded ? "var(--expense)" : "var(--text-muted)", fontFamily: "DM Mono, monospace", fontSize: "0.78rem" }}>
                  {fmt(b.current_spending)} / {fmt(b.monthly_limit)}
                </span>
              </div>
              <div className="budget-bar-wrap">
                <div className={`budget-bar ${b.exceeded ? "over" : ""}`} style={{ width: `${pct}%` }} />
              </div>
              
              <div style={{ display: "flex", justifyContent: "space-between", marginTop: 6, fontSize: "0.7rem", color: "var(--text-muted)" }}>
                <span>
                  Projected: <strong>{fmt(b.projected_spending)}</strong>
                  {isProjectedOver && <span style={{ color: "#d97706", marginLeft: 6, fontWeight: "bold" }}>⚠ Risky</span>}
                </span>
                {b.days_left > 0 && <span>{b.days_left} days left</span>}
              </div>

              {b.exceeded && (
                <div className="badge badge-warning" style={{ marginTop: 8, width: "100%", textAlign: "center", display: "block" }}>
                  ⚠ Budget Exceeded
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
