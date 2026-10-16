import re, json, sys, pathlib
SITE = 'https://www.convertkitlite.site'
MAIN = pathlib.Path('tools/pdftojpg/index.html')
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
 ('pdftojpg', 'PDF to JPG converter (main tool)'),
 ('pdf-to-jpeg', 'PDF to JPEG converter'),
 ('pdf-to-image-converter', 'PDF to image converter'),
 ('pdf-to-jpg-high-quality', 'PDF to JPG in high quality'),
 ('batch-pdf-to-jpg-converter', 'Batch PDF to JPG converter'),
 ('pdf-to-jpg-no-upload', 'PDF to JPG without uploading'),
 ('convert-one-page-of-pdf-to-jpg', 'Convert one page of a PDF to JPG'),
 ('convert-pdf-to-jpg-on-phone', 'PDF to JPG on Android and iPhone'),
 ('pdf-to-jpg-small-file-size', 'PDF to JPG with a small file size'),
]

MAIN_P = dict(
 slug='pdftojpg', name='PDF to JPG Converter',
 title='PDF to JPG Converter – Convert PDF Pages to JPG Free',
 desc='Convert PDF to JPG online free. Turn every PDF page into a JPG image in your browser, with a choice of resolution and quality. No signup, no upload.',
 h1=None,
 intro='Turn every page of your PDF into a JPG image, free and private. Choose the resolution and quality. Everything happens in your browser, so nothing is uploaded.',
 h2='Convert PDF to JPG, free and private',
 body='<p>This free PDF to JPG converter draws every page of your PDF as a JPG image in your browser. There is no signup, no watermark and no upload. Pick the guide below that matches your device or your goal.</p>',
 faqs=[
  ('How do I convert PDF to JPG for free?', 'Add your PDF, choose the resolution and quality, press Convert to JPG and download the images. It is free, needs no signup and runs in your browser.'),
  ('Can I convert PDF to JPEG instead of JPG?', 'JPG and JPEG are the same image format, so the files work everywhere JPEG files do. The files from this tool end in .jpg.'),
  ('Can I convert PDF to PNG with this tool?', 'No. This tool saves JPG images only. JPG suits photos and pages you want to share or upload.'),
 ])

