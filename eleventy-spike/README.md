# Eleventy Spike — 5RV Digital

Proof-of-concept for migrating the 5RV Digital site from patched Webflow HTML to
an Eleventy (11ty) static site generator with shared includes.

## Goal

Eliminate the Python patching workflow by making nav, footer, and `<head>` true
shared templates that rebuild all pages on every deploy.

## Structure

```
eleventy-spike/
├── _includes/
│   ├── base.njk      ← base layout (wraps every page)
│   ├── head.njk      ← <head> with templated title/description/canonical
│   ├── nav.njk       ← floating navbar (active-state via page.fileSlug)
│   └── footer.njk    ← footer with prefooter CTA
├── index.njk         ← sample homepage
├── .eleventy.js      ← Eleventy config
├── package.json
└── README.md
```

## Quick Start

```bash
cd eleventy-spike
npm install
npm run serve   # → http://localhost:8080
```

## Migration Path

1. Copy each production `.html` page into this directory as a `.njk` file
2. Strip `<head>`, nav, and footer — replace with `layout: base.njk` in front matter
3. Test `npm run build` — verify output in `_site/`
4. Update `vercel.json` `outputDirectory` to point at `eleventy-spike/_site`
5. Add `npm run build` as the Vercel build command

## Status

**SPIKE ONLY** — Not production-ready. See `adina_react_decision.txt` in the
project root for the broader framework decision.
