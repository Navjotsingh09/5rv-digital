# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Nav + footer fixes:
1. Reset :visited link colours so visited nav/footer links keep their normal colour.
2. Add `active` class to the matching nav item per page.

Idempotent. Marker: rv-nav-visited-v1.
"""
import os, re

MARK = 'rv-nav-visited-v1'

CSS = '''<style id="rv-nav-visited-v1">
/* Defeat the browser default purple :visited colour for in-app links */
.rv2-nav__link,.rv2-nav__link:visited{color:#0B1739}
.rv2-nav__link.active,.rv2-nav__link.active:visited{color:#356EFF;font-weight:600}
.rv-footer__col a:visited{color:#4b5563}
.rv-footer__contact a:visited{color:#374151}
.rv-footer__brand a:visited{color:inherit}
</style>
'''

# Page → nav label whose link should be marked .active
PAGE_TO_LABEL = {
    'about.html': 'About',
    'work.html': 'Work',
    'blog.html': 'Blog',
    'detail_post.html': 'Blog',
    'contact.html': 'Contact',
    # services hub + service detail pages → Services (button)
    'services.html': 'Services',
    'web-development.html': 'Services',
    'seo-expert.html': 'Services',
    'branding.html': 'Services',
    'social-media-marketing-agency.html': 'Services',
    'digital-marketing-strategies.html': 'Services',
    # case studies → Work
    'qcom-ltd.html': 'Work',
    'klassic-trade-frames.html': 'Work',
    'hilstonpark.html': 'Work',
    'halle-properties.html': 'Work',
    'halesowen-dental.html': 'Work',
    'lightologist.html': 'Work',
    'contello.html': 'Work',
    'bt-sports.html': 'Work',
    'iv-land.html': 'Work',
    'voip-experts.html': 'Work',
    'w13.html': 'Work',
    'pass-11-plus.html': 'Work',
    'university-of-birmingham.html': 'Work',
    'national-health-services.html': 'Work',
    'detail_api-test-properties.html': 'Work',
}

A_PATTERNS = {
    'About':   re.compile(r'(<a[^>]*\brv2-nav__link\b[^>]*>)(\s*About\s*)(</a>)'),
    'Work':    re.compile(r'(<a[^>]*\brv2-nav__link\b[^>]*>)(\s*Work\s*)(</a>)'),
    'Blog':    re.compile(r'(<a[^>]*\brv2-nav__link\b[^>]*>)(\s*Blog\s*)(</a>)'),
    'Contact': re.compile(r'(<a[^>]*\brv2-nav__link\b[^>]*>)(\s*Contact\s*)(</a>)'),
    # Services is a <button>
    'Services': re.compile(r'(<button[^>]*\brv2-nav__link\b[^>]*>)(\s*Services\b)'),
}

def add_active(s, label):
    pat = A_PATTERNS.get(label)
    if not pat: return s, 0
    def rep(m):
        tag = m.group(1)
        if 'active' in tag:
            return m.group(0)
        # insert "active" into class attribute
        new_tag = re.sub(r'class="([^"]*)"', lambda mm: 'class="'+mm.group(1)+' active"', tag, count=1)
        return new_tag + m.group(2) + (m.group(3) if pat.groups>=3 else '')
    return pat.subn(rep, s, count=1)[::-1] if False else (pat.sub(rep, s, count=1), 1)

def migrate(path):
    s = open(path).read()
    if MARK in s:
        return f'{path}: skip (already migrated)'
    if 'rv2-nav__link' not in s:
        return f'{path}: skip (no rv2 nav)'
    if '</head>' not in s:
        return f'{path}: SKIP no head'
    s = s.replace('</head>', CSS + '</head>', 1)
    label = PAGE_TO_LABEL.get(path)
    note = ''
    if label:
        s, n = add_active(s, label)
        note = f' active={label}({n})'
    open(path,'w').write(s)
    return f'{path}: OK{note}'

if __name__ == '__main__':
    files = sorted(f for f in os.listdir('.') if f.endswith('.html') and f not in ('index_backup_pre_revamp.html','footer-preview.html'))
    for f in files:
        print(migrate(f))
