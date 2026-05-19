# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Inject bottom dock nav + Book-a-Call pill markup on all main pages.
CSS for both already exists in pages. Markup injected after </header>.
Bakes-in visible classes so dock + pill show always (desktop). Idempotent."""
import sys, pathlib

PAGES = [
    'index.html','about.html','services.html','work.html','blog.html','contact.html',
    'branding.html','seo-expert.html','web-development.html',
    'social-media-marketing-agency.html','digital-marketing-strategies.html',
]

MARKER = '<!-- rv-dock-canonical -->'

DOCK = '''
<!-- rv-dock-canonical -->
<nav class="rv-navbar rv-dock--visible" role="navigation" aria-label="Floating navigation">
  <a href="index.html" class="rv-navbar__logo" aria-label="Home">
    <img src="images/logo-dark.png" alt="5RV Digital" width="44" height="44">
  </a>
  <div class="rv-navbar__sep"></div>
  <div class="rv-navbar__links">
    <a href="about.html" data-rv-page="about.html">About</a>
    <a href="work.html" data-rv-page="work.html">Work</a>
    <div class="rv-navbar__has-drop">
      <a href="services.html" data-rv-page="services.html">Services
        <svg class="rv-drop-caret" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
      <div class="rv-navbar__drop">
        <div class="rv-navbar__drop-inner">
          <a href="web-development.html">Web Design &amp; Dev</a>
          <a href="seo-expert.html">SEO</a>
          <a href="social-media-marketing-agency.html">Social Media</a>
          <a href="branding.html">Branding</a>
          <a href="digital-marketing-strategies.html">Paid Ads</a>
        </div>
      </div>
    </div>
    <a href="blog.html" data-rv-page="blog.html">Blog</a>
    <a href="contact.html" data-rv-page="contact.html">Contact</a>
  </div>
</nav>
<button class="rv-book-pill rv-pill--visible" data-cal-namespace="30min" data-cal-link="navjot-singh-gfjevp/30min" data-cal-config='{"layout":"month_view"}' aria-label="Book a 30 minute free call with 5RV Digital" style="cursor:pointer;border:none;">
  <div class="rv-book-pill__avatar">
    <img src="images/logo-dark.png" alt="" width="44" height="44">
    <span class="rv-book-pill__dot"></span>
  </div>
  <div class="rv-book-pill__text">
    <span class="rv-book-pill__main">Book a 30 Min Free Call</span>
    <span class="rv-book-pill__sub">Schedule Now</span>
  </div>
  <div class="rv-book-pill__arrow">
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>
  </div>
</button>
<script id="rv-dock-active-js">
(function(){
  try {
    var path = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    document.querySelectorAll('.rv-navbar [data-rv-page]').forEach(function(a){
      if (a.dataset.rvPage.toLowerCase() === path) a.classList.add('active');
    });
  } catch(e){}
})();
</script>
'''

def migrate(path):
    p = pathlib.Path(path)
    s = p.read_text()
    if MARKER in s:
        return f'{path}: dock already injected (skipped)'
    if '</header>' not in s:
        return f'{path}: SKIP (no </header>)'
    # Inject after the FIRST </header> only
    new = s.replace('</header>', '</header>\n' + DOCK, 1)
    p.write_text(new)
    return f'{path}: dock + book-pill injected'

if __name__ == '__main__':
    targets = sys.argv[1:] or PAGES
    for f in targets:
        print(migrate(f))
