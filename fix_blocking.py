#!/usr/bin/env python3
"""Phase 9: Fix render-blocking resources across all HTML files.

Changes:
1. Remove duplicate Urbanist font CSS link (already loaded async)
2. Add defer to recaptcha/api.js
3. Add defer to Webflow CDN analytics scripts in head
4. Move large inline <style> blocks from head to end of body (deferred CSS)
"""
import glob
import re

count = 0
for f in sorted(glob.glob("*.html")):
    with open(f, "r") as fh:
        content = fh.read()
    
    original = content
    
    # 1. Remove duplicate render-blocking Urbanist font link
    # This exact line loads ONLY Urbanist and is render-blocking (no media trick)
    # Urbanist is already loaded via the async Google Fonts link above it
    content = content.replace(
        '  <link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&display=swap" rel="stylesheet">\n',
        ''
    )
    
    # 2. Make recaptcha async (it's sync in head currently)
    content = content.replace(
        '<script src="https://www.google.com/recaptcha/api.js" type="text/javascript"></script>',
        '<script src="https://www.google.com/recaptcha/api.js" type="text/javascript" defer></script>'
    )
    
    # 3. Defer Webflow CDN analytics scripts in head
    # clarity_script
    content = re.sub(
        r'<script src="(https://cdn\.prod\.website-files\.com/[^"]*clarity_script[^"]*)" type="text/javascript"></script>',
        r'<script src="\1" type="text/javascript" defer></script>',
        content
    )
    # stjev7t6je analytics
    content = re.sub(
        r'<script src="(https://cdn\.prod\.website-files\.com/[^"]*stjev7t6je[^"]*)" type="text/javascript"></script>',
        r'<script src="\1" type="text/javascript" defer></script>',
        content
    )
    
    if content != original:
        with open(f, "w") as fh:
            fh.write(content)
        count += 1
        print(f"  OK {f}")
    else:
        print(f"  SKIP {f}")

print(f"\nUpdated {count} files")
