import re, json, sys, pathlib
SITE = 'https://www.convertkitlite.site'
MAIN = pathlib.Path('tools/webptojpg/index.html')
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
 ('webptojpg', 'WebP to JPG converter (main tool)'),
 ('webp-to-jpeg', 'WebP to JPEG converter'),
 ('webp-to-jpg-no-upload', 'WebP to JPG without uploading'),
 ('batch-webp-to-jpg-converter', 'Batch WebP to JPG converter'),
 ('webp-to-jpg-high-quality', 'WebP to JPG in high quality'),
 ('webp-to-jpg-transparent-background', 'WebP to JPG with a transparent background'),
 ('convert-webp-to-jpg-on-phone', 'WebP to JPG on Android and iPhone'),
 ('convert-webp-to-jpg-on-windows-and-mac', 'WebP to JPG on Windows and Mac'),
 ('save-webp-as-jpg', 'Picture saved as WebP? Convert it to JPG'),
]

MAIN_P = dict(
 slug='webptojpg', name='WebP to JPG Converter',
 title='WebP to JPG Converter – Convert WebP to JPG Free, No Upload',
 desc='Convert WebP to JPG online free. Add one or many WebP images, choose the JPG quality and download. Runs in your browser, no signup, no upload.',
 h1=None,
 intro='Convert WebP images to JPG so they open in almost any app, email or upload form. Choose the quality, convert many files at once, and nothing leaves your device.',
 h2='Convert WebP to JPG, free and private',
 body='<p>This free WebP to JPG converter turns .webp images into JPG files in your browser. There is no signup, no watermark and no upload. Pick the guide below that matches your device or your goal, or read the full guide: <a href="/blog/convert-webp-to-jpg-free-private-bulk/">How to convert WebP to JPG, free, private and in bulk</a>.</p>',
 faqs=[
  ('How do I convert WebP to JPG for free?', 'Add your .webp files, choose the JPG quality, press Convert to JPG and download the results. It is free, needs no signup and runs in your browser.'),
  ('Is WebP better than JPG?', 'WebP usually makes smaller files at similar quality, which is why websites use it. JPG is better when you need a file that opens everywhere, such as for email, print and older software.'),
  ('Why did my picture download as a WebP file?', 'Many websites serve pictures as WebP because it loads faster. When you save such a picture, the file keeps the .webp format, so convert it to JPG if an app will not open it.'),
 ])

