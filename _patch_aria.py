#!/usr/bin/env python3

# --- pre-flight git check ---
import subprocess, sys as _sys
_res = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
if _res.stdout.strip():
    print("ABORT: Uncommitted changes detected. Commit or stash before running this script.")
    _sys.exit(1)
del _res
# --- end pre-flight ---

"""
_patch_aria.py
==============
1. FAQ ARIA: Convert .rv-faq-item__q divs to <button type="button"> with
   aria-expanded + aria-controls.  Add id to .rv-faq-item__a panels.
   Add aria-hidden to icon wrappers.  Update FAQ click JS to toggle aria-expanded.

2. Mega menu: Add aria-haspopup="true" to the Services nav link.

3. Skip link: Add <a class="skip-to-main" href="#main-content"> after <body>.

4. rv-components.css additions: button reset for faq trigger + :focus-within
   for mega dropdown.
"""
import glob, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

pages = sorted(p for p in glob.glob(os.path.join(BASE, '*.html'))
               if not any(x in os.path.basename(p) for x in
                          ['backup', 'preview', '_restore', '.bak',
                           'index_backup', 'detail_api']))

OLD_FAQ_JS = ("(function(){var items=document.querySelectorAll('.rv-faq-item');"
              "items.forEach(function(item){var q=item.querySelector('.rv-faq-item__q')"
              ",a=item.querySelector('.rv-faq-item__a');"
              "q.addEventListener('click',function(){var open=item.classList.contains('active');"
              "items.forEach(function(o){o.classList.remove('active');"
              "o.querySelector('.rv-faq-item__a').style.maxHeight=null});"
              "if(!open){item.classList.add('active');a.style.maxHeight=a.scrollHeight+'px'}"
              "})})})();")

NEW_FAQ_JS = ("(function(){var items=document.querySelectorAll('.rv-faq-item');"
              "items.forEach(function(item){var q=item.querySelector('.rv-faq-item__q')"
              ",a=item.querySelector('.rv-faq-item__a');"
              "q.addEventListener('click',function(){var open=item.classList.contains('active');"
              "items.forEach(function(o){o.classList.remove('active');"
              "o.querySelector('.rv-faq-item__a').style.maxHeight=null;"
              "o.querySelector('.rv-faq-item__q').setAttribute('aria-expanded','false');"
              "});"
              "if(!open){item.classList.add('active');a.style.maxHeight=a.scrollHeight+'px';"
              "q.setAttribute('aria-expanded','true');}"
              "})})})();")

FAQ_Q_PAT = re.compile(
    r'<div class="rv-faq-item__q">'
    r'(.*?<div class="rv-faq-item__icon">.*?</div>)'
    r'</div>\s*<div class="rv-faq-item__a">',
    re.DOTALL
)

SERVICES_LINK_PAT = re.compile(
    r'<a (href="services\.html" data-rv-page="services\.html")'
    r'(?!\s+aria-haspopup)',  # don't double-add
)

SKIP_LINK_HTML = '<a href="#main-content" class="skip-to-main">Skip to main content</a>\n'

stats = {'faq_pages': 0, 'faq_items': 0, 'mega_pages': 0, 'skip_pages': 0, 'js_updated': 0}

for p in pages:
    fname = os.path.basename(p)
    with open(p, encoding='utf-8') as f:
        html = f.read()
    original = html
    changed = False

    # ── 1. Skip-to-main link ─────────────────────────────────────────────────
    if 'skip-to-main' not in html:
        html = html.replace('<body', '<body', 1)  # noop, find proper body tag
        html = re.sub(r'(<body[^>]*>)', r'\1\n' + SKIP_LINK_HTML, html, count=1)
        stats['skip_pages'] += 1
        changed = True

    # ── 2. FAQ ARIA ──────────────────────────────────────────────────────────
    counter = [0]
    def replace_faq(m):
        counter[0] += 1
        n = counter[0]
        content = m.group(1)
        content = content.replace(
            '<div class="rv-faq-item__icon">',
            '<div class="rv-faq-item__icon" aria-hidden="true">',
            1
        )
        return (
            f'<button type="button" class="rv-faq-item__q" '
            f'aria-expanded="false" aria-controls="faq-answer-{n}">'
            f'{content}'
            f'</button>'
            f'<div class="rv-faq-item__a" id="faq-answer-{n}">'
        )

    new_html = FAQ_Q_PAT.sub(replace_faq, html)
    if counter[0] > 0:
        stats['faq_pages'] += 1
        stats['faq_items'] += counter[0]
        html = new_html
        changed = True

    # ── 3. FAQ JS: update to toggle aria-expanded ────────────────────────────
    if OLD_FAQ_JS in html:
        html = html.replace(OLD_FAQ_JS, NEW_FAQ_JS, 1)
        stats['js_updated'] += 1
        changed = True

    # ── 4. Mega menu: add aria-haspopup to Services link ────────────────────
    new_html = SERVICES_LINK_PAT.sub(
        r'<a \1 aria-haspopup="true"', html
    )
    if new_html != html:
        html = new_html
        stats['mega_pages'] += 1
        changed = True

    if changed:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  {fname}: faq_q={counter[0]} skip={"y" if "skip-to-main" in html else "n"} mega={"y" if "aria-haspopup" in html else "n"}')

print(f'\nSummary:')
print(f'  Skip link added to: {stats["skip_pages"]} pages')
print(f'  FAQ: {stats["faq_items"]} items converted across {stats["faq_pages"]} pages')
print(f'  FAQ JS updated: {stats["js_updated"]} pages')
print(f'  Mega menu aria-haspopup added: {stats["mega_pages"]} pages')
