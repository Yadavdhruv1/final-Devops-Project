import { useState, useEffect } from 'react';
import { checkHealth } from '../api';

export default function Header() {
  const [healthy, setHealthy] = useState(null);

  useEffect(() => {
    checkHealth()
      .then(() => setHealthy(true))
      .catch(() => setHealthy(false));
  }, []);

  return (
    <header className="header">
      <div className="header-left">
        <div className="header-logo">FP</div>
        <div>
          <h1>FinPilot</h1>
          <span className="header-subtitle">Personal Finance Dashboard</span>
        </div>
      </div>
      <div className="header-right">
        {healthy !== null && (
          <div className="status-badge">
            <span className="status-dot" style={healthy ? {} : { background: '#f43f5e' }} />
            {healthy ? 'API Connected' : 'API Offline'}
          </div>
        )}
      </div>
    </header>
  );
}
