import { useState, useEffect, createContext, useContext } from 'react';
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
          {page === 'scanner' && <Scanner onNav={setPage} />}
          {page === 'dashboard' && (user ? <Dashboard /> : <Login onNav={setPage} />)}
          {page === 'login' && <Login onNav={setPage} />}
          {page === 'register' && <Register onNav={setPage} />}
        </main>
      </div>
    </AuthContext.Provider>
  );
}