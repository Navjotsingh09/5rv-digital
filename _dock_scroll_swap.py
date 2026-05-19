#!/usr/bin/env python3
"""Add scroll-driven swap: top header <-> bottom dock+book-pill.
- Strip baked-in 'rv-dock--visible' and 'rv-pill--visible' classes added previously
- Inject canonical CSS rule that hides .rv2-header when body.rv-scrolled
- Inject canonical JS that toggles body.rv-scrolled + adds .rv-dock--visible / .rv-pill--visible at scrollY >= 80
Idempotent."""
import re, sys, pathlib

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

CSS_MARKER = '/* rv-scroll-swap-css */'
JS_MARKER  = 'rv-scroll-swap-js'

CSS = ('<style id="rv-scroll-swap-css">' + CSS_MARKER + ' '
       'body.rv-scrolled .rv2-header{opacity:0;pointer-events:none;transform:translateY(-12px);transition:opacity .35s ease,transform .4s ease}'
       '.rv2-header{transition:opacity .35s ease,transform .4s ease}'
       '</style>')

JS = ('<script id="' + JS_MARKER + '">'
      '(function(){'
      'var THRESH=80;'
      'var nav=document.querySelector(".rv-navbar");'
      'var pill=document.querySelector(".rv-book-pill");'
      'function apply(){'
      'var scrolled=window.scrollY>THRESH;'
      'document.body.classList.toggle("rv-scrolled",scrolled);'
      'if(nav)nav.classList.toggle("rv-dock--visible",scrolled);'
      'if(pill)pill.classList.toggle("rv-pill--visible",scrolled);'
      '}'
      'window.addEventListener("scroll",apply,{passive:true});'
      'window.addEventListener("resize",apply);'
      'apply();'
      '})();'
      '</script>')

def migrate(path):
    p = pathlib.Path(path)
    s = p.read_text()
    changed = False
    # Strip the baked-in always-visible classes from the canonical dock markup
    s2 = s.replace('<nav class="rv-navbar rv-dock--visible"', '<nav class="rv-navbar"')
    s2 = s2.replace('<button class="rv-book-pill rv-pill--visible"', '<button class="rv-book-pill"')
    if s2 != s:
        changed = True
        s = s2
    # Inject CSS in <head> if missing
    if CSS_MARKER not in s and '</head>' in s:
        s = s.replace('</head>', CSS + '</head>', 1)
        changed = True
    # Inject JS before LAST </body> if missing
    if JS_MARKER not in s and '</body>' in s:
        parts = s.rsplit('</body>', 1)
        s = parts[0] + JS + '</body>' + parts[1]
        changed = True
    if not changed:
        return f'{path}: already up-to-date'
    p.write_text(s)
    return f'{path}: scroll-swap applied'

if __name__ == '__main__':
    for f in (sys.argv[1:] or PAGES):
        print(migrate(f))
