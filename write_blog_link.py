html = open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', encoding='utf-8').read()

old = '<a class="nav-link" href="https://getedgeposture.com">Consulting</a>'
new = '<a class="nav-link" href="https://getedgeposture.com">Consulting</a>\n    <a class="nav-link" href="https://blog.edgeposture.ai">Blog</a>'

if old in html:
    html = html.replace(old, new)
    print('Blog link added to nav')
else:
    print('NOT FOUND')

with open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', 'w', encoding='utf-8') as f:
    f.write(html)