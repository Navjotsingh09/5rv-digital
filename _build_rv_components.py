#!/usr/bin/env python3

# --- pre-flight git check ---
import subprocess, sys as _sys
_res = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
if _res.stdout.strip():
    print("ABORT: Uncommitted changes detected. Commit or stash before running this script.")
    _sys.exit(1)
del _res
# --- end pre-flight ---

"""
_build_rv_components.py
=======================
Phase 1: Extract all id'd <style> blocks (except critical-css) from every HTML
page into a single css/rv-components.css file.

Phase 2: Add <link> to rv-components.css in every page's <head>.

Phase 3: Remove the now-redundant inline <style id="..."> blocks from every page
         (critical-css is preserved in-place).

Phase 4: Fix Inter font references → Urbanist/Plus Jakarta Sans in the
         extracted CSS.

Phase 5: Append new utility styles:
         - @media prefers-reduced-motion block for all rv- animations
         - :focus-visible styles for rv- interactive components
         - .rv-btn--primary and .rv-btn--ghost utility classes
         - .sr-only utility class
"""
import glob, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
CSS_OUT = os.path.join(BASE, 'css', 'rv-components.css')

KEEP_INLINE = {'critical-css'}  # These stay in the HTML

# ── 1. Collect canonical CSS for every style ID ─────────────────────────────
pages = sorted(p for p in glob.glob(os.path.join(BASE, '*.html'))
               if not any(x in os.path.basename(p) for x in
                          ['backup', 'preview', '_restore', '.bak',
                           'index_backup', 'detail_api']))

canonical = {}   # id → css string
for p in pages:
    with open(p, encoding='utf-8') as f:
        html = f.read()
    for m in re.finditer(r'<style\s+id="([^"]+)">(.*?)</style>', html, re.DOTALL):
        sid, css = m.group(1), m.group(2)
        if sid in KEEP_INLINE:
            continue
        if sid not in canonical:
            canonical[sid] = css
        else:
            # Keep the largest version (most complete)
            if len(css) > len(canonical[sid]):
                canonical[sid] = css

print(f'Collected {len(canonical)} unique style blocks from {len(pages)} pages')

# ── 2. Fix Inter font references ────────────────────────────────────────────
inter_fix = re.compile(r"font-family\s*:\s*'Inter'\s*,\s*'Helvetica Neue'\s*,\s*Arial\s*,\s*sans-serif")
inter_fix2 = re.compile(r"font-family\s*:\s*'Inter'([^;]*);")

fixed_count = 0
for sid in canonical:
    original = canonical[sid]
    css = inter_fix.sub("font-family:'Urbanist','Plus Jakarta Sans',sans-serif", original)
    css = inter_fix2.sub(r"font-family:'Urbanist','Plus Jakarta Sans',sans-serif\1;", css)
    if css != original:
        fixed_count += 1
    canonical[sid] = css

print(f'Fixed Inter font references in {fixed_count} style blocks')

# ── 3. Build rv-components.css ──────────────────────────────────────────────
SECTION_ORDER = [
    # Navigation (top bar)
    'rv2-nav', 'rv2-panel-img-css', 'rv2-panel-bridge-css',
    # Floating navbar
    'rv-nav', 'rv-mega-canonical-css', 'rv-mega-spacing-v2',
    # Scroll behaviour
    'rv-scroll-swap-css', 'rv-nav-visited-v1',
    # Hero
    'rv-hero-slider-css', 'rv-media-banner-css',
    # Sections / layout
    'rv-sections-v2', 'rv-mobile-responsive', 'rv-reduced-motion-safety',
    'rv-anim-css',
    # Services page
    'rv-services', 'rv-svc-extras-css', 'rv-gs-full-css',
    # Case studies
    'rv-cs-css',
    # FAQ
    'rv-faq-canonical-css',
    # SEO page (page-specific heavy blocks)
    'rv-seo-features-css', 'rv-seo-revamp-css', 'rv-seo-legacy-css',
    'rv-seo-posh-overrides',
    # Branding / web dev / social pages
    'srv-parallax-pill-css',
    # Cookie
    'rv-cookie-override',
    # Dock (kept for any pages still using it)
    'rv-dock-css-restored',
]

