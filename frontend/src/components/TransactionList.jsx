const fmt = (n) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);

const CATEGORIES = ['', 'salary', 'freelance', 'investment', 'food', 'transport', 'housing', 'utilities', 'entertainment', 'healthcare', 'education', 'shopping', 'travel', 'insurance', 'savings', 'other'];
const TYPES = ['', 'income', 'expense'];

export default function TransactionList({
  transactions, total, page, perPage, onDelete, onEdit,
  onPageChange, onFilterChange, filters, title, compact
}) {
  const totalPages = total ? Math.ceil(total / (perPage || 10)) : 1;

  if (!transactions?.length) {
    return (
      <div className="txn-card">
        {title && <div className="section-title">{title}</div>}
        <div className="empty-state">
          <div className="empty-state-icon">💳</div>
          <div className="empty-state-text">No transactions found</div>
          <div className="empty-state-sub">Create your first transaction to get started</div>
        </div>
      </div>
    );
  }

  return (
    <div className="txn-card">
      {title && <div className="section-title">{title}</div>}

      {!compact && onFilterChange && (
        <div className="filters-bar">
          <select
            className="filter-select"
            value={filters?.type || ''}
            onChange={e => onFilterChange({ type: e.target.value || undefined })}
          >
            <option value="">All Types</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
          <select
            className="filter-select"
            value={filters?.category || ''}
            onChange={e => onFilterChange({ category: e.target.value || undefined })}
          >
            <option value="">All Categories</option>
            {CATEGORIES.slice(1).map(c => (
              <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>
            ))}
          </select>
          <input
            className="filter-input"
            type="text"
            placeholder="Search transactions..."
            value={filters?.search || ''}
            onChange={e => onFilterChange({ search: e.target.value || undefined })}
          />
        </div>
      )}

      <div style={{ overflowX: 'auto' }}>
        <table className="txn-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Amount</th>
              <th>Type</th>
              <th>Category</th>
              <th>Date</th>
              {!compact && <th>Actions</th>}
            </tr>
          </thead>
          <tbody>
            {transactions.map(txn => (
              <tr key={txn.id}>
                <td style={{ fontWeight: 500 }}>{txn.title}</td>
                <td className={`txn-amount ${txn.type}`}>
                  {txn.type === 'income' ? '+' : '-'}{fmt(txn.amount)}
                </td>
                <td><span className={`txn-type ${txn.type}`}>{txn.type}</span></td>
                <td><span className="txn-category">{txn.category}</span></td>
                <td style={{ color: 'var(--text-muted)', fontSize: 13 }}>
                  {new Date(txn.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </td>
                {!compact && (
                  <td>
                    <div className="txn-actions">
                      {onEdit && <button className="btn-icon" onClick={() => onEdit(txn)} title="Edit">✏️</button>}
                      {onDelete && <button className="btn-icon delete" onClick={() => onDelete(txn.id)} title="Delete">🗑️</button>}
                    </div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {!compact && total > 0 && (
        <div className="pagination">
          <button disabled={page <= 1} onClick={() => onPageChange(page - 1)}>← Prev</button>
          <span className="page-info">Page {page} of {totalPages} ({total} total)</span>
          <button disabled={page >= totalPages} onClick={() => onPageChange(page + 1)}>Next →</button>
        </div>
      )}
    </div>
  );
}
