import re, shutil, sys
from pathlib import Path

path = Path("tools/PdfToWord/index.html")
if not path.exists():
    sys.exit("Can't find tools/PdfToWord/index.html. Run this from the repo root.")
html = path.read_text(encoding="utf-8")
if 'data-b="img1"' in html:
    sys.exit("Already fixed. Nothing to do.")

NEW = '''<div class="article-list">
    <a class="article-card" href="articles/pdf-to-word-guide/">
      <div class="article-banner"><span class="glyph">📘</span><img data-b="img1" alt="" loading="lazy"/><span class="article-tag">PDF TO WORD</span></div>
      <div class="article-body"><h3>How to Convert PDF to Word</h3><p>Learn the easiest ways to turn PDFs into editable Word documents.</p><span class="article-read">Read article →</span></div>
    </a>
    <a class="article-card" href="articles/what-is-a-docx-file/">
      <div class="article-banner b2"><span class="glyph">📄</span><img data-b="img2" alt="" loading="lazy"/><span class="article-tag">FILE FORMATS</span></div>
      <div class="article-body"><h3>What Is a DOCX File?</h3><p>Understand what DOCX is and when to use it.</p><span class="article-read">Read article →</span></div>
    </a>
    <a class="article-card" href="articles/rtf-vs-docx-vs-pdf/">
      <div class="article-banner b3"><span class="glyph">⚖️</span><img data-b="img3" alt="" loading="lazy"/><span class="article-tag">COMPARISON</span></div>
      <div class="article-body"><h3>RTF vs DOCX vs PDF</h3><p>Compare the most common document formats and pick the right one.</p><span class="article-read">Read article →</span></div>
    </a>
  </div>
  <script>document.querySelectorAll('.article-list img[data-b]').forEach(i=>{const b=i.dataset.b,e=['.jpg','.png','.webp','.jpeg',''];let n=0;i.onerror=()=>{n++;n<e.length?i.src=b+e[n]:i.remove()};i.src=b+e[0]})</script>
</section>'''

pat = re.compile(r'<div class="article-list">.*?</div>\s*</section>', re.S)
if not pat.search(html):
    sys.exit("Couldn't find the article-list block. Nothing was changed.")
html = pat.sub(lambda m: NEW, html, count=1)
html = html.replace("/tools/pdftoword/", "/tools/PdfToWord/")
shutil.copy(path, str(path) + ".bak")
path.write_text(html, encoding="utf-8")
print("Done. Fixed", path, "(backup saved as index.html.bak)")