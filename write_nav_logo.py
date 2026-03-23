import os

# Inline SVG mark - small version for nav (32x32)
nav_svg = '''<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg>'''

# 1. edgeposture-ai - replace nav logo div
path = 'C:/Users/miked/edgeposture/edgeposture-ai/index.html'
html = open(path, encoding='utf-8').read()
html = html.replace(
    '<div class="nav-logo">EP</div>',
    nav_svg
)
html = html.replace(
    '<div class="footer-logo">EP</div>',
    '<svg width="28" height="28" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg>'
)
open(path, 'w', encoding='utf-8').write(html)
print('edgeposture-ai updated')

# 2. getedgeposture - orange theme nav logo
path = 'C:/Users/miked/edgeposture/getedgeposture/index.html'
html = open(path, encoding='utf-8').read()
html = html.replace(
    '<div class="nav-logo">EP</div>',
    nav_svg
)
# Footer logo
html = html.replace(
    '<div style="width:28px;height:28px;background:#e85d20;border-radius:6px;display:flex;align-items:center;justify-content:center;font-family:\'Syne\',sans-serif;font-size:11px;font-weight:800;color:#fff;">EP</div>',
    '<svg width="28" height="28" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg>'
)
open(path, 'w', encoding='utf-8').write(html)
print('getedgeposture updated')

# 3. blog frontend
path = 'C:/Users/miked/edgeposture/blog-frontend/index.html'
html = open(path, encoding='utf-8').read()
html = html.replace(
    '<div class="nav-logo">EP</div>',
    nav_svg
)
open(path, 'w', encoding='utf-8').write(html)
print('blog-frontend updated')

# 4. chat frontend
path = 'C:/Users/miked/edgeposture/chat-frontend/index.html'
html = open(path, encoding='utf-8').read()
html = html.replace(
    '<div class="nav-logo">EP</div>',
    nav_svg
)
open(path, 'w', encoding='utf-8').write(html)
print('chat-frontend updated')

# 5. edgepostureapp - update Nav.jsx component
path = 'C:/Users/miked/edgeposture/edgepostureapp/src/components/Nav.jsx'
jsx = open(path, encoding='utf-8').read()
jsx = jsx.replace(
    '<span className="nav-logo">EP</span>',
    '<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg>'
)
open(path, 'w', encoding='utf-8').write(jsx)
print('edgepostureapp Nav.jsx updated')

# Also update auth pages logo in Login.jsx
path = 'C:/Users/miked/edgeposture/edgepostureapp/src/pages/Login.jsx'
jsx = open(path, encoding='utf-8').read()
jsx = jsx.replace(
    '<div className="auth-logo">EP</div>',
    '<div className="auth-logo" style={{background:"none",padding:0}}><svg width="44" height="44" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><rect width="32" height="32" rx="4" fill="#080a0f"/><polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/><rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/><rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/><rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/><rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/><rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/></svg></div>'
)
open(path, 'w', encoding='utf-8').write(jsx)
print('Login.jsx auth logo updated')

print('All nav logos updated!')