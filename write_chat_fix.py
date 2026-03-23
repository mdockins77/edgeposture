html = open('C:/Users/miked/edgeposture/chat-frontend/index.html', encoding='utf-8').read()

# Rename history variable to chatHistory throughout
html = html.replace('var history=[];', 'var chatHistory=[];')
html = html.replace('history.push({role:"user",content:msg});', 'chatHistory.push({role:"user",content:msg});')
html = html.replace('history:history.slice(-10)', 'history:chatHistory.slice(-10)')
html = html.replace('if(!d.blocked)history.push({role:"assistant",content:d.reply});', 'if(!d.blocked)chatHistory.push({role:"assistant",content:d.reply});')

with open('C:/Users/miked/edgeposture/chat-frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Fixed')