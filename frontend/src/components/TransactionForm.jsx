import { useState, useEffect } from 'react';

const CATEGORIES = {
  income: ['salary', 'freelance', 'investment', 'other'],
  expense: ['food', 'transport', 'housing', 'utilities', 'entertainment', 'healthcare', 'education', 'shopping', 'travel', 'insurance', 'savings', 'other'],
};

export default function TransactionForm({ onSubmit, onClose, initialData }) {
  const [form, setForm] = useState({
    title: '',
    amount: '',
    type: 'expense',
    category: 'food',
    description: '',
    date: new Date().toISOString().split('T')[0],
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        title: initialData.title || '',
        amount: initialData.amount || '',
        type: initialData.type || 'expense',
        category: initialData.category || 'food',
        description: initialData.description || '',
        date: initialData.date || new Date().toISOString().split('T')[0],
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => {
      const next = { ...prev, [name]: value };
      // Reset category when type changes
      if (name === 'type') {
        next.category = CATEGORIES[value][0];
      }
      return next;
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      ...form,
      amount: parseFloat(form.amount),
    });
  };

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal-content">
        <h3 className="modal-title">{initialData ? 'Edit Transaction' : 'New Transaction'}</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Title</label>
            <input
              className="form-input"
              name="title"
              value={form.title}
              onChange={handleChange}
              placeholder="e.g. Monthly Salary"
              required
              maxLength={200}
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Amount ($)</label>
              <input
                className="form-input"
                name="amount"
                type="number"
                step="0.01"
                min="0.01"
                value={form.amount}
                onChange={handleChange}
                placeholder="0.00"
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Date</label>
              <input
                className="form-input"
                name="date"
                type="date"
                value={form.date}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Type</label>
              <select className="form-select" name="type" value={form.type} onChange={handleChange}>
                <option value="income">💰 Income</option>
                <option value="expense">💸 Expense</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Category</label>
              <select className="form-select" name="category" value={form.category} onChange={handleChange}>
                {CATEGORIES[form.type].map(cat => (
                  <option key={cat} value={cat}>
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Description (optional)</label>
            <textarea
              className="form-textarea"
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Add a note..."
              maxLength={500}
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn-primary">
              {initialData ? 'Update' : 'Create'} Transaction
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
