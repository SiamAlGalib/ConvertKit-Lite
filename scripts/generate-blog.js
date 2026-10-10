#!/usr/bin/env node
/**
 * Generates static blog pages from Firestore:
 *   blog/<slug>/index.html   (one folder per published post)
 *
 * - Uses blog/post.html as the template, so the design always matches.
 * - Reads collection "convertkitBlogPosts" (status === "published").
 * - Removes folders of posts that were unpublished/deleted (tracked in blog/generated-posts.json).
 * - Updates sitemap.xml between <!-- BLOG-START --> and <!-- BLOG-END --> (if present).
 *
 * Needs env var FIREBASE_SERVICE_ACCOUNT (service account JSON).
 */
const fs = require('fs');
const path = require('path');

const SITE = 'https://www.convertkitlite.site';
const COLLECTION = 'convertkitBlogPosts';
const BLOG_DIR = 'blog';
const TEMPLATE = path.join(BLOG_DIR, 'post.html');
const MANIFEST = path.join(BLOG_DIR, 'generated-posts.json');
const SITEMAP = 'sitemap.xml';
const SLUG_OK = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

// GitHub Pages URLs are case-sensitive: /tools/AgeCalculator/ 404s, /tools/agecalculator/ works.
const fixToolLinks = h => String(h).replace(/(href=["'](?:https?:\/\/www\.convertkitlite\.site)?\/tools\/)([A-Za-z0-9-]+)(\/?["'])/g, (m, a, slug, z) => a + slug.toLowerCase() + z);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[c]));
const toMs = v => (v && typeof v.toMillis === 'function') ? v.toMillis() : (Number(v) || Date.parse(v) || 0);
const minutes = h => Math.max(1, Math.round((h || '').replace(/<[^>]*>/g, ' ').split(/\s+/).filter(Boolean).length / 200));
const fmtDate = ms => ms ? new Date(ms).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' }) : '';

function articleHtml(p) {
  const ms = toMs(p.publishedAt || p.updatedAt);
  const tags = (p.tags || []).map(x => `<span>${esc(x)}</span>`).join('');
  return `
      <a class="back" href="/blog/">← All articles</a>
      <div class="tags">${tags}</div>
      <h1>${esc(p.title)}</h1>
      <div class="meta"><span>${fmtDate(ms)}</span><i></i><span>${minutes(p.content)} min read</span></div>
      ${p.coverImageUrl ? `<img class="cover" src="${esc(localImg(p.coverImageUrl))}" alt="${esc(p.title)}">` : ''}
      <div class="prose">${fixToolLinks(p.content || '')}</div>
      <div class="cta"><div><h3>Need to convert a file?</h3><p>Try our free PDF, image, audio and video tools. No sign-up needed.</p></div><a class="primary" href="/#tools">Browse all tools</a></div>`;
}

function buildPage(template, p, slug) {
  const url = `${SITE}/blog/${slug}/`;
  const desc = p.metaDescription || p.excerpt || '';
  let title = p.metaTitle || p.title || slug;
  if (!/convertkit lite/i.test(title)) title += ' — ConvertKit Lite';

  const published = toMs(p.publishedAt || p.createdAt || p.updatedAt);
  const modified = toMs(p.updatedAt || p.publishedAt);
  const ld = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: p.title || slug,
    description: desc,
    mainEntityOfPage: url,
    author: { '@type': 'Person', name: p.author || 'SAG' },
    publisher: { '@type': 'Organization', name: 'ConvertKit Lite', logo: { '@type': 'ImageObject', url: SITE + '/logo.png' } }
  };
  if (p.coverImageUrl) ld.image = p.coverImageUrl;
  if (published) ld.datePublished = new Date(published).toISOString();
  if (modified) ld.dateModified = new Date(modified).toISOString();

  let html = template;
  const swap = (re, fn, label) => {
    if (!re.test(html)) throw new Error(`Template marker not found in ${TEMPLATE}: ${label}`);
    html = html.replace(re, fn);
  };

  swap(/<title>[\s\S]*?<\/title>/, () => `<title>${esc(title)}</title>`, '<title>');
  swap(/<meta name="description" content="[^"]*">/, () => `<meta name="description" content="${esc(desc)}">`, 'meta description');
  swap(/<article id="post">[\s\S]*?<\/article>/, () => `<article id="post">${articleHtml(p)}</article>`, '<article id="post">');
  // Remove the client-side Firebase loader (page is static now)
  swap(/<script type="module">(?:(?!<\/script>)[\s\S])*?import\("\.\/firebase\.js"\)[\s\S]*?<\/script>\s*/, () => '', 'firebase module script');
  html = html.replace(/<link rel="modulepreload"[^>]*firebase[^>]*>\s*/g, ''); // static posts don't need the Firestore preload

  if (p.coverImageUrl) {
    html = html.replace(/<meta property="og:image" content="[^"]*">/, () => `<meta property="og:image" content="${esc(p.coverImageUrl)}">`);
  }

  const head = [
    `<link rel="canonical" href="${url}">`,
    `<meta property="og:title" content="${esc(title)}">`,
    `<meta property="og:description" content="${esc(desc)}">`,
    `<meta property="og:url" content="${url}">`,
    `<meta name="twitter:card" content="summary_large_image">`,
    `<meta name="twitter:title" content="${esc(title)}">`,
    `<meta name="twitter:description" content="${esc(desc)}">`,
    `<meta name="twitter:image" content="${esc(p.coverImageUrl || SITE + '/logo.png')}">`,
    `<script type="application/ld+json">${JSON.stringify(ld).replace(/</g, '\\u003c')}</script>`
  ].join('\n');
  swap(/<\/head>/, () => `${head}\n</head>`, '</head>');
  return html;
}

function updateSitemap(entries) {
  if (!fs.existsSync(SITEMAP)) return console.log('sitemap.xml not found, skipping sitemap');
  const START = '<!-- BLOG-START -->', END = '<!-- BLOG-END -->';
  let xml = fs.readFileSync(SITEMAP, 'utf8');
  if (!xml.includes(START) || !xml.includes(END)) return console.log('Sitemap markers not found, skipping sitemap (see setup notes)');
  const lines = entries.map(e => `  <url><loc>${SITE}/blog/${e.slug}/</loc>${e.lastmod ? `<lastmod>${e.lastmod}</lastmod>` : ''}</url>`).join('\n');
  xml = xml.replace(new RegExp(`${START}[\\s\\S]*?${END}`), () => `${START}\n${lines}\n  ${END}`);
  fs.writeFileSync(SITEMAP, xml);
}

async function main() {
  const raw = process.env.FIREBASE_SERVICE_ACCOUNT;
  if (!raw) throw new Error('FIREBASE_SERVICE_ACCOUNT secret is missing');
  const admin = require('firebase-admin');
  admin.initializeApp({ credential: admin.credential.cert(JSON.parse(raw)) });

  const snap = await admin.firestore().collection(COLLECTION).get();
  const posts = snap.docs.map(d => ({ id: d.id, ...d.data() })).filter(p => p.status === 'published');
  const template = fs.readFileSync(TEMPLATE, 'utf8');

  const done = [];
  for (const p of posts) {
    const slug = String(p.slug || p.id).trim();
    if (!SLUG_OK.test(slug)) { console.warn(`Skipping "${slug}": slug must be lowercase letters, numbers and hyphens`); continue; }
    const dir = path.join(BLOG_DIR, slug);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'index.html'), buildPage(template, p, slug));
    const m = toMs(p.updatedAt || p.publishedAt);
    done.push({ slug, lastmod: m ? new Date(m).toISOString().slice(0, 10) : '' });
    console.log(`✓ blog/${slug}/index.html`);
  }

  // Remove folders for posts that are no longer published (only ones we generated before)
  let previous = [];
  try { previous = JSON.parse(fs.readFileSync(MANIFEST, 'utf8')); } catch (_) {}
  const keep = new Set(done.map(d => d.slug));
  for (const slug of previous) {
    if (!keep.has(slug) && SLUG_OK.test(slug)) {
      fs.rmSync(path.join(BLOG_DIR, slug), { recursive: true, force: true });
      console.log(`✗ removed blog/${slug}/ (no longer published)`);
    }
  }
  fs.writeFileSync(MANIFEST, JSON.stringify([...keep].sort(), null, 2) + '\n');
  updateSitemap(done);
  // NEW: write real links to the posts into blog/index.html and index.html
  try { require('./inject-blog-links').run(); } catch (e) { console.warn('inject-blog-links failed:', e.message); }
  console.log(`Done: ${done.length} post(s).`);
}

module.exports = { buildPage };
if (require.main === module) main().catch(e => { console.error(e); process.exit(1); });


// Prefer the local optimized .webp banner over the heavy remote PNG/JFIF
function localImg(u) {
  if (!u) return u;
  const m = u.match(/\/blog\/BannerImage\/([^\/?#]+)\.(png|jpe?g|jfif)$/i);
  if (!m) return u;
  const rel = 'blog/BannerImage/' + m[1] + '.webp';
  const fs = require('fs'), path = require('path');
  return fs.existsSync(path.join(__dirname, '..', rel)) ? '/' + rel : u;
}