VARIANTS = [
 dict(slug='pdf-to-jpeg', name='PDF to JPEG Converter',
  title='PDF to JPEG Converter – Free, Private, No Upload',
  desc='Convert PDF to JPEG for free in your browser. Every page becomes an image, and your PDF is never uploaded. No signup, no watermark.',
  h1='PDF to <span>JPEG</span>',
  intro='Convert PDF pages to JPEG images in your browser. Free, no signup, and your PDF is never uploaded.',
  h2='PDF to JPEG: the same format as JPG',
  body='<p>JPEG and JPG are the same image format. The shorter .jpg ending comes from old systems that allowed only three letters after the dot. The files from this converter end in .jpg, and every app that opens JPEG files opens them.</p><p>Each PDF page becomes one image, saved on a white background. You choose the resolution (72, 150 or 220 DPI) and the quality from 40% to 100%.</p>',
  faqs=[('Is JPG the same as JPEG?', 'Yes. They are two names for the same image format.'),
        ('Will my files end in .jpg or .jpeg?', 'They end in .jpg. Any program that opens JPEG files will open them.')]),
 dict(slug='pdf-to-image-converter', name='PDF to Image Converter',
  title='PDF to Image Converter – Save PDF Pages as JPG',
  desc='Convert PDF to images for free. Every PDF page is saved as a JPG image in your browser. No signup, no watermark, no upload.',
  h1='PDF to <span>Image</span>',
  intro='Save every page of a PDF as an image. The images are JPG files, made in your browser with nothing uploaded.',
  h2='Turn PDF pages into images',
  body='<p>This converter saves each PDF page as a JPG image. JPG is the only image format it makes, so there is no PNG or TIFF option. JPG is a good choice for pages you want to share, upload or send in a chat.</p><ul><li>The text becomes part of the picture, so it can no longer be selected or searched.</li><li>If you need the text itself, use <a href="../pdftotxt/">PDF to Text</a> or <a href="../pdftoword/">PDF to Word</a>.</li><li>Each page is saved on a white background.</li></ul>',
  faqs=[('Which image formats can I get from a PDF here?', 'JPG only. The tool does not make PNG, TIFF or other formats.'),
        ('Can I select the text in the image?', 'No. A JPG is a picture, so the text cannot be selected or searched.')]),
 dict(slug='pdf-to-jpg-high-quality', name='PDF to JPG High Quality',
  title='PDF to JPG in High Quality – Sharp Images, Free',
  desc='Convert PDF to high quality JPG images. Choose 220 DPI and 100% quality for the sharpest pages. Free, private, runs in your browser.',
  h1='PDF to JPG, <span>High Quality</span>',
  intro='Get the sharpest JPG images from your PDF. Choose the highest resolution and quality. Free, and nothing is uploaded.',
  h2='How to get sharp JPG images from a PDF',
  body='<p>For the sharpest result, set Resolution to Very high (220 DPI) and drag the JPG quality slider to 100%. An A4 page then comes out at about 1819 × 2572 pixels.</p><ul><li>The highest resolution here is 220 DPI. There is no 300 or 600 DPI option.</li><li>JPG is a lossy format, so even at 100% fine text edges can look slightly softer than in the PDF.</li><li>Very large pages, such as posters, are scaled down so the image stays at about 16 million pixels or fewer.</li><li>High settings make bigger files, and the size of every image is shown before you download it.</li></ul>',
  faqs=[('Is there a 300 DPI option?', 'No. The highest option is 220 DPI, which gives about 1819 × 2572 pixels for an A4 page.'),
        ('Does JPG lose quality?', 'Yes, JPG is a lossy format. A high quality setting keeps the loss small, but it is never zero.')]),
 dict(slug='batch-pdf-to-jpg-converter', name='Batch PDF to JPG Converter',
  title='Batch PDF to JPG Converter – Many PDFs at Once',
  desc='Convert several PDF files to JPG at once, free. Every page becomes an image. Download each image or one ZIP. Private, no signup.',
  h1='Batch PDF to <span>JPG</span>',
  intro='Convert many PDF files to JPG in one go. Download each image or all of them as one ZIP. Everything stays in your browser.',
  h2='Convert several PDFs to JPG together',
  body='<p>Select several PDF files at once, or drop them on the upload area, then press Convert to JPG. Every page of every PDF becomes its own image. When there is more than one image, a Download all (ZIP) button appears.</p><ul><li>A one-page PDF gives name.jpg. A PDF with several pages gives names such as report-page-1.jpg and report-page-2.jpg.</li><li>If two PDFs share a name, a number is added so nothing is overwritten.</li><li>The tool sets no limit on the number of files, but a 50-page PDF gives 50 images and your browser uses your device memory. Convert very large batches in smaller groups.</li></ul>',
  faqs=[('How many PDFs can I convert at once?', 'The tool sets no limit on the number of files. Large batches use your device memory, so convert in smaller groups if your browser slows down.'),
        ('How are the images named?', 'A one-page PDF gives name.jpg. A PDF with several pages gives name-page-1.jpg, name-page-2.jpg and so on.')]),
 dict(slug='pdf-to-jpg-no-upload', name='PDF to JPG Without Uploading',
  title='PDF to JPG Without Uploading – Private Converter',
  desc='Convert PDF to JPG without uploading your file. The images are made in your browser, so private documents stay on your device.',
  h1='PDF to JPG, <span>No Upload</span>',
  intro='Convert PDF to JPG without sending your file anywhere. The pages are drawn on your own device.',
  h2='Convert a PDF to JPG without uploading it',
  body='<p>Your browser reads the PDF from your computer or phone and draws each page itself. The JPG images are made there too, so your PDF is never sent to a server.</p><p>That matters for private files such as contracts, ID copies and bank statements. The converter code is downloaded when you open the page, but your PDF stays on your device.</p>',
  faqs=[('Is my PDF sent to a server?', 'No. The pages are drawn in your browser and the images are made on your device.'),
        ('Do I need an internet connection?', 'The page needs a connection to load the converter code. Your PDF itself is not sent anywhere.')]),
 dict(slug='convert-one-page-of-pdf-to-jpg', name='Convert One Page of a PDF to JPG',
  title='Convert One Page of a PDF to JPG – Free',
  desc='Convert a single PDF page to JPG for free. Use First page only, or pull any page out with Split PDF first. Private, no signup.',
  h1='Convert One PDF Page to <span>JPG</span>',
  intro='Turn a single page of a PDF into a JPG image. Free, no signup, and nothing is uploaded.',
  h2='How to convert just one page of a PDF',
  body='<p>The tool can convert all pages or only the first page. There is no page range option. Here is how to get the page you want:</p><ul><li><b>The first page:</b> set Pages to First page only, then convert.</li><li><b>Any other page:</b> use <a href="../splitpdf/">Split PDF</a> to pull that page into its own file, then convert the new file.</li></ul>',
  faqs=[('Can I choose a page range?', 'No. The tool converts all pages or only the first page. For other pages, use Split PDF first.'),
        ('What will the file be called?', 'A one-page PDF gives name.jpg. If the PDF has several pages, the image is called name-page-1.jpg.')]),
 dict(slug='convert-pdf-to-jpg-on-phone', name='PDF to JPG on Android and iPhone',
  title='PDF to JPG on Android & iPhone – Free, No App',
  desc='Convert PDF to JPG on your Android phone or iPhone for free. Use your browser, with no app to install and no upload.',
  h1='PDF to JPG on <span>Your Phone</span>',
  intro='Convert a PDF to JPG images on your Android phone or iPhone. Use your browser, with no app to install and no upload.',
  h2='Convert PDF to JPG on Android and iPhone',
  body='<p>Open this page in Chrome on Android or Safari on iPhone, tap the upload area and choose your PDF. Pick the resolution, tap Convert to JPG, then download the images.</p><ul><li>On Android the images go to your usual Downloads folder.</li><li>On iPhone they are saved in the Files app, usually in Downloads.</li><li>Long PDFs and the 220 DPI setting can be slow on older phones, so try 150 DPI first.</li><li>For a long PDF, use the ZIP download instead of saving every image one by one.</li></ul><p>Your PDF is drawn on your phone and is not sent to a server.</p>',
  faqs=[('Do I need an app to convert PDF to JPG on my phone?', 'No. The converter works in your phone browser, such as Chrome or Safari.'),
        ('Why is it slow on my phone?', 'Your phone draws every page itself, so long PDFs and the highest resolution take longer on older devices. Try 150 DPI.')]),
 dict(slug='pdf-to-jpg-small-file-size', name='PDF to JPG with a Small File Size',
  title='PDF to JPG with a Small File Size – Free',
  desc='Convert PDF to smaller JPG images. Choose 72 DPI and a lower quality for the smallest files. Free, private, runs in your browser.',
  h1='PDF to JPG, <span>Small File Size</span>',
  intro='Convert PDF pages to JPG images that are small enough to email or upload. Free, and nothing is uploaded.',
  h2='How to get smaller JPG files from a PDF',
  body='<p>Two settings decide the size of each image: the resolution and the JPG quality.</p><ul><li><b>Resolution:</b> choose Standard (72 DPI) for the smallest images. 150 DPI is the default, and 220 DPI makes the largest.</li><li><b>Quality:</b> drag the slider down. The size of every image is shown in the results list, so you can compare before you download.</li><li>Pages with photos or dense graphics always make bigger files than pages of plain text.</li></ul><p>If an image is still too big, run it through <a href="../imagecompressor/">Image Compressor &amp; Resizer</a>.</p>',
  faqs=[('Can I set an exact file size, such as 100 KB?', 'No. The tool does not aim for a set size. Lower the resolution and quality until the size shown in the results list is small enough.'),
        ('Why are some pages much bigger than others?', 'Pages with photos or dense graphics produce bigger JPGs than pages of plain text.')]),
]

def section(p):
    lis = ''.join('<li><a href="../%s/">%s</a></li>' % (s, esc(l)) for s, l in LINKS if s != p['slug'])
    return ('<section class="narrow prose"><!--seo-upgrade--><h2>%s</h2>%s<h2>More PDF to JPG options</h2><ul>%s</ul></section>\n\n'
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
        html = rep(html, '<h1>PDF to <span>JPG</span></h1>', '<h1>%s</h1>' % p['h1'])
    html = rep(html, '<p>Turn every page of your PDF into a JPG image. Choose the resolution and quality you need. Everything happens in your browser.</p>', '<p>%s</p>' % esc(p['intro']))
    blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S))
    if len(blocks) != 1: sys.exit('Expected 1 JSON-LD block, found %d' % len(blocks))
    m = blocks[0]
    data = json.loads(m.group(2))
    for node in data['@graph']:
        if node['@type'] == 'WebApplication':
            node['name'], node['description'], node['url'] = p['name'], p['desc'], url
        elif node['@type'] == 'BreadcrumbList' and p['slug'] != 'pdftojpg':
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
