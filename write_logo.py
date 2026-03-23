import os

svg = '''<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
<rect width="500" height="500" rx="40" fill="#080a0f"/>
<rect width="500" height="500" rx="40" fill="none" stroke="#1a1f2e" stroke-width="2"/>
<text font-family="Share Tech Mono,Courier New,monospace" font-size="11" fill="#0d2040">
  <tspan x="18" y="40">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">1</tspan><tspan x="18" dy="16">0</tspan>
</text>
<text font-family="Share Tech Mono,Courier New,monospace" font-size="11" fill="#152a4a">
  <tspan x="32" y="48">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan><tspan x="32" dy="16">1</tspan><tspan x="32" dy="16">0</tspan>
</text>
<text font-family="Share Tech Mono,Courier New,monospace" font-size="11" fill="#0d2040">
  <tspan x="456" y="40">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">0</tspan><tspan x="456" dy="16">1</tspan><tspan x="456" dy="16">0</tspan>
</text>
<text font-family="Share Tech Mono,Courier New,monospace" font-size="11" fill="#152a4a">
  <tspan x="470" y="48">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">0</tspan><tspan x="470" dy="16">1</tspan>
</text>
<polygon points="250,28 338,78 338,178 250,228 162,178 162,78" fill="none" stroke="#1e2a3a" stroke-width="2"/>
<polygon points="250,36 330,83 330,174 250,221 170,174 170,83" fill="none" stroke="#243040" stroke-width="1"/>
<polygon points="250,46 322,88 322,170 250,212 178,170 178,88" fill="#0c1420"/>
<polygon points="250,46 322,88 322,170 250,212 178,170 178,88" fill="none" stroke="#1a3a5c" stroke-width="2"/>
<path d="M170 92 L170 83 L179 83" fill="none" stroke="#4f7bff" stroke-width="2.5" stroke-linecap="square"/>
<path d="M330 92 L330 83 L321 83" fill="none" stroke="#4f7bff" stroke-width="2.5" stroke-linecap="square"/>
<path d="M170 162 L170 174 L179 174" fill="none" stroke="#4f7bff" stroke-width="2.5" stroke-linecap="square"/>
<path d="M330 162 L330 174 L321 174" fill="none" stroke="#4f7bff" stroke-width="2.5" stroke-linecap="square"/>
<rect x="195" y="92" width="42" height="8" rx="1" fill="#4f7bff"/>
<rect x="195" y="108" width="32" height="7" rx="1" fill="#4f7bff"/>
<rect x="195" y="121" width="42" height="7" rx="1" fill="#4f7bff"/>
<rect x="195" y="134" width="32" height="7" rx="1" fill="#4f7bff"/>
<rect x="195" y="147" width="42" height="8" rx="1" fill="#4f7bff"/>
<rect x="195" y="92" width="8" height="63" rx="1" fill="#4f7bff"/>
<rect x="243" y="92" width="8" height="63" rx="1" fill="#7c9fff"/>
<rect x="243" y="92" width="32" height="7" rx="1" fill="#7c9fff"/>
<rect x="243" y="121" width="32" height="7" rx="1" fill="#7c9fff"/>
<rect x="267" y="92" width="8" height="35" rx="1" fill="#7c9fff"/>
<rect x="168" y="182" width="164" height="2" rx="1" fill="#4f7bff" opacity="0.6"/>
<rect x="200" y="188" width="100" height="1" rx="0.5" fill="#4f7bff" opacity="0.3"/>
<text x="250" y="270" font-family="Bebas Neue,Arial Narrow,sans-serif" font-size="72" fill="#e8eaf0" text-anchor="middle" letter-spacing="6">EDGE</text>
<text x="250" y="340" font-family="Bebas Neue,Arial Narrow,sans-serif" font-size="58" fill="#4f7bff" text-anchor="middle" letter-spacing="6">POSTURE</text>
<rect x="60" y="348" width="50" height="2" rx="1" fill="#4f7bff" opacity="0.5"/>
<rect x="390" y="348" width="50" height="2" rx="1" fill="#4f7bff" opacity="0.5"/>
<text x="250" y="378" font-family="Share Tech Mono,Courier New,monospace" font-size="12" fill="#3a4560" text-anchor="middle" letter-spacing="3">SECURE · PERFORM · DEFEND</text>
<rect x="130" y="392" width="240" height="2.5" rx="1" fill="#4f7bff" opacity="0.35"/>
<rect x="22" y="22" width="20" height="2.5" fill="#4f7bff" opacity="0.5"/>
<rect x="22" y="22" width="2.5" height="20" fill="#4f7bff" opacity="0.5"/>
<rect x="458" y="22" width="20" height="2.5" fill="#4f7bff" opacity="0.5"/>
<rect x="475.5" y="22" width="2.5" height="20" fill="#4f7bff" opacity="0.5"/>
<rect x="22" y="458" width="20" height="2.5" fill="#4f7bff" opacity="0.5"/>
<rect x="22" y="438" width="2.5" height="20" fill="#4f7bff" opacity="0.5"/>
<rect x="458" y="458" width="20" height="2.5" fill="#4f7bff" opacity="0.5"/>
<rect x="475.5" y="438" width="2.5" height="20" fill="#4f7bff" opacity="0.5"/>
<text x="250" y="425" font-family="Share Tech Mono,Courier New,monospace" font-size="9" fill="#1e2540" text-anchor="middle" letter-spacing="2">EST. 2025 · EDGE NATIVE</text>
</svg>'''

