#!/usr/bin/env python3
"""Replace the 4 'Discover More' parallax CTAs on services.html with a
gradient pill button matching the home hero 'Be Seen' button style."""
import pathlib, re

P = pathlib.Path('services.html')
s = P.read_text()

MARKER = 'srv-parallax-pill-css'
if MARKER in s and 'srv-parallax-pill"' in s:
    print('services.html: already converted')
else:
    # 1. Inject scoped CSS (cloned from rv-hero__pill-btn)
    CSS = (
    '<style id="srv-parallax-pill-css">'
    '.srv-parallax-pill{display:inline-flex;align-items:center;gap:0;background:linear-gradient(135deg,#5a85ff 0%,#356EFF 55%,#1e50d8 100%);color:#fff;font-family:var(--font-primary,Urbanist,sans-serif);font-size:15px;font-weight:600;padding:6px 6px 6px 24px;border-radius:100px;text-decoration:none;transition:filter .2s,transform .2s;overflow:hidden;white-space:nowrap}'
    '.srv-parallax-pill:hover{filter:brightness(1.1);transform:translateY(-2px)}'
    '.srv-parallax-pill__text{position:relative;overflow:hidden;height:22px;display:flex;align-items:center}'
    '.srv-parallax-pill__text span{display:block;line-height:22px;transition:transform .35s cubic-bezier(.32,1.2,.68,1);color:#fff}'
    '.srv-parallax-pill__text span.srv-parallax-pill__clone{position:absolute;left:0;top:0;transform:translateY(100%)}'
    '.srv-parallax-pill:hover .srv-parallax-pill__text span:first-child{transform:translateY(-100%)}'
    '.srv-parallax-pill:hover .srv-parallax-pill__text span.srv-parallax-pill__clone{transform:translateY(0)}'
    '.srv-parallax-pill__circ{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.22);display:grid;place-items:center;margin-left:12px;flex-shrink:0}'
    '.srv-parallax-pill__circ svg{width:16px;height:16px;stroke:#fff;fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;transition:transform .3s cubic-bezier(.32,1.2,.68,1);transform:rotate(-45deg)}'
    '.srv-parallax-pill:hover .srv-parallax-pill__circ svg{transform:rotate(0deg)}'
    '</style>'
    )
    if MARKER not in s:
        s = s.replace('</head>', CSS + '</head>', 1)

    # 2. Swap each <a class="srv-parallax-cta"> ... </a> for the new pill markup
    pattern = re.compile(r'<a href="([^"]+)" class="srv-parallax-cta">\s*Discover More\s*<span class="srv-parallax-cta__circ"><svg[^>]*>.*?</svg></span></a>', re.DOTALL)
    new_html_tpl = (
    '<a href="{href}" class="srv-parallax-pill">'
    '<span class="srv-parallax-pill__text">'
    '<span>Discover More</span>'
    '<span class="srv-parallax-pill__clone">Discover More</span>'
    '</span>'
    '<span class="srv-parallax-pill__circ">'
    '<svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>'
    '</span>'
    '</a>'
    )
    def repl(m): return new_html_tpl.format(href=m.group(1))
    s2, n = pattern.subn(repl, s)
    print(f'services.html: replaced {n} CTA(s)')
    s = s2
    P.write_text(s)
    print('services.html: written')
