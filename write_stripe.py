html = open('C:/Users/miked/edgeposture/getedgeposture/index.html', encoding='utf-8').read()

replacements = [
    (
        '<a class="pkg-btn" href="mailto:mike.2.dockins@gmail.com?subject=Posture Review Engagement">Book this \u2192</a>',
        '<a class="pkg-btn" href="https://buy.stripe.com/28E5kCeLe1Yr5PS7oA4ZG02" target="_blank" rel="noreferrer">Buy now \u2192</a>'
    ),
    (
        '<a class="pkg-btn" href="mailto:mike.2.dockins@gmail.com?subject=Security + Performance Engagement">Book this \u2192</a>',
        '<a class="pkg-btn" href="https://buy.stripe.com/4gM5kC6eI7iLdikfV64ZG00" target="_blank" rel="noreferrer">Buy now \u2192</a>'
    ),
    (
        '<a class="pkg-btn" href="mailto:mike.2.dockins@gmail.com?subject=Architecture Advisory Engagement">Book this \u2192</a>',
        '<a class="pkg-btn" href="https://buy.stripe.com/cNi00i6eI6eH5PSaAM4ZG01" target="_blank" rel="noreferrer">Buy now \u2192</a>'
    ),
    (
        '<a class="btn-orange" href="mailto:mike.2.dockins@gmail.com?subject=EdgePosture Consulting">Book a consultation \u2192</a>',
        '<a class="btn-orange" href="https://buy.stripe.com/4gM5kC6eI7iLdikfV64ZG00" target="_blank" rel="noreferrer">Book a consultation \u2192</a>'
    ),
]

count = 0
for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        count += 1
        print(f'Replaced: {old[:70]}')
    else:
        print(f'NOT FOUND: {old[:70]}')

with open('C:/Users/miked/edgeposture/getedgeposture/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f'Done - {count} replacements made')