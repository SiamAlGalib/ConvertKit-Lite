import re, json, sys, pathlib
SITE = 'https://www.convertkitlite.site'
MAIN = pathlib.Path('tools/docxtotxt/index.html')
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

# Analytics: match the other tool pages (only if missing)
tracked = []
if '/lazy-track.js' not in base and '<!-- Tools - below result -->' in base:
    base = base.replace('<!-- Tools - below result -->', '<script src="/lazy-presence.js" defer></script>\n<script src="/lazy-track.js" defer></script>\n<!-- Tools - below result -->', 1)
    tracked.append('lazy-presence.js + lazy-track.js')
old_dl = "a.download=base(it.name)+'.txt';ac.appendChild(a);"
if old_dl in base and 'trackUse' not in base:
    base = base.replace(old_dl, "a.download=base(it.name)+'.txt';a.onclick=()=>import('/stats.js').then(m=>m.trackUse());ac.appendChild(a);", 1)
    tracked.append('trackUse on download')

LINKS = [
 ('docxtotxt', 'DOCX to TXT converter (main tool)'),
 ('word-to-txt', 'Word to TXT converter'),
 ('doc-to-txt', 'DOC to TXT (old Word files)'),
 ('extract-text-from-docx', 'Extract text from DOCX'),
 ('batch-docx-to-txt-converter', 'Batch DOCX to TXT converter'),
 ('docx-to-txt-no-upload', 'DOCX to TXT without uploading'),
 ('docx-to-txt-utf8', 'DOCX to TXT in UTF-8'),
 ('convert-word-table-to-text', 'Convert a Word table to text'),
 ('remove-formatting-from-word-document', 'Remove formatting from a Word document'),
]

MAIN_P = dict(
 slug='docxtotxt', name='DOCX to TXT Converter',
 title='DOCX to TXT Converter – Convert Word to Plain Text Free',
 desc='Convert DOCX to TXT online free. Extract the plain text from Word documents in your browser, with UTF-8 output. No signup, no upload.',
 h1=None,
 intro='Extract the plain text from Word documents, free and private. Paragraphs, line breaks, lists and tables are kept as readable text, and nothing is uploaded.',
 h2='Convert DOCX to TXT, free and private',
 body='<p>This free DOCX to TXT converter reads your Word document in your browser and gives you a plain .txt file. There is no signup, no watermark and no upload. Pick the guide below that matches your goal.</p>',
 faqs=[
  ('How do I convert DOCX to TXT for free?', 'Add your .docx files, choose the paragraph spacing and encoding, press Convert to TXT and download the result. It is free, needs no signup and runs in your browser.'),
  ('Can I convert Word to TXT without Microsoft Word?', 'Yes. The converter reads the .docx file in your browser, so you do not need Word or any other program.'),
  ('Are tracked changes included in the TXT file?', 'Inserted text is kept and deleted text is dropped, so you get the clean, final version of the document.'),
 ])

