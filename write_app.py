import os

base = 'C:/Users/miked/edgeposture/edgepostureapp'
os.makedirs(f'{base}/src/components', exist_ok=True)
os.makedirs(f'{base}/src/pages', exist_ok=True)

files = {}

files[f'{base}/package.json'] = '''{
  "name": "edgepostureapp",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.1",
    "vite": "^5.4.10"
  }
}'''

files[f'{base}/vite.config.js'] = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
export default defineConfig({ plugins: [react()] })"""

files[f'{base}/index.html'] = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EdgePosture — Web Security & Performance Scanner</title>
    <meta name="description" content="Analyze any URL for security headers, performance, compliance, and CDN posture." />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>"""

files[f'{base}/wrangler.toml'] = """name = "edgepostureapp"
compatibility_date = "2024-11-01"

[build]
command = "npm run build"
destination = "dist"
"""

files[f'{base}/src/main.jsx'] = """import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
createRoot(document.getElementById('root')).render(<StrictMode><App /></StrictMode>)"""

files[f'{base}/src/App.jsx'] = """import { useState, useEffect, createContext, useContext } from 'react';
import Scanner from './pages/Scanner.jsx';
import Dashboard from './pages/Dashboard.jsx';
import { Login } from './pages/Login.jsx';
import { Register } from './pages/Login.jsx';
import Nav from './components/Nav.jsx';

const API = 'https://api.edgepostureapp.com';
export const AuthContext = createContext(null);
export function useAuth() { return useContext(AuthContext); }
export { API };

export default function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('ep_token'));
  const [page, setPage] = useState('scanner');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetch(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } })
        .then(r => r.json())
        .then(d => { if (d.user) setUser(d.user); else { setToken(null); localStorage.removeItem('ep_token'); } })
        .catch(() => { setToken(null); localStorage.removeItem('ep_token'); })
        .finally(() => setLoading(false));
    } else { setLoading(false); }
  }, [token]);

  const login = (t, u) => { setToken(t); setUser(u); localStorage.setItem('ep_token', t); setPage('scanner'); };
  const logout = () => { setToken(null); setUser(null); localStorage.removeItem('ep_token'); setPage('scanner'); };

  if (loading) return <div className="loading-screen"><div className="loading-logo">EP</div></div>;

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      <div className="app">
        <Nav page={page} setPage={setPage} />
        <main>
          {page === 'scanner' && <Scanner />}
          {page === 'dashboard' && (user ? <Dashboard /> : <Login onNav={setPage} />)}
          {page === 'login' && <Login onNav={setPage} />}
          {page === 'register' && <Register onNav={setPage} />}
        </main>
      </div>
    </AuthContext.Provider>
  );
}"""

files[f'{base}/src/pages/Scanner.jsx'] = """import { useState } from 'react';
import { API } from '../App.jsx';
import { ScoreCard } from '../components/ScoreCard.jsx';
import { FindingsList } from '../components/ScoreCard.jsx';
import { RecentScans } from '../components/ScoreCard.jsx';

export default function Scanner() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const scan = async (e) => {
    e.preventDefault();
    setError(null); setResult(null); setLoading(true);
    let target = url.trim();
    if (!target.startsWith('http')) target = 'https://' + target;
    try {
      const res = await fetch(`${API}/scan`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url: target }) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Scan failed');
      setResult(data);
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  const grade = (s) => s >= 80 ? 'good' : s >= 50 ? 'warn' : 'poor';

  return (
    <div className="scanner-page">
      <div className="scanner-hero">
        <h1 className="hero-title"><span className="hero-accent">Analyze</span> your web posture</h1>
        <p className="hero-sub">Security · Performance · Compliance · CDN — scored in seconds, powered by AI at the edge.</p>
        <form className="scan-form" onSubmit={scan}>
          <div className="scan-input-wrap">
            <span className="scan-prefix">https://</span>
            <input className="scan-input" type="text" value={url} onChange={e => setUrl(e.target.value)} placeholder="example.com" autoFocus required />
            <button className="scan-btn" type="submit" disabled={loading}>{loading ? <span className="spinner" /> : 'Scan'}</button>
          </div>
        </form>
        {error && <div className="scan-error">{error}</div>}
      </div>
      {loading && <div className="scanning-state"><div className="scan-pulse" /><p>Analyzing {url}...</p></div>}
      {result && (
        <div className="results-wrap">
          <div className="results-header">
            <div>
              <h2 className="results-url">{result.finalUrl || result.url}</h2>
              <p className="results-meta">Scanned {new Date(result.scannedAt).toLocaleString()} · TTFB {result.ttfb}ms{result.cached ? ' · cached' : ''}</p>
            </div>
            <div className={`overall-score score-${grade(result.overallScore)}`}>
              <span className="score-num">{result.overallScore}</span>
              <span className="score-label">/ 100</span>
            </div>
          </div>
          <div className="score-grid">
            <ScoreCard label="Security" score={result.scores.security} icon="🔒" />
            <ScoreCard label="Performance" score={result.scores.performance} icon="⚡" />
            <ScoreCard label="Compliance" score={result.scores.compliance} icon="✅" />
            <ScoreCard label="CDN Posture" score={result.scores.cdn} icon="🌐" />
          </div>
          <div className="summary-card"><h3>AI Summary</h3><p>{result.summary}</p></div>
          <div className="findings-recs">
            <FindingsList findings={result.findings} title="Findings" />
            <FindingsList findings={result.recommendations} title="Recommendations" isRecs={true} />
          </div>
        </div>
      )}
      {!result && !loading && <RecentScans />}
    </div>
  );
}"""

