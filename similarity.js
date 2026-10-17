const fs = require('fs'), path = require('path');
const dir = path.join(process.cwd(), 'tools');
const pages = [];
for (const d of fs.readdirSync(dir, { withFileTypes: true })) {
  if (!d.isDirectory()) continue;
  const f = path.join(dir, d.name, 'index.html');
  if (!fs.existsSync(f)) continue;
  let h = fs.readFileSync(f, 'utf8');
  h = h.replace(/<(script|style|noscript|svg)[\s\S]*?<\/\1>/gi, ' ')
       .replace(/<(header|nav|footer)[\s\S]*?<\/\1>/gi, ' ')
       .replace(/<[^>]+>/g, ' ').replace(/&[a-z#0-9]+;/gi, ' ')
       .toLowerCase().replace(/[^a-z0-9\s]/g, ' ');
  const w = h.split(/\s+/).filter(Boolean);
  const sh = new Set();
  for (let i = 0; i + 5 <= w.length; i++) sh.add(w.slice(i, i + 5).join(' '));
  pages.push({ slug: d.name, words: w.length, sh });
}
const inter = (a, b) => { let n = 0; const [s, l] = a.size < b.size ? [a, b] : [b, a]; for (const x of s) if (l.has(x)) n++; return n; };
const worst = new Map(); const pairs = [];
for (let i = 0; i < pages.length; i++) for (let j = i + 1; j < pages.length; j++) {
  const A = pages[i], B = pages[j];
  const n = inter(A.sh, B.sh), u = A.sh.size + B.sh.size - n;
  const sim = u ? n / u : 0;
  if (sim > 0.5) pairs.push([sim, A.slug, B.slug]);
  for (const p of [A, B]) worst.set(p.slug, Math.max(worst.get(p.slug) || 0, sim));
}
const vals = [...worst.values()];
const c = t => vals.filter(v => v >= t).length;
console.log(`Pages: ${pages.length}`);
console.log(`Avg main-text words per page: ${Math.round(pages.reduce((s, p) => s + p.words, 0) / pages.length)}`);
console.log(`Pages with a near-twin >=90% similar: ${c(0.9)}`);
console.log(`Pages with a near-twin >=70% similar: ${c(0.7)}`);
console.log(`Pages with a near-twin >=50% similar: ${c(0.5)}\n`);
pairs.sort((a, b) => b[0] - a[0]).slice(0, 25).forEach(([s, a, b]) => console.log(`${(s * 100).toFixed(0)}%  ${a}  <->  ${b}`));
fs.writeFileSync('similar-pairs.txt', pairs.map(p => `${(p[0] * 100).toFixed(0)}% ${p[1]} <-> ${p[2]}`).join('\n'));
console.log('\nAll pairs over 50% saved to similar-pairs.txt');
