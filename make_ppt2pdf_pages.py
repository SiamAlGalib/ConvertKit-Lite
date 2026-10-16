import re, json, sys, pathlib
SITE = 'https://www.convertkitlite.site'
MAIN = pathlib.Path('tools/powerpointtopdf/index.html')
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
 ('powerpointtopdf', 'PowerPoint to PDF converter (main tool)'),
 ('ppt-to-pdf-converter', 'PPT to PDF converter'),
 ('ppsx-to-pdf', 'PPSX slideshow to PDF'),
 ('convert-powerpoint-to-pdf-on-phone', 'PowerPoint to PDF on Android and iPhone'),
 ('batch-powerpoint-to-pdf-converter', 'Batch PowerPoint to PDF converter'),
 ('powerpoint-to-pdf-without-powerpoint', 'Convert PowerPoint to PDF without PowerPoint'),
 ('powerpoint-to-pdf-small-file-size', 'PowerPoint to PDF with a small file size'),
 ('powerpoint-to-pdf-a4-letter-print', 'PowerPoint to PDF on A4 or US Letter'),
 ('powerpoint-to-pdf-without-notes', 'PowerPoint to PDF without speaker notes'),
]

MAIN_P = dict(
 slug='powerpointtopdf', name='PowerPoint to PDF Converter',
 title='PowerPoint to PDF Converter – Free, Private, No Upload',
 desc='Convert PowerPoint to PDF online free. Turn PPTX slides into a PDF in your browser, with your choice of page size and quality. No signup, no upload.',
 h1=None,
 intro='Turn PowerPoint presentations into clean PDF files, free and private. Pick the page size and quality. Everything happens in your browser, so nothing is uploaded.',
 h2='Convert PowerPoint to PDF, free and private',
 body='<p>This free PowerPoint to PDF converter builds the PDF in your browser. There is no signup, no watermark and no upload. It reads .pptx, .pptm, .ppsx and .potx files. Pick the guide below that matches your device or your goal.</p>',
 faqs=[
  ('How do I convert PowerPoint to PDF for free?', 'Add your .pptx file, choose the page size and quality, press Convert to PDF and download the result. It is free, needs no signup and runs in your browser.'),
  ('Can I convert PPTX to PDF without PowerPoint installed?', 'Yes. The converter reads the .pptx file in your browser, so you do not need PowerPoint or any other Office program.'),
  ('Are speaker notes included in the PDF?', 'No. Each slide becomes one PDF page showing only the slide. Speaker notes are not read and are not included.'),
 ])