VARIANTS = [
 dict(slug='webp-to-jpeg', name='WebP to JPEG Converter',
  title='WebP to JPEG Converter – Free, Private, No Upload',
  desc='Convert WebP to JPEG for free in your browser. Choose the quality and keep the same image size. No signup, no watermark, no upload.',
  h1='WebP to <span>JPEG</span>',
  intro='Convert WebP images to JPEG in your browser. Free, no signup, and your pictures are never uploaded.',
  h2='WebP to JPEG: the same format as JPG',
  body='<p>JPEG and JPG are the same image format. The shorter .jpg ending comes from old systems that allowed only three letters after the dot. The files from this converter end in .jpg, and every app that opens JPEG files opens them.</p><p>The JPEG keeps the same width and height as your WebP. You choose the quality from 40% to 100%, and the default is 90%.</p>',
  faqs=[('Is JPG the same as JPEG?', 'Yes. They are two names for the same image format.'),
        ('Will the image size in pixels change?', 'No. The JPEG has the same width and height as your WebP. Only the file format and quality change.')]),
 dict(slug='webp-to-jpg-no-upload', name='WebP to JPG Without Uploading',
  title='WebP to JPG Without Uploading – Private Converter',
  desc='Convert WebP to JPG without uploading your pictures. The conversion runs in your browser, so your images stay on your device.',
  h1='WebP to JPG, <span>No Upload</span>',
  intro='Convert WebP to JPG without sending your pictures anywhere. The conversion happens on your own device.',
  h2='Convert WebP to JPG without uploading',
  body='<p>Your browser reads each WebP file from your computer or phone and saves the JPG there too, so your pictures are never sent to a server. The page loads its code when you open it, but your images stay on your device.</p><p>There is also a privacy bonus. The image is redrawn and saved as a new JPG, so details stored inside the original file, such as camera settings or GPS location, are not carried over.</p>',
  faqs=[('Are my images sent to a server?', 'No. The WebP files are converted in your browser and the JPG files are made on your device.'),
        ('Is photo information such as location kept?', 'No. The image is redrawn and saved as a new JPG, so camera settings and GPS location stored in the original file are not carried over.')]),
 dict(slug='batch-webp-to-jpg-converter', name='Batch WebP to JPG Converter',
  title='Batch WebP to JPG Converter – Many Images at Once',
  desc='Convert many WebP images to JPG at once, free. Download each JPG or all of them as one ZIP. Private, runs in your browser.',
  h1='Batch WebP to <span>JPG</span>',
  intro='Convert many WebP images to JPG in one go. Download each file or all of them as one ZIP. Everything stays in your browser.',
  h2='Convert many WebP files to JPG together',
  body='<p>Select several .webp files at once, or drop them on the upload area, then press Convert to JPG. Each image becomes a JPG with the same name. When more than one file is done, a Download all (ZIP) button appears.</p><ul><li>The list shows the old and new file size and the pixel size of every image.</li><li>If two files share a name, a number is added in the ZIP so nothing is overwritten.</li><li>The tool sets no limit on the number of files, but your browser uses your device memory. Convert very large batches in smaller groups.</li></ul>',
  faqs=[('How many WebP files can I convert at once?', 'The tool sets no limit. Large batches use your device memory, so convert in smaller groups if your browser slows down.'),
        ('Can I download all the JPG files together?', 'Yes. After conversion, press Download all (ZIP) to get every JPG in one file.')]),
 dict(slug='webp-to-jpg-high-quality', name='WebP to JPG High Quality',
  title='WebP to JPG in High Quality – Free Converter',
  desc='Convert WebP to JPG with the quality slider at 100% for the best result. Same image size, free, and nothing is uploaded.',
  h1='WebP to JPG, <span>High Quality</span>',
  intro='Convert WebP to JPG with the least possible loss. Set the quality to 100% and keep the original image size. Free and private.',
  h2='How to get the best quality from WebP to JPG',
  body='<p>Drag the JPG quality slider to 100% before you convert. The JPG keeps the same width and height as your WebP, so nothing is resized.</p><ul><li>JPG is a lossy format, so saving always compresses the picture a little. At 90% or higher the difference is hard to see on most photos.</li><li>Converting cannot bring back detail that was already lost when the WebP was made.</li><li>The JPG is often bigger than the WebP, because WebP is a more efficient format. That is normal.</li></ul>',
  faqs=[('Will converting WebP to JPG reduce quality?', 'Saving as JPG always compresses the image a little. At 90% or higher the difference is hard to see on most photos, and 100% gives the best result.'),
        ('Why is my JPG bigger than the WebP?', 'WebP compresses images more efficiently than JPG, so the JPG is often larger at the same visual quality. Lower the quality slider if you need a smaller file.')]),
 dict(slug='webp-to-jpg-transparent-background', name='WebP to JPG with a Transparent Background',
  title='WebP to JPG with a Transparent Background – What Happens',
  desc='JPG cannot be see-through. Convert WebP to JPG and fill transparent areas with white, black or gray. Free, private, in your browser.',
  h1='WebP to JPG and <span>Transparent Areas</span>',
  intro='JPG cannot store transparency. Choose white, black or gray to fill the see-through parts of your WebP. Free and private.',
  h2='What happens to a transparent WebP',
  body='<p>A WebP image can have a see-through background, but a JPG cannot. When you convert, the transparent areas are filled with the color you pick in the menu.</p><ul><li><b>White:</b> the safest choice for most pictures.</li><li><b>Black or gray:</b> can look better for white logos or light artwork.</li><li>If you need to keep the transparent background, do not convert to JPG. Keep the image as PNG instead. <a href="../imageconverter/">Image Converter</a> can help with other formats.</li></ul>',
  faqs=[('Can I keep the transparent background in a JPG?', 'No. JPG does not support transparency, so see-through areas are filled with white, black or gray, whichever you choose.'),
        ('Which color should I choose for transparent areas?', 'White is the safest choice for most pictures. Black or gray can look better for white logos or light artwork.')]),
 dict(slug='convert-webp-to-jpg-on-phone', name='WebP to JPG on Android and iPhone',
  title='WebP to JPG on Android & iPhone – Free, No App',
  desc='Convert WebP to JPG on your Android phone or iPhone for free. Use your browser, with no app to install and no upload.',
  h1='WebP to JPG on <span>Your Phone</span>',
  intro='Convert a WebP picture to JPG on your Android phone or iPhone. Use your browser, with no app to install and no upload.',
  h2='Convert WebP to JPG on Android and iPhone',
  body='<p>Open this page in Chrome on Android or Safari on iPhone, tap the upload area and choose your .webp pictures. Pick the quality, tap Convert to JPG, then download the files.</p><ul><li>On Android the JPG files go to your usual Downloads folder.</li><li>On iPhone they are saved in the Files app, usually in Downloads.</li><li>Very large images can take longer on older phones.</li></ul><p>Your pictures are converted on your phone and are not sent to a server.</p>',
  faqs=[('Do I need an app to convert WebP to JPG on my phone?', 'No. The converter works in your phone browser, such as Chrome or Safari.'),
        ('Where is the JPG saved on my phone?', 'On Android it goes to your Downloads folder. On iPhone it appears in the Files app, usually in Downloads.')]),
 dict(slug='convert-webp-to-jpg-on-windows-and-mac', name='WebP to JPG on Windows and Mac',
  title='WebP to JPG on Windows & Mac – Free, No Software',
  desc='Convert WebP to JPG on Windows or Mac for free. Use any modern browser, with no software to install and no upload.',
  h1='WebP to JPG on <span>Windows and Mac</span>',
  intro='Convert WebP pictures to JPG on a Windows PC or a Mac. Use your browser, with no software to install and no upload.',
  h2='Convert WebP to JPG on a computer',
  body='<p>Open this page in Chrome, Edge, Firefox or Safari. Drag your .webp files onto the upload area, choose the quality and press Convert to JPG. Then download each JPG or one ZIP.</p><ul><li>There is nothing to install and no account to create.</li><li>The JPG files go to your usual Downloads folder.</li><li>You can add many files at once, so a whole folder of pictures takes one conversion.</li></ul>',
  faqs=[('Do I need to install software on Windows or Mac?', 'No. The converter runs in your browser, so there is nothing to install.'),
        ('Which browsers work?', 'Any modern browser, including Chrome, Edge, Firefox and Safari. Your browser needs to be able to open WebP images, which current versions can.')]),
 dict(slug='save-webp-as-jpg', name='Picture Saved as WebP? Convert It to JPG',
  title='Picture Saved as WebP? Convert It to JPG – Free',
  desc='Saved a picture and got a WebP file? Convert it to JPG so it opens in any app or upload form. Free, private, in your browser.',
  h1='Saved as WebP? <span>Convert to JPG</span>',
  intro='Saved a picture and got a .webp file that will not open or upload? Convert it to JPG here. Free, and nothing is uploaded.',
  h2='Why your picture was saved as WebP',
  body='<p>Many websites serve pictures as WebP because it makes small files that load fast. When you save one of those pictures, the file can arrive as .webp. Some older apps, email programs, print shops and upload forms do not accept it.</p><p>To fix that, add the .webp file to the converter above, choose the quality and download the JPG. The converter makes a new JPG from the WebP, so it cannot restore an original JPG that the website may have had.</p>',
  faqs=[('Why did my picture download as WebP?', 'Websites often serve pictures as WebP because it loads faster. When you save the picture, the file keeps the .webp format.'),
        ('What happens to an animated WebP?', 'Only the first frame is converted, because JPG does not support animation.')]),
]

