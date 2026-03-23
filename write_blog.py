import os

os.makedirs('C:/Users/miked/edgeposture/blog-worker/src', exist_ok=True)
os.makedirs('C:/Users/miked/edgeposture/blog-worker/migrations', exist_ok=True)
os.makedirs('C:/Users/miked/edgeposture/blog-frontend', exist_ok=True)

files = {}

files['C:/Users/miked/edgeposture/blog-worker/migrations/0001_init.sql'] = """
CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  excerpt TEXT,
  content TEXT NOT NULL,
  published INTEGER DEFAULT 0,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  tags TEXT DEFAULT '[]'
);
CREATE INDEX IF NOT EXISTS idx_posts_slug ON posts(slug);
CREATE INDEX IF NOT EXISTS idx_posts_published ON posts(published);
"""

files['C:/Users/miked/edgeposture/blog-worker/wrangler.toml'] = """name = "edgeposture-blog-api"
main = "src/index.js"
compatibility_date = "2024-11-01"
account_id = "7a6e19dfbfa3334906ed8dcd3fe4027e"

[[d1_databases]]
binding = "DB"
database_name = "edgeposture-blog"
database_id = "e22da152-9a07-4e3b-9a28-52faf7182dc6"

[vars]
ENVIRONMENT = "production"
"""

files['C:/Users/miked/edgeposture/blog-worker/package.json'] = """{
  "name": "edgeposture-blog-api",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy"
  }
}"""

files['C:/Users/miked/edgeposture/blog-worker/src/index.js'] = """
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

const respond = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });

function checkAdmin(request, env) {
  const auth = request.headers.get('Authorization') || '';
  const token = auth.replace('Bearer ', '');
  return token === env.ADMIN_TOKEN;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });

    try {
      // Public: list published posts
      if (path === '/posts' && request.method === 'GET') {
        const result = await env.DB.prepare(
          'SELECT id, slug, title, excerpt, tags, created_at FROM posts WHERE published = 1 ORDER BY created_at DESC'
        ).all();
        return respond({ posts: result.results });
      }

      // Public: get single post by slug
      if (path.startsWith('/posts/') && request.method === 'GET') {
        const slug = path.split('/')[2];
        const post = await env.DB.prepare(
          'SELECT * FROM posts WHERE slug = ? AND published = 1'
        ).bind(slug).first();
        if (!post) return respond({ error: 'Post not found' }, 404);
        return respond({ post });
      }

      // Admin: list all posts including drafts
      if (path === '/admin/posts' && request.method === 'GET') {
        if (!checkAdmin(request, env)) return respond({ error: 'Unauthorized' }, 401);
        const result = await env.DB.prepare(
          'SELECT id, slug, title, excerpt, published, tags, created_at, updated_at FROM posts ORDER BY created_at DESC'
        ).all();
        return respond({ posts: result.results });
      }

      // Admin: create post
      if (path === '/admin/posts' && request.method === 'POST') {
        if (!checkAdmin(request, env)) return respond({ error: 'Unauthorized' }, 401);
        const { title, content, excerpt, tags, published, slug } = await request.json();
        if (!title || !content) return respond({ error: 'Title and content required' }, 400);
        const id = crypto.randomUUID();
        const finalSlug = slug || title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
        const now = new Date().toISOString();
        await env.DB.prepare(
          'INSERT INTO posts (id, slug, title, excerpt, content, published, tags, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        ).bind(id, finalSlug, title, excerpt || '', content, published ? 1 : 0, JSON.stringify(tags || []), now, now).run();
        return respond({ id, slug: finalSlug });
      }

      // Admin: update post
      if (path.startsWith('/admin/posts/') && request.method === 'PUT') {
        if (!checkAdmin(request, env)) return respond({ error: 'Unauthorized' }, 401);
        const id = path.split('/')[3];
        const { title, content, excerpt, tags, published, slug } = await request.json();
        const now = new Date().toISOString();
        await env.DB.prepare(
          'UPDATE posts SET title=?, content=?, excerpt=?, tags=?, published=?, slug=?, updated_at=? WHERE id=?'
        ).bind(title, content, excerpt || '', JSON.stringify(tags || []), published ? 1 : 0, slug, now, id).run();
        return respond({ success: true });
      }

      // Admin: delete post
      if (path.startsWith('/admin/posts/') && request.method === 'DELETE') {
        if (!checkAdmin(request, env)) return respond({ error: 'Unauthorized' }, 401);
        const id = path.split('/')[3];
        await env.DB.prepare('DELETE FROM posts WHERE id = ?').bind(id).run();
        return respond({ success: true });
      }

      return respond({ error: 'Not found' }, 404);
    } catch (err) {
      console.error(err);
      return respond({ error: err.message }, 500);
    }
  }
};
"""

