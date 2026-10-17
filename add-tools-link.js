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

// 1) Footer link on every page that has a </footer>
let pages = 0, noFooter = [];
for (const f of walk(root).filter(f => f.endsWith('.html'))) {
  const rel = path.relative(root, f);
  if (/^(admin|404|yandex_)/.test(rel)) continue;
  const html = fs.readFileSync(f, 'utf8');
  if (html.includes('href="/tools/"')) continue;
  if (!html.includes('</footer>')) { noFooter.push(rel); continue; }
  const out = html.replace('</footer>', '<p><a href="/tools/">All Tools</a></p>\n</footer>');
  pages++;
  if (APPLY) fs.writeFileSync(f, out);
}
console.log(`${APPLY ? 'Added' : 'Would add'} /tools/ footer link to ${pages} pages`);
console.log(`Pages with no </footer> (skipped): ${noFooter.length}`);
noFooter.slice(0, 10).forEach(p => console.log('  ' + p));

// 2) Sitemap
const sm = path.join(root, 'sitemap.xml');
if (fs.existsSync(sm)) {
  const x = fs.readFileSync(sm, 'utf8');
  if (x.includes('<loc>https://www.convertkitlite.site/tools/</loc>')) console.log('sitemap: /tools/ already listed');
  else if (x.includes('</urlset>')) {
    console.log(`${APPLY ? 'Added' : 'Would add'} /tools/ to sitemap.xml`);
    if (APPLY) fs.writeFileSync(sm, x.replace('</urlset>', '  <url><loc>https://www.convertkitlite.site/tools/</loc></url>\n</urlset>'));
  } else console.log('sitemap.xml has no </urlset> (maybe a sitemap index). Add /tools/ manually.');
} else console.log('No sitemap.xml in project root');
if (!APPLY) console.log('\nRun again with --apply to write changes.');