lines = []
lines.append('/*')
lines.append(' * rv-components.css')
lines.append(' * Auto-extracted from inline <style id="rv-*"> blocks.')
lines.append(' * Source of truth for all custom rv- components.')
lines.append(' * Generated: ' + __import__('datetime').date.today().isoformat())
lines.append(' */')
lines.append('')

written = set()

def write_block(sid):
    if sid in canonical and sid not in written:
        lines.append(f'/* ── {sid} ──────────────────────────────────────── */')
        lines.append(canonical[sid])
        lines.append('')
        written.add(sid)

# Write in preferred order first
for sid in SECTION_ORDER:
    write_block(sid)

# Then any remaining IDs not in the order list
for sid in sorted(canonical):
    write_block(sid)

# ── 4. Append utility additions ─────────────────────────────────────────────
lines.append("""/* ── Utility: sr-only (visually hidden, screen-reader accessible) ── */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}

/* ── Utility: Button variants ──────────────────────────────────────────── */
.rv-btn--primary{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:#356eff;color:#fff;border:none;border-radius:8px;padding:12px 24px;font-family:'Urbanist','Plus Jakarta Sans',sans-serif;font-size:15px;font-weight:600;line-height:1.2;text-decoration:none;cursor:pointer;transition:background .2s,transform .2s,box-shadow .2s;white-space:nowrap}
.rv-btn--primary:hover{background:#0263e0;transform:translateY(-1px);box-shadow:0 4px 16px rgba(53,110,255,.3)}
.rv-btn--primary:focus-visible{outline:2px solid #356eff;outline-offset:3px}
.rv-btn--ghost{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:transparent;color:#374151;border:1.5px solid rgba(0,0,0,.15);border-radius:8px;padding:11px 24px;font-family:'Urbanist','Plus Jakarta Sans',sans-serif;font-size:15px;font-weight:600;line-height:1.2;text-decoration:none;cursor:pointer;transition:background .2s,border-color .2s;white-space:nowrap}
.rv-btn--ghost:hover{background:#f9fafb;border-color:rgba(0,0,0,.25)}
.rv-btn--ghost:focus-visible{outline:2px solid #356eff;outline-offset:3px}

/* ── Focus-visible: interactive rv- components ─────────────────────────── */
.rv-mega__card:focus-visible,.rv-mega__card:focus{outline:2px solid #356eff;outline-offset:2px;border-radius:12px}
.rv-faq-item__q:focus-visible,.rv-faq-item__q:focus{outline:2px solid #356eff;outline-offset:2px;border-radius:4px}
.rv-navbar__logo:focus-visible,.rv-navbar__logo:focus{outline:2px solid #356eff;outline-offset:3px;border-radius:4px}

/* ── prefers-reduced-motion: disable all rv- animations ────────────────── */
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
  .rv-hero__marquee-track{animation:none!important}
  .rv-hero__blob--1,.rv-hero__blob--2,.rv-hero__blob--3{animation:none!important}
  .rv-hero__badge-dot,.rv-hero__dash-live-dot{animation:none!important;box-shadow:0 0 0 3px rgba(53,110,255,.18)}
  .rv-h1-cursor{animation:none!important;opacity:1}
  .rv-hero__chip--roas,.rv-hero__chip--clients{animation:none!important}
}
""")

out_css = '\n'.join(lines)
with open(CSS_OUT, 'w', encoding='utf-8') as f:
    f.write(out_css)
print(f'Written: css/rv-components.css ({len(out_css)//1024}KB, {out_css.count(chr(10))} lines)')
print(f'Style blocks included: {len(written)}')
