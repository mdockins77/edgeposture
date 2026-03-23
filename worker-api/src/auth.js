export async function handleAuth(request, env, action) {
  if (action === 'login') {
    const { email, password } = await request.json();
    if (!email || !password) throw new Error('Email and password required');
    const user = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(email.toLowerCase()).first();
    if (!user) throw new Error('Invalid credentials');
    const valid = await verifyPassword(password, user.password_hash);
    if (!valid) throw new Error('Invalid credentials');
    const token = await createToken({ id: user.id, email: user.email }, env.JWT_SECRET);
    return { token, user: { id: user.id, email: user.email, name: user.name } };
  }
  if (action === 'register') {
    const { email, password, name } = await request.json();
    if (!email || !password || !name) throw new Error('Name, email, and password required');
    if (password.length < 8) throw new Error('Password must be at least 8 characters');
    const existing = await env.DB.prepare('SELECT id FROM users WHERE email = ?').bind(email.toLowerCase()).first();
    if (existing) throw new Error('Email already registered');
    const id = crypto.randomUUID();
    const hash = await hashPassword(password);
    await env.DB.prepare('INSERT INTO users (id, email, name, password_hash, created_at) VALUES (?, ?, ?, ?, ?)').bind(id, email.toLowerCase(), name, hash, new Date().toISOString()).run();
    const token = await createToken({ id, email: email.toLowerCase() }, env.JWT_SECRET);
    return { token, user: { id, email: email.toLowerCase(), name } };
  }
  if (action === 'me') {
    const user = await requireAuth(request, env);
    return { user };
  }
}

export async function requireAuth(request, env) {
  const auth = request.headers.get('Authorization');
  if (!auth || !auth.startsWith('Bearer ')) throw new Error('Authentication required');
  const token = auth.slice(7);
  const payload = await verifyToken(token, env.JWT_SECRET);
  if (!payload) throw new Error('Invalid or expired token');
  const user = await env.DB.prepare('SELECT id, email, name FROM users WHERE id = ?').bind(payload.id).first();
  if (!user) throw new Error('User not found');
  return user;
}

async function hashPassword(password) {
  const encoder = new TextEncoder();
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const keyMaterial = await crypto.subtle.importKey('raw', encoder.encode(password), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' }, keyMaterial, 256);
  const hashArray = new Uint8Array(bits);
  return btoa(String.fromCharCode(...salt)) + ':' + btoa(String.fromCharCode(...hashArray));
}

async function verifyPassword(password, stored) {
  const [saltB64, hashB64] = stored.split(':');
  const salt = Uint8Array.from(atob(saltB64), c => c.charCodeAt(0));
  const encoder = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey('raw', encoder.encode(password), 'PBKDF2', false, ['deriveBits']);
  const bits = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' }, keyMaterial, 256);
  const newHash = btoa(String.fromCharCode(...new Uint8Array(bits)));
  return newHash === hashB64;
}

async function createToken(payload, secret) {
  const encoder = new TextEncoder();
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const body = btoa(JSON.stringify({ ...payload, exp: Math.floor(Date.now() / 1000) + 86400 * 30 }));
  const data = `${header}.${body}`;
  const key = await crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(data));
  return `${data}.${btoa(String.fromCharCode(...new Uint8Array(sig)))}`;
}

async function verifyToken(token, secret) {
  try {
    const [header, body, sig] = token.split('.');
    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey('raw', encoder.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['verify']);
    const valid = await crypto.subtle.verify('HMAC', key, Uint8Array.from(atob(sig), c => c.charCodeAt(0)), encoder.encode(`${header}.${body}`));
    if (!valid) return null;
    const payload = JSON.parse(atob(body));
    if (payload.exp < Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch { return null; }
}
