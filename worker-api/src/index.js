import { handleScan } from './scanner.js';
import { handleAuth } from './auth.js';
import { handleHistory } from './history.js';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS });
    }

    const respond = (data, status = 200) =>
      new Response(JSON.stringify(data), {
        status,
        headers: { ...CORS, 'Content-Type': 'application/json' },
      });

    try {
      // Auth routes - pass env for Turnstile secret access
      if (url.pathname === '/auth/login' && request.method === 'POST') {
        return respond(await handleAuth(request, env, 'login'));
      }
      if (url.pathname === '/auth/register' && request.method === 'POST') {
        return respond(await handleAuth(request, env, 'register'));
      }
      if (url.pathname === '/auth/me' && request.method === 'GET') {
        return respond(await handleAuth(request, env, 'me'));
      }

      // Scanner route - public
      if (url.pathname === '/scan' && request.method === 'POST') {
        return respond(await handleScan(request, env, ctx));
      }

      // History routes - auth required
      if (url.pathname === '/history' && request.method === 'GET') {
        return respond(await handleHistory(request, env, 'list'));
      }
      if (url.pathname.startsWith('/history/') && request.method === 'GET') {
        const id = url.pathname.split('/')[2];
        return respond(await handleHistory(request, env, 'get', id));
      }

      // Public recent scans feed
      if (url.pathname === '/scans/recent' && request.method === 'GET') {
        return respond(await handleHistory(request, env, 'recent'));
      }

      return respond({ error: 'Not found' }, 404);
    } catch (err) {
      console.error(err);
      return respond({ error: err.message || 'Internal server error' }, 500);
    }
  },
};
