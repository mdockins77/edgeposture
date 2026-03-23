import { requireAuth } from './auth.js';

export async function handleHistory(request, env, action, id) {
  if (action === 'recent') {
    const result = await env.DB.prepare(
      'SELECT id, url, overall_score, security_score, performance_score, compliance_score, cdn_score, summary, scanned_at, ttfb FROM scans ORDER BY scanned_at DESC LIMIT 20'
    ).all();
    return { scans: result.results };
  }
  const user = await requireAuth(request, env);
  if (action === 'list') {
    const result = await env.DB.prepare(
      'SELECT id, url, overall_score, security_score, performance_score, compliance_score, cdn_score, summary, scanned_at, ttfb FROM scans WHERE user_id = ? ORDER BY scanned_at DESC LIMIT 50'
    ).bind(user.id).all();
    return { scans: result.results };
  }
  if (action === 'get') {
    const scan = await env.DB.prepare(
      'SELECT * FROM scans WHERE id = ? AND (user_id = ? OR user_id IS NULL)'
    ).bind(id, user.id).first();
    if (!scan) throw new Error('Scan not found');
    return { ...scan, findings: JSON.parse(scan.findings_json || '[]'), recommendations: JSON.parse(scan.recommendations_json || '[]') };
  }
}
