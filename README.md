# ConvertKit Lite

**Free online file tools that run in your browser.** Merge, split, compress and convert PDFs, work with images, and more, with no sign-up and no installs.

🌐 **Live site:** [convertkitlite.site](https://www.convertkitlite.site)

---

## Features

### PDF tools
- **Merge PDF**: combine multiple PDFs into one file
- **Split PDF**: extract pages or split a document into parts
- **Compress PDF**: reduce file size while keeping it readable
- **PDF to Word**: convert PDFs into editable documents
- **PDF to PowerPoint / PDF to Excel**
- **Word to PDF / PowerPoint to PDF**

### Image & other tools
- Image Converter
- Image Compressor
- QR Code Generator
- Background Remover

### Site features
- Tools mega-menu for quick navigation between categories
- Light / dark mode toggle
- Responsive layout for desktop and mobile
- SEO-ready (`sitemap.xml`, `robots.txt`, custom `404.html`)

> Some tools may still be in progress. Check the live site for what's currently available.

---

## Tech stack

- HTML, CSS and vanilla JavaScript (no build step)
- Static hosting on **GitHub Pages** with a custom domain (`CNAME`)
- Deployment via GitHub Actions (`.github/workflows`)

---

## Project structure

```
ConvertKit-Lite/
├── .github/workflows/   # Deployment workflow
├── tools/               # Individual tool pages (e.g. tools/merge-pdf.html)
├── 404.html             # Custom not-found page
├── CNAME                # Custom domain for GitHub Pages
├── index.html           # Homepage with tool grid and navigation
├── robots.txt
└── sitemap.xml
```

Each tool lives on its own page under `/tools/`, so URLs look like `https://www.convertkitlite.site/tools/<tool-name>.html`.

---

## Running locally

No dependencies are needed. Clone the repo and serve it with any static server:

```bash
git clone https://github.com/solus-stay-focused/ConvertKit-Lite.git
cd ConvertKit-Lite

# Option 1: Python
python -m http.server 8000

# Option 2: Node
npx serve .
```

Then open `http://localhost:8000` in your browser.

---

## Deployment

The site is deployed with GitHub Pages from the `main` branch.

1. Push your changes to `main`.
2. The workflow in `.github/workflows` publishes the site.
3. Make sure `CNAME` contains your custom domain and the domain's DNS points to GitHub Pages.

If a page works locally but not on the live site, check that the Actions run finished successfully and hard-refresh to bypass the cache.

---

## Adding a new tool

1. Copy an existing page in `tools/` as a starting point.
2. Update the title, meta description and tool logic.
3. Add a card for it on `index.html` and an entry in the Tools menu.
4. Add the new URL to `sitemap.xml`.

---

## Contributing

Issues and pull requests are welcome. For larger changes, please open an issue first to discuss what you'd like to change.

---

## Author

Built by **SAG** ([@solus-stay-focused](https://github.com/solus-stay-focused)).

---

## License

No license has been added yet. Until one is, all rights are reserved. Add a `LICENSE` file (for example MIT) if you want others to use or modify the code.
