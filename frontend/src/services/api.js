// src/services/api.js – Axios-based API client for the Finance Tracker backend
import axios from "axios";

const BASE = "http://localhost:8000";

const api = axios.create({ baseURL: BASE });

// Transactions
export const addTransaction = (data) => api.post("/transactions/", data);
export const getTransactions = ({ month, year, category, transaction_type, search } = {}) =>
  api.get("/transactions/", { params: { month, year, category, transaction_type, search } });
export const deleteTransaction = (id) => api.delete(`/transactions/${id}`);
export const reclassify = (id, category) =>
  api.patch(`/transactions/${id}/reclassify`, { category });
export const bulkDeleteTransactions = (ids) => api.post("/transactions/bulk-delete", ids);

// Summary
export const getSummary = ({ month, year } = {}) => 
  api.get("/transactions/summary", { params: { month, year } });

// Dashboard
export const getDashboard = ({ month, year } = {}) => 
  api.get("/dashboard", { params: { month, year } });

// Export CSV
export const exportCSV = () =>
  api.get("/transactions/export", { responseType: "blob" });

// Budgets
export const setBudget = (data) => api.post("/budget/", data);
export const getBudgetStatus = ({ month, year } = {}) => 
  api.get("/budget/status", { params: { month, year } });

// Recurring
export const addRecurring = (data) => api.post("/recurring/", data);
export const getRecurring = () => api.get("/recurring/");
export const deleteRecurring = (id) => api.delete(`/recurring/${id}`);

// Savings
export const addSavingGoal = (data) => api.post("/savings/", data);
export const getSavingGoals = () => api.get("/savings/");
export const addAmountToGoal = (id, amount) => api.patch(`/savings/${id}/add`, { amount });
export const depositToSavings = (data) => api.post("/savings/deposit", data);
export const withdrawFromSavings = (data) => api.post("/savings/withdraw", data);
export const getSavingsHistory = () => api.get("/savings/history");
export const getSavingsBalance = () => api.get("/savings/balance");

// Optimization & Gamification
export const getOptimization = () => api.get("/optimization");
export const getGamification = () => api.get("/gamification");

// Reports & Bulk
export const importCSV = (formData, month, year) => {
  const params = {};
  if (month) params.month = month;
  if (year) params.year = year;
  return api.post("/csv/import", formData, {
    params,
    headers: { "Content-Type": "multipart/form-data" }
  });
};
export const downloadPDF = () => api.get("/report/pdf", { responseType: "blob" });

// AI Features
export const chatAI = (message, month, year) => api.post("/ai/chat", { message, month, year });
export const parseReceipt = (fileData) => {
  const formData = new FormData();
  formData.append("file", fileData);
  return api.post("/ai/receipt", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};
