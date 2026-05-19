#!/usr/bin/env python3
"""Restore the rv2-header base properties that were stripped by _inject_dock.py.
Idempotent."""
import os, glob, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {"index_backup_pre_revamp.html", "footer-preview.html"}

BROKEN = ".rv2-header{transition:transform .5s cubic-bezier(.32,1,.68,1),opacity .4s ease,box-shadow .3s}.rv2-header.rv2--hidden{transform:translateY(-115%);opacity:0;pointer-events:none}"
FIXED  = ".rv2-header{position:fixed;top:0;left:0;right:0;z-index:9999;background:#fff;border-bottom:1px solid rgba(11,23,57,.07);transition:transform .5s cubic-bezier(.32,1,.68,1),opacity .4s ease,box-shadow .3s}.rv2-header.rv2--hidden{transform:translateY(-115%);opacity:0;pointer-events:none}"

# detail_post.html got a separate <style> block injection
BROKEN_STYLE = "<style>.rv2-header{transition:transform .5s cubic-bezier(.32,1,.68,1),opacity .4s ease,box-shadow .3s}.rv2-header.rv2--hidden{transform:translateY(-115%);opacity:0;pointer-events:none}</style>"
FIXED_STYLE  = "<style>" + FIXED + "</style>"

done = 0
for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    name = os.path.basename(p)
    if name in SKIP: 
        continue
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    orig = s
    if BROKEN in s:
        s = s.replace(BROKEN, FIXED)
    if BROKEN_STYLE in s:
        s = s.replace(BROKEN_STYLE, FIXED_STYLE)
    if s != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(s)
        print("fixed", name); done += 1
    elif FIXED in s or FIXED_STYLE in s:
        print("ok   ", name)
    else:
        print("?    ", name)
print("done:", done)
