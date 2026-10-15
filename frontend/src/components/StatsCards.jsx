const fmt = (n) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);

export default function StatsCards({ data }) {
  const cards = [
    { label: 'Total Income', value: fmt(data.total_income), cls: 'income', sub: 'All time earnings' },
    { label: 'Total Expenses', value: fmt(data.total_expenses), cls: 'expense', sub: 'All time spending' },
    { label: 'Net Balance', value: fmt(data.net_balance), cls: 'balance', sub: data.net_balance >= 0 ? 'You\'re in good shape!' : 'Spending exceeds income' },
    { label: 'Transactions', value: data.transaction_count.toLocaleString(), cls: 'count', sub: 'Total records' },
  ];

  return (
    <div className="stats-grid">
      {cards.map((card) => (
        <div key={card.label} className={`stat-card ${card.cls} animate-fade-in`}>
          <div className="stat-label">{card.label}</div>
          <div className={`stat-value ${card.cls}`}>{card.value}</div>
          <div className="stat-sub">{card.sub}</div>
        </div>
      ))}
    </div>
  );
}
