content = open('C:/Users/miked/edgeposture/worker-api/src/scanner.js', encoding='utf-8').read()

# Fix 1: Update the AI prompt to be CDN-agnostic
old_prompt_end = '''Be specific, actionable, and accurate. Include 3-8 findings and 3-6 recommendations.`;'''

new_prompt_end = '''Be specific, actionable, and accurate. Include 3-8 findings and 3-6 recommendations.

IMPORTANT RULES:
- Never mention "Cloudflare" by name in findings or recommendations. Use "CDN", "edge platform", or "your CDN provider" instead.
- Never mention specific vendor product names. Keep findings vendor-neutral.
- Scores must be integers between 0 and 100. Do not return 0 unless the site is completely broken.
- Base scores on actual evidence from the headers and page data provided.`;'''

content = content.replace(old_prompt_end, new_prompt_end)

# Fix 2: Tighten fetch timeout from 10000 to 5000ms
content = content.replace(
    'const timeout = setTimeout(() => controller.abort(), 10000);',
    'const timeout = setTimeout(() => controller.abort(), 5000);'
)

# Fix 3: Better error message for timeout/bad URL
content = content.replace(
    "throw new Error(`Failed to fetch URL: ${err.message}`);",
    "throw new Error(err.name === 'AbortError' ? 'Request timed out — the URL may be invalid or the server is not responding.' : `Failed to fetch URL: ${err.message}`);"
)

with open('C:/Users/miked/edgeposture/worker-api/src/scanner.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('prompt and timeout fixed')