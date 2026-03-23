html = open('C:/Users/miked/edgeposture/blog-frontend/index.html', encoding='utf-8').read()

old = '      h+="<span class=\\"badge "+(p.published?"badge-pub":"badge-draft)+"\\">"+(p.published?"published":"draft")+"</span>";'
new = '      h+="<span class=\\"badge "+(p.published?"badge-pub":"badge-draft")+"\\">"+(p.published?"published":"draft")+"</span>";'

if old in html:
    html = html.replace(old, new)
    print("Fixed")
else:
    print("Not found - showing line 203:")
    lines = html.split('\n')
    print(repr(lines[202]))

with open('C:/Users/miked/edgeposture/blog-frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)