VARIANTS = [
 dict(slug='word-to-txt', name='Word to TXT Converter',
  title='Word to TXT Converter – Free, Private, No Upload',
  desc='Convert a Word document to TXT for free in your browser. Works with .docx files. No signup, no watermark, no upload.',
  h1='Word to <span>TXT</span>',
  intro='Convert a Word document to plain text in your browser. It works with .docx files, it is free, and nothing is uploaded.',
  h2='Convert Word to TXT',
  body='<p>Word saves modern documents as .docx, and this converter reads that format. Add your file, choose the paragraph spacing and the encoding, and download a .txt file with the text of the document.</p><ul><li>Old .doc files are not supported. Open them in Word and save them as .docx first.</li><li>Only the main text is converted. Fonts, colors, images, headers and footers are left out.</li><li>You do not need Word installed.</li></ul>',
  faqs=[('Do I need Microsoft Word to convert Word to TXT?', 'No. The converter reads the .docx file in your browser, so you do not need Word installed.'),
        ('Does it work with .doc files?', 'No. It reads .docx files only. Open an old .doc file in Word and save it as .docx first.')]),
 dict(slug='doc-to-txt', name='DOC to TXT Converter',
  title='DOC to TXT – Convert Old Word Files to Text (Free)',
  desc='Convert a Word document to TXT for free. Modern .docx files work directly, and old .doc files need one quick re-save. No signup, no upload.',
  h1='DOC to <span>TXT</span>',
  intro='Convert a Word document to TXT in your browser. Modern .docx files work directly. Old .doc files need one quick re-save first.',
  h2='DOC to TXT: which files work',
  body='<p>There are two Word formats. Word 2007 and newer save .docx, and this converter reads it directly. The older .doc format, used by Word 2003 and earlier, is not supported.</p><p>If you have an old .doc file:</p><ul><li>Open it in Word, LibreOffice or Google Docs.</li><li>Save or download it as .docx. In Word, choose File &gt; Save As and pick Word Document (.docx).</li><li>Add the new .docx file to the converter above.</li></ul>',
  faqs=[('Does this converter open .doc files?', 'No. It reads .docx files only. Save an old .doc file as .docx in Word first, then add it here.'),
        ('What is the difference between DOC and DOCX?', 'DOC is the older Word format used by Word 2003 and earlier. DOCX is the modern format used since Word 2007, and it is the one this tool reads.')]),
 dict(slug='extract-text-from-docx', name='Extract Text from DOCX',
  title='Extract Text from DOCX – Free, Private, No Upload',
  desc='Pull the plain text out of a Word DOCX file in your browser. Free, no signup, and your document is never uploaded.',
  h1='Extract Text from <span>DOCX</span>',
  intro='Pull the plain text out of a Word document in your browser. Free, and your file is never uploaded.',
  h2='What the tool extracts from a DOCX file',
  body='<p>A .docx file is a ZIP archive, and the main text sits in one part of it. The tool opens the archive in your browser and writes that text to a .txt file.</p><ul><li><b>Kept:</b> paragraphs as lines, line breaks, tabs, and table rows with cells separated by tabs.</li><li><b>Lists:</b> bulleted and numbered items both start with a bullet mark, so list numbers are not kept.</li><li><b>Tracked changes:</b> inserted text is kept and deleted text is dropped.</li><li><b>Not read:</b> headers, footers, footnotes and comments live in other parts of the file, and images contain no text to extract.</li></ul>',
  faqs=[('Which parts of a DOCX file are extracted?', 'The main body text: paragraphs, line breaks, tabs, list items and table rows. Headers, footers, footnotes, comments and images are not included.'),
        ('Can it read text that is inside an image?', 'No. The tool reads real text only and has no text recognition (OCR), so text inside a picture is not extracted.')]),
 dict(slug='batch-docx-to-txt-converter', name='Batch DOCX to TXT Converter',
  title='Batch DOCX to TXT Converter – Many Files at Once',
  desc='Convert many Word DOCX files to TXT at once, free. Download each TXT or all of them as one ZIP. Private, runs in your browser.',
  h1='Batch DOCX to <span>TXT</span>',
  intro='Convert many Word documents to TXT in one go. Download each file or all of them as one ZIP. Everything stays in your browser.',
  h2='Convert several DOCX files to TXT together',
  body='<p>Select several .docx files at once, or drop them on the upload area, then press Convert to TXT. Each document becomes its own .txt file with the same name. When more than one file is done, a Download all (ZIP) button appears.</p><ul><li>The list shows the word count of every file.</li><li>If two files share a name, a number is added in the ZIP so nothing is overwritten.</li><li>The tool makes one TXT file per document. It does not join them into a single file.</li><li>The tool sets no limit on the number of files, but your browser uses your device memory. Convert very large batches in smaller groups.</li></ul>',
  faqs=[('How many DOCX files can I convert at once?', 'The tool sets no limit on the number of files. Large batches use your device memory, so convert in smaller groups if your browser slows down.'),
        ('Can I join all the documents into one TXT file?', 'No. The tool makes one TXT file per document. You can download them all together as a ZIP.')]),
 dict(slug='docx-to-txt-no-upload', name='DOCX to TXT Without Uploading',
  title='DOCX to TXT Without Uploading – Private Converter',
  desc='Convert Word DOCX to TXT without uploading your document. The text is extracted in your browser, so private files stay on your device.',
  h1='DOCX to TXT, <span>No Upload</span>',
  intro='Convert a Word document to TXT without sending it anywhere. The text is extracted on your own device.',
  h2='Convert DOCX to TXT without uploading',
  body='<p>Your browser opens the .docx file from your computer or phone, reads the text and saves the .txt file there too. The document is never sent to a server. The page loads its code when you open it, but your documents stay on your device.</p><p>That matters for contracts, reports, notes and other private files.</p>',
  faqs=[('Is my Word document sent to a server?', 'No. The text is extracted in your browser, so your files stay on your device.'),
        ('Is there a file size limit?', 'There is no fixed limit, because nothing is uploaded. Very large documents are limited only by your device memory.')]),
 dict(slug='docx-to-txt-utf8', name='DOCX to TXT in UTF-8',
  title='DOCX to TXT in UTF-8 – Keep Accents and Any Language',
  desc='Convert DOCX to TXT in UTF-8 so accents and non-Latin text stay correct. Optional UTF-8 with BOM for old Windows programs. Free and private.',
  h1='DOCX to TXT in <span>UTF-8</span>',
  intro='Convert a Word document to a UTF-8 text file, so accents and other languages stay correct. Free, and nothing is uploaded.',
  h2='Choosing the right encoding for your TXT file',
  body='<p>UTF-8 is the default. It works almost everywhere and keeps accented letters and text in any language, including Arabic, Bengali, Chinese and Japanese.</p><ul><li><b>UTF-8:</b> the right choice for nearly every program.</li><li><b>UTF-8 with BOM:</b> adds a small marker that helps some older Windows programs notice that the file is UTF-8. Choose it only if accented characters look broken.</li><li>Other encodings, such as UTF-16, are not offered.</li></ul>',
  faqs=[('Which encoding should I choose?', 'UTF-8 works almost everywhere. Choose UTF-8 with BOM only if an older Windows program shows broken accented characters.'),
        ('Does it keep non-English text?', 'Yes. Text in any language is kept, including accents, Arabic, Bengali, Chinese, Japanese and emoji. Open the file in a modern text editor.')]),
 dict(slug='convert-word-table-to-text', name='Convert a Word Table to Text',
  title='Convert a Word Table to Text – Tab-Separated Rows',
  desc='Turn a Word table into plain text with one line per row and tabs between cells. Paste it into Excel or Google Sheets. Free and private.',
  h1='Convert a Word Table to <span>Text</span>',
  intro='Turn a table in a Word document into plain text, one line per row with tabs between the cells. Free, and nothing is uploaded.',
  h2='How Word tables become text',
  body='<p>Each table row becomes one line in the TXT file, and the cells in that row are separated by tabs. Paste the result into Excel or Google Sheets and the columns come back.</p><ul><li>Borders, shading and column widths are not kept, because plain text cannot store them.</li><li>Merged cells are not rebuilt, so the columns can shift in rows that contain them.</li><li>Text outside the table is converted too, in the original order.</li></ul>',
  faqs=[('How do I get a Word table into Excel?', 'Convert the document to TXT, open the file, copy the table lines and paste them into Excel or Google Sheets. The tabs put each cell in its own column.'),
        ('Are merged cells kept?', 'Merged cells are not rebuilt. The text of each cell appears in its row, but the columns can shift where cells were merged.')]),
 dict(slug='remove-formatting-from-word-document', name='Remove Formatting from a Word Document',
  title='Remove Formatting from a Word Document – Plain Text',
  desc='Strip fonts, colors and styles from a Word document and keep only the text. Free, private, and your file is never uploaded.',
  h1='Remove Formatting from a <span>Word Document</span>',
  intro='Strip the fonts, colors and styles from a Word document and keep only the text. Free, and nothing is uploaded.',
  h2='Get the text of a Word document without its formatting',
  body='<p>Converting a .docx file to TXT removes all formatting: fonts, sizes, colors, bold, italic, styles and images. What is left is the text, with its paragraph breaks and line breaks.</p><ul><li>Plain text pastes into emails, web editors and chat apps without carrying any style with it.</li><li>Your original .docx is not changed. The tool makes a new .txt file.</li><li>Formatting cannot be brought back from the TXT file, so keep the original document.</li></ul>',
  faqs=[('Will my original Word file change?', 'No. The tool reads your .docx file and makes a new .txt file. The original stays as it was.'),
        ('Can I get the formatting back later?', 'No. A TXT file cannot store formatting, so keep your original document if you may need it.')]),
]

