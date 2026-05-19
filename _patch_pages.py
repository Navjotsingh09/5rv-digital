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
_patch_pages.py
===============
For every HTML page:
  1. Add <link rel="stylesheet" href="css/rv-components.css"> after the last
     existing CSS link in <head> (or before </head> if no CSS links).
  2. Remove every <style id="..."> block EXCEPT critical-css.
  3. Report bytes saved per page.
"""
import glob, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
KEEP_INLINE = {'critical-css'}

LINK_TAG = '<link href="css/rv-components.css" rel="stylesheet" type="text/css">'
MARKER   = 'rv-components.css'

pages = sorted(p for p in glob.glob(os.path.join(BASE, '*.html'))
               if not any(x in os.path.basename(p) for x in
                          ['backup', 'preview', '_restore', '.bak',
                           'index_backup', 'detail_api']))

total_saved = 0
for p in pages:
    fname = os.path.basename(p)
    with open(p, encoding='utf-8') as f:
        original = f.read()

    html = original

    # ── 2. Remove all <style id="..."> blocks except KEEP_INLINE ────────────
    def should_remove(m):
        sid = m.group(1)
        return sid not in KEEP_INLINE

    html = re.sub(
        r'\s*<style\s+id="([^"]+)">.*?</style>',
        lambda m: '' if should_remove(m) else m.group(0),
        html, flags=re.DOTALL
    )

    # ── 1. Add link tag if not already present ───────────────────────────────
    if MARKER not in html:
        # Insert after the last <link ... webflow.css ...> line
        # (i.e., after the main stylesheet links)
        insert_after = re.search(
            r'(<link\s[^>]*5rv-revamp\.webflow\.css[^>]*>)',
            html
        )
        if insert_after:
            html = html[:insert_after.end()] + '\n  ' + LINK_TAG + html[insert_after.end():]
        else:
            # Fallback: before </head>
            html = html.replace('</head>', f'  {LINK_TAG}\n</head>', 1)

    saved = len(original) - len(html)
    total_saved += saved
    print(f'  {fname}: -{saved//1024}KB ({len(original)//1024}KB → {len(html)//1024}KB)')

    if html != original:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)

print(f'\nTotal saved across {len(pages)} pages: {total_saved//1024}KB')
