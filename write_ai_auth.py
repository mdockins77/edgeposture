html = open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', encoding='utf-8').read()

# Add auth CSS before closing </style>
auth_css = '''
    .modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:200;display:flex;align-items:center;justify-content:center;padding:1rem}
    .modal-overlay.hidden{display:none}
    .modal-card{background:#111318;border:1px solid rgba(255,255,255,0.14);border-radius:16px;padding:2.5rem;width:100%;max-width:420px}
    .modal-logo{width:44px;height:44px;margin:0 auto 1.25rem;display:block}
    .modal-card h2{font-family:"Space Mono",monospace;font-size:18px;margin-bottom:0.5rem;color:#e8eaf0;text-align:center}
    .modal-card p{color:#8b8fa8;font-size:14px;margin-bottom:1.5rem;text-align:center}
    .modal-field{margin-bottom:1rem}
    .modal-field label{display:block;font-size:12px;color:#8b8fa8;margin-bottom:5px}
    .modal-field input{width:100%;background:#0a0c10;border:1px solid rgba(255,255,255,0.14);color:#e8eaf0;padding:10px 14px;border-radius:8px;font-size:14px;font-family:"DM Sans",sans-serif;outline:none;box-sizing:border-box}
    .modal-field input:focus{border-color:#4f7bff}
    .modal-btn{width:100%;background:#4f7bff;color:#fff;border:none;padding:12px;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;font-family:"DM Sans",sans-serif;transition:opacity 0.15s;margin-top:0.5rem}
    .modal-btn:hover{opacity:0.85}
    .modal-err{color:#ef4444;font-size:12px;margin-top:6px;padding:6px 10px;background:rgba(239,68,68,0.1);border-radius:6px;display:none}
    .modal-switch{margin-top:1rem;text-align:center;font-size:13px;color:#8b8fa8}
    .modal-switch button{background:none;border:none;color:#7c9fff;cursor:pointer;font-size:13px;font-family:"DM Sans",sans-serif;padding:0;text-decoration:underline}
    .modal-close{float:right;background:none;border:none;color:#555870;cursor:pointer;font-size:20px;line-height:1;margin-top:-8px}
    .user-pill{display:inline-flex;align-items:center;gap:8px;background:rgba(79,123,255,0.1);border:1px solid rgba(79,123,255,0.2);color:#7c9fff;padding:5px 12px;border-radius:20px;font-size:13px;font-weight:500}
    .user-pill-name{max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .signout-btn{background:none;border:none;color:#555870;cursor:pointer;font-size:12px;font-family:"DM Sans",sans-serif;padding:0;transition:color 0.15s}
    .signout-btn:hover{color:#e8eaf0}
'''

html = html.replace('    .cf-badge {', auth_css + '\n    .cf-badge {')

# Replace the nav CTA with auth-aware nav
old_nav_cta = '<a class="nav-cta" href="https://edgepostureapp.com">Launch scanner</a>'
new_nav_cta = '''<div id="nav-auth-area" style="display:flex;align-items:center;gap:10px">
    <div id="user-pill-nav" class="user-pill" style="display:none">
      <span>&#128100;</span>
      <span class="user-pill-name" id="nav-username"></span>
      <button class="signout-btn" onclick="doSignOut()">&#x2715;</button>
    </div>
    <button id="nav-signin-btn" class="nav-cta" onclick="openModal('login')" style="display:none">Sign in</button>
    <a id="nav-scanner-btn" class="nav-cta" href="https://edgepostureapp.com" onclick="return gatedNav(event,'https://edgepostureapp.com')">Launch scanner</a>
  </div>'''

html = html.replace(old_nav_cta, new_nav_cta)

# Replace hero action buttons with gated versions
old_hero_actions = '''<div class="hero-actions">
      <a class="btn-primary" href="https://edgepostureapp.com">Scan your site free &rarr;</a>
      <a class="btn-secondary" href="https://getedgeposture.com">Hire an Edge SME</a>
    </div>'''

new_hero_actions = '''<div class="hero-actions">
      <a class="btn-primary" href="https://edgepostureapp.com" onclick="return gatedNav(event,'https://edgepostureapp.com')">Scan your site free &rarr;</a>
      <a class="btn-primary" href="https://chat.edgeposture.ai" onclick="return gatedNav(event,'https://chat.edgeposture.ai')" style="background:#0f6e56">AI Assistant &rarr;</a>
      <a class="btn-secondary" href="https://blog.edgeposture.ai" onclick="return gatedNav(event,'https://blog.edgeposture.ai')">Blog</a>
      <a class="btn-secondary" href="https://getedgeposture.com">Hire an Edge SME</a>
    </div>'''

html = html.replace(old_hero_actions, new_hero_actions)

