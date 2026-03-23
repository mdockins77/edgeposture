import os

# 1. Update edgeposture.ai - pass token when redirecting
path = 'C:/Users/miked/edgeposture/edgeposture-ai/index.html'
html = open(path, encoding='utf-8').read()

old_authed = '''function onAuthed(token, userData) {
  tok = token;
  user = userData;
  localStorage.setItem('ep_token', token);
  localStorage.setItem('ep_user', JSON.stringify(userData));
  showUserPill(userData.name);
  closeModal();
  if (pendingUrl) { window.location.href = pendingUrl; pendingUrl = null; }
}'''

new_authed = '''function onAuthed(token, userData) {
  tok = token;
  user = userData;
  localStorage.setItem('ep_token', token);
  localStorage.setItem('ep_user', JSON.stringify(userData));
  showUserPill(userData.name);
  closeModal();
  if (pendingUrl) {
    var sep = pendingUrl.indexOf('?') >= 0 ? '&' : '?';
    window.location.href = pendingUrl + sep + 'ep_token=' + encodeURIComponent(token) + '&ep_user=' + encodeURIComponent(JSON.stringify(userData));
    pendingUrl = null;
  }
}'''

if old_authed in html:
    html = html.replace(old_authed, new_authed)
    print('edgeposture-ai onAuthed updated')
else:
    print('WARNING: onAuthed not found in edgeposture-ai')

# Also update gatedNav to pass token if already logged in
old_gated = '''document.addEventListener('click', function(e) {
  var el = e.target.closest('[data-gated]');
  if (!el) return;
  var url = el.getAttribute('data-gated');
  if (!url) return;
  if (tok && user) {
    window.location.href = url;
  } else {
    e.preventDefault();
    pendingUrl = url;
    openModal('login');
  }
});'''

new_gated = '''document.addEventListener('click', function(e) {
  var el = e.target.closest('[data-gated]');
  if (!el) return;
  var url = el.getAttribute('data-gated');
  if (!url) return;
  if (tok && user) {
    var sep = url.indexOf('?') >= 0 ? '&' : '?';
    window.location.href = url + sep + 'ep_token=' + encodeURIComponent(tok) + '&ep_user=' + encodeURIComponent(JSON.stringify(user));
  } else {
    e.preventDefault();
    pendingUrl = url;
    openModal('login');
  }
});'''

if old_gated in html:
    html = html.replace(old_gated, new_gated)
    print('edgeposture-ai gatedNav updated')
else:
    print('WARNING: gatedNav listener not found')

open(path, 'w', encoding='utf-8').write(html)

# SSO receiver script - add to each receiving site
sso_script = '''
<script>
(function() {
  try {
    var params = new URLSearchParams(window.location.search);
    var token = params.get('ep_token');
    var userStr = params.get('ep_user');
    if (token) {
      localStorage.setItem('ep_token', token);
      if (userStr) localStorage.setItem('ep_user', userStr);
      // Clean URL without reloading
      var clean = window.location.pathname;
      window.history.replaceState({}, document.title, clean);
    }
  } catch(e) {}
})();
</script>
'''

# 2. Add SSO receiver to edgepostureapp index.html
path = 'C:/Users/miked/edgeposture/edgepostureapp/index.html'
html = open(path, encoding='utf-8').read()
if 'ep_token' not in html:
    html = html.replace('<div id="root"></div>', sso_script + '\n<div id="root"></div>')
    open(path, 'w', encoding='utf-8').write(html)
    print('edgepostureapp SSO receiver added')
else:
    print('edgepostureapp SSO already present')

# 3. Add SSO receiver to blog-frontend
path = 'C:/Users/miked/edgeposture/blog-frontend/index.html'
html = open(path, encoding='utf-8').read()
if 'ep_token' not in html:
    html = html.replace('<main id="app"></main>', sso_script + '\n<main id="app"></main>')
    open(path, 'w', encoding='utf-8').write(html)
    print('blog SSO receiver added')
else:
    print('blog SSO already present')

# 4. Add SSO receiver to chat-frontend
path = 'C:/Users/miked/edgeposture/chat-frontend/index.html'
html = open(path, encoding='utf-8').read()
if 'ep_token' not in html:
    html = html.replace('<div class="app-body" id="app-body">', sso_script + '\n<div class="app-body" id="app-body">')
    open(path, 'w', encoding='utf-8').write(html)
    print('chat SSO receiver added')
else:
    print('chat SSO already present')

print('All SSO updates done')