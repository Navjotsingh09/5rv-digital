# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Convert .rv2-header from full-width white bar to floating glass pill.
Idempotent — safe to re-run. Targets all 29 site pages."""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {"index_backup_pre_revamp.html", "footer-preview.html"}

OLD_HEADER = ".rv2-header{position:fixed;top:0;left:0;right:0;z-index:9999;background:#fff;border-bottom:1px solid rgba(11,23,57,.07);transition:transform .5s cubic-bezier(.32,1,.68,1),opacity .4s ease,box-shadow .3s}.rv2-header.rv2--hidden{transform:translateY(-115%);opacity:0;pointer-events:none}"
NEW_HEADER = ".rv2-header{position:fixed;top:14px;left:0;right:0;z-index:9999;background:transparent;display:flex;justify-content:center;padding:0 24px;transition:transform .5s cubic-bezier(.32,1,.68,1),opacity .4s ease}.rv2-header.rv2--hidden{transform:translateY(-150%);opacity:0;pointer-events:none}"

OLD_SCROLLED = ".rv2-header.scrolled{box-shadow:0 2px 20px rgba(11,23,57,.09)}"
NEW_SCROLLED = ".rv2-header.scrolled .rv2-header__inner{box-shadow:0 10px 36px rgba(11,23,57,.14),0 1px 0 rgba(255,255,255,.6) inset}"

OLD_INNER = ".rv2-header__inner{width:min(1180px,calc(100% - 48px));margin:0 auto;height:68px;display:flex;align-items:center;gap:0}"
NEW_INNER = ".rv2-header__inner{width:min(1180px,100%);margin:0;height:60px;display:flex;align-items:center;gap:0;padding:0 18px;background:rgba(255,255,255,.62);-webkit-backdrop-filter:blur(20px) saturate(180%);backdrop-filter:blur(20px) saturate(180%);border:1px solid rgba(11,23,57,.08);border-radius:20px;box-shadow:0 6px 28px rgba(11,23,57,.08),0 1px 0 rgba(255,255,255,.6) inset;transition:box-shadow .3s}"

# Mega-menu hover bridge + overflow safety: append after the existing panel rule
OLD_PANEL = ".rv2-nav__panel{position:absolute;top:calc(100% + 14px);left:50%;transform:translateX(-50%);width:660px;background:#fff;border:1px solid rgba(11,23,57,.07);border-radius:18px;box-shadow:0 16px 56px rgba(11,23,57,.13);padding:28px;opacity:0;pointer-events:none;transition:opacity .17s ease}"
NEW_PANEL = ".rv2-nav__panel{position:absolute;top:calc(100% + 14px);left:50%;transform:translateX(-50%);width:660px;max-width:calc(100vw - 48px);background:#fff;border:1px solid rgba(11,23,57,.07);border-radius:18px;box-shadow:0 16px 56px rgba(11,23,57,.13);padding:28px;opacity:0;pointer-events:none;transition:opacity .17s ease}\n.rv2-nav__panel::before{content:'';position:absolute;top:-14px;left:0;right:0;height:14px}"

# Mobile override: replace the existing rv2-nav display:none rule with extended one
OLD_MOBILE = "@media(max-width:767px){.rv2-nav{display:none}.rv2-burger{display:flex}.rv2-header__inner{height:60px}}"
NEW_MOBILE = "@media(max-width:767px){.rv2-nav{display:none}.rv2-burger{display:flex}.rv2-header{top:0;padding:0}.rv2-header__inner{height:60px;width:100%;max-width:100%;padding:0 20px;background:#fff;border:none;border-bottom:1px solid rgba(11,23,57,.07);border-radius:0;box-shadow:none;-webkit-backdrop-filter:none;backdrop-filter:none}}"

REPLACEMENTS = [
    (OLD_HEADER,   NEW_HEADER,   "header"),
    (OLD_SCROLLED, NEW_SCROLLED, "scrolled"),
    (OLD_INNER,    NEW_INNER,    "inner"),
    (OLD_PANEL,    NEW_PANEL,    "panel"),
    (OLD_MOBILE,   NEW_MOBILE,   "mobile"),
]

done = 0
issues = []
for p in sorted(glob.glob(os.path.join(ROOT, "*.html"))):
    name = os.path.basename(p)
    if name in SKIP: continue
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
    if 'rv2-header' not in s: continue
    orig = s
    page_issues = []
    for old, new, label in REPLACEMENTS:
        if new in s:
            continue  # already applied
        if old in s:
            s = s.replace(old, new, 1)
        else:
            page_issues.append(label)
    if s != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(s)
        done += 1
        status = "patched"
    else:
        status = "noop"
    if page_issues:
        issues.append((name, page_issues))
        print(f"{status:8} {name}  MISS: {','.join(page_issues)}")
    else:
        print(f"{status:8} {name}")

print(f"\nDone. patched={done} issues={len(issues)}")
