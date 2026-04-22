import React, { useState } from "react";
import { exportCSV, importCSV, downloadPDF } from "../services/api";
import Skeleton from "./Skeleton";

const RATES = { INR: 1, USD: 1 / 83 };

export default function Dashboard({ dashboard, onRefresh, filters, setFilters, summary, currency }) {
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

  if (!dashboard) {
    return (
      <div className="kpi-grid" style={{ marginBottom: "24px" }}>
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="kpi-card" style={{ height: "120px", padding: "20px", background: "var(--surface)", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <Skeleton width="50%" height="12px" margin="0 0 16px 0" />
            <Skeleton width="80%" height="28px" margin="0 0 10px 0" />
            <Skeleton width="40%" height="10px" />
          </div>
        ))}
      </div>
    );
  }

  const handleExport = async () => {
    try {
      const res = await exportCSV();
      const url = URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "transactions.csv";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("Export failed.");
    }
  };

  const handleDownloadPDF = async () => {
    try {
      const res = await downloadPDF();
      const url = URL.createObjectURL(new Blob([res.data], { type: "application/pdf" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = "Financial_Statement.pdf";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("PDF download failed.");
    }
  };

  const handleImport = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      await importCSV(formData, filters.month, filters.year);
      alert("CSV imported successfully!");
      if (onRefresh) onRefresh();
    } catch (err) {
      alert("Import failed: " + (err.response?.data?.detail || "Unknown error"));
    }
  };

  const currentYear = new Date().getFullYear();
  const years = [String(currentYear), String(currentYear - 1)];
  const months = [
    { v: "1", l: "January" }, { v: "2", l: "February" }, { v: "3", l: "March" },
    { v: "4", l: "April" }, { v: "5", l: "May" }, { v: "6", l: "June" },
    { v: "7", l: "July" }, { v: "8", l: "August" }, { v: "9", l: "September" },
    { v: "10", l: "October" }, { v: "11", l: "November" }, { v: "12", l: "December" },
  ];

  return (
    <>
      <section className="card" style={{ padding: "20px", marginBottom: "24px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "25px", flexWrap: "wrap", gap: "20px" }}>
          <div>
            <h2 style={{ margin: 0, fontSize: "1.6rem", fontWeight: "800", background: "linear-gradient(135deg, var(--primary), #a855f7)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>
              Hello {months.find(m => m.v === filters.month)?.l || "April"} {filters.year}
            </h2>
            <div style={{ fontSize: "0.85rem", color: "var(--text-muted)", marginTop: "4px" }}>Here's what your finances look like for this period.</div>
          </div>

          <div style={{ display: "flex", gap: "10px", alignItems: "center", background: "var(--surface2)", padding: "6px 12px", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <span style={{ fontSize: "0.75rem", fontWeight: "bold", textTransform: "uppercase", color: "var(--text-muted)", marginRight: "5px" }}>Switch Period:</span>
            <select
              className="filter-select-minimal"
              style={{ padding: "4px 8px", borderRadius: "6px", border: "none", background: "transparent", fontWeight: "600", color: "var(--text)", width: "100px", textAlign: "center", cursor: "pointer", outline: "none" }}
              value={filters.month}
              onChange={(e) => setFilters({ ...filters, month: e.target.value })}
            >
              {months.map(m => <option key={m.v} value={m.v}>{m.l}</option>)}
            </select>
            <select
              className="filter-select-minimal"
              style={{ padding: "4px 8px", borderRadius: "6px", border: "none", background: "transparent", fontWeight: "600", color: "var(--text)", width: "70px", textAlign: "center", cursor: "pointer", outline: "none" }}
              value={filters.year}
              onChange={(e) => setFilters({ ...filters, year: e.target.value })}
            >
              {years.length > 0 ? years.map(y => <option key={y} value={y}>{y}</option>) : <option value={new Date().getFullYear()}>{new Date().getFullYear()}</option>}
            </select>
          </div>

          <div style={{ display: "flex", gap: "10px", alignItems: "center" }}>
            <label className="export-btn" style={{ cursor: "pointer", display: "inline-block", padding: "8px 16px", borderRadius: "8px", border: "1px dashed var(--border)", fontSize: "0.85rem" }}>
              ⬆ Import CSV
              <input type="file" hidden accept=".csv" onChange={handleImport} />
            </label>
            <button className="export-btn" onClick={handleExport} style={{ padding: "8px 16px", borderRadius: "8px", border: "1px solid var(--border)", fontSize: "0.85rem" }}>⬇ Export CSV</button>
            <button className="export-btn" onClick={handleDownloadPDF} style={{ padding: "8px 16px", borderRadius: "8px", background: "var(--primary)", color: "#fff", border: "none", fontSize: "0.85rem", fontWeight: "bold" }}>📄 Review PDF</button>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "15px" }}>

          <div className="kpi-card" style={{ padding: "20px", background: "var(--surface2)", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "5px" }}>
              {filters.month ? "Cumulative Balance" : "Total Balance"}
            </div>
            <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "var(--text)" }}>{fmt(dashboard.balance)}</div>
            <div style={{ fontSize: "0.7rem", marginTop: "8px", color: "var(--text-muted)" }}>
              As of {months.find(m => m.v === filters.month)?.l} {filters.year}
            </div>
          </div>

          <div className="kpi-card" style={{ padding: "20px", background: "var(--surface2)", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "5px" }}>Monthly Income</div>
            <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "var(--income)" }}>{fmt(dashboard.monthly_income)}</div>
            <div style={{ fontSize: "0.7rem", marginTop: "8px", color: "var(--text-muted)" }}>Money in for period</div>
          </div>

          <div className="kpi-card" style={{ padding: "20px", background: "var(--surface2)", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "5px" }}>Monthly Expenses</div>
            <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "var(--expense)" }}>{fmt(dashboard.monthly_expenses)}</div>
            <div style={{ fontSize: "0.7rem", marginTop: "8px", color: "var(--text-muted)" }}>Money out for period</div>
          </div>

          <div className="kpi-card" style={{ padding: "20px", background: "var(--surface2)", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "5px" }}>Carried Savings</div>
            <div style={{ fontSize: "1.5rem", fontWeight: "bold", color: "var(--primary)" }}>{fmt(dashboard.carried_savings)}</div>
            <div style={{ fontSize: "0.7rem", marginTop: "8px", color: "var(--text-muted)" }}>Previously retained wealth</div>
          </div>

        </div>

      </section>

      {dashboard.recent_activity?.length > 0 && (
        <section className="card" style={{ marginTop: "24px" }}>
          <h2 className="section-title">Historic Activity for Period</h2>
          <div className="recent-list">
            {dashboard.recent_activity.map((tx) => (
              <div key={tx.id} className="recent-item" style={{ borderBottom: "1px solid var(--border)", padding: "10px 0" }}>
                <div>
                  <strong>{tx.description}</strong>
                  <span className="badge badge-auto" style={{ marginLeft: 10 }}>{tx.category}</span>
                </div>
                <span className={tx.transaction_type === "income" ? "amount-inline-income" : "amount-inline-expense"} style={{ fontWeight: "bold" }}>
                  {fmt(tx.amount)}
                </span>
              </div>
            ))}
          </div>
          <style>{`
            .amount-inline-income { color: var(--income); }
            .amount-inline-expense { color: var(--expense); }
          `}</style>
        </section>
      )}
    </>
  );
}
