// src/components/Charts.js – Pie chart (expense distribution) + Line chart (monthly trend)
import React, { useMemo } from "react";
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, XAxis, YAxis, CartesianGrid,
} from "recharts";

const COLORS = [
  "#2d6a4f", "#e76f51", "#5c7cfa", "#f4a261", "#48cae4",
  "#9b5de5", "#f15bb5", "#fee440", "#00bbf9",
];

export default function Charts({ summary, filters }) {
  // Filter summary based on active time travel period
  const filteredSummary = useMemo(() => {
    if (!filters?.month && !filters?.year) return summary;
    
    // Target format: "2026-04"
    const target = `${filters.year || new Date().getFullYear()}-${String(filters.month || "").padStart(2, '0')}`;
    return summary.filter(s => s.month === target);
  }, [summary, filters]);

  // Expense distribution by category (pie chart)
  const pieData = useMemo(() => {
    const map = {};
    filteredSummary.forEach((s) => {
      // In this system, negative total means net expense
      // Some categories like 'Salary' might be net positive (income)
      if (s.total < 0) {
        if (!map[s.category]) map[s.category] = 0;
        map[s.category] += Math.abs(s.total);
      }
    });

    const entries = Object.entries(map).map(([name, value]) => ({ name, value: Math.round(value) }));
    return entries
      .filter((d) => d.value > 0)
      .sort((a, b) => b.value - a.value);
  }, [filteredSummary]);

  // Monthly trend (line chart) — net expenses per month
  const lineData = useMemo(() => {
    const map = {};
    summary.forEach((s) => {
      if (!map[s.month]) map[s.month] = 0;
      // We want to show net expenses on the trend line
      // If sum of transactions is -1000, it's a 1000 expense.
      if (s.total < 0) {
        map[s.month] += Math.abs(s.total);
      }
    });
    return Object.entries(map)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([month, total]) => ({ month, total: Math.round(total) }));
  }, [summary]);

  if (!summary.length) return null;

  return (
    <div className="charts-grid">
      {/* Pie chart */}
      <section className="card">
        <h2 className="section-title">Expense Distribution {filters?.month ? `(${filters.month}/${filters.year})` : ""}</h2>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                outerRadius={75}
                dataKey="value"
                // label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                label={true}
                labelLine={true}
                minAngle={15} // Ensures tiny slices have space for labels
                paddingAngle={2}
              >
                {pieData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => `₹${v.toLocaleString("en-IN")}`} />
              <Legend verticalAlign="bottom" height={36}/>
            </PieChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* Line chart */}
      <section className="card">
        <h2 className="section-title">Yearly Spending Trend</h2>
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={lineData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
              <XAxis dataKey="month" tick={{ fontSize: 11, fontFamily: "DM Mono, monospace" }} />
              <YAxis tick={{ fontSize: 11, fontFamily: "DM Mono, monospace" }} tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => `₹${v.toLocaleString("en-IN")}`} />
              <Line
                type="monotone"
                dataKey="total"
                stroke="#5c7cfa"
                strokeWidth={2.5}
                dot={{ r: 4, fill: "#5c7cfa" }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    </div>
  );
}
