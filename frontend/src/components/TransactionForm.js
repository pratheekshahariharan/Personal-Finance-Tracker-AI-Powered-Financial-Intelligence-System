// src/components/TransactionForm.js – Add transaction form
import React, { useState, useRef } from "react";
import { addTransaction, parseReceipt } from "../services/api";

const INITIAL = { description: "", amount: "", transaction_type: "expense", note: "" };

export default function TransactionForm({ onSuccess }) {
  const [form, setForm] = useState(INITIAL);
  const [loading, setLoading] = useState(false);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setOcrLoading(true);
    setError("");
    try {
      const res = await parseReceipt(file);
      if (res.data.is_error) {
        setError(res.data.description);
        return;
      }
      setForm((prev) => ({
        ...prev,
        amount: res.data.amount,
        description: res.data.description,
        transaction_type: "expense" // default for receipts
      }));
      onSuccess("Receipt parsed successfully! Please review before saving.");
    } catch (err) {
      setError("Failed to parse receipt. Using mock or check API key.");
    } finally {
      setOcrLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async () => {
    if (!form.description || !form.amount) {
      setError("Description and amount are required.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const res = await addTransaction({
        description: form.description,
        amount: parseFloat(form.amount),
        transaction_type: form.transaction_type,
        note: form.note || undefined,
      });
      setForm(INITIAL);
      onSuccess("Transaction added successfully!", res.data);
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        (Array.isArray(err.response?.data?.detail)
          ? err.response.data.detail.map((e) => e.msg).join(", ")
          : "Failed to add transaction.");
      setError(typeof msg === "string" ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card" style={{ position: "relative" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 15 }}>
        <h2 className="section-title" style={{ margin: 0 }}>Add Transaction</h2>
        <div>
          <button 
            className="btn-secondary" 
            style={{ fontSize: "0.8rem", display: "flex", alignItems: "center", gap: 5 }}
            onClick={() => fileInputRef.current?.click()}
            disabled={ocrLoading}
          >
            {ocrLoading ? "Scanning..." : "📷 Parse Receipt (AI)"}
          </button>
          <input 
            type="file" 
            accept="image/*" 
            ref={fileInputRef} 
            onChange={handleFileUpload} 
            style={{ display: "none" }} 
          />
        </div>
      </div>
      {error && (
        <div style={{ color: "var(--expense)", background: "#fceee8", border: "1px solid #f4b9a0", borderRadius: 8, padding: "8px 14px", marginBottom: 14, fontSize: "0.85rem" }}>
          {error}
        </div>
      )}
      <div className="form-grid">
        <div className="form-group">
          <label className="form-label">Description</label>
          <input className="form-input" placeholder="e.g. Zomato order" value={form.description} onChange={set("description")} />
        </div>
        <div className="form-group">
          <label className="form-label">Amount (₹)</label>
          <input className="form-input" type="number" min="0.01" step="0.01" placeholder="500" value={form.amount} onChange={set("amount")} />
        </div>
        <div className="form-group">
          <label className="form-label">Type</label>
          <select className="form-select" value={form.transaction_type} onChange={set("transaction_type")}>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>
        <div className="form-group">
          <label className="form-label">Note (optional)</label>
          <input className="form-input" placeholder="Optional note" value={form.note} onChange={set("note")} />
        </div>
        <button className="btn-primary" onClick={handleSubmit} disabled={loading}>
          {loading ? "Adding…" : "+ Add"}
        </button>
      </div>
    </section>
  );
}
