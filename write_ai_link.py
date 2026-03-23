html = open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', encoding='utf-8').read()

# Fix modal card styling - make it much more visible
old_modal_css = '''.modal-card{background:#111318;border:1px solid rgba(255,255,255,0.14);border-radius:16px;padding:2.5rem;width:100%;max-width:420px}'''

new_modal_css = '''.modal-card{background:#1a1f2e;border:2px solid #4f7bff;border-radius:16px;padding:2.5rem;width:100%;max-width:420px;box-shadow:0 0 60px rgba(0,0,0,0.8)}'''

if old_modal_css in html:
    html = html.replace(old_modal_css, new_modal_css)
    print('Modal card CSS updated')
else:
    # Try to find and update it differently
    import re
    html = re.sub(
        r'\.modal-card\{background:[^}]+\}',
        '.modal-card{background:#1a1f2e;border:2px solid #4f7bff;border-radius:16px;padding:2.5rem;width:100%;max-width:420px}',
        html
    )
    print('Modal card CSS updated via regex')

# Also make the overlay more visible
old_overlay = 'background:rgba(0,0,0,0.75)'
new_overlay = 'background:rgba(0,0,0,0.85)'
html = html.replace(old_overlay, new_overlay)

# Fix modal field input colors to be clearly visible
old_input = '''.modal-field input{width:100%;background:#0a0c10;border:1px solid rgba(255,255,255,0.14);color:#e8eaf0;padding:10px 14px;border-radius:8px;font-size:14px;font-family:"DM Sans",sans-serif;outline:none;box-sizing:border-box}'''
new_input = '''.modal-field input{width:100%;background:#0d1117;border:1px solid rgba(79,123,255,0.4);color:#e8eaf0;padding:10px 14px;border-radius:8px;font-size:14px;font-family:"DM Sans",sans-serif;outline:none;box-sizing:border-box}'''

if old_input in html:
    html = html.replace(old_input, new_input)
    print('Input CSS updated')

with open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')