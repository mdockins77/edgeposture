html = open('C:/Users/miked/edgeposture/getedgeposture/index.html', encoding='utf-8').read()

# Swap Syne font import for Space Mono
html = html.replace(
    "family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300",
    "family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600"
)

# Replace all Syne font-family references with Space Mono
html = html.replace("font-family: 'Syne', sans-serif;", "font-family: 'Space Mono', monospace;")
html = html.replace('font-family:"Syne",sans-serif', 'font-family:"Space Mono",monospace')
html = html.replace("font-family:'Syne',sans-serif", "font-family:'Space Mono',monospace")

# Syne at weight 800 looks very wide - Space Mono only has 400 and 700
html = html.replace("font-weight: 800;", "font-weight: 700;")
html = html.replace("font-weight:800;", "font-weight:700;")

# Reduce letter-spacing on titles since Space Mono is already wide
html = html.replace("letter-spacing: -1px;", "letter-spacing: -0.5px;")

with open('C:/Users/miked/edgeposture/getedgeposture/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Font fixed')