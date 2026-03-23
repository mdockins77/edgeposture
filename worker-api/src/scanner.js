export async function handleScan(request, env, ctx) {
  const { url } = await request.json();

  if (!url || !isValidUrl(url)) {
    throw new Error('Invalid URL provided');
  }

  const cacheKey = `scan:${url}`;
  const cached = await env.CACHE.get(cacheKey, 'json');
  if (cached) return { ...cached, cached: true };

  // Fetch the target page
  const fetchStart = Date.now();
  let pageData;
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    const resp = await fetch(url, {
      signal: controller.signal,
      headers: { 'User-Agent': 'EdgePosture-Scanner/1.0 (+https://edgeposture.ai)' },
      redirect: 'follow',
    });
    clearTimeout(timeout);

    const ttfb = Date.now() - fetchStart;
    const headers = Object.fromEntries(resp.headers.entries());
    const body = await resp.text();

    pageData = {
      url,
      finalUrl: resp.url,
      status: resp.status,
      ttfb,
      headers,
      bodyLength: body.length,
      body: body.slice(0, 8000), // cap for AI context
    };
  } catch (err) {
    throw new Error(err.name === 'AbortError' ? 'Request timed out — the URL may be invalid or the server is not responding.' : `Failed to fetch URL: ${err.message}`);
  }

  // Run AI analysis
  const analysis = await analyzeWithAI(pageData, env);

  const result = {
    id: crypto.randomUUID(),
    url,
    finalUrl: pageData.finalUrl,
    scannedAt: new Date().toISOString(),
    ttfb: pageData.ttfb,
    scores: analysis.scores,
    findings: analysis.findings,
    recommendations: analysis.recommendations,
    summary: analysis.summary,
    overallScore: analysis.overallScore,
  };

  // Save to D1
  ctx.waitUntil(saveScan(result, env));

  // Cache for 1 hour
  ctx.waitUntil(env.CACHE.put(cacheKey, JSON.stringify(result), { expirationTtl: 3600 }));

  return result;
}

async function analyzeWithAI(pageData, env) {
  const securityHeaders = checkSecurityHeaders(pageData.headers);
  const performanceSignals = checkPerformance(pageData);
  const complianceSignals = checkCompliance(pageData.body, pageData.headers);
  const cdnSignals = checkCDN(pageData.headers);

  const prompt = `You are EdgePosture, an expert web security and performance analyzer. Analyze this website data and return a JSON report.

URL: ${pageData.url}
HTTP Status: ${pageData.status}
TTFB: ${pageData.ttfb}ms
Response size: ${pageData.bodyLength} bytes

SECURITY HEADERS FOUND:
${JSON.stringify(securityHeaders, null, 2)}

PERFORMANCE SIGNALS:
${JSON.stringify(performanceSignals, null, 2)}

COMPLIANCE SIGNALS:
${JSON.stringify(complianceSignals, null, 2)}

CDN/EDGE SIGNALS:
${JSON.stringify(cdnSignals, null, 2)}

PAGE CONTENT SAMPLE:
${pageData.body.slice(0, 3000)}

Return ONLY valid JSON with this exact structure:
{
  "overallScore": <0-100 integer>,
  "scores": {
    "security": <0-100>,
    "performance": <0-100>,
    "compliance": <0-100>,
    "cdn": <0-100>
  },
  "summary": "<2-3 sentence plain English summary of the site's overall posture>",
  "findings": [
    {
      "category": "<security|performance|compliance|cdn>",
      "severity": "<critical|high|medium|low|info>",
      "title": "<short finding title>",
      "detail": "<1-2 sentence explanation of the issue>"
    }
  ],
  "recommendations": [
    {
      "priority": "<1-5 integer, 1=most urgent>",
      "category": "<security|performance|compliance|cdn>",
      "title": "<actionable recommendation title>",
      "detail": "<specific steps to fix this>",
      "edgeFix": "<relevant edge platform feature or configuration that would fix this, or null>"
    }
  ]
}

Be specific, actionable, and accurate. Include 3-8 findings and 3-6 recommendations.

IMPORTANT RULES:
- Never mention "Cloudflare" by name in findings or recommendations. Use "CDN", "edge platform", or "your CDN provider" instead.
- Never mention specific vendor product names. Keep findings vendor-neutral.
- Scores must be integers between 0 and 100. Do not return 0 unless the site is completely broken.
- Base scores on actual evidence from the headers and page data provided.`;

  const aiResponse = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 2000,
  });

  let parsed;
  try {
    const text = aiResponse.response || '';
    const jsonMatch = text.match(/\{[\s\S]*\}/);
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

  return parsed;
}

