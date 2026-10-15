import re, json, sys, pathlib
SITE = 'https://www.convertkitlite.site'
MAIN = pathlib.Path('tools/removebg/index.html')
SITEMAP = pathlib.Path('sitemap.xml')
base = MAIN.read_text(encoding='utf-8')
if 'seo-upgrade' in base:
    sys.exit('Already applied. Nothing changed.')

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def rep(s, old, new):
    if old not in s: sys.exit('Not found in page: ' + old[:60])
    return s.replace(old, new, 1)
def sub1(pat, new, s):
    out, n = re.subn(pat, lambda m: new, s, count=1, flags=re.S)
    if n != 1: sys.exit('Pattern not found: ' + pat[:60])
    return out

LINKS = [
 ('removebg', 'Remove background from image (main tool)'),
 ('make-background-transparent', 'Make image background transparent'),
 ('remove-white-background', 'Remove white background from image'),
 ('change-image-background-color', 'Change image background color'),
 ('product-photo-background-remover', 'Product photo background remover'),
 ('remove-background-from-portrait', 'Remove background from portrait'),
 ('background-remover-no-signup', 'Free background remover, no signup'),
 ('background-remover-for-android', 'Background remover for Android'),
 ('background-remover-for-iphone', 'Background remover for iPhone and iPad'),
]

MAIN_P = dict(
 slug='removebg', name='Remove Background from Image',
 title='Remove Background from Image – Free AI Background Remover',
 desc='Remove background from image online free. Upload JPG, PNG or WebP and get a transparent PNG with AI. No signup, no watermark, runs in your browser.',
 h1='Remove <span>Background</span> from Image',
 intro='Remove the background from an image automatically with AI. Free, no signup, and your image stays on your device.',
 h2='Remove the background from an image, free and private',
 body='<p>This free background remover cuts the background out of a photo with AI, right in your browser. There is no signup and no watermark, and your image is never uploaded. Pick the guide below that matches your use, device or background.</p>',
 faqs=[
  ('How do I remove the background from an image for free?', 'Choose a JPG, PNG or WebP image and wait for the AI to remove the background. Then pick transparent, white or a color and press Download PNG. There is no account to create.'),
  ('Can I make an image background transparent?', 'Yes. Transparent is the default. The download is a PNG, because PNG is the format that keeps transparency.'),
  ('Does it work on Android and iPhone?', 'It runs in a modern phone browser, with nothing to install. The first use downloads an AI model of about 45 MB, and older phones can take longer.'),
 ])

