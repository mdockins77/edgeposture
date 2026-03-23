import { useState, useEffect } from 'react';
import { API, useAuth } from '../App.jsx';

export default function Dashboard() {
  const { token } = useAuth();
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/history`, { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.json()).then(d => setScans(d.scans || [])).finally(() => setLoading(false));
  }, [token]);

  const pill = (s) => s >= 80 ? 'good' : s >= 50 ? 'warn' : 'poor';

  return (
    <div className="dashboard-page">
      <h2 className="page-title">Scan History</h2>
      {loading && <div className="loading-rows"><div className="skeleton"/><div className="skeleton"/><div className="skeleton"/></div>}
      {!loading && scans.length === 0 && <div className="empty-state"><p>No scans yet. Head to the scanner tab to analyze your first URL.</p></div>}
      {!loading && scans.length > 0 && (
        <div className="history-table-wrap">
          <table className="history-table">
            <thead><tr><th>URL</th><th>Overall</th><th>Security</th><th>Performance</th><th>Compliance</th><th>CDN</th><th>TTFB</th><th>Date</th></tr></thead>
            <tbody>
              {scans.map(s => (
                <tr key={s.id}>
                  <td className="url-cell" title={s.url}>{s.url.length > 40 ? s.url.slice(0,40)+'...' : s.url}</td>
                  <td><span className={`pill pill-${pill(s.overall_score)}`}>{s.overall_score}</span></td>
                  <td><span className={`pill pill-${pill(s.security_score)}`}>{s.security_score}</span></td>
                  <td><span className={`pill pill-${pill(s.performance_score)}`}>{s.performance_score}</span></td>
                  <td><span className={`pill pill-${pill(s.compliance_score)}`}>{s.compliance_score}</span></td>
                  <td><span className={`pill pill-${pill(s.cdn_score)}`}>{s.cdn_score}</span></td>
                  <td>{s.ttfb}ms</td>
                  <td>{new Date(s.scanned_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}