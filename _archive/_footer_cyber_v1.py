# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Footer: add Cyber Essentials badge next to socials + make contact icons visible.
Idempotent. Marker: rv-footer-cyber-v1."""
import os, sys

MARK = 'rv-footer-cyber-v1'

CSS = '''<style id="rv-footer-cyber-v1">
/* contact icons — make legible */
.rv-footer__contact svg{width:17px!important;height:17px!important;fill:#0B1739!important;flex-shrink:0;margin-top:2px}
.rv-footer__contact a:hover svg{fill:#356EFF!important}
/* cyber essentials badge sits next to socials */
.rv-footer__cyber{display:inline-flex;align-items:center;justify-content:center;height:42px;padding:0 14px;border-radius:10px;background:#fff;border:1px solid rgba(11,23,57,.08);box-shadow:0 2px 10px rgba(11,23,57,.06);transition:transform .2s ease,box-shadow .2s ease;text-decoration:none;margin-left:4px}
.rv-footer__cyber:hover{transform:translateY(-2px);box-shadow:0 6px 16px rgba(11,23,57,.12)}
.rv-footer__cyber img{height:22px;width:auto;display:block}
@media(max-width:560px){.rv-footer__cyber{margin-left:0;margin-top:8px}}
</style>
'''

X_OLD = '''        <a href="https://x.com/5rvdigital" target="_blank" rel="noopener noreferrer" aria-label="X (Twitter)">
          <svg viewBox="0 0 24 24"><path d="M4 4l16 16M4 20L20 4"/></svg>
        </a>
      </div>'''

X_NEW = '''        <a href="https://x.com/5rvdigital" target="_blank" rel="noopener noreferrer" aria-label="X (Twitter)">
          <svg viewBox="0 0 24 24"><path d="M4 4l16 16M4 20L20 4"/></svg>
        </a>
        <a class="rv-footer__cyber" href="https://www.qcom.ltd/media/2fkdbggh/cyber-essential-certificate.pdf" target="_blank" rel="noopener noreferrer" aria-label="Cyber Essentials Certified — view certificate (PDF)">
          <img src="images/Cyber-Essentials.svg" alt="Cyber Essentials Certified" loading="lazy">
        </a>
      </div>'''

def migrate(path):
    s = open(path).read()
    if MARK in s:
        return f'{path}: skip (already migrated)'
    if 'rv-footer__social' not in s:
        return f'{path}: skip (no footer)'
    if X_OLD not in s:
        return f'{path}: SKIP — X anchor pattern not found'
    s2 = s.replace(X_OLD, X_NEW, 1)
    # inject CSS before </head>
    if '</head>' not in s2:
        return f'{path}: SKIP — no </head>'
    s2 = s2.replace('</head>', CSS + '</head>', 1)
    open(path,'w').write(s2)
    return f'{path}: OK'

if __name__ == '__main__':
    files = sorted(f for f in os.listdir('.') if f.endswith('.html') and f != 'index_backup_pre_revamp.html' and f != 'footer-preview.html')
    for f in files:
        print(migrate(f))
