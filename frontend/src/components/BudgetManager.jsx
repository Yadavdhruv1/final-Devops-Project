import { useState } from 'react';

const fmt = (n) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);
const ALL_CATEGORIES = ['food', 'transport', 'housing', 'utilities', 'entertainment', 'healthcare', 'education', 'shopping', 'travel', 'insurance', 'savings', 'other'];

export default function BudgetManager({ budgets, spending, onCreate, onDelete }) {
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({
    category: 'food',
    monthly_limit: '',
    month: new Date().getMonth() + 1,
    year: new Date().getFullYear(),
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onCreate({
      ...form,
      monthly_limit: parseFloat(form.monthly_limit),
      month: parseInt(form.month),
      year: parseInt(form.year),
    });
    setShowForm(false);
    setForm({ ...form, monthly_limit: '' });
  };

  const getProgressClass = (pct) => {
    if (pct >= 90) return 'danger';
    if (pct >= 70) return 'warning';
    return 'safe';
  };

  return (
    <div>
      <div className="page-header">
        <h2>Budget Manager</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Budget'}
        </button>
      </div>

      {showForm && (
        <form className="budget-form-inline animate-fade-in" onSubmit={handleSubmit} style={{ marginBottom: 24 }}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Category</label>
              <select className="form-select" value={form.category}
                onChange={e => setForm(p => ({ ...p, category: e.target.value }))}>
                {ALL_CATEGORIES.map(c => (
                  <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Monthly Limit ($)</label>
              <input className="form-input" type="number" step="0.01" min="0.01"
                value={form.monthly_limit} placeholder="500.00"
                onChange={e => setForm(p => ({ ...p, monthly_limit: e.target.value }))} required />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Month</label>
              <select className="form-select" value={form.month}
                onChange={e => setForm(p => ({ ...p, month: e.target.value }))}>
                {Array.from({ length: 12 }, (_, i) => (
                  <option key={i + 1} value={i + 1}>
                    {new Date(2026, i).toLocaleString('en', { month: 'long' })}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Year</label>
              <input className="form-input" type="number" min="2020" max="2100"
                value={form.year} onChange={e => setForm(p => ({ ...p, year: e.target.value }))} />
            </div>
          </div>
          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <button type="submit" className="btn-primary">Create Budget</button>
          </div>
        </form>
      )}

      {spending?.length > 0 ? (
        <div className="budget-grid stagger">
          {spending.map(b => (
            <div key={b.id} className="budget-card animate-fade-in">
              <div className="budget-header">
                <span className="budget-category">{b.category}</span>
                <button className="btn-icon delete" onClick={() => onDelete(b.id)} title="Delete">🗑️</button>
              </div>
              <div className="budget-limit">Limit: {fmt(b.monthly_limit)}</div>
              <div className="budget-progress">
                <div
                  className={`budget-progress-bar ${getProgressClass(b.percentage_used)}`}
                  style={{ width: `${Math.min(100, b.percentage_used)}%` }}
                />
              </div>
              <div className="budget-stats">
                <span>Spent: {fmt(b.spent)}</span>
                <span>Remaining: {fmt(b.remaining)}</span>
                <span>{b.percentage_used}%</span>
              </div>
            </div>
          ))}
        </div>
      ) : budgets?.length > 0 ? (
        <div className="budget-grid stagger">
          {budgets.map(b => (
            <div key={b.id} className="budget-card animate-fade-in">
              <div className="budget-header">
                <span className="budget-category">{b.category}</span>
                <button className="btn-icon delete" onClick={() => onDelete(b.id)} title="Delete">🗑️</button>
              </div>
              <div className="budget-limit">Limit: {fmt(b.monthly_limit)}</div>
              <div className="budget-stats">
                <span>Month: {b.month}/{b.year}</span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state-icon">🎯</div>
          <div className="empty-state-text">No budgets set</div>
          <div className="empty-state-sub">Create a budget to track your spending limits</div>
        </div>
      )}
    </div>
  );
}
