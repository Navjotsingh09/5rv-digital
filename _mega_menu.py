#!/usr/bin/env python3
"""Replace small Services dropdown with image-based mega menu in bottom dock.
Idempotent via marker. Operates on all 11 main pages."""
import re, sys, pathlib

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

MARKER = 'rv-mega-canonical-css'

# Match the EXISTING small dropdown injected by _inject_bottom_dock.py
OLD_DROP_RE = re.compile(
    r'<div class="rv-navbar__drop">\s*<div class="rv-navbar__drop-inner">.*?</div>\s*</div>',
    re.DOTALL,
)

NEW_DROP = (
'<div class="rv-navbar__drop rv-mega">'
'<div class="rv-mega__inner">'
'<a class="rv-mega__card" href="web-development.html">'
'<div class="rv-mega__thumb"><img src="images/Rectangle-6_2.webp" alt="" loading="lazy" width="48" height="48"></div>'
'<div class="rv-mega__txt"><div class="rv-mega__t">Web Design &amp; Dev</div><div class="rv-mega__s">Conversion-focused websites</div></div>'
'</a>'
'<a class="rv-mega__card" href="seo-expert.html">'
'<div class="rv-mega__thumb"><img src="images/Rectangle-6-5_1.webp" alt="" loading="lazy" width="48" height="48"></div>'
'<div class="rv-mega__txt"><div class="rv-mega__t">SEO</div><div class="rv-mega__s">Rank, traffic &amp; growth</div></div>'
'</a>'
'<a class="rv-mega__card" href="social-media-marketing-agency.html">'
'<div class="rv-mega__thumb"><img src="images/Rectangle-6_5.webp" alt="" loading="lazy" width="48" height="48"></div>'
'<div class="rv-mega__txt"><div class="rv-mega__t">Social Media</div><div class="rv-mega__s">Content that converts</div></div>'
'</a>'
'<a class="rv-mega__card" href="branding.html">'
'<div class="rv-mega__thumb"><img src="images/Rectangle-6_4.webp" alt="" loading="lazy" width="48" height="48"></div>'
'<div class="rv-mega__txt"><div class="rv-mega__t">Branding</div><div class="rv-mega__s">Identity &amp; positioning</div></div>'
'</a>'
'<a class="rv-mega__card" href="digital-marketing-strategies.html">'
'<div class="rv-mega__thumb"><img src="images/Rectangle-6-3.webp" alt="" loading="lazy" width="48" height="48"></div>'
'<div class="rv-mega__txt"><div class="rv-mega__t">Paid Ads</div><div class="rv-mega__s">Performance media</div></div>'
'</a>'
'<a class="rv-mega__card rv-mega__card--all" href="services.html">'
'<div class="rv-mega__thumb rv-mega__thumb--all"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></div>'
'<div class="rv-mega__txt"><div class="rv-mega__t">All Services</div><div class="rv-mega__s">Full overview</div></div>'
'</a>'
'</div>'
'</div>'
)

CSS = (
'<style id="rv-mega-canonical-css">'
# Widen dropdown container, give it a hover buffer so cursor can travel down
'.rv-navbar__has-drop .rv-navbar__drop.rv-mega{width:560px;bottom:calc(100% + 14px);padding-bottom:0}'
'.rv-navbar__has-drop::after{content:"";position:absolute;left:0;right:0;bottom:100%;height:18px}'
# Grid panel
'.rv-mega .rv-mega__inner{background:rgba(16,16,18,0.97);-webkit-backdrop-filter:blur(24px);backdrop-filter:blur(24px);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:12px;box-shadow:0 18px 48px rgba(0,0,0,.55);display:grid;grid-template-columns:1fr 1fr;gap:4px}'
# Card
'.rv-mega__card{display:flex;align-items:center;gap:12px;padding:10px;border-radius:12px;text-decoration:none;transition:background .18s ease;background:transparent}'
'.rv-mega__card:hover{background:rgba(255,255,255,.07)}'
'.rv-mega__card::before{display:none!important}'  # kill old dot bullet
'.rv-mega__thumb{width:46px;height:46px;border-radius:10px;overflow:hidden;flex-shrink:0;background:rgba(255,255,255,.05);display:flex;align-items:center;justify-content:center}'
'.rv-mega__thumb img{width:100%;height:100%;object-fit:cover;display:block}'
'.rv-mega__thumb--all{background:linear-gradient(135deg,#5a85ff,#1e50d8)}'
'.rv-mega__txt{display:flex;flex-direction:column;gap:3px;min-width:0}'
'.rv-mega__t{font-family:var(--font-primary);font-size:13px;font-weight:600;color:#fff;line-height:1.2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
'.rv-mega__s{font-family:var(--font-primary);font-size:11px;font-weight:500;color:rgba(255,255,255,.55);line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}'
'@media(max-width:767px){.rv-navbar__drop.rv-mega{display:none}}'
'</style>'
)

def migrate(path):
    p = pathlib.Path(path)
    s = p.read_text()
    changed = False
    # Inject CSS once
    if MARKER not in s and '</head>' in s:
        s = s.replace('</head>', CSS + '</head>', 1)
        changed = True
    # Swap markup (check for unique markup-only token, not CSS class names)
    if 'class="rv-mega__card"' not in s:
        new = OLD_DROP_RE.sub(NEW_DROP, s, count=1)
        if new != s:
            s = new
            changed = True
        else:
            return f'{path}: SKIP (could not find old dropdown to replace)'
    if not changed:
        return f'{path}: already up-to-date'
    p.write_text(s)
    return f'{path}: mega menu applied'

if __name__ == '__main__':
    for f in (sys.argv[1:] or PAGES):
        print(migrate(f))
