const fs = require('fs'), path = require('path');
const dir = path.join(process.cwd(), 'tools');
const pages = [], df = new Map();
for (const d of fs.readdirSync(dir, { withFileTypes: true })) {
  if (!d.isDirectory()) continue;
  const f = path.join(dir, d.name, 'index.html');
  if (!fs.existsSync(f)) continue;
  let h = fs.readFileSync(f, 'utf8')
    .replace(/<(script|style|noscript|svg)[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<(header|nav|footer)[\s\S]*?<\/\1>/gi, ' ');
  const blocks = h.split(/<\/?(?:p|li|h[1-6]|div|section|article|summary|details|td|th|button|a|span|label)[^>]*>/gi)
    .map(b => b.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().toLowerCase())
    .filter(b => b.split(' ').length >= 8);
  const set = new Set(blocks);
  for (const b of set) df.set(b, (df.get(b) || 0) + 1);
  pages.push({ slug: d.name, blocks: [...set] });
}
// share of each page's words that sit in blocks found on 10+ pages
let tot = 0, rows = [];
for (const p of pages) {
  let all = 0, shared = 0;
  for (const b of p.blocks) { const n = b.split(' ').length; all += n; if (df.get(b) >= 10) shared += n; }
  rows.push({ slug: p.slug, all, shared, pct: all ? shared / all : 0 });
  tot += all ? shared / all : 0;
}
console.log(`Average share of main text found on 10+ other pages: ${(tot / rows.length * 100).toFixed(0)}%`);
console.log(`Pages where >50% is shared boilerplate: ${rows.filter(r => r.pct > 0.5).length}`);
console.log(`Avg UNIQUE words per page: ${Math.round(rows.reduce((s, r) => s + (r.all - r.shared), 0) / rows.length)}\n`);
console.log('Most repeated blocks (pages | text):');
[...df.entries()].sort((a, b) => b[1] - a[1]).slice(0, 15)
  .forEach(([b, n]) => console.log(`${n} | ${b.slice(0, 110)}`));
