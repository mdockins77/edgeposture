import { useAuth } from '../App.jsx';

export default function Nav({ page, setPage }) {
  const { user, logout } = useAuth();
  return (
    <nav className="nav">
      <div className="nav-brand" onClick={() => setPage('scanner')}>
        <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg>
        <span className="nav-name">EdgePosture</span>
      </div>
      <div className="nav-links">
        <button className={`nav-link ${page==='scanner'?'active':''}`} onClick={() => setPage('scanner')}>Scanner</button>
        {user && <button className={`nav-link ${page==='dashboard'?'active':''}`} onClick={() => setPage('dashboard')}>History</button>}
        <a className="nav-link" href="https://edgeposture.ai" target="_blank" rel="noreferrer">About</a>
        <a className="nav-link" href="https://getedgeposture.com" target="_blank" rel="noreferrer">Consulting</a>
        <a className="nav-link" href="https://chat.edgeposture.ai" target="_blank" rel="noreferrer">AI Chat</a>
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
}