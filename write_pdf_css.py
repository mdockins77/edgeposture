css = open('C:/Users/miked/edgeposture/edgepostureapp/src/index.css', encoding='utf-8').read()
css += '\n.pdf-btn{background:none;border:1px solid var(--border2);color:var(--text2);padding:8px 16px;border-radius:8px;font-size:13px;font-weight:500;cursor:pointer;font-family:"DM Sans",sans-serif;transition:border-color 0.15s,color 0.15s}.pdf-btn:hover{border-color:var(--accent);color:var(--accent2)}'
open('C:/Users/miked/edgeposture/edgepostureapp/src/index.css', 'w', encoding='utf-8').write(css)
print('CSS added')