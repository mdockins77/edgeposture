import { useState } from 'react';
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
        <div className="auth-logo" style={{background:"none",padding:0}}><svg width="44" height="44" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg></div>
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
        <div className="auth-logo" style={{background:"none",padding:0}}><svg width="44" height="44" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg></div>
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

export default Login;