# Add modal + auth script before </body>
auth_html = '''
<!-- Auth Modal -->
<div class="modal-overlay hidden" id="auth-modal">
  <div class="modal-card">
    <button class="modal-close" onclick="closeModal()">&#x2715;</button>

    <!-- Login form -->
    <div id="login-form">
      <svg class="modal-logo" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg>
      <h2>Welcome back</h2>
      <p>Sign in to access the scanner, AI assistant, and blog.</p>
      <div class="modal-field"><label>Email</label><input type="email" id="login-email" placeholder="you@example.com"/></div>
      <div class="modal-field"><label>Password</label><input type="password" id="login-password" placeholder="Your password"/></div>
      <div class="modal-err" id="login-err"></div>
      <button class="modal-btn" id="login-submit-btn" onclick="doLogin()">Sign in</button>
      <div class="modal-switch">No account? <button onclick="showRegister()">Create one free</button></div>
    </div>

    <!-- Register form -->
    <div id="register-form" style="display:none">
      <svg class="modal-logo" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg>
      <h2>Create your account</h2>
      <p>Free to join. Access the scanner, AI assistant, and blog.</p>
      <div class="modal-field"><label>Name</label><input type="text" id="reg-name" placeholder="Your name"/></div>
      <div class="modal-field"><label>Email</label><input type="email" id="reg-email" placeholder="you@example.com"/></div>
      <div class="modal-field"><label>Password</label><input type="password" id="reg-password" placeholder="Min 8 characters"/></div>
      <div class="modal-err" id="reg-err"></div>
      <button class="modal-btn" id="reg-submit-btn" onclick="doRegister()">Create account</button>
      <div class="modal-switch">Already have an account? <button onclick="showLogin()">Sign in</button></div>
    </div>
  </div>
</div>

<script>
var API = 'https://api.edgepostureapp.com';
var tok = localStorage.getItem('ep_token') || null;
var user = null;
var pendingUrl = null;

try { user = JSON.parse(localStorage.getItem('ep_user') || 'null'); } catch(e) {}

function initAuth() {
  if (tok && user) {
    showUserPill(user.name);
  } else {
    document.getElementById('nav-signin-btn').style.display = 'block';
  }
}

function showUserPill(name) {
  document.getElementById('nav-username').textContent = name;
  document.getElementById('user-pill-nav').style.display = 'flex';
  document.getElementById('nav-signin-btn').style.display = 'none';
}

function gatedNav(e, url) {
  if (tok && user) return true;
  e.preventDefault();
  pendingUrl = url;
  openModal('login');
  return false;
}

function openModal(mode) {
  document.getElementById('auth-modal').classList.remove('hidden');
  if (mode === 'register') showRegister();
  else showLogin();
}

function closeModal() {
  document.getElementById('auth-modal').classList.add('hidden');
  pendingUrl = null;
  clearErrors();
}

function showLogin() {
  document.getElementById('login-form').style.display = 'block';
  document.getElementById('register-form').style.display = 'none';
  clearErrors();
}

function showRegister() {
  document.getElementById('login-form').style.display = 'none';
  document.getElementById('register-form').style.display = 'block';
  clearErrors();
}

function clearErrors() {
  var els = document.querySelectorAll('.modal-err');
  els.forEach(function(el) { el.style.display = 'none'; el.textContent = ''; });
}

function showErr(id, msg) {
  var el = document.getElementById(id);
  el.textContent = msg;
  el.style.display = 'block';
}

async function doLogin() {
  var email = document.getElementById('login-email').value.trim();
  var password = document.getElementById('login-password').value;
  var btn = document.getElementById('login-submit-btn');
  if (!email || !password) { showErr('login-err', 'Email and password required'); return; }
  btn.textContent = 'Signing in...'; btn.disabled = true;
  try {
    var r = await fetch(API + '/auth/login', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({email, password}) });
    var d = await r.json();
    if (!r.ok) { showErr('login-err', d.error || 'Invalid credentials'); return; }
    onAuthed(d.token, d.user);
  } catch(e) { showErr('login-err', 'Connection error. Please try again.'); }
  finally { btn.textContent = 'Sign in'; btn.disabled = false; }
}

async function doRegister() {
  var name = document.getElementById('reg-name').value.trim();
  var email = document.getElementById('reg-email').value.trim();
  var password = document.getElementById('reg-password').value;
  var btn = document.getElementById('reg-submit-btn');
  if (!name || !email || !password) { showErr('reg-err', 'All fields required'); return; }
  if (password.length < 8) { showErr('reg-err', 'Password must be at least 8 characters'); return; }
  btn.textContent = 'Creating account...'; btn.disabled = true;
  try {
    var r = await fetch(API + '/auth/register', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({name, email, password}) });
    var d = await r.json();
    if (!r.ok) { showErr('reg-err', d.error || 'Registration failed'); return; }
    onAuthed(d.token, d.user);
  } catch(e) { showErr('reg-err', 'Connection error. Please try again.'); }
  finally { btn.textContent = 'Create account'; btn.disabled = false; }
}

function onAuthed(token, userData) {
  tok = token;
  user = userData;
  localStorage.setItem('ep_token', token);
  localStorage.setItem('ep_user', JSON.stringify(userData));
  showUserPill(userData.name);
  closeModal();
  if (pendingUrl) { window.location.href = pendingUrl; pendingUrl = null; }
}

function doSignOut() {
  tok = null; user = null;
  localStorage.removeItem('ep_token');
  localStorage.removeItem('ep_user');
  document.getElementById('user-pill-nav').style.display = 'none';
  document.getElementById('nav-signin-btn').style.display = 'block';
}

document.getElementById('auth-modal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeModal();
});

initAuth();
</script>
'''

html = html.replace('</body>', auth_html + '\n</body>')

with open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('edgeposture-ai auth gate written')