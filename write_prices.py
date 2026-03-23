import re

for path in ['C:/Users/miked/edgeposture/edgeposture-ai/index.html', 'C:/Users/miked/edgeposture/getedgeposture/index.html']:
    html = open(path, encoding='utf-8').read()
    prices = re.findall(r'\$[\d,]+[^<"\s]*', html)
    print(f'\n{path.split("/")[-2]} prices found:')
    for p in set(prices):
        print(' ', p)