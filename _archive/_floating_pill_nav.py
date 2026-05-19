# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Swap solid white rv2-header bar -> floating glass pill (CSS only).
Markup + JS untouched. Idempotent."""
import re, sys, pathlib

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

# Old CSS lines we replace (two width variants)
OLD_HEADER = re.compile(
    r'\.rv2-header\{position:fixed;top:0;left:0;right:0;z-index:9999;background:#fff;border-bottom:1px solid rgba\(11,23,57,\.07\);transition:box-shadow \.3s\}'
)
OLD_SCROLLED = re.compile(
    r'\.rv2-header\.scrolled\{box-shadow:0 2px 20px rgba\(11,23,57,\.09\)\}'
)
OLD_INNER = re.compile(
    r'\.rv2-header__inner\{width:(min\(1180px,calc\(100% - 48px\)\)|var\(--container\));margin:0 auto;height:68px;display:flex;align-items:center;gap:0\}'
)

NEW_HEADER   = '.rv2-header{position:fixed;top:0;left:0;right:0;z-index:9999;background:transparent;border:none;pointer-events:none;transition:none}'
NEW_SCROLLED = '.rv2-header.scrolled .rv2-header__inner{box-shadow:0 8px 32px rgba(11,23,57,.14),0 1px 0 rgba(255,255,255,.65) inset}'
NEW_INNER    = ('.rv2-header__inner{width:min(1180px,calc(100% - 48px));margin:14px auto 0;height:60px;'
                'display:flex;align-items:center;gap:0;padding:0 22px;pointer-events:auto;'
                'background:rgba(255,255,255,.55);-webkit-backdrop-filter:blur(20px) saturate(180%);'
                'backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(255,255,255,.55);'
                'border-radius:20px;box-shadow:0 4px 24px rgba(11,23,57,.08),0 1px 0 rgba(255,255,255,.6) inset;'
                'transition:box-shadow .3s}')

# Marker so we can detect already-migrated pages
MARKER = 'pointer-events:auto;background:rgba(255,255,255,.55)'

def migrate(path):
    p = pathlib.Path(path)
    s = p.read_text()
    if MARKER in s:
        return f'{path}: already floating (skipped)'
    n_h = len(OLD_HEADER.findall(s))
    n_s = len(OLD_SCROLLED.findall(s))
    n_i = len(OLD_INNER.findall(s))
    if not (n_h == 1 and n_s == 1 and n_i == 1):
        return f'{path}: SKIP (matches header={n_h} scrolled={n_s} inner={n_i})'
    s2 = OLD_HEADER.sub(NEW_HEADER, s, count=1)
    s2 = OLD_SCROLLED.sub(NEW_SCROLLED, s2, count=1)
    s2 = OLD_INNER.sub(NEW_INNER, s2, count=1)
    p.write_text(s2)
    return f'{path}: floating pill applied'

if __name__ == '__main__':
    targets = sys.argv[1:] or PAGES
    for f in targets:
        print(migrate(f))
