const fs = require('fs'), path = require('path');
const root = process.cwd();
const APPLY = process.argv.includes('--apply');
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

let fixes = 0, files = 0;
const sample = [];
for (const f of walk(root).filter(f => f.endsWith('.html'))) {
  const html = fs.readFileSync(f, 'utf8');
  let changed = false;
  const out = html.replace(/\b(href|src)="([^"]+)"/g, (full, attr, val) => {
    const u = val.trim();
    if (/^(mailto:|tel:|javascript:|data:|#|\/|https?:|\/\/)/.test(u)) return full;
    if (/[${}']|\+/.test(u)) return full;
    const clean = u.split('#')[0].split('?')[0];
    if (!clean) return full;
    const rel = path.resolve(path.dirname(f), clean);
    if (exists(rel)) return full;                    // already works
    if (!exists(path.join(root, clean))) return full; // can't fix safely
    changed = true; fixes++;
    if (sample.length < 15) sample.push(`${path.relative(root, f)}: ${u} -> /${u}`);
    return `${attr}="/${u}"`;
  });
  if (changed) { files++; if (APPLY) fs.writeFileSync(f, out); }
}
console.log(`${APPLY ? 'Fixed' : 'Would fix'} ${fixes} links in ${files} files`);
sample.forEach(s => console.log('  ' + s));
if (!APPLY) console.log('\nRun again with --apply to write changes.');
