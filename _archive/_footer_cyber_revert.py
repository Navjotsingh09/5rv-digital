# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Revert: remove Cyber Essentials badge + all rv-footer-cyber-* style blocks
from every HTML page, restoring the pre-cyber footer state."""
import os, re

STYLE_RE = re.compile(r'<style id="rv-footer-cyber-v\d+">.*?</style>', re.DOTALL)
ANCHOR_RE = re.compile(r'\s*<a class="rv-footer__cyber"[^>]*>.*?</a>', re.DOTALL)

def revert(path):
    s = open(path).read()
    o = s
    s = STYLE_RE.sub('', s)
    s = ANCHOR_RE.sub('', s)
    if s == o:
        return f'{path}: no change'
    open(path,'w').write(s)
    return f'{path}: cleaned'

if __name__ == '__main__':
    for f in sorted(x for x in os.listdir('.') if x.endswith('.html')):
        print(revert(f))