def section(p):
    lis = ''.join('<li><a href="../%s/">%s</a></li>' % (s, esc(l)) for s, l in LINKS if s != p['slug'])
    return ('<section class="narrow prose"><!--seo-upgrade--><h2>%s</h2>%s<h2>More WebP to JPG options</h2><ul>%s</ul></section>\n\n'
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
    if p['h1']:
        html = rep(html, '<h1>WebP to <span>JPG</span></h1>', '<h1>%s</h1>' % p['h1'])
    html = rep(html, '<p>Convert WebP images to JPG for easy sharing and wide compatibility. Choose your quality and convert many files at once. Everything happens in your browser.</p>', '<p>%s</p>' % esc(p['intro']))
    blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S))
    if len(blocks) != 1: sys.exit('Expected 1 JSON-LD block, found %d' % len(blocks))
    m = blocks[0]
    data = json.loads(m.group(2))
    for node in data['@graph']:
        if node['@type'] == 'WebApplication':
            node['name'], node['description'], node['url'] = p['name'], p['desc'], url
        elif node['@type'] == 'BreadcrumbList' and p['slug'] != 'webptojpg':
            node['itemListElement'][1]['name'] = p['name']
            node['itemListElement'][1]['item'] = url
        elif node['@type'] == 'FAQPage':
            for q, a in p['faqs']:
                node['mainEntity'].append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    html = html[:m.start(2)] + json.dumps(data, ensure_ascii=False) + html[m.end(2):]
    extra = ''.join('<details><summary>%s</summary><p>%s</p></details>\n  ' % (esc(q), esc(a)) for q, a in p['faqs'])
    html, n = re.subn(r'(</details>)(\s*</section>\s*<section class="related")', lambda mm: mm.group(1) + '\n  ' + extra.rstrip() + mm.group(2), html, count=1)
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