# Favicon SVG - simple EP mark, works at 32x32
favicon_svg = '''<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
<rect width="32" height="32" rx="4" fill="#080a0f"/>
<polygon points="16,3 27,9 27,23 16,29 5,23 5,9" fill="#0c1420" stroke="#1a3a5c" stroke-width="1"/>
<rect x="8" y="9" width="7" height="2" rx="0.5" fill="#4f7bff"/>
<rect x="8" y="13" width="5" height="2" rx="0.5" fill="#4f7bff"/>
<rect x="8" y="17" width="7" height="2" rx="0.5" fill="#4f7bff"/>
<rect x="8" y="9" width="2" height="12" rx="0.5" fill="#4f7bff"/>
<rect x="17" y="9" width="2" height="12" rx="0.5" fill="#7c9fff"/>
<rect x="17" y="9" width="7" height="2" rx="0.5" fill="#7c9fff"/>
<rect x="17" y="13" width="7" height="2" rx="0.5" fill="#7c9fff"/>
<rect x="22" y="9" width="2" height="6" rx="0.5" fill="#7c9fff"/>
</svg>'''

# Write logo SVG
os.makedirs('C:/Users/miked/edgeposture/logo', exist_ok=True)
with open('C:/Users/miked/edgeposture/logo/edgeposture-logo.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print('Logo SVG written')

# Write favicon SVG for each site
sites = [
    'C:/Users/miked/edgeposture/edgeposture-ai',
    'C:/Users/miked/edgeposture/edgepostureapp',
    'C:/Users/miked/edgeposture/getedgeposture',
    'C:/Users/miked/edgeposture/blog-frontend',
    'C:/Users/miked/edgeposture/chat-frontend',
]

for site in sites:
    path = site + '/favicon.svg'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(favicon_svg)
    print(f'Favicon written: {path}')

# Update each HTML site to reference the favicon
html_sites = [
    ('C:/Users/miked/edgeposture/edgeposture-ai/index.html', 'edgeposture-ai'),
    ('C:/Users/miked/edgeposture/getedgeposture/index.html', 'getedgeposture'),
    ('C:/Users/miked/edgeposture/blog-frontend/index.html', 'blog'),
    ('C:/Users/miked/edgeposture/chat-frontend/index.html', 'chat'),
]

for path, name in html_sites:
    html = open(path, encoding='utf-8').read()
    if 'favicon' not in html:
        html = html.replace('</head>', '<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>\n</head>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Favicon link added: {name}')
    else:
        html = html.replace(
            'href="/favicon.svg"',
            'href="/favicon.svg"'
        )
        # Replace any existing favicon
        import re
        html = re.sub(r'<link rel="icon"[^>]*>', '<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'Favicon updated: {name}')

# Update edgepostureapp index.html
app_html = open('C:/Users/miked/edgeposture/edgepostureapp/index.html', encoding='utf-8').read()
import re
app_html = re.sub(r'<link rel="icon"[^>]*>', '<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>', app_html)
if 'favicon' not in app_html:
    app_html = app_html.replace('</head>', '<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>\n</head>')
with open('C:/Users/miked/edgeposture/edgepostureapp/index.html', 'w', encoding='utf-8') as f:
    f.write(app_html)
print('Favicon updated: edgepostureapp')

print('All done!')