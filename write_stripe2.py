html = open('C:/Users/miked/edgeposture/getedgeposture/index.html', encoding='utf-8').read()

replacements = [
    ('https://buy.stripe.com/28E5kCeLe1Yr5PS7oA4ZG02', 'https://buy.stripe.com/9B6bJ01Ys0Unemo7oA4ZG03'),
    ('https://buy.stripe.com/4gM5kC6eI7iLdikfV64ZG00', 'https://buy.stripe.com/3cI14m6eIcD51zCeR24ZG04'),
    ('https://buy.stripe.com/cNi00i6eI6eH5PSaAM4ZG01', 'https://buy.stripe.com/dRm9ASgTm0Un924aAM4ZG05'),
]

count = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        count += 1
        print(f'Updated: {old[-10:]} -> {new[-10:]}')
    else:
        print(f'NOT FOUND: {old[-10:]}')

with open('C:/Users/miked/edgeposture/getedgeposture/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Done - {count} links updated')