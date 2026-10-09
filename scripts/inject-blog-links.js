#!/usr/bin/env node
/**
 * Writes real <a> links to the blog posts into blog/index.html and index.html,
 * so crawlers see them without running JavaScript. The page's own JS still
 * replaces the list with live data, so nothing changes for visitors.
 * Also adds footer links to the programmatic tool pages on the homepage.
 * Safe to run repeatedly. Run from repo root.
 */
const fs = require('fs');
const path = require('path');

const BLOG = 'blog';
const START = '<!--POSTS-START-->';
const END = '<!--POSTS-END-->';
const HOME_COUNT = 3;

const EXTRA_TOOLS = [
  ['compress-pdf-to-100kb', 'Compress PDF to 100KB'],
  ['compress-pdf-to-200kb', 'Compress PDF to 200KB'],
  ['compress-pdf-to-500kb', 'Compress PDF to 500KB'],
  ['compress-pdf-to-1mb', 'Compress PDF to 1MB'],
  ['merge-pdf-without-watermark', 'Merge PDF Without Watermark'],
  ['heic-to-jpg-windows', 'HEIC to JPG on Windows'],
  ['mp4-to-mp3-320kbps', 'MP4 to MP3 320kbps']
];

const strip = h => h.replace(/<[^>]*>/g, ' ');
const fmtDate = ms => ms ? new Date(ms).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' }) : '';

function readPost(slug) {
  const file = path.join(BLOG, slug, 'index.html');
  if (!fs.existsSync(file)) return null;
  const html = fs.readFileSync(file, 'utf8');
  const article = (html.match(/<article id="post">([\s\S]*?)<\/article>/) || [])[1] || '';
  const title = (article.match(/<h1>([\s\S]*?)<\/h1>/) || [])[1];
  if (!title) return null;
  const prose = (article.match(/<div class="prose">([\s\S]*?)<div class="cta">/) || [])[1] || '';
  const tagsHtml = (article.match(/<div class="tags">([\s\S]*?)<\/div>/) || [])[1] || '';
  const ts = Date.parse((html.match(/"datePublished":"([^"]+)"/) || [])[1] || '') || 0;
  return {
    slug,
    title, // already HTML-escaped by generate-blog.js
    desc: (html.match(/<meta name="description" content="([^"]*)">/) || [])[1] || '',
    img: localImg((article.match(/<img class="cover" src="([^"]*)"/) || [])[1] || ''),
    tags: (tagsHtml.match(/<span>[\s\S]*?<\/span>/g) || []).slice(0, 3).join(''),
    ts,
    date: fmtDate(ts),
    mins: Math.max(1, Math.round(strip(prose).split(/\s+/).filter(Boolean).length / 200))
  };
}

const blogCard = p => `<a class="card" href="/blog/${p.slug}/"><span class="accent"></span>${p.img ? `<div class="cover"><img src="${p.img}" alt="${p.title}" loading="lazy" decoding="async"></div>` : '<div class="cover ph"></div>'}<div class="cb"><div class="tags">${p.tags}</div><h2>${p.title}</h2><p>${p.desc}</p><div class="meta"><span>${p.date}</span><i></i><span>${p.mins} min read</span><b>Read →</b></div></div></a>`;

const homeCard = p => `<a class="blog-card" href="blog/${p.slug}/">${p.img ? `<img src="${p.img}" alt="${p.title}" loading="lazy" decoding="async">` : '<div class="ph"></div>'}<div class="bc"><h3>${p.title}</h3><p>${p.desc}</p></div></a>`;

function setBlock(html, bootstrapRe, content, label) {
  const marked = new RegExp(`${START}[\\s\\S]*?${END}`);
  const block = `${START}${content}${END}`;
  if (marked.test(html)) return html.replace(marked, () => block);
  if (bootstrapRe.test(html)) return html.replace(bootstrapRe, (_, open, close) => `${open}${block}${close}`);
  console.warn(`inject-blog-links: could not find the ${label}, skipped`);
  return html;
}

function addFooterLinks(html) {
  const missing = EXTRA_TOOLS.filter(([s]) => !html.includes(`href="tools/${s}/"`));
  if (!missing.length) return html;
  const links = missing.map(([s, l]) => `<a href="tools/${s}/">${l}</a>`).join('');
  if (!/<div class="foot-links"/.test(html)) { console.warn('inject-blog-links: .foot-links not found, footer links skipped'); return html; }
  return html.replace(/(<div class="foot-links"[^>]*>[\s\S]*?)(<\/div>)/, (_, a, b) => a + links + b);
}

function run() {
  const manifest = JSON.parse(fs.readFileSync(path.join(BLOG, 'generated-posts.json'), 'utf8'));
  const posts = manifest.map(readPost).filter(Boolean).sort((a, b) => b.ts - a.ts);
  if (!posts.length) return console.warn('inject-blog-links: no posts found, nothing changed');

  const blogFile = path.join(BLOG, 'index.html');
  let h = fs.readFileSync(blogFile, 'utf8');
  h = setBlock(h, /(<section id="grid"[^>]*>\s*)(?:<div class="sk"><\/div>\s*)+(<\/section>)/, posts.map(blogCard).join('\n'), 'blog grid');
  h = h.replace(/<span id="count">[^<]*<\/span>/, `<span id="count">${posts.length} ${posts.length === 1 ? 'ARTICLE' : 'ARTICLES'}</span>`);
  fs.writeFileSync(blogFile, h);

  let home = fs.readFileSync('index.html', 'utf8');
  home = setBlock(home, /(<div class="blog-grid" id="blogGrid">)(?:<div class="blog-card sk"><\/div>)+(<\/div>)/, posts.slice(0, HOME_COUNT).map(homeCard).join(''), 'homepage blog grid');
  home = addFooterLinks(home);
  fs.writeFileSync('index.html', home);

  console.log(`inject-blog-links: ${posts.length} post(s) linked, homepage updated.`);
}

module.exports = { run };
if (require.main === module) run();

// Prefer the local optimized .webp banner over the heavy remote PNG/JFIF
function localImg(u) {
  if (!u) return u;
  const m = u.match(/\/blog\/BannerImage\/([^\/?#]+)\.(png|jpe?g|jfif)$/i);
  if (!m) return u;
  const rel = 'blog/BannerImage/' + m[1] + '.webp';
  const fs = require('fs'), path = require('path');
  return fs.existsSync(path.join(__dirname, '..', rel)) ? '/' + rel : u;
}
