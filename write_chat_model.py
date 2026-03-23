content = open('C:/Users/miked/edgeposture/chat-worker/src/index.js', encoding='utf-8').read()

old = '"@cf/meta/llama-3.1-8b-instruct"'
new = '"@cf/mistral/mistral-7b-instruct-v0.1"'

if old in content:
    content = content.replace(old, new)
    print('Model switched to Mistral 7B')
else:
    print('NOT FOUND')

with open('C:/Users/miked/edgeposture/chat-worker/src/index.js', 'w', encoding='utf-8') as f:
    f.write(content)