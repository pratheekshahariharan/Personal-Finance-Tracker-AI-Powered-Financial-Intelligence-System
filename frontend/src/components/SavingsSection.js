import React, { useState, useEffect } from "react";
import { 
  addSavingGoal, getSavingGoals, addAmountToGoal,
  depositToSavings, withdrawFromSavings, getSavingsHistory, getSavingsBalance 
} from "../services/api";

const fmt = (n) => "₹" + (n || 0).toLocaleString("en-IN", { maximumFractionDigits: 0 });

export default function SavingsSection({ onUpdate, showToast }) {
  const [goals, setGoals] = useState([]);
  const [balance, setBalance] = useState(0);
  const [history, setHistory] = useState([]);
  const [actionForm, setActionForm] = useState({ amount: "", reason: "", type: "deposit", goal_id: "" });
  const [goalForm, setGoalForm] = useState({ name: "", target_amount: "" });
  const [loading, setLoading] = useState(false);

  const loadAll = async () => {
    try {
      const gRes = await getSavingGoals();
      setGoals(gRes.data);
      
      const bRes = await getSavingsBalance();
      setBalance(bRes.data.balance);
      
      const hRes = await getSavingsHistory();
      setHistory(hRes.data);
    } catch (err) {
      console.error("Savings load error:", err);
    }
  };

  useEffect(() => { loadAll(); }, []);

  const handleGoalCreate = async () => {
    if (!goalForm.name || !goalForm.target_amount) return;
    try {
      await addSavingGoal({
        name: goalForm.name,
        target_amount: parseFloat(goalForm.target_amount)
      });
      setGoalForm({ name: "", target_amount: "" });
      loadAll();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to create goal.");
    }
  };

  const [amounts, setAmounts] = useState({}); // goalId -> amount string

  const handleError = (err, fallback) => {
    console.error(fallback, err);
    if (!err.response) {
      // Check if it's a timeout or a real network failure
      const detail = err.message || "Unknown Network Error";
      alert(`Connection failed: ${detail}. Please refresh and check if the backend terminal shows any errors.`);
      return;
    }
    const msg = err.response.data?.detail;
    if (typeof msg === "string") alert(msg);
    else if (Array.isArray(msg)) alert(msg[0]?.msg || fallback);
    else alert(JSON.stringify(msg) || fallback);
  };

  const handleCardAction = async (goalId, type) => {
    const amount = amounts[goalId];
    if (!amount || parseFloat(amount) <= 0) {
      alert("Please enter a positive amount.");
      return;
    }
    setLoading(true);
    try {
      const payload = { 
        amount: parseFloat(amount), 
        goal_id: goalId
      };
      if (type === "deposit") {
        await depositToSavings(payload);
      } else {
        await withdrawFromSavings(payload);
      }
      setAmounts(prev => ({ ...prev, [goalId]: "" }));
      await loadAll();
      if (onUpdate) onUpdate();
      
      // Add undo support
      if (showToast) {
        showToast(
          `${type === "deposit" ? "Deposited" : "Withdrawn"} ${fmt(payload.amount)}`, 
          "success", 
          { type: "savings", data: { ...payload, actionType: type } }
        );
      }
    } catch (err) {
      handleError(err, "Action failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card savings-container" style={{ padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 20 }}>
        <h2 className="section-title" style={{ marginBottom: 0 }}>Savings Goals</h2>
        <div style={{ textAlign: "right" }}>
          <div className="kpi-label">Stored Wealth</div>
          <div className="kpi-value" style={{ fontSize: "1.3rem", color: "var(--accent)" }}>{fmt(balance)}</div>
        </div>
      </div>

      {/* Goal Creation Row */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr auto", gap: 10, alignItems: "end", marginBottom: 24, background: "var(--surface2)", padding: 12, borderRadius: 12 }}>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="form-label" style={{ fontSize: "0.65rem" }}>Goal Name</label>
          <input className="form-input" style={{ padding: "8px" }} placeholder="e.g. New Car" value={goalForm.name} onChange={(e) => setGoalForm({...goalForm, name: e.target.value})} />
        </div>
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="form-label" style={{ fontSize: "0.65rem" }}>Target Amount (₹)</label>
          <input className="form-input" style={{ padding: "8px" }} type="number" placeholder="50000" value={goalForm.target_amount} onChange={(e) => setGoalForm({...goalForm, target_amount: e.target.value})} />
        </div>
        <button className="btn-primary" onClick={handleGoalCreate} disabled={!goalForm.name || !goalForm.target_amount} style={{ padding: "8px 16px", height: "38px" }}>+ Add</button>
      </div>

      {/* Sliding Box / Carousel */}
      <div className="savings-carousel">
        {goals.map((g) => {
          const percent = Math.min((g.current_amount / g.target_amount) * 100, 100).toFixed(1);
          return (
            <div key={g.id} className="goal-card">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start" }}>
                <strong style={{ fontSize: "0.95rem" }}>{g.name}</strong>
                <span style={{ fontSize: "0.75rem", color: "var(--primary)", fontWeight: 700 }}>{percent}%</span>
              </div>
              
              <div className="budget-bar-wrap" style={{ height: 6, marginTop: 4 }}>
                <div className="budget-bar" style={{ width: `${percent}%` }} />
              </div>
              
              <div style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginBottom: 4 }}>
                {fmt(g.current_amount)} / <span style={{ color: "var(--text)" }}>{fmt(g.target_amount)}</span>
              </div>

              <div style={{ marginTop: "auto", display: "flex", flexDirection: "column", gap: 8 }}>
                <input 
                  className="card-amount-input" 
                  placeholder="Amount" 
                  type="number"
                  value={amounts[g.id] || ""}
                  onChange={(e) => setAmounts({...amounts, [g.id]: e.target.value})}
                />
                <div className="card-action-row">
                  <button className="card-action-btn deposit" onClick={() => handleCardAction(g.id, "deposit")} disabled={loading}>Deposit</button>
                  <button className="card-action-btn withdraw" onClick={() => handleCardAction(g.id, "withdrawal")} disabled={loading}>Withdraw</button>
                </div>
              </div>
            </div>
          );
        })}
        {goals.length === 0 && (
          <div className="empty-state" style={{ width: "100%", padding: "20px" }}>
            No goals yet. Create one above to start saving!
          </div>
        )}
      </div>

      {/* Mini History Tab */}
      <details style={{ marginTop: 12 }}>
        <summary style={{ fontSize: "0.75rem", color: "var(--text-muted)", cursor: "pointer", fontWeight: 700 }}>View Savings History</summary>
        <div className="history-table-wrap" style={{ maxHeight: 150, overflowY: "auto", fontSize: "0.7rem", marginTop: 10 }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ textAlign: "left", color: "var(--text-muted)", borderBottom: "1px solid var(--border)" }}>
                <th style={{ padding: "8px 4px", width: "80px" }}>Date</th>
                <th style={{ padding: "8px 4px", width: "80px" }}>Type</th>
                <th style={{ padding: "8px 4px", textAlign: "right" }}>Amount</th>
              </tr>
            </thead>
            <tbody>
              {history.map((h) => (
                <tr key={h.id} style={{ borderBottom: "1px solid var(--border)" }}>
                  <td style={{ padding: "8px 4px" }}>{new Date(h.timestamp).toLocaleDateString()}</td>
                  <td style={{ padding: "8px 4px", fontWeight: 700, color: h.type === "deposit" ? "var(--income)" : "var(--expense)" }}>{h.type}</td>
                  <td style={{ padding: "8px 4px", textAlign: "right" }}>{fmt(h.amount)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </details>
    </section>
  );
}