VARIANTS = [
 dict(slug='make-background-transparent', name='Make Background Transparent',
  title='Make Image Background Transparent – Free PNG Maker',
  desc='Make an image background transparent online for free. Upload JPG, PNG or WebP and download a transparent PNG. No signup, no watermark.',
  h1='Make Background <span>Transparent</span>',
  intro='Make the background of any photo transparent with AI and save it as a PNG. Free, no signup, and your image stays on your device.',
  h2='How to make an image background transparent',
  body='<p>Choose your image and the AI finds the subject and removes everything behind it. The Transparent option is selected by default, so you can download a transparent PNG straight away.</p><p>Only PNG can hold a transparent background, which is why the download is always a PNG and not a JPG. The grey squares in the preview only show which parts are transparent, and they are not saved in the file.</p><p>Transparent PNG files work in most slide, document and design apps, so you can place the cut-out on any color or picture.</p>',
  faqs=[('Why is my transparent image a PNG and not a JPG?', 'JPG cannot store transparency. PNG can, so the download is always a PNG.'),
        ('Can I use the transparent PNG in PowerPoint or Word?', 'Yes. Most slide, document and design apps accept transparent PNG files, so you can place the cut-out on any background.')]),
 dict(slug='remove-white-background', name='Remove White Background',
  title='Remove White Background from Image – Free Online',
  desc='Remove a white background from an image online for free and get a transparent PNG. Private, no signup, no watermark.',
  h1='Remove <span>White Background</span>',
  intro='Remove a white background from a photo or product picture and get a transparent PNG. Free, no signup, and your image stays on your device.',
  h2='Remove a white background from an image',
  body='<p>Product photos, scans and screenshots often come on plain white. Upload the image and the AI cuts out the subject, leaving a transparent background.</p><p>The AI looks for the subject instead of erasing every white pixel, so white parts of the subject, such as a white shirt or label, are usually kept. A white object on a white background is still hard for any tool, so check the edges in the preview.</p><p>If the AI cannot load on your connection, the tool offers a simple mode that removes one similar color from the edges, with a sensitivity slider. That mode suits plain white backgrounds.</p>',
  faqs=[('Will it also remove white inside my object?', 'The AI looks for the subject, so white areas that belong to it are usually kept. A white object on a plain white background can still be difficult, so check the edges.'),
        ('Can I put a new color behind the cut-out?', 'Yes. After the white is removed, choose transparent, white, black or any color before you download.')]),
 dict(slug='change-image-background-color', name='Change Image Background Color',
  title='Change Image Background Color – Free Online Tool',
  desc='Change the background color of a photo online for free. Remove the old background, pick white, black or any color, and download.',
  h1='Change Image <span>Background Color</span>',
  intro='Remove the old background with AI, then put white, black or any color you pick behind your subject. Free and private.',
  h2='How to change the background color of a photo',
  body='<p>First the AI removes the original background. Then you choose the new one: transparent, white, black, or any color from the color picker. The preview updates straight away, so you can try a few colors before you download.</p><p>The file you download has the new color filled in behind the subject and is saved as a PNG. For a smaller file, convert it with <a href="../pngtojpg/">PNG to JPG</a>.</p>',
  faqs=[('Can I change the background to white?', 'Yes. Choose the white swatch after the background is removed, then press Download PNG.'),
        ('Can I choose any color?', 'Yes. Use the color picker next to the swatches to choose any color, and the preview changes at once.')]),
 dict(slug='product-photo-background-remover', name='Product Photo Background Remover',
  title='Product Photo Background Remover – White or Transparent',
  desc='Remove the background from product photos for free. Get a clean white or transparent PNG. Private, no signup, no watermark.',
  h1='Product Photo <span>Background Remover</span>',
  intro='Cut the background out of a product photo and get a clean white or transparent PNG. Free, no signup, and your photos stay on your device.',
  h2='Clean product photos for listings and catalogs',
  body='<p>A plain white or transparent background keeps the focus on the product. Upload a photo, let the AI remove the background, then choose the White swatch for a pure white background or keep it transparent.</p><ul><li>Shoot in even light, with the product clearly different in color from what is behind it.</li><li>Try Best quality for fine edges such as strings, mesh or fur.</li><li>Check the edges in the preview before you download.</li><li>Photos larger than about 2500 pixels on the longest side are scaled down to that size.</li></ul><p>Each marketplace has its own image rules, so check the requirements of the store you sell on. The tool works on one image at a time, so it suits a handful of photos better than a whole catalog.</p>',
  faqs=[('Is the white background pure white?', 'Yes. The White option fills the background with pure white (#FFFFFF).'),
        ('Can I remove the background from many product photos at once?', 'Not at the moment. The tool works on one image at a time, so press Use another image after each download.')]),
 dict(slug='remove-background-from-portrait', name='Remove Background from Portrait',
  title='Remove Background from Portrait – Free AI Tool',
  desc='Remove the background from a portrait, headshot or profile picture for free. Keep the person and choose a new background. Private, no signup.',
  h1='Remove Background from <span>Portrait</span>',
  intro='Cut the background out of a portrait, headshot or profile picture with AI. Free, no signup, and your photo stays on your device.',
  h2='Remove the background from a portrait or profile picture',
  body='<p>Upload a photo of a person and the AI separates them from the background. Then keep it transparent, or choose white, black or any color for a clean profile picture.</p><ul><li>Use a sharp, well-lit photo where the person stands out from the background.</li><li>Choose Best quality to keep more detail in hair.</li><li>Very fine hair, or a background close to the hair color, can leave rough edges. Crop closer to the person or try another photo.</li></ul><p>Your photo is processed in your browser and is never uploaded, which is useful for personal pictures.</p>',
  faqs=[('Does it keep hair detail?', 'Best quality keeps the most fine detail, including hair. Very fine hair on a busy or similar-colored background can still leave rough edges.'),
        ('Can I use the result as a profile picture?', 'Yes. Pick a color behind the person, download the PNG and use it wherever you need a profile picture.')]),
 dict(slug='background-remover-no-signup', name='Free Background Remover, No Signup',
  title='Free Background Remover – No Signup, No Watermark',
  desc='Free background remover with no signup and no watermark. Remove the background from any JPG, PNG or WebP in your browser.',
  h1='Free Background Remover, <span>No Signup</span>',
  intro='Remove the background from an image with AI. No account, no watermark, and your image stays on your device.',
  h2='A background remover with no signup and no watermark',
  body='<p>There is no account to create, and the tool does not add a watermark to your image. You do not need to install anything either: it runs in your browser.</p><p>Here is what to expect:</p><ul><li>The first use downloads an AI model of about 45 MB, which your browser keeps for next time.</li><li>Each image takes roughly 10 to 30 seconds, depending on your device.</li><li>It works on one image at a time.</li><li>The result is a PNG, with a transparent or solid-color background.</li></ul>',
  faqs=[('Is there a limit on how many images I can process?', 'The tool sets no usage limit. It handles one image at a time, so press Use another image to start the next.'),
        ('Do I need to create an account?', 'No. There is no sign-up or login.')]),
 dict(slug='background-remover-for-android', name='Background Remover for Android',
  title='Background Remover for Android – Free, No App',
  desc='Remove image backgrounds on your Android phone for free. Works in Chrome, no app to install, and your photos are not uploaded.',
  h1='Background Remover for <span>Android</span>',
  intro='Remove the background from a photo on your Android phone or tablet. Use Chrome, with no app to install and no upload.',
  h2='Remove a background on Android',
  body='<p>Open this page in Chrome, tap the upload area and choose a photo from your gallery or Files. Wait for the before and after preview, pick transparent, white or a color, then tap Download PNG.</p><ul><li>The first use downloads an AI model of about 45 MB, so use Wi-Fi if your mobile data is limited.</li><li>Phones are slower than computers. If it takes too long, choose Fast in the Speed / quality menu.</li><li>The PNG is saved to your usual Downloads folder.</li></ul>',
  faqs=[('Do I need an app?', 'No. The tool works in your phone browser, such as Chrome.'),
        ('Why is it slow on my phone?', 'The AI runs on your own device, so older phones take longer. Choose Fast in the Speed / quality menu to finish sooner.')]),
 dict(slug='background-remover-for-iphone', name='Background Remover for iPhone and iPad',
  title='Background Remover for iPhone & iPad – Free, No App',
  desc='Remove image backgrounds on iPhone or iPad for free. Use Safari, no app to install, and your photos are not uploaded.',
  h1='Background Remover for <span>iPhone</span>',
  intro='Remove the background from a photo on your iPhone or iPad. Use your browser, with no app to install and no upload.',
  h2='Remove a background on iPhone and iPad',
  body='<p>Open this page in Safari, tap the upload area and choose a photo from your Photos library or the Files app. Wait for the preview, pick transparent, white or a color, then tap Download PNG.</p><ul><li>The first use downloads an AI model of about 45 MB, so use Wi-Fi if your data is limited.</li><li>If the page struggles on an older device, choose Fast in the Speed / quality menu.</li><li>The PNG is saved to the Files app, usually in Downloads.</li></ul><p>Your photo is processed on your device and is not sent to a server.</p>',
  faqs=[('Do I need an app on iPhone?', 'No. Open the page in Safari or another modern browser.'),
        ('Where is the PNG saved on my iPhone?', 'Downloaded files appear in the Files app, usually in the Downloads folder.')]),
]