def section(p):
    lis = ''.join('<li><a href="../%s/">%s</a></li>' % (s, esc(l)) for s, l in LINKS if s != p['slug'])
    return ('<section class="narrow seo"><!--seo-upgrade--><h2>%s</h2>%s<h2>More DOCX to TXT options</h2><ul>%s</ul></section>\n\n'
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
        html = rep(html, '<h1>DOCX to <span>TXT</span></h1>', '<h1>%s</h1>' % p['h1'])
    html = rep(html, '<p>Extract the plain text from Word documents. Paragraphs, line breaks, lists and tables are kept as readable text. Everything happens in your browser.</p>', '<p>%s</p>' % esc(p['intro']))
    blocks = list(re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', html, re.S))
    if len(blocks) != 1: sys.exit('Expected 1 JSON-LD block, found %d' % len(blocks))
    m = blocks[0]
    data = json.loads(m.group(2))
    for node in data['@graph']:
        if node['@type'] == 'WebApplication':
            node['name'], node['description'], node['url'] = p['name'], p['desc'], url
        elif node['@type'] == 'BreadcrumbList' and p['slug'] != 'docxtotxt':
            node['itemListElement'][1]['name'] = p['name']
            node['itemListElement'][1]['item'] = url
        elif node['@type'] == 'FAQPage':
            for q, a in p['faqs']:
                node['mainEntity'].append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}})
    html = html[:m.start(2)] + json.dumps(data, ensure_ascii=False) + html[m.end(2):]
    extra = ''.join('<details><summary>%s</summary><p>%s</p></details>\n  ' % (esc(q), esc(a)) for q, a in p['faqs'])
    html, n = re.subn(r'(</details>)(\s*</section>\s*<section class="related")', lambda mm: mm.group(1) + '\n  ' + extra.rstrip() + mm.group(2), html, count=1)
    if n != 1: sys.exit('FAQ insertion point not found')
    html = rep(html, '<section class="narrow seo" id="why">', section(p) + '<section class="narrow seo" id="why">')
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
print('Tracking added:', ', '.join(tracked) if tracked else 'nothing (already there or spots not found)')
