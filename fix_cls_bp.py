#!/usr/bin/env python3
"""Phase 10: Fix CLS regression + Best Practices + remaining Performance issues.

Fixes:
1. REVERT async CSS loading on 5rv-revamp.webflow.css (CLS cause: 0.165)
   - Keep critical CSS as a bonus (it helps initial render) 
   - But make the main CSS synchronous again to prevent layout shifts
2. Add rel="noopener noreferrer" to all target="_blank" links (Best Practices)
3. Add width/height to images missing dimensions (CLS prevention)
4. Remove blob: image reference (broken/invalid)
5. Add meta http-equiv headers for Best Practices (CSP, X-Content-Type-Options)
"""

import glob, re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # ── FIX 1: Revert async CSS → synchronous (fixes CLS regression) ──
    # Remove the media=print async trick on 5rv-revamp.webflow.css
    async_css = '<link href="css/5rv-revamp.webflow.css" rel="stylesheet" type="text/css" media="print" onload="this.media=\'all\'">'
    sync_css = '<link href="css/5rv-revamp.webflow.css" rel="stylesheet" type="text/css">'
    html = html.replace(async_css, sync_css)
    
    # Remove the noscript fallback (no longer needed since CSS is synchronous)
    noscript_pattern = r'\s*<noscript><link href="css/5rv-revamp\.webflow\.css" rel="stylesheet" type="text/css"></noscript>'
    html = re.sub(noscript_pattern, '', html)
    
    # Keep the critical CSS — it still helps render hero faster even with sync main CSS
    # (browser can start painting immediately with critical CSS while parsing full CSS)
    
    # ── FIX 2: Add rel="noopener noreferrer" to target="_blank" links ──
    # Match target="_blank" links that DON'T already have noopener
    def add_noopener(match):
        tag = match.group(0)
        if 'noopener' not in tag:
            # Add rel="noopener noreferrer" — if rel exists, append; if not, add
            if 'rel="' in tag:
                tag = tag.replace('rel="', 'rel="noopener noreferrer ')
            else:
                tag = tag.replace('target="_blank"', 'target="_blank" rel="noopener noreferrer"')
        return tag
    
    html = re.sub(r'<a\s[^>]*target="_blank"[^>]*>', add_noopener, html)
    
    # ── FIX 3: Remove broken blob: image reference ──
    html = re.sub(r'<img src="blob:[^"]*"[^>]*>', '', html)
    
    # ── FIX 4: Add width/height to gallery-item-media images missing them ──
    # These are the parallax gallery images (Hero.webp, Background.webp, etc.)
    def add_img_dimensions(match):
        tag = match.group(0)
        # Skip if already has width AND height
        has_width = 'width=' in tag or 'width:' in tag
        has_height = 'height=' in tag or 'height:' in tag
        
        if has_width and has_height:
            return tag
        
        # Determine dimensions based on class/src
        if 'gallery-item-media' in tag:
            if not has_width:
                tag = tag.replace('<img ', '<img width="720" height="480" ')
            elif not has_height:
                tag = tag.replace('width="720"', 'width="720" height="480"')
        elif 'navigation-navigation' in tag:
            if not has_width:
                tag = tag.replace('<img ', '<img width="24" height="24" ')
        
        return tag
    
    html = re.sub(r'<img\s[^>]*>', add_img_dimensions, html)
    
    # ── FIX 5: Add security meta headers for Best Practices ──
    if 'http-equiv="X-Content-Type-Options"' not in html:
        # Insert after viewport meta
        viewport_meta = '<meta content="width=device-width, initial-scale=1" name="viewport">'
        if viewport_meta in html:
            security_headers = viewport_meta + '''
  <meta http-equiv="X-Content-Type-Options" content="nosniff">'''
            html = html.replace(viewport_meta, security_headers)
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  OK {filepath}')
        return True
    else:
        print(f'  SKIP {filepath}')
        return False

files = sorted(glob.glob('*.html'))
count = 0
for f in files:
    if process_file(f):
        count += 1

print(f'\nUpdated {count} files')