def section(p):
    lis = ''.join('<li><a href="../%s/">%s</a></li>' % (s, esc(l)) for s, l in LINKS if s != p['slug'])
    return ('<section class="narrow prose"><!--seo-upgrade--><h2>%s</h2>%s<h2>More background remover options</h2><ul>%s</ul></section>\n\n'
            % (esc(p['h2']), p['body'], lis))

def build(html, p):
    url = '%s/tools/%s/' % (SITE, p['slug'])
    t, d = esc(p['title']), esc(p['desc'])
    html = sub1(r'<title>.*?</title>', '<title>%s</title>' % t, html)
    html = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % d, html)
    html = sub1(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, html)
    html = sub1(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, html)
    html = sub1(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % t, html)
    html = sub1(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % d, html)
    html = sub1(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="%s">' % t, html)
    html = sub1(r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="%s">' % d, html)
    html = rep(html, '<h1>Remove <span>Background</span></h1>', '<h1>%s</h1>' % p['h1'])
    html = rep(html, '<p class="sub">Erase the background from a photo automatically with AI. Your image stays on your device.</p>', '<p class="sub">%s</p>' % esc(p['intro']))
    blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S))
    if len(blocks) != 2: sys.exit('Expected 2 JSON-LD blocks, found %d' % len(blocks))
    for m in reversed(blocks):
        data = json.loads(m.group(2))
        if '@graph' in data:
            for node in data['@graph']:
                if node['@type'] == 'WebApplication':
                    node['name'], node['description'], node['url'] = p['name'], p['desc'], url
                elif node['@type'] == 'BreadcrumbList' and p['slug'] != 'removebg':
                    node['itemListElement'][1]['name'] = p['name']
                    node['itemListElement'][1]['item'] = url
        elif data.get('@type') == 'FAQPage':
            for q, a in p['faqs']:
                data['mainEntity'].append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
        html = html[:m.start(2)] + json.dumps(data, ensure_ascii=False) + html[m.end(2):]
    extra = ''.join('<details><summary>%s</summary><p>%s</p></details>\n  ' % (esc(q), esc(a)) for q, a in p['faqs'])
    html, n = re.subn(r'(</details>)(\s*</section>\s*<section class="related")', lambda m: m.group(1) + '\n  ' + extra.rstrip() + m.group(2), html, count=1)
    if n != 1: sys.exit('FAQ insertion point not found')
    html = rep(html, '<section class="narrow prose">', section(p) + '<section class="narrow prose">')
    return html

created = []
for v in VARIANTS:
    out = pathlib.Path('tools') / v['slug'] / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(base, v), encoding='utf-8')
    created.append(v['slug'])
MAIN.write_text(build(base, MAIN_P), encoding='utf-8')

sm = SITEMAP.read_text(encoding='utf-8')
add = ''
for s in created:
    loc = '%s/tools/%s/' % (SITE, s)
    if loc not in sm: add += '  <url><loc>%s</loc></url>\n' % loc
if add:
    if '</urlset>' not in sm: sys.exit('sitemap has no </urlset>')
    SITEMAP.write_text(sm.replace('</urlset>', add + '</urlset>', 1), encoding='utf-8')
print('Main page upgraded. New pages:', *created, sep='\n  ')
print('Sitemap entries added:', add.count('<url>'))
