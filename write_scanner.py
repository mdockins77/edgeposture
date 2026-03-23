content = open('C:/Users/miked/edgeposture/worker-api/src/scanner.js', encoding='utf-8').read()

# Fix 1: Remove cfFeature Cloudflare reference from prompt
content = content.replace(
    '"cfFeature": "<relevant Cloudflare feature if applicable, or null>"',
    '"edgeFix": "<relevant edge platform feature or configuration that would fix this, or null>"'
)

# Fix 2: Fix negative scores in fallback - clamp all scores 0-100
old_fallback = '''function buildFallbackAnalysis(security, perf, compliance, cdn, pageData) {
  const missingHeaders = Object.entries(security).filter(([, v]) => !v).map(([k]) => k);
  const secScore = Math.max(0, 100 - missingHeaders.length * 10);
  const perfScore = perf.ttfbRating === 'good' ? 85 : perf.ttfbRating === 'needs-improvement' ? 60 : 35;
  const compScore = (compliance.hasCookieBanner ? 25 : 0) + (compliance.hasPrivacyPolicy ? 25 : 0) + (compliance.hasTermsOfService ? 25 : 0) + (compliance.cookieSecureFlags?.secure ? 25 : 0);
  const cdnScore = cdn.isCloudflare ? 90 : cdn.cdnProvider !== 'None detected' ? 70 : 30;
  const overall = Math.round((secScore + perfScore + compScore + cdnScore) / 4);'''

new_fallback = '''function buildFallbackAnalysis(security, perf, compliance, cdn, pageData) {
  const missingHeaders = Object.entries(security).filter(([, v]) => !v).map(([k]) => k);
  const clamp = (n) => Math.min(100, Math.max(0, Math.round(n)));
  const secScore = clamp(100 - missingHeaders.length * 10);
  const perfScore = clamp(perf.ttfbRating === 'good' ? 85 : perf.ttfbRating === 'needs-improvement' ? 60 : 35);
  const compScore = clamp((compliance.hasCookieBanner ? 25 : 0) + (compliance.hasPrivacyPolicy ? 25 : 0) + (compliance.hasTermsOfService ? 25 : 0) + (compliance.cookieSecureFlags?.secure ? 25 : 0));
  const cdnScore = clamp(cdn.cdnProvider !== 'None detected' ? 75 : 30);
  const overall = clamp((secScore + perfScore + compScore + cdnScore) / 4);'''

content = content.replace(old_fallback, new_fallback)

# Fix 3: Remove Cloudflare reference from fallback recommendation
content = content.replace(
    "cfFeature: 'Cloudflare Transform Rules can inject response headers without touching your origin.'",
    "edgeFix: 'Use your CDN or edge platform Transform Rules to inject response headers without touching your origin.'"
)

# Fix 4: Improve AI JSON parsing to clamp scores after parsing
old_parse = '''  let parsed;
  try {
    const text = aiResponse.response || '';
    const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);
    parsed = JSON.parse(jsonMatch ? jsonMatch[0] : text);
  } catch {
    // Fallback if AI returns malformed JSON
    parsed = buildFallbackAnalysis(securityHeaders, performanceSignals, complianceSignals, cdnSignals, pageData);
  }

  return parsed;'''

new_parse = '''  let parsed;
  try {
    const text = aiResponse.response || '';
    const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);
    parsed = JSON.parse(jsonMatch ? jsonMatch[0] : text);
    // Clamp all scores to valid 0-100 range
    const clamp = (n) => Math.min(100, Math.max(0, Math.round(Number(n) || 0)));
    if (parsed.scores) {
      parsed.scores.security = clamp(parsed.scores.security);
      parsed.scores.performance = clamp(parsed.scores.performance);
      parsed.scores.compliance = clamp(parsed.scores.compliance);
      parsed.scores.cdn = clamp(parsed.scores.cdn);
    }
    parsed.overallScore = clamp(parsed.overallScore || (
      ((parsed.scores?.security || 0) + (parsed.scores?.performance || 0) +
       (parsed.scores?.compliance || 0) + (parsed.scores?.cdn || 0)) / 4
    ));
  } catch {
    // Fallback if AI returns malformed JSON
    parsed = buildFallbackAnalysis(securityHeaders, performanceSignals, complianceSignals, cdnSignals, pageData);
  }

  return parsed;'''

content = content.replace(old_parse, new_parse)

with open('C:/Users/miked/edgeposture/worker-api/src/scanner.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('scanner.js fixed')