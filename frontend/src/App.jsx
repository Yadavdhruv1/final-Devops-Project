import { useState, useEffect, useCallback } from 'react';
import { fetchDashboard, fetchTransactions, createTransaction, deleteTransaction, updateTransaction, fetchBudgets, createBudget, deleteBudget, fetchBudgetsWithSpending } from './api';
import Header from './components/Header';
import StatsCards from './components/StatsCards';
import SpendingChart from './components/SpendingChart';
import TrendChart from './components/TrendChart';
import TransactionList from './components/TransactionList';
import TransactionForm from './components/TransactionForm';
import BudgetManager from './components/BudgetManager';
import './App.css';

const TABS = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'transactions', label: 'Transactions', icon: '💳' },
  { id: 'budgets', label: 'Budgets', icon: '🎯' },
];

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboard, setDashboard] = useState(null);
  const [transactions, setTransactions] = useState({ transactions: [], total: 0 });
  const [budgets, setBudgets] = useState([]);
  const [budgetSpending, setBudgetSpending] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTxn, setEditingTxn] = useState(null);
  const [filters, setFilters] = useState({ page: 1, per_page: 10 });

  const loadDashboard = useCallback(async () => {
    try {
      const data = await fetchDashboard();
      setDashboard(data);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  const loadTransactions = useCallback(async () => {
    try {
      const data = await fetchTransactions(filters);
      setTransactions(data);
    } catch (err) {
      setError(err.message);
    }
  }, [filters]);

  const loadBudgets = useCallback(async () => {
    try {
      const now = new Date();
      const data = await fetchBudgets();
      setBudgets(data);
      try {
        const spending = await fetchBudgetsWithSpending(now.getMonth() + 1, now.getFullYear());
        setBudgetSpending(spending);
      } catch { setBudgetSpending([]); }
    } catch (err) {
      setError(err.message);
    }
  }, []);

  useEffect(() => {
    const init = async () => {
      setLoading(true);
      await Promise.all([loadDashboard(), loadTransactions(), loadBudgets()]);
      setLoading(false);
    };
    init();
  }, [loadDashboard, loadTransactions, loadBudgets]);

  const handleCreateTransaction = async (data) => {
    try {
      await createTransaction(data);
      setShowForm(false);
      await Promise.all([loadDashboard(), loadTransactions()]);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateTransaction = async (data) => {
    try {
      await updateTransaction(editingTxn.id, data);
      setEditingTxn(null);
      setShowForm(false);
      await Promise.all([loadDashboard(), loadTransactions()]);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteTransaction = async (id) => {
    try {
      await deleteTransaction(id);
      await Promise.all([loadDashboard(), loadTransactions()]);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreateBudget = async (data) => {
    try {
      await createBudget(data);
      await loadBudgets();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteBudget = async (id) => {
    try {
      await deleteBudget(id);
      await loadBudgets();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleEditTxn = (txn) => {
    setEditingTxn(txn);
    setShowForm(true);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters, page: 1 }));
  };

  useEffect(() => {
    loadTransactions();
  }, [filters, loadTransactions]);

  return (
    <div className="app">
      <Header />

      <nav className="tab-nav">
        <div className="tab-nav-inner">
          {TABS.map(tab => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.label}</span>
            </button>
          ))}
        </div>
      </nav>

      {error && (
        <div className="error-banner animate-fade-in">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)} className="error-close">✕</button>
        </div>
      )}

      <main className="main-content">
        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner" />
            <p className="loading-text">Loading your financial data...</p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && dashboard && (
              <div className="dashboard animate-fade-in stagger">
                <StatsCards data={dashboard} />
                <div className="charts-grid">
                  <SpendingChart categories={dashboard.expense_by_category} />
                  <TrendChart trends={dashboard.monthly_trend} />
                </div>
                <TransactionList
                  transactions={dashboard.recent_transactions}
                  title="Recent Transactions"
                  compact
                />
              </div>
            )}

            {activeTab === 'transactions' && (
              <div className="transactions-page animate-fade-in">
                <div className="page-header">
                  <h2>Transactions</h2>
                  <button className="btn-primary" onClick={() => { setEditingTxn(null); setShowForm(true); }}>
                    + New Transaction
                  </button>
                </div>
                <TransactionList
                  transactions={transactions.transactions}
                  total={transactions.total}
                  page={filters.page}
                  perPage={filters.per_page}
                  onDelete={handleDeleteTransaction}
                  onEdit={handleEditTxn}
                  onPageChange={(p) => setFilters(prev => ({ ...prev, page: p }))}
                  onFilterChange={handleFilterChange}
                  filters={filters}
                />
              </div>
            )}

            {activeTab === 'budgets' && (
              <div className="budgets-page animate-fade-in">
                <BudgetManager
                  budgets={budgets}
                  spending={budgetSpending}
                  onCreate={handleCreateBudget}
                  onDelete={handleDeleteBudget}
                />
              </div>
            )}
          </>
        )}
      </main>

      {showForm && (
        <TransactionForm
          onSubmit={editingTxn ? handleUpdateTransaction : handleCreateTransaction}
          onClose={() => { setShowForm(false); setEditingTxn(null); }}
          initialData={editingTxn}
        />
      )}
    </div>
  );
}

export default App;
