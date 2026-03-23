part1 = open('C:/Users/miked/edgeposture/blog-frontend/index.html', encoding='utf-8').read()

# Replace the broken renderMarkdown function with a safe version
old_func = """function renderMarkdown(md) {
  if (!md) return '';
  var s = md;
  s = s.replace(/^### (.+)$/gm,'<h3>$1</h3>');
  s = s.replace(/^## (.+)$/gm,'<h2>$1</h2>');
  s = s.replace(/^# (.+)$/gm,'<h1>$1</h1>');
  s = s.replace(/\\*\\*([^*]+)\\*\\*/g,'<strong>$1</strong>');
  s = s.replace(/\\*([^*]+)\\*/g,'<em>$1</em>');
  s = s.replace(/^> (.+)$/gm,'<blockquote>$1</blockquote>');
  s = s.replace(/^- (.+)$/gm,'<li>$1</li>');
  s = s.replace(/`([^`\\n]+)`/g,'<code>$1</code>');
  var parts = s.split('\\n\\n');
  var out = parts.map(function(p) {
    if (p.match(/^<(h[123]|ul|ol|li|blockquote|pre)/)) return p;
    return '<p>' + p.replace(/\\n/g,' ') + '</p>';
  });
  return out.join('\\n');
}"""

new_func = """function renderMarkdown(md) {
  if (!md) return '';
  var s = md;
  var h3 = new RegExp('^### (.+)$','gm');
  var h2 = new RegExp('^## (.+)$','gm');
  var h1 = new RegExp('^# (.+)$','gm');
  var bold = new RegExp('[*][*]([^*]+)[*][*]','g');
  var italic = new RegExp('[*]([^*]+)[*]','g');
  var bq = new RegExp('^> (.+)$','gm');
  var li = new RegExp('^- (.+)$','gm');
  var code = new RegExp('`([^`]+)`','g');
  var nl = new RegExp('\\n','g');
  s = s.replace(h3,'<h3>$1</h3>');
  s = s.replace(h2,'<h2>$1</h2>');
  s = s.replace(h1,'<h1>$1</h1>');
  s = s.replace(bold,'<strong>$1</strong>');
  s = s.replace(italic,'<em>$1</em>');
  s = s.replace(bq,'<blockquote>$1</blockquote>');
  s = s.replace(li,'<li>$1</li>');
  s = s.replace(code,'<code>$1</code>');
  var parts = s.split('\\n\\n');
  var out = parts.map(function(p) {
    if (p.indexOf('<h')==0||p.indexOf('<ul')==0||p.indexOf('<li')==0||p.indexOf('<block')==0) return p;
    return '<p>' + p.replace(nl,' ') + '</p>';
  });
  return out.join('\\n');
}"""

result = part1.replace(old_func, new_func)
if old_func in part1:
    print('Found and replaced renderMarkdown')
else:
    print('WARNING: function not found, writing safe fallback')
    result = part1.replace(
        'function renderMarkdown(md) {',
        'function renderMarkdown_BROKEN(md) {'
    )
    result = result.replace(
        'renderMarkdown(post.content)',
        'renderMarkdown_safe(post.content)'
    )
    result = result.replace(
        '</script>',
        '''function renderMarkdown(md) {
  if (!md) return '<p>' + md + '</p>';
  var s = md;
  var parts = s.split('\\n\\n');
  return parts.map(function(p){ return '<p>'+p+'</p>'; }).join('');
}
</script>'''
    )

with open('C:/Users/miked/edgeposture/blog-frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(result)
print('Done')