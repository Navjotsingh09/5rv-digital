#!/usr/bin/env python3
"""Add hover bridge for top-nav rv2 Services panel so it stays open while
the cursor travels from the button into the panel."""
import pathlib, sys

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

MARKER = 'rv2-panel-bridge-css'

CSS = (
'<style id="rv2-panel-bridge-css">'
# Invisible hover bridge spans the 14px gap below the Services button
'.rv2-nav__item--drop::after{content:"";position:absolute;left:-12px;right:-12px;top:100%;height:18px;pointer-events:auto;z-index:5}'
# Keep panel visible on hover OR when cursor is inside panel (focus-within for keyboard)
'.rv2-nav__item--drop:hover .rv2-nav__panel,.rv2-nav__item--drop:focus-within .rv2-nav__panel,.rv2-nav__panel:hover{opacity:1!important;pointer-events:all!important}'
# Slow the close so brief hover-loss does not kill it
'.rv2-nav__panel{transition:opacity .25s ease .12s!important}'
'.rv2-nav__item--drop:hover .rv2-nav__panel,.rv2-nav__panel:hover{transition:opacity .18s ease 0s!important}'
'</style>'
)

def migrate(p):
    fp = pathlib.Path(p); s = fp.read_text()
    if MARKER in s: return f'{p}: already up-to-date'
    if '</head>' not in s: return f'{p}: SKIP no </head>'
    s = s.replace('</head>', CSS + '</head>', 1)
    fp.write_text(s); return f'{p}: rv2 bridge injected'

if __name__=='__main__':
    for f in (sys.argv[1:] or PAGES): print(migrate(f))