function checkSecurityHeaders(headers) {
  const checks = {
    'strict-transport-security': headers['strict-transport-security'] || null,
    'content-security-policy': headers['content-security-policy'] || headers['content-security-policy-report-only'] || null,
    'x-frame-options': headers['x-frame-options'] || null,
    'x-content-type-options': headers['x-content-type-options'] || null,
    'referrer-policy': headers['referrer-policy'] || null,
    'permissions-policy': headers['permissions-policy'] || headers['feature-policy'] || null,
    'x-xss-protection': headers['x-xss-protection'] || null,
    'cross-origin-opener-policy': headers['cross-origin-opener-policy'] || null,
    'cross-origin-embedder-policy': headers['cross-origin-embedder-policy'] || null,
    'cross-origin-resource-policy': headers['cross-origin-resource-policy'] || null,
  };
  return checks;
}

function checkPerformance(pageData) {
  return {
    ttfb: pageData.ttfb,
    ttfbRating: pageData.ttfb < 200 ? 'good' : pageData.ttfb < 500 ? 'needs-improvement' : 'poor',
    responseSize: pageData.bodyLength,
    responseSizeRating: pageData.bodyLength < 100000 ? 'good' : pageData.bodyLength < 500000 ? 'needs-improvement' : 'large',
    hasCompression: !!(pageData.headers['content-encoding']),
    compressionType: pageData.headers['content-encoding'] || null,
    cacheControl: pageData.headers['cache-control'] || null,
    etag: !!pageData.headers['etag'],
    lastModified: !!pageData.headers['last-modified'],
    http2: pageData.headers[':status'] !== undefined,
    transferEncoding: pageData.headers['transfer-encoding'] || null,
  };
}

function checkCompliance(body, headers) {
  const lower = body.toLowerCase();
  return {
    hasCookieBanner: lower.includes('cookie') && (lower.includes('consent') || lower.includes('accept') || lower.includes('gdpr') || lower.includes('ccpa')),
    hasPrivacyPolicy: lower.includes('privacy policy') || lower.includes('privacy-policy'),
    hasTermsOfService: lower.includes('terms of service') || lower.includes('terms-of-service') || lower.includes('terms and conditions'),
    trackingScripts: {
      googleAnalytics: lower.includes('google-analytics') || lower.includes('gtag') || lower.includes('ga.js'),
      googleTagManager: lower.includes('googletagmanager'),
      meta: lower.includes('connect.facebook.net') || lower.includes('fbevents'),
      hotjar: lower.includes('hotjar'),
      intercom: lower.includes('intercom'),
    },
    setCookieHeader: headers['set-cookie'] || null,
    cookieSecureFlags: headers['set-cookie'] ? {
      secure: headers['set-cookie'].toLowerCase().includes('secure'),
      httpOnly: headers['set-cookie'].toLowerCase().includes('httponly'),
      sameSite: headers['set-cookie'].toLowerCase().includes('samesite'),
    } : null,
  };
}

