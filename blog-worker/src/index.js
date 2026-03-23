
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
