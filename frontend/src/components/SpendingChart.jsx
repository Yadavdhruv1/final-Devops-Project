import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#f43f5e', '#a855f7', '#ec4899', '#14b8a6', '#f97316', '#8b5cf6'];

const fmt = (n) => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n);

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div style={{ background: '#1a1a2e', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, padding: '10px 14px' }}>
      <div style={{ fontWeight: 600, textTransform: 'capitalize', marginBottom: 4 }}>{d.category}</div>
      <div style={{ color: '#94a3b8', fontSize: 13 }}>{fmt(d.total)} ({d.percentage}%)</div>
    </div>
  );
};

export default function SpendingChart({ categories }) {
  if (!categories?.length) {
    return (
      <div className="chart-card">
        <div className="chart-title">Spending by Category</div>
        <div className="empty-state">
          <div className="empty-state-icon">📊</div>
          <div className="empty-state-text">No expense data yet</div>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-card">
      <div className="chart-title">Spending by Category</div>
      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={categories}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={100}
            paddingAngle={3}
            dataKey="total"
            nameKey="category"
            animationBegin={0}
            animationDuration={800}
          >
            {categories.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} stroke="transparent" />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px 16px', marginTop: 8 }}>
        {categories.map((cat, i) => (
          <div key={cat.category} style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 12, color: '#94a3b8' }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: COLORS[i % COLORS.length], display: 'inline-block' }} />
            <span style={{ textTransform: 'capitalize' }}>{cat.category}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
