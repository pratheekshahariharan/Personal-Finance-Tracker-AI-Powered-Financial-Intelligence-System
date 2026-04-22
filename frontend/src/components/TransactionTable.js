import React, { useState } from "react";
import { reclassify } from "../services/api";

const fmtDate = (ts) =>
  ts ? new Date(ts).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" }) : "—";

const CATEGORIES = [
  "Food", "Transport", "Shopping", "Housing", "Entertainment",
  "Healthcare", "Education", "Salary", "Savings", "Other",
];

const RATES = { INR: 1, USD: 1 / 83 };

export default function TransactionTable({ transactions, onDelete, onReclassify, onBulkDelete, currency }) {
  const fmt = (n) => {
    if (n === undefined || n === null) return "—";
    const val = n * RATES[currency];
    const absVal = Math.abs(val).toLocaleString(currency === "INR" ? "en-IN" : "en-US", { 
      maximumFractionDigits: currency === "USD" ? 2 : 0,
      minimumFractionDigits: currency === "USD" ? 2 : 0,
    });
    const symbol = currency === "INR" ? "₹" : "$";
    return n < 0 ? "−" + symbol + absVal : symbol + absVal;
  };
  const [reclassifyId, setReclassifyId] = useState(null);
  const [newCat, setNewCat] = useState("");
  const [search, setSearch] = useState("");
  const [selectedIds, setSelectedIds] = useState([]);

  const filteredTransactions = transactions.filter(tx => 
    tx.description.toLowerCase().includes(search.toLowerCase()) ||
    tx.category.toLowerCase().includes(search.toLowerCase())
  );

  const toggleSelect = (id) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const handleBulkDelete = async () => {
    if (window.confirm(`Delete ${selectedIds.length} transactions?`)) {
      await onBulkDelete(selectedIds);
      setSelectedIds([]);
    }
  };

  const handleReclassify = async (id, oldCat) => {
    if (!newCat) return;
    try {
      await reclassify(id, newCat);
      setReclassifyId(null);
      setNewCat("");
      onReclassify(id, oldCat);
    } catch (err) {
      alert(err.response?.data?.detail || "Reclassify failed.");
    }
  };

  if (!transactions.length) {
    return <div className="empty-state">No transactions found. Add one above!</div>;
  }

  return (
    <div className="tx-table-wrap">
      <div style={{ display: "flex", gap: 12, marginBottom: 16, alignItems: "center" }}>
        <input 
          className="form-input" 
          placeholder="Search transactions..." 
          value={search} 
          onChange={(e) => setSearch(e.target.value)}
          style={{ maxWidth: 300 }}
        />
        {selectedIds.length > 0 && (
          <button className="btn-danger" onClick={handleBulkDelete} style={{ height: 42 }}>
            Delete Selected ({selectedIds.length})
          </button>
        )}
      </div>

      <table className="tx-table">
        <thead>
          <tr>
            <th>
              <input 
                type="checkbox" 
                onChange={(e) => setSelectedIds(e.target.checked ? filteredTransactions.map(t => t.id) : [])}
                checked={selectedIds.length === filteredTransactions.length && filteredTransactions.length > 0}
              />
            </th>
            <th>#</th>
            <th>Description</th>
            <th>Amount</th>
            <th>Type</th>
            <th>Category</th>
            <th>Date</th>
            <th>Note</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredTransactions.map((tx) => (
            <tr key={tx.id} className={selectedIds.includes(tx.id) ? "row-selected" : ""}>
              <td>
                <input 
                  type="checkbox" 
                  checked={selectedIds.includes(tx.id)} 
                  onChange={() => toggleSelect(tx.id)} 
                />
              </td>
              <td className="ts">{tx.id}</td>
              <td>
                <strong>{tx.description}</strong>
                {tx.auto_tagged ? (
                  <span className="badge badge-auto" style={{ marginLeft: 6 }}>auto</span>
                ) : (
                  <span className="badge badge-manual" style={{ marginLeft: 6 }}>manual</span>
                )}
              </td>
              <td>
                <span className={tx.transaction_type === "income" ? "amount-income" : "amount-expense"}>
                  {fmt(tx.amount)}
                </span>
              </td>
              <td>
                <span className={`badge badge-${tx.transaction_type}`}>
                  {tx.transaction_type}
                </span>
              </td>
              <td>
                {reclassifyId === tx.id ? (
                  <div className="reclassify-row">
                    <select
                      className="reclassify-input"
                      value={newCat}
                      onChange={(e) => setNewCat(e.target.value)}
                    >
                      <option value="">Pick…</option>
                      {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
                    </select>
                    <button className="btn-primary" style={{ padding: "4px 10px", height: "auto", fontSize: "0.75rem" }} onClick={() => handleReclassify(tx.id, tx.category)}>✓</button>
                    <button className="btn-secondary" style={{ padding: "4px 8px" }} onClick={() => { setReclassifyId(null); setNewCat(""); }}>✕</button>
                  </div>
                ) : (
                  <span className="badge badge-auto">{tx.category}</span>
                )}
              </td>
              <td className="ts">{fmtDate(tx.timestamp)}</td>
              <td style={{ color: "var(--text-muted)", fontSize: "0.8rem" }}>{tx.note || "—"}</td>
              <td>
                <div className="action-row">
                  <button
                    className="btn-secondary"
                    style={{ fontSize: "0.72rem", padding: "4px 10px" }}
                    onClick={() => { setReclassifyId(tx.id); setNewCat(tx.category); }}
                  >
                    ✏ Reclassify
                  </button>
                  <button className="btn-danger" onClick={() => onDelete(tx)}>✕</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
