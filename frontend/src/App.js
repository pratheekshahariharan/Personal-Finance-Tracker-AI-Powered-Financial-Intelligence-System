// src/App.js – Root component with dark mode, global styles, and layout
import React, { useState, useEffect, useCallback } from "react";
import Dashboard from "./components/Dashboard";
import TransactionForm from "./components/TransactionForm";
import TransactionTable from "./components/TransactionTable";
import Charts from "./components/Charts";
import BudgetSection from "./components/BudgetSection";
import RecurringSection from "./components/RecurringSection";
import SavingsSection from "./components/SavingsSection";
import AiAssistant from "./components/AiAssistant";
import { 
  getDashboard, getTransactions, getSummary, getBudgetStatus, 
  deleteTransaction, deleteRecurring, reclassify 
} from "./services/api";
import "./App.css";

const RATES = { INR: 1, USD: 1 / 83 };

export default function App() {
  const [dark, setDark] = useState(() => localStorage.getItem("theme") === "dark");
  const [currency, setCurrency] = useState("INR");
  const [dashboard, setDashboard] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [summary, setSummary] = useState([]);
  const [budgetStatus, setBudgetStatus] = useState([]);
  const [pendingDeletes, setPendingDeletes] = useState([]);
  const now = new Date();
  const [filters, setFilters] = useState({
    month: String(now.getMonth() + 1),
    year: String(now.getFullYear()),
    category: "",
    transaction_type: ""
  });
  const [toast, setToast] = useState(null);
  const [undoStack, setUndoStack] = useState([]);

  const fmt = useCallback((n) => {
    if (n === undefined || n === null) return "—";
    const val = n * RATES[currency];
    const absVal = Math.abs(val).toLocaleString(currency === "INR" ? "en-IN" : "en-US", { 
      maximumFractionDigits: currency === "USD" ? 2 : 0,
      minimumFractionDigits: currency === "USD" ? 2 : 0,
    });
    const symbol = currency === "INR" ? "₹" : "$";
    return n < 0 ? "−" + symbol + absVal : symbol + absVal;
  }, [currency]);

  const toggleCurrency = () => setCurrency(prev => prev === "INR" ? "USD" : "INR");

  useEffect(() => {
    if (dark) document.body.classList.add("dark");
    else document.body.classList.remove("dark");
  }, [dark]);

  const toggleDark = () => {
    setDark((d) => {
      localStorage.setItem("theme", !d ? "dark" : "light");
      return !d;
    });
  };

  const [refreshing, setRefreshing] = useState(false);

  const refresh = useCallback(async () => {
    setRefreshing(true);
    const timeParams = {};
    if (filters.month) timeParams.month = filters.month;
    if (filters.year) timeParams.year = filters.year;
    if (filters.category) timeParams.category = filters.category;
    if (filters.transaction_type) timeParams.transaction_type = filters.transaction_type;

    try {
      const [dRes, tRes, sRes, bRes] = await Promise.all([
        getDashboard(timeParams),
        getTransactions(timeParams),
        getSummary(),
        getBudgetStatus(timeParams)
      ]);
      
      setDashboard(dRes.data);
      setTransactions(tRes.data.filter(t => !pendingDeletes.includes(t.id)));
      setSummary(sRes.data);
      setBudgetStatus(bRes.data);
    } catch (e) {
      console.error("Sync error", e);
    } finally {
      setTimeout(() => setRefreshing(false), 500); // Small delay for visual feedback
    }
  }, [filters, pendingDeletes]);

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 3000); // Faster sync
    return () => clearInterval(id);
  }, [refresh]);

  const handleBulkDelete = async (ids) => {
    try {
      const { bulkDeleteTransactions } = await import("./services/api");
      await bulkDeleteTransactions(ids);
      refresh();
      showToast(`Deleted ${ids.length} transactions`, "success");
    } catch (e) {
      showToast("Bulk delete failed", "error");
    }
  };

  const showToast = (msg, type = "success", action = null) => {
    let timer = null;
    if (action && action.type === "delete") {
      const { id, isRecurring } = action.data;
      setPendingDeletes(prev => [...prev, id]);
      timer = setTimeout(async () => {
        try {
          if (isRecurring) { await deleteRecurring(id); }
          else { await deleteTransaction(id); }
          setPendingDeletes(prev => prev.filter(pid => pid !== id));
        } catch (e) { console.error("Delete failed", e); }
      }, 7000); 
    }
    setToast({ msg, type });
    if (action) { setUndoStack(prev => [...prev, { ...action, timer }]); }
    setTimeout(() => { setToast(prev => prev?.msg === msg ? null : prev); }, 8000);
  };

  const handleUndo = async () => {
    if (undoStack.length === 0) return;
    const { type, data, timer } = undoStack[undoStack.length - 1];
    if (timer) clearTimeout(timer);
    try {
      if (type === "delete") { setPendingDeletes(prev => prev.filter(pid => pid !== data.id)); }
      else if (type === "reclassify") { await reclassify(data.id, data.oldCategory); }
      else if (type === "add") { await deleteTransaction(data.id); }
      else if (type === "savings") {
        const { amount, goal_id, actionType } = data;
        const { withdrawFromSavings, depositToSavings } = await import("./services/api");
        if (actionType === "deposit") await withdrawFromSavings({ amount, goal_id });
        else await depositToSavings({ amount, goal_id });
      } else if (type === "budget") {
        const { setBudget } = await import("./services/api");
        await setBudget({ category: data.category, monthly_limit: data.oldLimit });
      }
      await refresh();
      setUndoStack(prev => prev.slice(0, -1));
      setToast(null);
    } catch (e) { showToast("Failed to undo.", "error"); }
  };

  return (
    <div className={`app ${dark ? "dark" : ""}`}>
      <header className="app-header" style={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 24px", background: "var(--surface)", borderBottom: "1px solid var(--border)", position: "sticky", top: 0, zIndex: 1100 }}>
        <div className="header-brand" style={{ flexShrink: 0 }}>
          <div className="brand-logo-gradient"><span className="brand-icon">₹</span></div>
          <span className="brand-name">Personal Finance Tracker</span>
        </div>
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <div className="system-status" style={{ display: "flex", gap: 12, marginRight: 20, padding: "4px 12px", background: "var(--bg)", borderRadius: "20px", border: "1px solid var(--border)", fontSize: "0.65rem", fontWeight: "700", textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--text-muted)" }}>
            <span style={{ display: "flex", alignItems: "center", gap: 6 }}>
              <span className={`status-dot ${refreshing ? 'pulse-sync' : ''}`} style={{ width: 6, height: 6, borderRadius: "50%", background: refreshing ? "var(--primary)" : "#10B981" }}></span>
              {refreshing ? "Syncing..." : "Live Data"}
            </span>
            <span style={{ display: "flex", alignItems: "center", gap: 6, borderLeft: "1px solid var(--border)", paddingLeft: 12 }}>
              <span className="status-dot" style={{ width: 6, height: 6, borderRadius: "50%", background: "#6366F1" }}></span>
              AI: Ready
            </span>
          </div>
          <button className="theme-toggle" onClick={toggleCurrency} style={{ whiteSpace: "nowrap", background: "var(--primary)", color: "#fff", border: "none", padding: "8px 16px", borderRadius: "8px", fontWeight: "700", cursor: "pointer" }}>
            {currency === "INR" ? "₹ INR" : "$ USD"}
          </button>
          <button className="theme-toggle" onClick={toggleDark} style={{ whiteSpace: "nowrap", background: "var(--surface2)", border: "1px solid var(--border)", padding: "8px 16px", borderRadius: "8px", fontWeight: "700", color: "var(--text)", cursor: "pointer" }}>
            {dark ? "☀ Light" : "☾ Dark"}
          </button>
        </div>
      </header>

      {toast && (
        <div className={`toast toast-${toast.type}`} style={{ display: "flex", alignItems: "center", gap: 15 }}>
          <span>{toast.msg}</span>
          <button className="undo-btn" onClick={handleUndo}>Undo Action</button>
        </div>
      )}

      <main className="app-main">
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: budgetStatus.some(b => b.exceeded) ? 20 : 0 }}>
          {budgetStatus.filter(b => b.exceeded).map(b => (
            <div key={b.category} className="budget-alert">
              <span>⚠ <strong>{b.category}</strong> budget exceeded</span>
              <span className="badge badge-warning">{fmt(b.current_spending)} / {fmt(b.monthly_limit)}</span>
            </div>
          ))}
        </div>

        <Dashboard dashboard={dashboard} onRefresh={refresh} filters={filters} setFilters={setFilters} summary={summary} currency={currency} />

        <div className="dashboard-grid">
          <div className="main-column">
            <div className="two-col" style={{ marginBottom: "24px" }}>
              <TransactionForm onSuccess={(msg, data) => { refresh(); showToast(msg, "success", data ? { type: "add", data } : null); }} />
              <BudgetSection budgetStatus={budgetStatus} showToast={showToast} onSave={() => refresh()} />
            </div>
            <section className="card">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
                <h2 className="section-title">Transaction History</h2>
                <div style={{ display: "flex", gap: "10px" }}>
                  <select className="filter-select" value={filters.transaction_type} onChange={e => setFilters({...filters, transaction_type: e.target.value})}>
                    <option value="">All Types</option><option value="expense">Expense</option><option value="income">Income</option>
                  </select>
                  <select className="filter-select" value={filters.category} onChange={e => setFilters({...filters, category: e.target.value})}>
                    <option value="">All Categories</option>
                    {["Food", "Transport", "Shopping", "Housing", "Entertainment", "Healthcare", "Education", "Salary", "Savings", "Other"].map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
              </div>
              <TransactionTable transactions={transactions} onDelete={tx => { setTransactions(prev => prev.filter(t => t.id !== tx.id)); showToast("Transaction deleted", "warn", { type: "delete", data: tx }); }} onReclassify={(id, oldCategory) => { refresh(); showToast("Category updated", "success", { type: "reclassify", data: { id, oldCategory } }); }} onBulkDelete={handleBulkDelete} currency={currency} />
            </section>
          </div>
          <div className="sidebar-column"><Charts summary={summary} filters={filters} /></div>
        </div>

        <div style={{ marginTop: "24px" }}><SavingsSection showToast={showToast} onUpdate={() => refresh()} /></div>
        <div style={{ marginTop: "20px" }}><RecurringSection onSave={() => { refresh(); showToast("Recurring added!", "success", { type: "recurring" }); }} showToast={showToast} /></div>
      </main>
      <AiAssistant filters={filters} />
    </div>
  );
}
