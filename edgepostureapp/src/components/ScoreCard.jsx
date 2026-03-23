import { useState, useEffect } from 'react';
import { API } from '../App.jsx';

export function ScoreCard({ label, score, icon }) {
  const grade = score >= 80 ? 'good' : score >= 50 ? 'warn' : 'poor';
  return (
    <div className={`score-card score-card-${grade}`}>
      <div className="score-card-icon">{icon}</div>
      <div className="score-card-score">{score}</div>
      <div className="score-card-label">{label}</div>
      <div className="score-card-bar"><div className="score-card-fill" style={{ width: `${score}%` }} /></div>
    </div>
  );
}

export function FindingsList({ findings, title, isRecs }) {
  if (!findings?.length) return null;
  return (
    <div className="findings-section">
      <h3>{title}</h3>
      <div className="findings-list">
        {findings.map((f, i) => (
          <div key={i} className={`finding-item severity-${f.severity || 'info'}`}>
            <div className="finding-header">
              {!isRecs && <span className={`severity-badge sev-${f.severity}`}>{f.severity}</span>}
              {isRecs && <span className="priority-badge">P{f.priority}</span>}
              <span className={`cat-badge cat-${f.category}`}>{f.category}</span>
              <span className="finding-title">{f.title}</span>
            </div>
            <p className="finding-detail">{f.detail}</p>
            {isRecs && f.cfFeature && <div className="cf-feature-tag"><span className="cf-dot" />Cloudflare: {f.cfFeature}</div>}
          </div>
        ))}
      </div>
    </div>
  );
}

export function RecentScans() {
  const [scans, setScans] = useState([]);
  useEffect(() => {
    fetch(`${API}/scans/recent`).then(r => r.json()).then(d => setScans(d.scans || [])).catch(() => {});
  }, []);
  if (!scans.length) return null;
  return (
    <div className="recent-scans">
      <h3>Recently analyzed</h3>
      <div className="recent-list">
        {scans.map(s => (
          <div key={s.id} className="recent-item">
            <span className="recent-url">{s.url}</span>
            <span className={`pill pill-${s.overall_score>=80?'good':s.overall_score>=50?'warn':'poor'}`}>{s.overall_score}</span>
            <span className="recent-date">{new Date(s.scanned_at).toLocaleDateString()}</span>
          </div>
        ))}
      </div>
    </div>
  );
}