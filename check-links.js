const fs = require('fs'), path = require('path');
const root = process.cwd();
const skip = new Set(['node_modules', '.git']);

function walk(d, out = []) {
  for (const f of fs.readdirSync(d, { withFileTypes: true })) {
    if (skip.has(f.name)) continue;
    const p = path.join(d, f.name);
    f.isDirectory() ? walk(p, out) : out.push(p);
  }
  return out;
}
function exists(p) {
  if (!fs.existsSync(p)) return false;
  return fs.statSync(p).isFile() || fs.existsSync(path.join(p, 'index.html'));
}

const htmls = walk(root).filter(f => f.endsWith('.html'));
const re = /(?:href|src)="([^"]+)"/g;
let total = 0;
const broken = [];

for (const f of htmls) {
  const html = fs.readFileSync(f, 'utf8');
  let m;
  while ((m = re.exec(html))) {
    let u = m[1].trim();
    if (/^(mailto:|tel:|javascript:|data:|#)/.test(u)) continue;
    if (/[${}']|\+/.test(u)) continue; // skip JS template fragments
    u = u.replace(/^https?:\/\/(www\.)?convertkitlite\.site/, '');
    if (/^(https?:)?\/\//.test(u)) continue; // external
    u = u.split('#')[0].split('?')[0];
    if (!u) continue;
    try { u = decodeURIComponent(u); } catch {}
    total++;
    const target = u.startsWith('/') ? path.join(root, u) : path.resolve(path.dirname(f), u);
    if (!exists(target)) broken.push({ page: path.relative(root, f), link: m[1] });
  }
}

const byLink = {};
broken.forEach(b => (byLink[b.link] = (byLink[b.link] || 0) + 1));
console.log(`Checked ${total} internal links/assets in ${htmls.length} pages`);
console.log(`Broken: ${broken.length} (${Object.keys(byLink).length} unique targets)\n`);
Object.entries(byLink).sort((a, b) => b[1] - a[1]).forEach(([l, c]) => console.log(`${c}x  ${l}`));
fs.writeFileSync('broken-links.txt', broken.map(b => `${b.page}  ->  ${b.link}`).join('\n'));
console.log('\nFull list (page -> broken link) saved to broken-links.txt');
