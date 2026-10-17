const fs = require('fs'), path = require('path');
const dir = path.join(process.cwd(), 'tools');
const items = [];
for (const d of fs.readdirSync(dir, { withFileTypes: true })) {
  if (!d.isDirectory()) continue;
  const f = path.join(dir, d.name, 'index.html');
  if (!fs.existsSync(f)) continue;
  const html = fs.readFileSync(f, 'utf8');
  const t = (html.match(/<title>([^<]+)<\/title>/i) || [])[1] || d.name;
  items.push({ slug: d.name, title: t.split(/[|–-]\s*ConvertKit/i)[0].trim() });
}
items.sort((a, b) => a.title.localeCompare(b.title));
const esc = s => s.replace(/&(?!amp;)/g, '&amp;').replace(/</g, '&lt;');
const page = `<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>All Free Online Tools | ConvertKit Lite</title>
<meta name="description" content="Browse every free ConvertKit Lite tool: PDF, image, audio, video, spreadsheet and calculator tools. No signup, runs in your browser.">
<link rel="canonical" href="https://www.convertkitlite.site/tools/">
<style>body{font-family:system-ui,sans-serif;max-width:960px;margin:0 auto;padding:24px}
ul{columns:2;gap:32px;padding-left:18px}li{margin:6px 0}a{color:#2563eb}
@media(max-width:600px){ul{columns:1}}</style>
</head><body>
<p><a href="/">&larr; Home</a></p>
<h1>All Free Online Tools</h1>
<p>${items.length} tools. Everything is free and runs in your browser.</p>
<ul>
${items.map(i => `<li><a href="/tools/${i.slug}/">${esc(i.title)}</a></li>`).join('\n')}
</ul>
</body></html>`;
fs.writeFileSync(path.join(dir, 'index.html'), page);
console.log(`Wrote tools/index.html with ${items.length} tools`);
