content = open('C:/Users/miked/edgeposture/worker-api/src/scanner.js', encoding='utf-8').read()

old_parse = '''  let parsed;
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

new_parse = '''  let parsed;
  try {
    const text = aiResponse.response || '';
    const jsonMatch = text.match(/\\{[\\s\\S]*\\}/);
    parsed = JSON.parse(jsonMatch ? jsonMatch[0] : text);
  } catch {
    parsed = buildFallbackAnalysis(securityHeaders, performanceSignals, complianceSignals, cdnSignals, pageData);
  }

  // Always recalculate scores from findings — don't trust AI-returned scores
  parsed.scores = calculateScoresFromFindings(
    parsed.findings || [],
    securityHeaders,
    performanceSignals,
    complianceSignals,
    cdnSignals
  );
  const s = parsed.scores;
  parsed.overallScore = Math.round((s.security + s.performance + s.compliance + s.cdn) / 4);

  return parsed;'''

content = content.replace(old_parse, new_parse)

# Add the score calculation function before buildFallbackAnalysis
new_function = '''function calculateScoresFromFindings(findings, security, perf, compliance, cdn) {
  const clamp = (n) => Math.min(100, Math.max(0, Math.round(n)));

  // Security score: start at 100, deduct for missing headers and findings
  const missingHeaders = Object.entries(security).filter(([, v]) => !v).length;
  let secScore = 100 - (missingHeaders * 8);
  findings.filter(f => f.category === 'security').forEach(f => {
    if (f.severity === 'critical') secScore -= 20;
    else if (f.severity === 'high') secScore -= 12;
    else if (f.severity === 'medium') secScore -= 6;
    else if (f.severity === 'low') secScore -= 3;
  });

  // Performance score: based on TTFB, compression, size
  let perfScore = 100;
  if (perf.ttfbRating === 'needs-improvement') perfScore -= 20;
  else if (perf.ttfbRating === 'poor') perfScore -= 40;
  if (!perf.hasCompression) perfScore -= 15;
  if (perf.responseSizeRating === 'needs-improvement') perfScore -= 10;
  else if (perf.responseSizeRating === 'large') perfScore -= 20;
  findings.filter(f => f.category === 'performance').forEach(f => {
    if (f.severity === 'critical') perfScore -= 15;
    else if (f.severity === 'high') perfScore -= 10;
    else if (f.severity === 'medium') perfScore -= 5;
    else if (f.severity === 'low') perfScore -= 2;
  });

  // Compliance score: based on signals
  let compScore = 50;
  if (compliance.hasCookieBanner) compScore += 15;
  if (compliance.hasPrivacyPolicy) compScore += 15;
  if (compliance.hasTermsOfService) compScore += 10;
  if (compliance.cookieSecureFlags?.secure) compScore += 5;
  if (compliance.cookieSecureFlags?.httpOnly) compScore += 5;
  findings.filter(f => f.category === 'compliance').forEach(f => {
    if (f.severity === 'high') compScore -= 10;
    else if (f.severity === 'medium') compScore -= 5;
    else if (f.severity === 'low') compScore -= 2;
  });

  // CDN score: based on CDN detection and cache signals
  let cdnScore = cdn.cdnProvider !== 'None detected' ? 70 : 20;
  if (cdn.cfCacheStatus === 'HIT') cdnScore += 20;
  else if (cdn.cfCacheStatus === 'MISS') cdnScore += 5;
  if (cdn.ageHeader) cdnScore += 5;
  if (cdn.varyHeader) cdnScore += 5;
  findings.filter(f => f.category === 'cdn').forEach(f => {
    if (f.severity === 'critical') cdnScore -= 20;
    else if (f.severity === 'high') cdnScore -= 12;
    else if (f.severity === 'medium') cdnScore -= 6;
    else if (f.severity === 'low') cdnScore -= 3;
  });

  return {
    security: clamp(secScore),
    performance: clamp(perfScore),
    compliance: clamp(compScore),
    cdn: clamp(cdnScore),
  };
}

'''

content = content.replace(
    'function buildFallbackAnalysis(',
    new_function + 'function buildFallbackAnalysis('
)

with open('C:/Users/miked/edgeposture/worker-api/src/scanner.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('scanner.js score calculation fixed')