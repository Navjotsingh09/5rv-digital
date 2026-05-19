# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Inject missing .rv-navbar{} dock CSS block + improve mega menu spacing.
Some pages (services.html etc.) lost the dock CSS in earlier edits; without
.rv-drop-caret sizing the SVG renders huge."""
import pathlib, sys

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

MARKER = 'rv-dock-css-restored'

# Extract from index.html (canonical source)
SRC = pathlib.Path('index.html').read_text()
i = SRC.find('.rv-navbar{')
j = SRC.find('.rv-navbar__drop a:hover{', i)
j = SRC.find('}', j) + 1
DOCK_CSS = SRC[i:j]
assert DOCK_CSS, 'Could not extract dock CSS from index.html'

WRAPPED = f'<style id="{MARKER}">' + DOCK_CSS + '</style>'

# Improved spacing for mega menu (overrides previous canonical)
MEGA_FIX_MARKER = 'rv-mega-spacing-v2'
MEGA_FIX = (
'<style id="rv-mega-spacing-v2">'
'.rv-navbar__has-drop .rv-navbar__drop.rv-mega{width:640px}'
'.rv-mega .rv-mega__inner{grid-template-columns:1fr 1fr;gap:6px;padding:14px}'
'.rv-mega__card{padding:12px;min-height:64px;align-items:center}'
'.rv-mega__thumb{width:48px;height:48px}'
'.rv-mega__t{font-size:13.5px}'
'.rv-mega__s{font-size:11.5px;white-space:normal}'
'</style>'
)

def migrate(p):
    fp = pathlib.Path(p); s = fp.read_text()
    changed = False
    # 1. Inject dock CSS if missing
    if MARKER not in s and '.rv-navbar{' not in s:
        if '</head>' not in s: return f'{p}: SKIP no </head>'
        s = s.replace('</head>', WRAPPED + '</head>', 1)
        changed = True
        msg1 = 'dock CSS injected'
    elif MARKER in s:
        msg1 = 'dock already restored'
    else:
        msg1 = 'dock CSS already present (canonical)'
    # 2. Inject mega spacing v2
    if MEGA_FIX_MARKER not in s:
        s = s.replace('</head>', MEGA_FIX + '</head>', 1)
        changed = True
        msg2 = 'mega spacing v2 added'
    else:
        msg2 = 'mega spacing already present'
    if changed: fp.write_text(s)
    return f'{p}: {msg1}; {msg2}'

if __name__=='__main__':
    for f in (sys.argv[1:] or PAGES): print(migrate(f))
