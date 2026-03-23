import os

ai_html = open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', encoding='utf-8').read()
consult_html = open('C:/Users/miked/edgeposture/getedgeposture/index.html', encoding='utf-8').read()

ai_replacements = [
    ("Expert Cloudflare consulting, web security posture analysis, and CDN optimization. Built by a Cloudflare Solutions Engineer.",
     "Expert CDN, application performance, and application security consulting. Built by an industry SME with deep edge network expertise."),
    ("Powered by Cloudflare AI", "AI-powered"),
    ("Expert Cloudflare consulting when you need to go deeper.", "Expert CDN and application security consulting when you need to go deeper."),
    ("Hire a Cloudflare SE", "Hire an Edge SME"),
    ("Cloudflare-native stack", "100% edge-native stack"),
    ("Add via Cloudflare Transform Rules", "Add via edge Transform Rules"),
    ("Enable Cloudflare proxying on this zone", "Enable CDN proxying on this zone"),
    ("Enable Cloudflare Tiered Cache", "Enable CDN Tiered Cache"),
    ("Expert Cloudflare help", "Expert edge &amp; security help"),
    ("Built by a Cloudflare Solutions Engineer. When your posture score isn't enough, get hands-on help configuring WAF rules, optimizing cache, hardening headers, and architecting edge-native applications.",
     "Built by a Subject Matter Expert in CDNs, Application Performance, and Application Security. When your posture score isn't enough, get hands-on help configuring WAF rules, optimizing cache, hardening headers, and architecting edge-native applications."),
    ('<div class="service-title">Cloudflare migration</div>', '<div class="service-title">CDN migration</div>'),
    ("Moving from another CDN or hosting provider to Cloudflare. Zone setup, DNS migration, SSL configuration, and Workers replatforming.",
     "Moving from another CDN or hosting provider to a modern edge network. Zone setup, DNS migration, SSL configuration, and edge compute replatforming."),
    ("privacy headers, data residency setup with Cloudflare Data Localization Suite.",
     "privacy headers, data residency setup, and edge-enforced compliance controls."),
    ("continuous posture monitoring, incident support, Cloudflare new feature evaluation, and architecture guidance.",
     "continuous posture monitoring, incident support, new edge feature evaluation, and architecture guidance."),
    ("A Cloudflare Worker fetches the page, extracting headers, response times, DOM signals, and CDN indicators.",
     "An edge Worker fetches the page, extracting headers, response times, DOM signals, and CDN indicators."),
    ("Built 100% on Cloudflare", "Built 100% on edge infrastructure"),
]

consult_replacements = [
    ("Get EdgePosture — Book a Cloudflare Consulting Engagement",
     "Get EdgePosture — Book a CDN & Application Security Consulting Engagement"),
    ("Book a Cloudflare consulting engagement with a certified Solutions Engineer.",
     "Book a consulting engagement with a CDN, Application Performance, and Application Security Subject Matter Expert."),
    ("Cloudflare SE · Available for hire", "CDN &amp; AppSec SME · Available for hire"),
    ("Cloudflare expertise, <span>on demand</span>", "Edge &amp; security expertise, <span>on demand</span>"),
    ("Get hands-on help from a Cloudflare Solutions Engineer.",
     "Get hands-on help from a Subject Matter Expert in CDNs, Application Performance, and Application Security."),
    ("Workers architecture, WAF configuration", "edge architecture, WAF configuration"),
    ("Cloudflare certified", "CDN &amp; AppSec certified"),
    ("hands-on implementation of fixes directly in your Cloudflare dashboard.",
     "hands-on implementation of fixes directly in your CDN dashboard."),
    ("Hands-on in your Cloudflare dashboard", "Hands-on in your CDN dashboard"),
    ('<div class="bio-role">Cloudflare Solutions Engineer</div>',
     '<div class="bio-role">CDN, Application Performance &amp; Security SME</div>'),
    ("I'm a Solutions Engineer at Cloudflare",
     "I'm a Subject Matter Expert in CDNs, Application Performance, and Application Security"),
    ("helping companies architect, secure, and optimize their presence on the Cloudflare network.",
     "helping companies architect, secure, and optimize their web presence at the edge."),
    ("EdgePosture is the tooling and consulting practice I built on the side to make that expertise accessible to teams that don't have enterprise contracts.",
     "EdgePosture is the tooling and consulting practice I built to make that expertise accessible to teams of all sizes."),
    ('<span class="bio-tag">Cloudflare Workers</span>', '<span class="bio-tag">Edge Compute</span>'),
]

for old, new in ai_replacements:
    ai_html = ai_html.replace(old, new)

for old, new in consult_replacements:
    consult_html = consult_html.replace(old, new)

with open('C:/Users/miked/edgeposture/edgeposture-ai/index.html', 'w', encoding='utf-8') as f:
    f.write(ai_html)
print('edgeposture-ai done')

with open('C:/Users/miked/edgeposture/getedgeposture/index.html', 'w', encoding='utf-8') as f:
    f.write(consult_html)
print('getedgeposture done')