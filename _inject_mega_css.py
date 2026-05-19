#!/usr/bin/env python3
"""Re-inject mega menu CSS + hover bridge so dropdown stays open while cursor
travels from the Services pill up into the panel."""
import pathlib, sys

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

MARKER = 'rv-mega-canonical-css'

CSS = (
'<style id="rv-mega-canonical-css">'
# Wider panel for mega; ensure parent has position so ::after anchors
'.rv-navbar__has-drop{position:relative}'
'.rv-navbar__has-drop .rv-navbar__drop.rv-mega{width:560px;bottom:calc(100% + 14px);padding-bottom:0}'
# Hover bridge: invisible strip filling the gap above the Services pill
'.rv-navbar__has-drop::after{content:"";position:absolute;left:-10px;right:-10px;bottom:100%;height:22px;pointer-events:auto;z-index:99}'
# Keep dropdown open while cursor is on the bridge OR the dropdown
'.rv-navbar__has-drop:hover .rv-navbar__drop,.rv-navbar__has-drop:focus-within .rv-navbar__drop{opacity:1;pointer-events:all;transform:translateX(-50%) translateY(0)}'
# Mega panel styling
'.rv-mega .rv-mega__inner{background:rgba(16,16,18,0.97);-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:12px;box-shadow:0 18px 48px rgba(0,0,0,.55);display:grid;grid-template-columns:1fr 1fr;gap:4px}'
'.rv-mega__card{display:flex;align-items:center;gap:12px;padding:10px;border-radius:12px;text-decoration:none;transition:background .18s ease;background:transparent}'
'.rv-mega__card:hover{background:rgba(255,255,255,.07)}'
'.rv-mega__card::before{display:none!important}'
'.rv-mega__thumb{width:46px;height:46px;border-radius:10px;overflow:hidden;flex-shrink:0;background:rgba(255,255,255,.05);display:flex;align-items:center;justify-content:center}'
'.rv-mega__thumb img{width:100%;height:100%;object-fit:cover;display:block}'
'.rv-mega__thumb--all{background:linear-gradient(135deg,#5a85ff,#1e50d8)}'
'.rv-mega__txt{display:flex;flex-direction:column;gap:3px;min-width:0}'
'.rv-mega__t{font-family:var(--font-primary);font-size:13px;font-weight:600;color:#fff;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
'.rv-mega__s{font-family:var(--font-primary);font-size:11px;font-weight:500;color:rgba(255,255,255,.55);line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
'@media(max-width:767px){.rv-navbar__drop.rv-mega{display:none}}'
'</style>'
)

def migrate(p):
    fp = pathlib.Path(p); s = fp.read_text()
    if MARKER in s: return f'{p}: already up-to-date'
    if '</head>' not in s: return f'{p}: SKIP no </head>'
    s = s.replace('</head>', CSS + '</head>', 1)
    fp.write_text(s); return f'{p}: mega css injected'

if __name__=='__main__':
    for f in (sys.argv[1:] or PAGES): print(migrate(f))