files[f'{base}/src/pages/Dashboard.jsx'] = """import { useState, useEffect } from 'react';
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
}"""

files[f'{base}/src/pages/Login.jsx'] = """import { useState } from 'react';
import { API, useAuth } from '../App.jsx';

export function Login({ onNav }) {
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault(); setError(null); setLoading(true);
    try {
      const res = await fetch(`${API}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      login(data.token, data.user); onNav('dashboard');
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">EP</div>
        <h2>Sign in to EdgePosture</h2>
        <form onSubmit={submit}>
          <label>Email</label>
          <input type="email" value={form.email} onChange={e => setForm(f => ({...f, email: e.target.value}))} required />
          <label>Password</label>
          <input type="password" value={form.password} onChange={e => setForm(f => ({...f, password: e.target.value}))} required />
          {error && <div className="auth-error">{error}</div>}
          <button type="submit" className="auth-btn" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
        </form>
        <p className="auth-switch">No account? <button className="link-btn" onClick={() => onNav('register')}>Create one</button></p>
      </div>
    </div>
  );
}

export function Register({ onNav }) {
  const { login } = useAuth();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault(); setError(null); setLoading(true);
    try {
      const res = await fetch(`${API}/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(form) });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      login(data.token, data.user); onNav('dashboard');
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-logo">EP</div>
        <h2>Create your account</h2>
        <form onSubmit={submit}>
          <label>Name</label>
          <input type="text" value={form.name} onChange={e => setForm(f => ({...f, name: e.target.value}))} required />
          <label>Email</label>
          <input type="email" value={form.email} onChange={e => setForm(f => ({...f, email: e.target.value}))} required />
          <label>Password</label>
          <input type="password" value={form.password} onChange={e => setForm(f => ({...f, password: e.target.value}))} required minLength={8} />
          {error && <div className="auth-error">{error}</div>}
          <button type="submit" className="auth-btn" disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
        </form>
        <p className="auth-switch">Have an account? <button className="link-btn" onClick={() => onNav('login')}>Sign in</button></p>
      </div>
    </div>
  );
}

export default Login;"""

files[f'{base}/src/components/Nav.jsx'] = """import { useAuth } from '../App.jsx';

export default function Nav({ page, setPage }) {
  const { user, logout } = useAuth();
  return (
    <nav className="nav">
      <div className="nav-brand" onClick={() => setPage('scanner')}>
        <span className="nav-logo">EP</span>
        <span className="nav-name">EdgePosture</span>
      </div>
      <div className="nav-links">
        <button className={`nav-link ${page==='scanner'?'active':''}`} onClick={() => setPage('scanner')}>Scanner</button>
        {user && <button className={`nav-link ${page==='dashboard'?'active':''}`} onClick={() => setPage('dashboard')}>History</button>}
        <a className="nav-link" href="https://edgeposture.ai" target="_blank" rel="noreferrer">About</a>
        <a className="nav-link" href="https://getedgeposture.com" target="_blank" rel="noreferrer">Consulting</a>
      </div>
      <div className="nav-auth">
        {user ? (
          <><span className="nav-user">{user.name}</span><button className="nav-btn-outline" onClick={logout}>Sign out</button></>
        ) : (
          <><button className="nav-btn-ghost" onClick={() => setPage('login')}>Sign in</button><button className="nav-btn" onClick={() => setPage('register')}>Get started</button></>
        )}
      </div>
    </nav>
  );
}"""

files[f'{base}/src/components/ScoreCard.jsx'] = """import { useState, useEffect } from 'react';
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
}"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {path}')

print('All files written successfully')