function checkCDN(headers) {
  return {
    isCloudflare: !!(headers['cf-ray'] || headers['cf-cache-status']),
    cfRay: headers['cf-ray'] || null,
    cfCacheStatus: headers['cf-cache-status'] || null,
    cfEdgeLocation: headers['cf-ray'] ? headers['cf-ray'].split('-').pop() : null,
    server: headers['server'] || null,
    cdnProvider: detectCDN(headers),
    ageHeader: headers['age'] || null,
    varyHeader: headers['vary'] || null,
    surrogateControl: headers['surrogate-control'] || null,
  };
}

function detectCDN(headers) {
  if (headers['cf-ray']) return 'Cloudflare';
  if (headers['x-amz-cf-id'] || headers['x-amz-cf-pop']) return 'AWS CloudFront';
  if (headers['x-fastly-request-id']) return 'Fastly';
  if (headers['x-akamai-transformed'] || headers['akamai-cache-status']) return 'Akamai';
  if (headers['x-azure-ref']) return 'Azure CDN';
  if (headers['x-varnish']) return 'Varnish';
  if (headers['x-cache'] && headers['x-cache'].includes('HIT')) return 'Unknown CDN (cache hit detected)';
  return 'None detected';
}

function calculateScoresFromFindings(findings, security, perf, compliance, cdn) {
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

function buildFallbackAnalysis(security, perf, compliance, cdn, pageData) {
  const missingHeaders = Object.entries(security).filter(([, v]) => !v).map(([k]) => k);
  const clamp = (n) => Math.min(100, Math.max(0, Math.round(n)));
  const secScore = clamp(100 - missingHeaders.length * 10);
  const perfScore = clamp(perf.ttfbRating === 'good' ? 85 : perf.ttfbRating === 'needs-improvement' ? 60 : 35);
  const compScore = clamp((compliance.hasCookieBanner ? 25 : 0) + (compliance.hasPrivacyPolicy ? 25 : 0) + (compliance.hasTermsOfService ? 25 : 0) + (compliance.cookieSecureFlags?.secure ? 25 : 0));
  const cdnScore = clamp(cdn.cdnProvider !== 'None detected' ? 75 : 30);
  const overall = clamp((secScore + perfScore + compScore + cdnScore) / 4);

  return {
    overallScore: overall,
    scores: { security: secScore, performance: perfScore, compliance: compScore, cdn: cdnScore },
    summary: `${pageData.url} scored ${overall}/100 overall. ${missingHeaders.length} security headers are missing. TTFB is ${perf.ttfb}ms (${perf.ttfbRating}). CDN: ${cdn.cdnProvider}.`,
    findings: missingHeaders.slice(0, 5).map(h => ({
      category: 'security',
      severity: ['content-security-policy', 'strict-transport-security'].includes(h) ? 'high' : 'medium',
      title: `Missing ${h} header`,
      detail: `The ${h} header is not present, which may expose users to attacks.`,
    })),
    recommendations: [{
      priority: 1,
      category: 'security',
      title: 'Add missing security headers',
      detail: `Add these headers: ${missingHeaders.join(', ')}`,
      edgeFix: 'Use your CDN or edge platform Transform Rules to inject response headers without touching your origin.',
    }],
  };
}

async function saveScan(result, env) {
  try {
    await env.DB.prepare(
      `INSERT INTO scans (id, url, final_url, scanned_at, overall_score, security_score, performance_score, compliance_score, cdn_score, summary, findings_json, recommendations_json, ttfb)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      result.id,
      result.url,
      result.finalUrl,
      result.scannedAt,
      result.overallScore,
      result.scores.security,
      result.scores.performance,
      result.scores.compliance,
      result.scores.cdn,
      result.summary,
      JSON.stringify(result.findings),
      JSON.stringify(result.recommendations),
      result.ttfb,
    ).run();
  } catch (err) {
    console.error('Failed to save scan:', err);
  }
}

function isValidUrl(str) {
  try {
    const u = new URL(str);
    return u.protocol === 'http:' || u.protocol === 'https:';
  } catch {
    return false;
  }
}
