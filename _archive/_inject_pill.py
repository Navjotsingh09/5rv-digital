# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Inject floating Book-a-Call pill + scroll JS (no second nav, no top-nav hiding).
Idempotent via marker. Injects after first </header> on all 11 pages."""
import pathlib, sys

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

MARKER = '<!-- rv-pill-canonical -->'

PILL_HTML = (
'\n<!-- rv-pill-canonical -->\n'
'<button class="rv-book-pill" id="rvBookPill" data-cal-namespace="30min" data-cal-link="navjot-singh-gfjevp/30min" data-cal-config=\'{"layout":"month_view"}\' aria-label="Book a 30 minute free call with 5RV Digital" style="cursor:pointer;border:none;">'
'<div class="rv-book-pill__avatar">'
'<img src="images/logo-dark.png" alt="" width="44" height="44">'
'<span class="rv-book-pill__dot"></span>'
'</div>'
'<div class="rv-book-pill__text">'
'<span class="rv-book-pill__main">Book a 30 Min Free Call</span>'
'<span class="rv-book-pill__sub">Schedule Now</span>'
'</div>'
'<div class="rv-book-pill__arrow">'
'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>'
'</div>'
'</button>'
'<script id="rv-pill-scroll-js">(function(){'
'var pill=document.getElementById("rvBookPill");'
'if(!pill)return;'
'function apply(){pill.classList.toggle("rv-pill--visible",window.scrollY>=80);}'
'window.addEventListener("scroll",apply,{passive:true});'
'apply();'
'})();</script>\n'
)

def inject_before_last_body(html, snippet):
    parts = html.rsplit('</body>', 1)
    return parts[0] + snippet + '</body>' + parts[1]

def migrate(path):
    p = pathlib.Path(path)
    s = p.read_text()
    if MARKER in s:
        return f'{path}: already up-to-date'
    if '</body>' not in s:
        return f'{path}: SKIP no </body>'
    s = inject_before_last_body(s, PILL_HTML)
    p.write_text(s)
    return f'{path}: pill injected'

if __name__ == '__main__':
    for f in (sys.argv[1:] or PAGES):
        print(migrate(f))