VARIANTS = [
 dict(slug='ppt-to-pdf-converter', name='PPT to PDF Converter',
  title='PPT to PDF Converter – Free Online, No Upload',
  desc='Convert PPT presentations to PDF free in your browser. Modern .pptx files work directly, and old .ppt files need one quick re-save. No signup, no upload.',
  h1='PPT to <span>PDF</span>',
  intro='Convert a PowerPoint presentation to PDF in your browser. Modern .pptx files work directly. Old .ppt files need one quick re-save first.',
  h2='PPT to PDF: which files work',
  body='<p>People say PPT for any PowerPoint file, but there are two formats. Modern PowerPoint saves .pptx, and this converter reads it directly. The older .ppt format, used by PowerPoint 2003 and earlier, is not supported.</p><p>If you have an old .ppt file:</p><ul><li>Open it in PowerPoint, LibreOffice Impress or Google Slides.</li><li>Save or download it as .pptx. In PowerPoint, choose File &gt; Save As and pick PowerPoint Presentation (.pptx).</li><li>Add the new .pptx file to the converter above.</li></ul><p>The converter also reads .pptm, .ppsx and .potx files.</p>',
  faqs=[('Does this converter open old .ppt files?', 'No. It reads .pptx, .pptm, .ppsx and .potx. Save an old .ppt file as .pptx in PowerPoint first, then add it here.'),
        ('What is the difference between PPT and PPTX?', 'PPT is the older PowerPoint format used by PowerPoint 2003 and earlier. PPTX is the modern format used since PowerPoint 2007, and it is the one this tool reads.')]),
 dict(slug='ppsx-to-pdf', name='PPSX to PDF Converter',
  title='PPSX to PDF Converter – Free Slideshow to PDF',
  desc='Convert a PPSX slideshow to PDF for free in your browser. Each slide becomes a PDF page. No signup, no upload, no watermark.',
  h1='PPSX to <span>PDF</span>',
  intro='Convert a PowerPoint slideshow (.ppsx) to a PDF in your browser. Each slide becomes one PDF page, and nothing is uploaded.',
  h2='Convert a PPSX slideshow to PDF',
  body='<p>A .ppsx file is a PowerPoint Show. It has the same slides as a .pptx file, but it opens straight in slideshow mode. That makes it hard to share or print, so many people convert it to PDF.</p><p>This tool reads a .ppsx file like any other presentation. Add it, choose the page size and quality, and download the PDF. Animations and transitions are not part of a PDF, so the result shows each slide as a still page.</p>',
  faqs=[('What is a PPSX file?', 'A PPSX file is a PowerPoint slideshow. It contains the same slides as a PPTX file but opens directly in presentation mode.'),
        ('Will animations be in the PDF?', 'No. A PDF is static, so animations, transitions and videos are not included. Each slide appears as a still page.')]),
 dict(slug='convert-powerpoint-to-pdf-on-phone', name='PowerPoint to PDF on Android and iPhone',
  title='PowerPoint to PDF on Android & iPhone – Free, No App',
  desc='Convert PowerPoint to PDF on your Android phone or iPhone for free. Use your browser, with no app to install and no upload.',
  h1='PowerPoint to PDF on <span>Your Phone</span>',
  intro='Convert a PowerPoint presentation to PDF on your Android phone or iPhone. Use your browser, with no app to install and no upload.',
  h2='Convert PowerPoint to PDF on Android and iPhone',
  body='<p>Open this page in Chrome on Android or Safari on iPhone, tap the upload area and choose your .pptx file. Choose the quality, tap Convert to PDF, then tap Download.</p><ul><li>On Android the PDF goes to your usual Downloads folder.</li><li>On iPhone it is saved in the Files app, usually in Downloads.</li><li>Big presentations take longer on older phones. If it struggles, choose Standard quality.</li><li>Each file can be up to 100 MB.</li></ul><p>Your slides are drawn on your phone and are not sent to a server.</p>',
  faqs=[('Do I need an app to convert PowerPoint to PDF on my phone?', 'No. The converter works in your phone browser, such as Chrome or Safari.'),
        ('Why is it slow on my phone?', 'Your phone draws every slide itself, so large decks take longer on older devices. Choose Standard quality to finish sooner.')]),
 dict(slug='batch-powerpoint-to-pdf-converter', name='Batch PowerPoint to PDF Converter',
  title='Batch PowerPoint to PDF Converter – Many Files at Once',
  desc='Convert several PowerPoint files to PDF at once, free. Download each PDF or one ZIP. Private, runs in your browser, no signup.',
  h1='Batch PowerPoint to <span>PDF</span>',
  intro='Convert many PowerPoint files to PDF in one go. Download each PDF or all of them as one ZIP. Everything stays in your browser.',
  h2='Convert several presentations to PDF together',
  body='<p>Select several .pptx files at once, or drop them on the upload area, then press Convert to PDF. Each presentation becomes its own PDF with the same name. When more than one file is done, a Download all (ZIP) button appears.</p><ul><li>Each presentation can be up to 100 MB.</li><li>The list shows the page count of every PDF, and how many slide objects were left out.</li><li>The tool sets no limit on the number of files, but your browser uses your device memory. Convert very large batches in smaller groups.</li></ul>',
  faqs=[('How many presentations can I convert at once?', 'The tool sets no limit on the number of files. Each file can be up to 100 MB, and large batches use your device memory, so convert in smaller groups if your browser slows down.'),
        ('Can I download all the PDFs together?', 'Yes. When more than one file has been converted, press Download all (ZIP) to get every PDF in one file.')]),
 dict(slug='powerpoint-to-pdf-without-powerpoint', name='Convert PowerPoint to PDF Without PowerPoint',
  title='Convert PowerPoint to PDF Without PowerPoint – Free',
  desc='Convert PPTX to PDF without PowerPoint or Office installed. Free, runs in your browser on any computer, and your file is never uploaded.',
  h1='PowerPoint to PDF, <span>No PowerPoint Needed</span>',
  intro='Convert a .pptx file to PDF without PowerPoint or Office. It runs in your browser and your file is never uploaded.',
  h2='Convert PPTX to PDF without Microsoft PowerPoint',
  body='<p>The converter reads your .pptx file inside the browser and draws each slide itself, so you do not need PowerPoint, Office or any add-in. It works on any computer or phone with a modern browser.</p><p>Because it draws the slides itself, the result is close to the original but not identical:</p><ul><li>Text, pictures, shapes, tables, backgrounds and bullets are kept.</li><li>Charts, SmartArt, videos, animations and transitions are not included. The file list tells you how many objects were left out.</li><li>Fonts that are not installed on your device are replaced with similar ones, so line breaks can shift slightly.</li></ul><p>If you do have PowerPoint and need a pixel-perfect result for a complex deck, its own PDF export is the better choice.</p>',
  faqs=[('Do I need Microsoft Office to use this converter?', 'No. The converter works in your browser and does not need PowerPoint, Office or any extra software.'),
        ('Will the PDF look the same as in PowerPoint?', 'For most presentations it is very close. Charts, SmartArt, videos and animations are not included, and missing fonts are replaced, so check the PDF after converting.')]),
 dict(slug='powerpoint-to-pdf-small-file-size', name='PowerPoint to PDF with a Small File Size',
  title='PowerPoint to PDF – Small File Size for Email',
  desc='Convert PowerPoint to a smaller PDF for email. Choose Standard quality for the smallest file. Free, private, runs in your browser.',
  h1='PowerPoint to PDF, <span>Small File Size</span>',
  intro='Convert PowerPoint to a PDF that is small enough to email. Choose the quality that suits you. Free, and nothing is uploaded.',
  h2='How to get a smaller PDF from PowerPoint',
  body='<p>This tool draws every slide as a picture at the quality you choose, so the quality setting decides the file size.</p><ul><li><b>Standard:</b> the smallest file. Good for email and on-screen reading.</li><li><b>High:</b> the default. Sharper when you zoom in.</li><li><b>Maximum:</b> the sharpest pages and the largest file. Use it only for printing.</li></ul><p>If the PDF is still too big, run it through <a href="../compresspdf/">Compress PDF</a>. Decks with many large photos can stay large, so you can also cut it into parts with <a href="../splitpdf/">Split PDF</a>.</p>',
  faqs=[('Which quality gives the smallest PDF?', 'Standard. High and Maximum draw slides at a higher resolution, which looks sharper when zoomed or printed but makes the file larger.'),
        ('Can I make the PDF smaller after converting?', 'Yes. Use the Compress PDF tool on the finished file. It runs in your browser too.')]),
 dict(slug='powerpoint-to-pdf-a4-letter-print', name='PowerPoint to PDF on A4 or US Letter',
  title='PowerPoint to PDF on A4 or US Letter – Print Ready',
  desc='Convert PowerPoint to PDF on A4 or US Letter pages for printing. Choose orientation and quality. Free, private, no signup.',
  h1='PowerPoint to PDF on <span>A4 or Letter</span>',
  intro='Convert PowerPoint to a PDF on A4 or US Letter pages, ready to print. Choose the orientation and quality. Free and private.',
  h2='Make a print-ready PDF from PowerPoint',
  body='<p>Set Page size to A4 or US Letter, and each slide is placed in the middle of a standard page. Orientation can match your slides, or be set to landscape or portrait. For printing, choose High or Maximum quality.</p><ul><li>Each slide gets its own page.</li><li>The tool does not make handouts with several slides on one page, and it does not print notes pages. For those, use the print or export options inside PowerPoint.</li><li>Orientation only applies to A4 and US Letter. With Same as slides, the pages already match your slides.</li></ul>',
  faqs=[('Can I print several slides on one page?', 'Not with this tool. Each slide gets its own PDF page. For several slides per page, use the print options in PowerPoint.'),
        ('Why is the orientation menu turned off?', 'Orientation applies only to A4 and US Letter. When Page size is Same as slides, the pages already match the shape of your slides.')]),
 dict(slug='powerpoint-to-pdf-without-notes', name='PowerPoint to PDF Without Speaker Notes',
  title='PowerPoint to PDF Without Speaker Notes – Slides Only',
  desc='Convert PowerPoint to a slides-only PDF. Speaker notes are not included, so private notes stay out. Free, private, runs in your browser.',
  h1='PowerPoint to PDF, <span>Slides Only</span>',
  intro='Convert PowerPoint to a PDF that shows only the slides. Speaker notes are not included. Free, and nothing is uploaded.',
  h2='A slides-only PDF, with no speaker notes',
  body='<p>Each slide becomes one PDF page that shows only what your audience sees. This tool does not read speaker notes at all, so private notes never end up in the PDF you share.</p><ul><li>Hidden slides are skipped by default. Choose Include hidden slides if you want them.</li><li>Animations, transitions and videos are not part of a PDF.</li><li>If you want the notes in the PDF, this tool cannot do that. The PDF export inside PowerPoint has an option for notes pages.</li></ul>',
  faqs=[('Are my speaker notes included in the PDF?', 'No. The converter draws only the slides, and notes are never read, so they cannot appear in the PDF.'),
        ('Can I make a PDF with speaker notes?', 'Not with this tool. Use the PDF export in PowerPoint and choose its notes pages option.')]),
]

def section(p):
    lis = ''.join('<li><a href="../%s/">%s</a></li>' % (s, esc(l)) for s, l in LINKS if s != p['slug'])
    return ('<section class="narrow prose"><!--seo-upgrade--><h2>%s</h2>%s<h2>More PowerPoint to PDF options</h2><ul>%s</ul></section>\n\n'
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
        html = rep(html, '<h1>PowerPoint to <span>PDF</span></h1>', '<h1>%s</h1>' % p['h1'])
    html = rep(html, '<p>Turn PowerPoint presentations into clean, ready-to-share PDF files. Choose the page size, orientation and quality. Everything happens in your browser.</p>', '<p>%s</p>' % esc(p['intro']))
    blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S))
    if len(blocks) != 1: sys.exit('Expected 1 JSON-LD block, found %d' % len(blocks))
    m = blocks[0]
    data = json.loads(m.group(2))
    for node in data['@graph']:
        if node['@type'] == 'WebApplication':
            node['name'], node['description'], node['url'] = p['name'], p['desc'], url
        elif node['@type'] == 'BreadcrumbList' and p['slug'] != 'powerpointtopdf':
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
