# Add chat link to scanner app nav
content = open('C:/Users/miked/edgeposture/edgepostureapp/src/components/Nav.jsx', encoding='utf-8').read()

old = '<a className="nav-link" href="https://getedgeposture.com" target="_blank" rel="noreferrer">Consulting</a>'
new = '<a className="nav-link" href="https://getedgeposture.com" target="_blank" rel="noreferrer">Consulting</a>\n        <a className="nav-link" href="https://chat.edgeposture.ai" target="_blank" rel="noreferrer">AI Chat</a>'

if old in content:
    content = content.replace(old, new)
    print('Chat link added to nav')
else:
    print('NOT FOUND - showing nav links:')
    for i, line in enumerate(content.split('\n')):
        if 'nav-link' in line:
            print(f'{i}: {line.strip()}')

with open('C:/Users/miked/edgeposture/edgepostureapp/src/components/Nav.jsx', 'w', encoding='utf-8') as f:
    f.write(content)