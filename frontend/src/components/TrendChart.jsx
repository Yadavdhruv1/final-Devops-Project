import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const MONTHS = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const fmt = (n) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n);

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, padding: '10px 14px' }}>
      <div style={{ fontWeight: 600, marginBottom: 6 }}>{label}</div>
      {payload.map((p) => (
        <div key={p.name} style={{ color: p.color, fontSize: 13, marginBottom: 2 }}>
          {p.name}: {fmt(p.value)}
        </div>
      ))}
    </div>
  );
};

export default function TrendChart({ trends }) {
  if (!trends?.length) {
    return (
      <div className="chart-card">
        <div className="chart-title">Monthly Trend</div>
        <div className="empty-state">
          <div className="empty-state-icon">📈</div>
          <div className="empty-state-text">No trend data yet</div>
        </div>
      </div>
    );
  }

  const data = [...trends].reverse().map(t => ({
    name: `${MONTHS[t.month]} ${t.year}`,
    Income: t.total_income,
    Expenses: t.total_expenses,
  }));

  return (
    <div className="chart-card">
      <div className="chart-title">Monthly Trend</div>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data} barGap={4}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
          <XAxis dataKey="name" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} tickFormatter={v => `$${(v / 1000).toFixed(0)}k`} />
          <Tooltip content={<CustomTooltip />} />
          <Legend wrapperStyle={{ fontSize: 12, color: '#94a3b8' }} />
          <Bar dataKey="Income" fill="#10b981" radius={[4, 4, 0, 0]} animationDuration={800} />
          <Bar dataKey="Expenses" fill="#f43f5e" radius={[4, 4, 0, 0]} animationDuration={800} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
