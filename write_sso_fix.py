html = open('C:/Users/miked/edgeposture/edgepostureapp/index.html', encoding='utf-8').read()
idx = html.find('ep_token')
print('SSO script in edgepostureapp/index.html:')
print(html[idx-100:idx+400])