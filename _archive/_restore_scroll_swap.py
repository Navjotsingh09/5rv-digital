# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Restore full scroll-swap nav system:
  - top .rv2-header hides on scroll (CSS)
  - bottom .rv-navbar dock with mega menu slides in on scroll
  - existing .rv-book-pill becomes part of the same scroll system
Idempotent via markers."""
import re, pathlib, sys

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

DOCK_MARKER  = '<!-- rv-dock-canonical -->'
SWAP_CSS_ID  = 'rv-scroll-swap-css'
SWAP_JS_ID   = 'rv-scroll-swap-js'
OLD_PILL_JS_RE = re.compile(r'<script id="rv-pill-scroll-js">.*?</script>', re.DOTALL)

# Bottom dock with mega menu baked in
DOCK_HTML = (
'\n<!-- rv-dock-canonical -->\n'
'<nav class="rv-navbar" role="navigation" aria-label="Floating navigation">'
'<a href="index.html" class="rv-navbar__logo" aria-label="Home">'
'<img src="images/logo-dark.png" alt="5RV Digital" width="44" height="44">'
'</a>'
'<div class="rv-navbar__sep"></div>'
'<div class="rv-navbar__links">'
'<a href="about.html" data-rv-page="about.html">About</a>'
'<a href="work.html" data-rv-page="work.html">Work</a>'
'<div class="rv-navbar__has-drop">'
'<a href="services.html" data-rv-page="services.html">Services'
'<svg class="rv-drop-caret" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
'</a>'
'<div class="rv-navbar__drop rv-mega"><div class="rv-mega__inner">'
'<a class="rv-mega__card" href="web-development.html"><div class="rv-mega__thumb"><img src="images/Rectangle-6_2.webp" alt="" loading="lazy" width="48" height="48"></div><div class="rv-mega__txt"><div class="rv-mega__t">Web Design &amp; Dev</div><div class="rv-mega__s">Conversion-focused websites</div></div></a>'
'<a class="rv-mega__card" href="seo-expert.html"><div class="rv-mega__thumb"><img src="images/Rectangle-6-5_1.webp" alt="" loading="lazy" width="48" height="48"></div><div class="rv-mega__txt"><div class="rv-mega__t">SEO</div><div class="rv-mega__s">Rank, traffic &amp; growth</div></div></a>'
'<a class="rv-mega__card" href="social-media-marketing-agency.html"><div class="rv-mega__thumb"><img src="images/Rectangle-6_5.webp" alt="" loading="lazy" width="48" height="48"></div><div class="rv-mega__txt"><div class="rv-mega__t">Social Media</div><div class="rv-mega__s">Content that converts</div></div></a>'
'<a class="rv-mega__card" href="branding.html"><div class="rv-mega__thumb"><img src="images/Rectangle-6_4.webp" alt="" loading="lazy" width="48" height="48"></div><div class="rv-mega__txt"><div class="rv-mega__t">Branding</div><div class="rv-mega__s">Identity &amp; positioning</div></div></a>'
'<a class="rv-mega__card" href="digital-marketing-strategies.html"><div class="rv-mega__thumb"><img src="images/Rectangle-6-3.webp" alt="" loading="lazy" width="48" height="48"></div><div class="rv-mega__txt"><div class="rv-mega__t">Paid Ads</div><div class="rv-mega__s">Performance media</div></div></a>'
'<a class="rv-mega__card rv-mega__card--all" href="services.html"><div class="rv-mega__thumb rv-mega__thumb--all"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></div><div class="rv-mega__txt"><div class="rv-mega__t">All Services</div><div class="rv-mega__s">Full overview</div></div></a>'
'</div></div>'
'</div>'
'<a href="blog.html" data-rv-page="blog.html">Blog</a>'
'<a href="contact.html" data-rv-page="contact.html">Contact</a>'
'</div>'
'</nav>\n'
'<script id="rv-dock-active-js">(function(){try{var path=(location.pathname.split("/").pop()||"index.html").toLowerCase();document.querySelectorAll(".rv-navbar [data-rv-page]").forEach(function(a){if(a.dataset.rvPage.toLowerCase()===path)a.classList.add("active");});}catch(e){}})();</script>\n'
)

SWAP_CSS = (
'<style id="rv-scroll-swap-css">'
'body.rv-scrolled .rv2-header{opacity:0;pointer-events:none;transform:translateY(-12px);transition:opacity .35s ease,transform .4s ease}'
'.rv2-header{transition:opacity .35s ease,transform .4s ease}'
'</style>'
)

SWAP_JS = (
'<script id="rv-scroll-swap-js">(function(){'
'var THRESH=80;'
'var nav=document.querySelector(".rv-navbar");'
'var pill=document.querySelector(".rv-book-pill");'
'function apply(){'
'var s=window.scrollY>=THRESH;'
'document.body.classList.toggle("rv-scrolled",s);'
'if(nav)nav.classList.toggle("rv-dock--visible",s);'
'if(pill)pill.classList.toggle("rv-pill--visible",s);'
'}'
'window.addEventListener("scroll",apply,{passive:true});'
'window.addEventListener("resize",apply);'
'apply();'
'})();</script>'
)

def migrate(path):
    p = pathlib.Path(path)
    s = p.read_text()
    orig = s
    # 1) Strip the simple pill-only script (replaced by full swap script)
    s = OLD_PILL_JS_RE.sub('', s)
    # 2) Inject bottom dock after first </header>
    if DOCK_MARKER not in s and '</header>' in s:
        s = s.replace('</header>', '</header>' + DOCK_HTML, 1)
    # 3) Inject swap CSS in head
    if SWAP_CSS_ID not in s and '</head>' in s:
        s = s.replace('</head>', SWAP_CSS + '</head>', 1)
    # 4) Inject swap JS before last </body>
    if SWAP_JS_ID not in s and '</body>' in s:
        parts = s.rsplit('</body>', 1)
        s = parts[0] + SWAP_JS + '</body>' + parts[1]
    if s == orig:
        return f'{path}: already up-to-date'
    p.write_text(s)
    return f'{path}: scroll-swap restored'

if __name__ == '__main__':
    for f in (sys.argv[1:] or PAGES):
        print(migrate(f))
