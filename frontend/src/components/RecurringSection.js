// src/components/RecurringSection.js – Add and list recurring transactions
import React, { useState, useEffect } from "react";
import { addRecurring, getRecurring, deleteRecurring } from "../services/api";
import OptimizationAdvisor from "./OptimizationAdvisor";

const fmt = (n) => {
  if (n === undefined || n === null) return "—";
  const absVal = Math.abs(n).toLocaleString("en-IN", { maximumFractionDigits: 0 });
  return n < 0 ? "−₹" + absVal : "₹" + absVal;
};

export default function RecurringSection({ onSave, showToast }) {
  const [list, setList] = useState([]);
  const [form, setForm] = useState({
    description: "", amount: "", transaction_type: "expense", frequency: "monthly", next_due_date: "",
  });
  const [loading, setLoading] = useState(false);

  const load = async () => {
    try {
      const res = await getRecurring();
      setList(res.data);
    } catch { /* silent */ }
  };

  useEffect(() => { load(); }, []);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const handleAdd = async () => {
    if (!form.description || !form.amount) return;
    setLoading(true);
    try {
      await addRecurring({
        description: form.description,
        amount: parseFloat(form.amount),
        transaction_type: form.transaction_type,
        frequency: form.frequency,
        next_due_date: form.next_due_date || undefined,
      });
      setForm({ description: "", amount: "", transaction_type: "expense", frequency: "monthly", next_due_date: "" });
      await load();
      onSave();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to add recurring.");
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (rec) => {
    // Optimistic removal
    setList(prev => prev.filter(r => r.id !== rec.id));
    
    showToast("Subscription cancelled", "warn", { 
      type: "delete", 
      data: { id: rec.id, isRecurring: true } 
    });
  };

  const freqBadge = (f) => ({ daily: "🔁 Daily", weekly: "📅 Weekly", monthly: "🗓 Monthly" }[f] || f);

  return (
    <section className="card">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
        <h2 className="section-title" style={{ margin: 0 }}>Recurring Transactions</h2>
        <button 
          className="export-btn" 
          style={{ background: "#f0f4f8", border: "1px solid #cce0ff", color: "#0056b3", fontSize: "0.8rem", padding: "6px 12px" }}
          onClick={() => {
            const event = new CustomEvent("trigger-ai-chat", { detail: { message: "Can you audit my recurring subscriptions? I want to see if I can save any money." } });
            window.dispatchEvent(event);
          }}
        >
          ✨ Ask AI to Audit
        </button>
      </div>

      {/* Form */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 16 }}>
        <div className="form-group" style={{ gridColumn: "1 / -1" }}>
          <label className="form-label">Description</label>
          <input className="form-input" placeholder="Netflix subscription" value={form.description} onChange={set("description")} />
        </div>
        <div className="form-group">
          <label className="form-label">Amount (₹)</label>
          <input className="form-input" type="number" placeholder="799" value={form.amount} onChange={set("amount")} />
        </div>
        <div className="form-group">
          <label className="form-label">Type</label>
          <select className="form-select" value={form.transaction_type} onChange={set("transaction_type")}>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Frequency</label>
          <select className="form-select" value={form.frequency} onChange={set("frequency")}>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Next Due Date</label>
          <input className="form-input" type="date" value={form.next_due_date} onChange={set("next_due_date")} />
        </div>
      </div>
      <button className="btn-primary" style={{ width: "100%" }} onClick={handleAdd} disabled={loading}>
        {loading ? "Adding…" : "+ Add Recurring"}
      </button>

      {/* List */}
      <div className="recurring-list">
        {list.length === 0 && (
          <div style={{ color: "var(--text-muted)", fontSize: "0.85rem", marginTop: 10 }}>No recurring transactions.</div>
        )}
        {list.map((r) => (
          <div key={r.id} className="recurring-item" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <strong style={{ fontSize: "0.88rem" }}>{r.description}</strong>
              <div style={{ fontSize: "0.72rem", color: "var(--text-muted)", marginTop: 2 }}>
                {freqBadge(r.frequency)} · {r.category}
                {r.next_due_date && ` · Due ${r.next_due_date}`}
              </div>
            </div>
            <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
              <span className={r.transaction_type === "income" ? "amount-income" : "amount-expense"} style={{ fontFamily: "DM Mono, monospace", fontSize: "0.88rem" }}>
                {fmt(r.amount)}
              </span>
              <button 
                onClick={() => handleCancel(r)} 
                style={{ background: "none", border: "1px solid var(--border)", borderRadius: "4px", padding: "4px 8px", cursor: "pointer", color: "var(--text-muted)", fontSize: "0.7rem", fontWeight: "bold" }}
                title="Cancel Subscription"
              >
                ✕ Cancel
              </button>
            </div>
          </div>
        ))}
      </div>
      
      <OptimizationAdvisor />
    </section>
  );
}
