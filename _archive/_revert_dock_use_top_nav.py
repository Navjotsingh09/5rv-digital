# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Revert bottom dock + book pill + scroll-swap. Use the EXISTING .rv2-header as
the single nav. Upgrade its Services dropdown to use images instead of icons."""
import re, sys, pathlib

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

# 1) Remove injected dock + book pill + active-js (between marker and end of script)
DOCK_RE = re.compile(
    r'\n?<!-- rv-dock-canonical -->.*?</script>\s*',
    re.DOTALL,
)
# 2) Remove our injected style/script blocks by id
STYLE_RE_MEGA   = re.compile(r'<style id="rv-mega-canonical-css">.*?</style>', re.DOTALL)
STYLE_RE_SWAP   = re.compile(r'<style id="rv-scroll-swap-css">.*?</style>', re.DOTALL)
SCRIPT_RE_SWAP  = re.compile(r'<script id="rv-scroll-swap-js">.*?</script>', re.DOTALL)

# Image map by service href
IMG_MAP = {
    'web-development.html':                'images/Rectangle-6_2.webp',
    'seo-expert.html':                     'images/Rectangle-6-5_1.webp',
    'social-media-marketing-agency.html':  'images/Rectangle-6_5.webp',
    'branding.html':                       'images/Rectangle-6_4.webp',
    'digital-marketing-strategies.html':   'images/Rectangle-6-3.webp',
}

# Replace each <div class="rv2-panel__link-icon"><svg ...>...</svg></div>
# inside an anchor whose href matches a known service page, with an <img>.
LINK_RE = re.compile(
    r'(<a href="([^"]+)" class="rv2-panel__link">\s*)'
    r'<div class="rv2-panel__link-icon"><svg[^>]*>.*?</svg></div>',
    re.DOTALL,
)

def swap_link(m):
    head, href = m.group(1), m.group(2)
    img = IMG_MAP.get(href)
    if not img:
        return m.group(0)  # leave unknown links untouched (e.g. content marketing)
    return (
        head
        + f'<div class="rv2-panel__link-icon rv2-panel__link-icon--img">'
        + f'<img src="{img}" alt="" loading="lazy" width="40" height="40">'
        + '</div>'
    )

# CSS to make icon container show an image cleanly (additive; original CSS keeps icon ver)
PANEL_IMG_CSS = (
'<style id="rv2-panel-img-css">'
'.rv2-panel__link-icon--img{width:40px;height:40px;border-radius:9px;overflow:hidden;background:rgba(53,110,255,.06);padding:0}'
'.rv2-panel__link-icon--img img{width:100%;height:100%;object-fit:cover;display:block}'
'</style>'
)
PANEL_IMG_MARKER = 'rv2-panel-img-css'

def migrate(path):
    p = pathlib.Path(path)
    s = p.read_text()
    orig = s
    # Strip injected blocks
    s = DOCK_RE.sub('\n', s)
    s = STYLE_RE_MEGA.sub('', s)
    s = STYLE_RE_SWAP.sub('', s)
    s = SCRIPT_RE_SWAP.sub('', s)
    # Swap dropdown link icons -> images
    s = LINK_RE.sub(swap_link, s)
    # Inject panel-img CSS once
    if PANEL_IMG_MARKER not in s and '</head>' in s:
        s = s.replace('</head>', PANEL_IMG_CSS + '</head>', 1)
    if s == orig:
        return f'{path}: no-op'
    p.write_text(s)
    return f'{path}: cleaned'

if __name__ == '__main__':
    for f in (sys.argv[1:] or PAGES):
        print(migrate(f))
