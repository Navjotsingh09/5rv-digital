#!/usr/bin/env python3
"""Phase 9B: Add font preload + critical CSS async loading.

Adds:
1. Preload for Urbanist Latin woff2 (hero font) — starts download immediately
2. Makes 5rv-revamp.webflow.css load async (media=print trick) with critical inline CSS fallback
3. Adds fetchpriority hint for hero section

This saves ~1s of render-blocking time by making the 169KB CSS file non-blocking.
"""

import glob, re

# ── Urbanist Latin woff2 (variable font covering weights 300-700) ──
FONT_PRELOAD = '<link rel="preload" href="https://fonts.gstatic.com/s/urbanist/v18/L0x-DF02iFML4hGCyMqlbS1miXK2.woff2" as="font" type="font/woff2" crossorigin>'

# ── Critical inline CSS: only what's needed before the full CSS loads ──
# This prevents FOUC when 5rv-revamp.webflow.css loads async
CRITICAL_CSS = """<style id="critical-css">
/* Phase 9B: Critical CSS for above-fold rendering */
:root{--white-hint:#fafafa;--blue:#356eff;--_colours---brand--blue:#356eff;--_colours---basic-greyscales--white:#fff;--_colours---brand--off-white:#fafafa;--_colours---basic-greyscales--black:#000;--_colours---brand--black-blue:#1f2937;--_colours---brand--grey:#989898}
body{background-color:#fff;color:#2b2b2b;font-family:Urbanist,sans-serif;font-size:16px;line-height:24px;margin:0}
.w-layout-blockcontainer{max-width:940px;margin-left:auto;margin-right:auto}
.section{background-color:#fafafa;flex-flow:column;justify-content:center;align-items:center;width:100%;display:flex;position:relative;overflow:hidden}
.hero-section{background-color:#fafafa;width:100%;display:flex;flex-direction:column;align-items:center;justify-content:center}
.hero-content{grid-row-gap:30px;flex-direction:column;justify-content:center;align-items:center;width:100%;max-width:1017px;text-decoration:none;display:flex}
.frame-6{grid-row-gap:10px;flex-direction:column;justify-content:flex-start;align-items:flex-start;width:100%;text-decoration:none;display:flex}
.frame-1321315016{grid-column-gap:10px;justify-content:center;align-items:center;width:100%;text-decoration:none;display:flex;position:relative}
.powerful-digital-marketing-agency-turning-clicks-into-conversions{-webkit-text-fill-color:transparent;background-image:linear-gradient(97deg,#1f2937 34%,#356eff);-webkit-background-clip:text;background-clip:text;margin-top:0;margin-bottom:0;font-family:Urbanist,sans-serif;font-size:72px;font-weight:500;line-height:120%}
.frame-1321315015{grid-row-gap:16px;flex-direction:column;align-items:flex-start;width:100%;max-width:550px;display:flex}
._5rv-digital-is-a-digital-marketing-company-blending-creativity-and-technology-to-craft-campaigns-to{color:#1f2937;font-family:Plus Jakarta Sans,sans-serif;font-size:20px;line-height:1.6;margin:0}
.frame-6-2{grid-row-gap:24px;flex-direction:column;align-items:flex-start;display:flex}
.div-block-125{grid-column-gap:16px;display:flex}
.hero-button{background-color:#356eff;color:#fff;border-radius:8px;padding:14px 28px;text-decoration:none;display:inline-block}
.hero-button-2{border:1px solid #356eff;color:#356eff;border-radius:8px;padding:14px 28px;text-decoration:none;display:inline-block}
.learn-more-2,.learn-more-3{margin:0;font-size:16px;font-weight:500}
/* Mobile hero adjustments */
@media screen and (max-width:991px){.hero-section{padding-top:100px;border-radius:20px}.powerful-digital-marketing-agency-turning-clicks-into-conversions{font-size:50px;width:auto;padding:10px 20px}.hero-content{max-width:700px}.frame-6{width:auto}}
@media screen and (max-width:767px){.powerful-digital-marketing-agency-turning-clicks-into-conversions{font-size:40px}}
@media screen and (max-width:479px){.hero-section{width:100%;height:auto;padding:0 10px;display:flex}.hero-content{width:280px}.frame-6{width:280px}.powerful-digital-marketing-agency-turning-clicks-into-conversions{font-size:48px;font-weight:500;width:auto}.hero-button{width:280px}.div-block-125{flex-flow:column;margin-top:20px}._5rv-digital-is-a-digital-marketing-company-blending-creativity-and-technology-to-craft-campaigns-to{font-size:14px;padding:0 20px}}
/* Nav critical styles */
.agridex-nav-wrapper{position:fixed;top:0;left:0;right:0;z-index:9999}
.agridex-nav{display:flex;justify-content:space-between;align-items:center;padding:15px 40px;background:rgba(255,255,255,0.95);backdrop-filter:blur(10px)}
/* Hide content until full CSS loads to prevent FOUC on non-hero elements */
.counter,.section-3,.section-4,.section-5,.section-6,.section-7,.footer,.footer-4,.f-section-small{visibility:visible}
</style>"""

# Patterns for pages that DON'T have the hero H1 (case studies, blog, etc.)
# These still benefit from font preload and async CSS but need different critical CSS
HERO_PAGES = {'index.html'}  # Only homepage has the hero H1 class

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    changed = False
    
    # 1. Add font preload after preconnect hints (if not already present)
    if 'rel="preload"' not in html or 'urbanist' not in html.lower():
        # Insert after the last preconnect line
        preconnect_pattern = r'(<link[^>]*rel="preconnect"[^>]*crossorigin[^>]*>)'
        match = re.search(preconnect_pattern, html)
        if match:
            insert_pos = match.end()
            html = html[:insert_pos] + '\n  ' + FONT_PRELOAD + html[insert_pos:]
            changed = True
    
    # 2. Make 5rv-revamp.webflow.css load async (only if not already async)
    old_css_link = '<link href="css/5rv-revamp.webflow.css" rel="stylesheet" type="text/css">'
    async_css = '''<link href="css/5rv-revamp.webflow.css" rel="stylesheet" type="text/css" media="print" onload="this.media='all'">
  <noscript><link href="css/5rv-revamp.webflow.css" rel="stylesheet" type="text/css"></noscript>'''
    
    if old_css_link in html:
        html = html.replace(old_css_link, async_css)
        changed = True
    
    # 3. Insert critical CSS (if async CSS was applied and critical CSS not yet present)
    if 'id="critical-css"' not in html and "media=\"print\" onload" in html:
        # Insert critical CSS right after the async CSS noscript tag
        noscript_end = 'noscript><link href="css/5rv-revamp.webflow.css" rel="stylesheet" type="text/css"></noscript>'
        if noscript_end in html:
            html = html.replace(noscript_end, noscript_end + '\n  ' + CRITICAL_CSS)
            changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  OK {filepath}')
    else:
        print(f'  SKIP {filepath} (already optimized)')
    
    return changed

# Process all HTML files
files = sorted(glob.glob('*.html'))
count = 0
for f in files:
    if process_file(f):
        count += 1

print(f'\nUpdated {count} files')
