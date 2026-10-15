/**
 * FinPilot API Client
 * Handles all communication with the FastAPI backend.
 */

const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };

  const response = await fetch(url, config);

  if (response.status === 204) return null;

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Network error' }));
    throw new Error(error.detail || `Request failed: ${response.status}`);
  }

  return response.json();
}

// ─── Transactions ───

export async function fetchTransactions(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== '') query.append(key, val);
  });
  const qs = query.toString();
  return request(`/transactions/${qs ? `?${qs}` : ''}`);
}

export async function createTransaction(data) {
  return request('/transactions/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateTransaction(id, data) {
  return request(`/transactions/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteTransaction(id) {
  return request(`/transactions/${id}`, { method: 'DELETE' });
}

// ─── Budgets ───

export async function fetchBudgets(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== '') query.append(key, val);
  });
  const qs = query.toString();
  return request(`/budgets/${qs ? `?${qs}` : ''}`);
}

export async function fetchBudgetsWithSpending(month, year) {
  return request(`/budgets/spending?month=${month}&year=${year}`);
}

export async function createBudget(data) {
  return request('/budgets/', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function deleteBudget(id) {
  return request(`/budgets/${id}`, { method: 'DELETE' });
}

// ─── Analytics ───

export async function fetchDashboard(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== '') query.append(key, val);
  });
  const qs = query.toString();
  return request(`/analytics/dashboard${qs ? `?${qs}` : ''}`);
}

// ─── Health ───

export async function checkHealth() {
  const resp = await fetch('/health');
  return resp.json();
}
