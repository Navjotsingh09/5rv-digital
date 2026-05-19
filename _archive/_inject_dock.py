# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Restore bottom dock pill + book-a-call pill across all pages.
Option B: top rv2-header hides on scroll, dock pill takes over.
Idempotent — safe to re-run."""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
SKIP = {"index_backup_pre_revamp.html", "footer-preview.html", "_inject_dock.py"}

CSS_HIDE_RULE = ".rv2-header{transition:transform .5s cubic-bezier(.32,1,.68,1),opacity .4s ease,box-shadow .3s}.rv2-header.rv2--hidden{transform:translateY(-115%);opacity:0;pointer-events:none}"

PILLS_MARKUP = '''
<!-- RV-DOCK-PILLS:START -->
<nav class="rv-navbar" role="navigation" aria-label="Scroll navigation">
  <a href="index.html" class="rv-navbar__logo">
    <img src="images/logo-light.png" alt="5RV Digital" width="44" height="44">
  </a>
  <div class="rv-navbar__sep"></div>
  <div class="rv-navbar__links">
    <a href="about.html">About</a>
    <a href="work.html">Work</a>
    <div class="rv-navbar__has-drop">
      <a href="services.html">Services
        <svg class="rv-drop-caret" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg>
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
    <a href="blog.html">Blog</a>
    <a href="contact.html">Contact</a>
  </div>
</nav>
<button class="rv-book-pill" data-cal-namespace="rv30min" data-cal-link="navjot-singh-gfjevp/rv30min" data-cal-config='{"layout":"month_view"}' aria-label="Book a 30 minute free call with 5RV Digital" style="cursor:pointer;border:none;">
  <div class="rv-book-pill__avatar">
    <img src="images/logo-light.png" alt="" width="44" height="44">
    <span class="rv-book-pill__dot"></span>
  </div>
  <div class="rv-book-pill__text">
    <span class="rv-book-pill__main">Book a 30 Min Free Call</span>
    <span class="rv-book-pill__sub">Schedule Now</span>
  </div>
  <div class="rv-book-pill__arrow">
    <svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg>
  </div>
</button>
<!-- RV-DOCK-PILLS:END -->
'''

PILLS_JS = '''
<!-- RV-DOCK-PILLS-JS:START -->
<script>
(function(){
  if(window.__rvDockPillsInit) return; window.__rvDockPillsInit = true;
  var DESKTOP = function(){ return window.innerWidth >= 768; };
  var hdr     = document.getElementById('rv2Header');
  var navbar  = document.querySelector('.rv-navbar');
  var bookPill= document.querySelector('.rv-book-pill');
  var SHOW_DOCK = 80, SHOW_BOOK = 120;

  function onScroll(){
    var y = window.scrollY;
    if(DESKTOP()){
      if(hdr)      hdr.classList.toggle('rv2--hidden', y > SHOW_DOCK);
      if(navbar)   navbar.classList.toggle('rv-dock--visible', y > SHOW_DOCK);
      if(bookPill) bookPill.classList.toggle('rv-pill--visible', y > SHOW_BOOK);
    } else {
      if(hdr)      hdr.classList.remove('rv2--hidden');
      if(navbar)   navbar.classList.remove('rv-dock--visible');
      if(bookPill) bookPill.classList.remove('rv-pill--visible');
    }
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);
  onScroll();

  /* Auto-mark active dock link by current page */
  var page = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.rv-navbar__links a, .rv-navbar__has-drop > a').forEach(function(a){
    var href = (a.getAttribute('href') || '').split('/').pop();
    if(href && href !== '#' && href === page) a.classList.add('active');
  });
})();
</script>
<!-- RV-DOCK-PILLS-JS:END -->
'''

CSS_MARKER = "rv2--hidden"
MARKUP_MARKER = "RV-DOCK-PILLS:START"
JS_MARKER = "RV-DOCK-PILLS-JS:START"

def process(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
    if 'rv2-header' not in s:
        return None
    changed = False

    # 1) inject CSS hide rule (replace the simple .rv2-header{...} that ends with transition:box-shadow .3s})
    if CSS_MARKER not in s:
        new = re.sub(
            r"\.rv2-header\{position:fixed;top:0;left:0;right:0;z-index:9999;background:#fff;border-bottom:1px solid rgba\(11,23,57,\.07\);transition:box-shadow \.3s\}",
            CSS_HIDE_RULE,
            s, count=1)
        if new != s:
            s = new; changed = True
        else:
            print("  ! could not patch CSS in", path)

    # 2) inject pill markup right after first </header>
    if MARKUP_MARKER not in s:
        new = s.replace("</header>", "</header>\n" + PILLS_MARKUP, 1)
        if new != s:
            s = new; changed = True
        else:
            print("  ! no </header> in", path)

    # 3) inject JS right before </body>
    if JS_MARKER not in s:
        new = s.replace("</body>", PILLS_JS + "\n</body>", 1)
        if new != s:
            s = new; changed = True
        else:
            print("  ! no </body> in", path)

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(s)
        return True
    return False

if __name__ == "__main__":
    pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    done, skipped = 0, 0
    for p in pages:
        name = os.path.basename(p)
        if name in SKIP:
            print("skip", name); skipped += 1; continue
        r = process(p)
        if r is True:
            print("patched", name); done += 1
        elif r is False:
            print("noop  ", name)
        else:
            print("skip  ", name); skipped += 1
    print(f"\nDone. patched={done} skipped={skipped}")