# Blog frontend - single HTML file with full blog + admin
files['C:/Users/miked/edgeposture/blog-frontend/index.html'] = """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>EdgePosture Blog</title>
<meta name="description" content="Technical insights on CDN, application security, and performance from an industry SME."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap" rel="stylesheet"/>
<style>
:root{--bg:#0a0c10;--bg2:#111318;--bg3:#181b22;--border:rgba(255,255,255,0.08);--border2:rgba(255,255,255,0.14);--text:#e8eaf0;--text2:#8b8fa8;--text3:#555870;--accent:#4f7bff;--accent2:#7c9fff;--good:#22c55e;--warn:#f59e0b;--poor:#ef4444}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;font-size:16px;line-height:1.65}
body::before{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(79,123,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(79,123,255,0.03) 1px,transparent 1px);background-size:60px 60px;pointer-events:none;z-index:0}
nav{position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:2rem;padding:0 2rem;height:60px;background:rgba(10,12,16,0.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}
.nav-brand{display:flex;align-items:center;gap:10px;cursor:pointer;text-decoration:none}
.nav-logo{width:32px;height:32px;background:var(--accent);border-radius:8px;display:flex;align-items:center;justify-content:center;font-family:'Space Mono',monospace;font-size:12px;font-weight:700;color:#fff}
.nav-name{font-weight:600;font-size:15px;color:var(--text)}
.nav-links{display:flex;gap:0.25rem;margin-left:auto}
.nav-link{background:none;border:none;color:var(--text2);font-size:14px;padding:6px 12px;border-radius:6px;cursor:pointer;text-decoration:none;font-family:'DM Sans',sans-serif;transition:color 0.15s,background 0.15s}
.nav-link:hover{color:var(--text);background:rgba(255,255,255,0.06)}
.nav-btn{background:var(--accent);color:#fff;border:none;padding:7px 16px;border-radius:7px;font-size:13px;font-weight:500;cursor:pointer;font-family:'DM Sans',sans-serif;transition:opacity 0.15s}
.nav-btn:hover{opacity:0.85}
main{position:relative;z-index:1;max-width:860px;margin:0 auto;padding:4rem 2rem 6rem}
.page-header{margin-bottom:3rem;padding-bottom:2rem;border-bottom:1px solid var(--border)}
.page-eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:0.1em;color:var(--accent2);font-family:'Space Mono',monospace;display:block;margin-bottom:0.75rem}
.page-title{font-family:'Space Mono',monospace;font-size:clamp(1.8rem,4vw,2.5rem);font-weight:700;letter-spacing:-1px;line-height:1.15;margin-bottom:0.75rem}
.page-sub{color:var(--text2);font-size:16px;max-width:520px}
.posts-grid{display:flex;flex-direction:column;gap:16px}
.post-card{background:var(--bg3);border:1px solid var(--border);border-radius:12px;padding:1.5rem;cursor:pointer;transition:border-color 0.15s,transform 0.15s;text-decoration:none;display:block}
.post-card:hover{border-color:var(--border2);transform:translateY(-2px)}
.post-card-meta{display:flex;align-items:center;gap:8px;margin-bottom:0.75rem;flex-wrap:wrap}
.post-date{font-size:12px;color:var(--text3);font-family:'Space Mono',monospace}
.post-tag{font-size:10px;padding:2px 8px;border-radius:4px;background:rgba(79,123,255,0.1);color:var(--accent2);font-family:'Space Mono',monospace;text-transform:uppercase;letter-spacing:0.04em}
.post-title{font-family:'Space Mono',monospace;font-size:18px;font-weight:700;margin-bottom:0.5rem;color:var(--text);line-height:1.3}
.post-excerpt{font-size:14px;color:var(--text2);line-height:1.6}
.post-arrow{float:right;color:var(--accent2);font-size:18px;margin-top:-2px}
.empty-state{text-align:center;padding:4rem;color:var(--text2)}
.empty-state p{margin-bottom:1rem}
/* Single post */
.post-back{display:inline-flex;align-items:center;gap:6px;color:var(--text2);font-size:14px;cursor:pointer;background:none;border:none;font-family:'DM Sans',sans-serif;margin-bottom:2rem;padding:0;transition:color 0.15s}
.post-back:hover{color:var(--text)}
.post-full-title{font-family:'Space Mono',monospace;font-size:clamp(1.8rem,4vw,2.8rem);font-weight:700;letter-spacing:-1px;line-height:1.15;margin-bottom:1rem}
.post-full-meta{display:flex;align-items:center;gap:8px;margin-bottom:2rem;padding-bottom:2rem;border-bottom:1px solid var(--border);flex-wrap:wrap}
.post-content{font-size:16px;line-height:1.85;color:var(--text2)}
.post-content h1,.post-content h2,.post-content h3{font-family:'Space Mono',monospace;color:var(--text);margin:2rem 0 1rem;line-height:1.3}
.post-content h2{font-size:1.4rem}
.post-content h3{font-size:1.15rem}
.post-content p{margin-bottom:1.25rem}
.post-content code{background:var(--bg3);border:1px solid var(--border);padding:2px 6px;border-radius:4px;font-family:'Space Mono',monospace;font-size:13px;color:var(--accent2)}
.post-content pre{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:1.25rem;overflow-x:auto;margin-bottom:1.25rem}
.post-content pre code{background:none;border:none;padding:0;font-size:13px;color:var(--text)}
.post-content ul,.post-content ol{margin-bottom:1.25rem;padding-left:1.5rem}
.post-content li{margin-bottom:0.4rem}
.post-content blockquote{border-left:3px solid var(--accent);padding-left:1rem;margin-bottom:1.25rem;color:var(--text2);font-style:italic}
.post-content a{color:var(--accent2);text-decoration:underline}
.post-content strong{color:var(--text);font-weight:600}
/* Admin */
.admin-panel{background:var(--bg2);border:1px solid var(--border2);border-radius:16px;padding:2rem;margin-bottom:2rem}
.admin-login{max-width:400px;margin:4rem auto}
.admin-login h2{font-family:'Space Mono',monospace;font-size:20px;margin-bottom:1.5rem}
.field{margin-bottom:1rem}
.field label{display:block;font-size:13px;color:var(--text2);margin-bottom:6px}
.field input,.field textarea,.field select{width:100%;background:var(--bg2);border:1px solid var(--border2);color:var(--text);padding:10px 14px;border-radius:8px;font-size:15px;font-family:'DM Sans',sans-serif;outline:none;transition:border-color 0.15s}
.field input:focus,.field textarea:focus{border-color:var(--accent)}
.field textarea{min-height:300px;resize:vertical;font-size:14px;line-height:1.6}
.btn{background:var(--accent);color:#fff;border:none;padding:10px 20px;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;font-family:'DM Sans',sans-serif;transition:opacity 0.15s;display:inline-flex;align-items:center;gap:6px}
.btn:hover{opacity:0.85}
.btn-danger{background:var(--poor)}
.btn-outline{background:none;border:1px solid var(--border2);color:var(--text2)}
.btn-outline:hover{border-color:var(--border2);color:var(--text);opacity:1}
.btn-sm{padding:6px 12px;font-size:12px}
.admin-post-row{display:flex;align-items:center;gap:1rem;padding:12px 0;border-bottom:1px solid var(--border)}
.admin-post-row:last-child{border-bottom:none}
.admin-post-title{flex:1;font-size:14px;font-weight:500}
.admin-post-status{font-size:11px;padding:2px 8px;border-radius:4px;font-family:'Space Mono',monospace}
.status-published{background:rgba(34,197,94,0.1);color:var(--good)}
.status-draft{background:rgba(255,255,255,0.06);color:var(--text3)}
.admin-actions{display:flex;gap:6px}
.error-msg{color:var(--poor);font-size:13px;margin-top:0.5rem;padding:8px 12px;background:rgba(239,68,68,0.1);border-radius:6px}
.success-msg{color:var(--good);font-size:13px;margin-top:0.5rem;padding:8px 12px;background:rgba(34,197,94,0.1);border-radius:6px}
.section-title{font-family:'Space Mono',monospace;font-size:16px;font-weight:700;margin-bottom:1.25rem;display:flex;align-items:center;justify-content:space-between}
.spinner-inline{display:inline-block;width:16px;height:16px;border:2px solid rgba(255,255,255,0.3);border-top-color:#fff;border-radius:50%;animation:spin 0.7s linear infinite;vertical-align:middle}
@keyframes spin{to{transform:rotate(360deg)}}
.tag-input-wrap{display:flex;gap:8px;flex-wrap:wrap;margin-top:6px}
.tag-pill{display:inline-flex;align-items:center;gap:4px;background:rgba(79,123,255,0.1);color:var(--accent2);padding:3px 10px;border-radius:20px;font-size:12px}
.tag-pill button{background:none;border:none;color:var(--accent2);cursor:pointer;font-size:14px;padding:0;line-height:1}
</style>
</head>
<body>
<nav>
  <a class="nav-brand" href="https://edgeposture.ai">
    <div class="nav-logo">EP</div>
    <span class="nav-name">EdgePosture</span>
  </a>
  <div class="nav-links">
    <a class="nav-link" href="https://edgeposture.ai">Home</a>
    <a class="nav-link" href="https://edgepostureapp.com">Scanner</a>
    <a class="nav-link" href="https://getedgeposture.com">Consulting</a>
    <button class="nav-link" onclick="showPage('blog')">Blog</button>
  </div>
  <button class="nav-btn" onclick="showPage('admin-login')" id="admin-btn">Admin</button>
</nav>

<main id="app"></main>

<script>
const API = 'https://blog-api.edgeposture.ai';
let adminToken = sessionStorage.getItem('blog_admin_token') || null;
let currentPage = 'blog';
let posts = [];
let editingPost = null;
let tags = [];

async function loadPosts(admin = false) {
  const url = admin ? `${API}/admin/posts` : `${API}/posts`;
  const headers = admin ? { Authorization: `Bearer ${adminToken}` } : {};
  const r = await fetch(url, { headers });
  const d = await r.json();
  return d.posts || [];
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

function renderMarkdown(md) {
  return md
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/```([\\s\\S]*?)```/g, '<pre><code>$1</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$1</strong>')
    .replace(/\\*([^*]+)\\*/g, '<em>$1</em>')
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\\/li>)/gs, '<ul>$1</ul>')
    .replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, '<a href="$2" target="_blank">$1</a>')
    .replace(/\\n\\n/g, '</p><p>')
    .replace(/^(?!<[hupbalo])/gm, '')
    .replace(/(<p><\\/p>)/g, '')
    .split('\\n\\n').map(p => p.startsWith('<') ? p : `<p>${p}</p>`).join('');
}

async function showPage(page, data) {
  currentPage = page;
  const app = document.getElementById('app');
  document.getElementById('admin-btn').style.display = (adminToken && page !== 'admin') ? 'block' : (adminToken ? 'none' : 'block');

  if (page === 'blog') {
    app.innerHTML = `<div class="page-header"><span class="page-eyebrow">Technical insights</span><h1 class="page-title">EdgePosture Blog</h1><p class="page-sub">CDN architecture, application security, performance engineering, and edge-native development.</p></div><div id="posts-container"><div class="empty-state"><div class="spinner-inline"></div></div></div>`;
    try {
      posts = await loadPosts();
      const container = document.getElementById('posts-container');
      if (!posts.length) {
        container.innerHTML = '<div class="empty-state"><p>No posts published yet. Check back soon.</p></div>';
      } else {
        container.innerHTML = '<div class="posts-grid">' + posts.map(p => {
          const t = JSON.parse(p.tags || '[]');
          return `<div class="post-card" onclick="showPage('post','${p.slug}')">
            <div class="post-card-meta">
              <span class="post-date">${formatDate(p.created_at)}</span>
              ${t.map(tag => `<span class="post-tag">${tag}</span>`).join('')}
            </div>
            <div class="post-title">${p.title} <span class="post-arrow">→</span></div>
            ${p.excerpt ? `<div class="post-excerpt">${p.excerpt}</div>` : ''}
          </div>`;
        }).join('') + '</div>';
      }
    } catch(e) { document.getElementById('posts-container').innerHTML = '<div class="empty-state"><p>Failed to load posts.</p></div>'; }
  }

  else if (page === 'post') {
    app.innerHTML = '<div><button class="post-back" onclick="showPage(\'blog\')">← Back to blog</button><div class="empty-state"><div class="spinner-inline"></div></div></div>';
    try {
      const r = await fetch(`${API}/posts/${data}`);
      const d = await r.json();
      const post = d.post;
      const t = JSON.parse(post.tags || '[]');
      app.innerHTML = `<div>
        <button class="post-back" onclick="showPage('blog')">← Back to blog</button>
        <h1 class="post-full-title">${post.title}</h1>
        <div class="post-full-meta">
          <span class="post-date">${formatDate(post.created_at)}</span>
          ${t.map(tag => `<span class="post-tag">${tag}</span>`).join('')}
        </div>
        <div class="post-content">${renderMarkdown(post.content)}</div>
      </div>`;
    } catch(e) { app.innerHTML = '<div class="empty-state"><p>Post not found.</p></div>'; }
  }

  else if (page === 'admin-login') {
    if (adminToken) { showPage('admin'); return; }
    app.innerHTML = `<div class="admin-login">
      <h2>Admin access</h2>
      <div class="field"><label>Admin token</label><input type="password" id="token-input" placeholder="Enter your admin token"/></div>
      <div id="login-error"></div>
      <button class="btn" onclick="adminLogin()" style="margin-top:1rem;width:100%">Sign in</button>
    </div>`;
    document.getElementById('token-input').addEventListener('keydown', e => { if(e.key==='Enter') adminLogin(); });
  }

  else if (page === 'admin') {
    if (!adminToken) { showPage('admin-login'); return; }
    document.getElementById('admin-btn').style.display = 'none';
    app.innerHTML = `<div>
      <div class="section-title">All posts <button class="btn btn-sm" onclick="showPage('edit',null)">+ New post</button></div>
      <div class="admin-panel" id="posts-list"><div class="spinner-inline"></div></div>
      <button class="btn btn-outline btn-sm" onclick="adminLogout()" style="margin-top:1rem">Sign out</button>
    </div>`;
    try {
      const allPosts = await loadPosts(true);
      const list = document.getElementById('posts-list');
      if (!allPosts.length) { list.innerHTML = '<p style="color:var(--text2);font-size:14px">No posts yet.</p>'; return; }
      list.innerHTML = allPosts.map(p => `
        <div class="admin-post-row">
          <div class="admin-post-title">${p.title}</div>
          <span class="admin-post-status ${p.published ? 'status-published' : 'status-draft'}">${p.published ? 'published' : 'draft'}</span>
          <div class="admin-actions">
            <button class="btn btn-sm btn-outline" onclick="showPage('edit','${p.id}')">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="deletePost('${p.id}')">Del</button>
          </div>
        </div>`).join('');
    } catch(e) {}
  }

  else if (page === 'edit') {
    if (!adminToken) { showPage('admin-login'); return; }
    let post = null;
    tags = [];
    if (data) {
      try {
        const allPosts = await loadPosts(true);
        post = allPosts.find(p => p.id === data);
        if (post) tags = JSON.parse(post.tags || '[]');
      } catch(e) {}
    }
    app.innerHTML = `<div>
      <button class="post-back" onclick="showPage('admin')">← Back to posts</button>
      <div class="section-title">${post ? 'Edit post' : 'New post'}</div>
      <div class="admin-panel">
        <div class="field"><label>Title</label><input type="text" id="post-title" value="${post ? post.title.replace(/"/g,'&quot;') : ''}" placeholder="Post title"/></div>
        <div class="field"><label>Slug (URL)</label><input type="text" id="post-slug" value="${post ? post.slug : ''}" placeholder="auto-generated-from-title"/></div>
        <div class="field"><label>Excerpt</label><input type="text" id="post-excerpt" value="${post ? (post.excerpt||'').replace(/"/g,'&quot;') : ''}" placeholder="Short description for the listing"/></div>
        <div class="field"><label>Tags (press Enter to add)</label>
          <input type="text" id="tag-input" placeholder="e.g. security, cdn, performance" onkeydown="addTag(event)"/>
          <div class="tag-input-wrap" id="tag-list">${tags.map(t => `<span class="tag-pill">${t}<button onclick="removeTag('${t}')">×</button></span>`).join('')}</div>
        </div>
        <div class="field"><label>Content (Markdown supported)</label><textarea id="post-content" placeholder="Write your post in Markdown...">${post ? post.content : ''}</textarea></div>
        <div class="field" style="display:flex;align-items:center;gap:10px">
          <input type="checkbox" id="post-published" ${post && post.published ? 'checked' : ''} style="width:auto"/>
          <label for="post-published" style="margin:0;cursor:pointer">Published (visible to public)</label>
        </div>
        <div id="save-msg"></div>
        <div style="display:flex;gap:8px;margin-top:1rem">
          <button class="btn" onclick="savePost('${post ? post.id : ''}')">${post ? 'Update post' : 'Create post'}</button>
          <button class="btn btn-outline" onclick="showPage('admin')">Cancel</button>
        </div>
      </div>
    </div>`;
    document.getElementById('post-title').addEventListener('input', function() {
      const slugEl = document.getElementById('post-slug');
      if (!slugEl.dataset.manual) slugEl.value = this.value.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
    });
    document.getElementById('post-slug').addEventListener('input', function() { this.dataset.manual = '1'; });
  }
}

function addTag(e) {
  if (e.key !== 'Enter') return;
  e.preventDefault();
  const val = e.target.value.trim();
  if (val && !tags.includes(val)) {
    tags.push(val);
    document.getElementById('tag-list').innerHTML = tags.map(t => `<span class="tag-pill">${t}<button onclick="removeTag('${t}')">×</button></span>`).join('');
  }
  e.target.value = '';
}

function removeTag(tag) {
  tags = tags.filter(t => t !== tag);
  document.getElementById('tag-list').innerHTML = tags.map(t => `<span class="tag-pill">${t}<button onclick="removeTag('${t}')">×</button></span>`).join('');
}

async function adminLogin() {
  const token = document.getElementById('token-input').value.trim();
  const r = await fetch(`${API}/admin/posts`, { headers: { Authorization: `Bearer ${token}` } });
  if (r.ok) {
    adminToken = token;
    sessionStorage.setItem('blog_admin_token', token);
    showPage('admin');
  } else {
    document.getElementById('login-error').innerHTML = '<div class="error-msg">Invalid token</div>';
  }
}

function adminLogout() {
  adminToken = null;
  sessionStorage.removeItem('blog_admin_token');
  document.getElementById('admin-btn').style.display = 'block';
  showPage('blog');
}

async function savePost(id) {
  const title = document.getElementById('post-title').value.trim();
  const slug = document.getElementById('post-slug').value.trim();
  const excerpt = document.getElementById('post-excerpt').value.trim();
  const content = document.getElementById('post-content').value;
  const published = document.getElementById('post-published').checked;
  const msgEl = document.getElementById('save-msg');

  if (!title || !content) { msgEl.innerHTML = '<div class="error-msg">Title and content are required</div>'; return; }

  const body = JSON.stringify({ title, slug, excerpt, content, published, tags });
  const url = id ? `${API}/admin/posts/${id}` : `${API}/admin/posts`;
  const method = id ? 'PUT' : 'POST';

  try {
    const r = await fetch(url, { method, headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${adminToken}` }, body });
    const d = await r.json();
    if (r.ok) {
      msgEl.innerHTML = '<div class="success-msg">Saved successfully</div>';
      setTimeout(() => showPage('admin'), 1000);
    } else {
      msgEl.innerHTML = `<div class="error-msg">${d.error}</div>`;
    }
  } catch(e) { msgEl.innerHTML = '<div class="error-msg">Failed to save</div>'; }
}

async function deletePost(id) {
  if (!confirm('Delete this post?')) return;
  await fetch(`${API}/admin/posts/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${adminToken}` } });
  showPage('admin');
}

showPage('blog');
</script>
</body>
</html>"""

files['C:/Users/miked/edgeposture/blog-frontend/wrangler.toml'] = """name = "edgeposture-blog"
compatibility_date = "2024-11-01"
pages_build_output_dir = "."
"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {path}')

print('All blog files written successfully')