#!/usr/bin/env python3
"""Inject the full rv2-nav style block into detail_post.html (which lacks it),
and remove the obsolete inline glass-pill <style> patch."""
import re

with open('index.html','r',encoding='utf-8') as f:
    src = f.read()
m = re.search(r'<style id="rv2-nav">.*?</style>', src, re.S)
assert m, "rv2-nav style block missing in index.html"
block = m.group(0)

with open('detail_post.html','r',encoding='utf-8') as f:
    s = f.read()

# Remove the inline glass-pill <style> patch I added earlier
s = re.sub(r'<style>\.rv2-header\{position:fixed;top:14px[^<]*</style>\n?', '', s)

# Inject the full rv2-nav block right before </head>
if 'id="rv2-nav"' not in s:
    s = s.replace('</head>', block + '\n</head>', 1)
    print("injected full rv2-nav block")
else:
    print("already had rv2-nav block")

with open('detail_post.html','w',encoding='utf-8') as f:
    f.write(s)
print("done")
