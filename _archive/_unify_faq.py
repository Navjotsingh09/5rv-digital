# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

#!/usr/bin/env python3
"""Unify FAQ sections across pages with the canonical rv-faq-sect markup.
Extracts existing Q&A from each page's "Frequently Asked Questions" section
and rewrites the section with the new markup. Injects shared CSS + JS once.
"""
import re, sys, os, html

PAGES = [
    'branding.html',
    'digital-marketing-strategies.html',
    'seo-expert.html',
    'social-media-marketing-agency.html',
    'web-development.html',
    'index.html',
]

# Canonical CSS block (id="rv-faq-canonical-css") — extracted from services.html
FAQ_CSS = '''<style id="rv-faq-canonical-css">
.rv-faq-sect{padding:80px 24px 100px;border-top:1px solid rgba(0,0,0,.055);background:#fff}
.rv-faq-sect__inner{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 1.2fr;gap:64px;align-items:start}
.rv-faq-sect__left{position:sticky;top:96px}
.rv-faq-sect__tag{display:inline-block;background:rgba(53,110,255,.09);color:#356eff;font-family:Urbanist,sans-serif;font-size:11px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;padding:5px 14px;border-radius:100px;margin-bottom:16px}
.rv-faq-sect__heading{font-family:Urbanist,sans-serif;font-size:44px;font-weight:700;line-height:1.1;color:#1f2937;margin:0 0 16px}
.rv-faq-sect__heading em{font-style:normal;background:linear-gradient(97deg,#1f2937 20%,#356eff);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.rv-faq-sect__sub{font-family:Plus Jakarta Sans,sans-serif;font-size:15px;color:#6b7280;line-height:1.72;margin:0 0 28px}
.rv-faq-sect__cta{display:inline-flex;align-items:center;gap:8px;background:#1f2937;color:#fff!important;-webkit-text-fill-color:#fff!important;font-family:Urbanist,sans-serif;font-size:14px;font-weight:600;padding:12px 26px;border-radius:100px;text-decoration:none!important;transition:background .2s,transform .2s;cursor:pointer;border:none}
.rv-faq-sect__cta:hover{background:#356eff;transform:translateY(-2px)}
.rv-faq-sect__cta:visited{color:#fff!important;-webkit-text-fill-color:#fff!important}
.rv-faq-sect__cta svg{width:15px;height:15px;stroke:#fff;fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.rv-faq-sect__list{display:flex;flex-direction:column;gap:8px}
.rv-faq-item-new{border:1px solid rgba(0,0,0,.08)!important;border-radius:14px!important;background:#f9fafb!important;overflow:hidden!important;margin:0!important;transition:border-color .2s,box-shadow .2s!important}
.rv-faq-item-new:hover{border-color:rgba(53,110,255,.2)!important;box-shadow:0 2px 16px rgba(53,110,255,.07)!important}
.rv-faq-item-new.open{background:#fff!important;border-color:rgba(53,110,255,.24)!important;box-shadow:0 4px 24px rgba(53,110,255,.09)!important}
.rv-faq-item-new .faq-title{display:flex!important;padding:0!important;cursor:pointer;border:none;background:none!important;width:100%}
.rv-faq-item-new .faq-title-wrapper{display:flex!important;align-items:center!important;justify-content:space-between!important;width:100%!important;gap:16px!important;padding:18px 20px!important;white-space:normal!important}
.rv-faq-q{font-family:Urbanist,sans-serif;font-size:15px;font-weight:600;color:#1f2937;line-height:1.4;flex:1;text-align:left}
.rv-faq-item-new.open .rv-faq-q{color:#356eff}
.rv-faq-icon{width:30px;height:30px;border-radius:50%;background:rgba(53,110,255,.08);display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .2s,transform .32s cubic-bezier(.4,0,.2,1)}
.rv-faq-icon svg{width:14px;height:14px;stroke:#356eff;fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;transition:stroke .2s}
.rv-faq-item-new.open .rv-faq-icon{background:#356eff;transform:rotate(45deg)}
.rv-faq-item-new.open .rv-faq-icon svg{stroke:#fff}
.rv-faq-item-new .faq-content{max-height:0;overflow:hidden;transition:max-height .38s cubic-bezier(.4,0,.2,1)}
.rv-faq-item-new .faq-tab{padding:0 20px 18px}
.rv-faq-item-new .faq-tab p{font-family:Plus Jakarta Sans,sans-serif;font-size:14px;color:#6b7280;line-height:1.72;margin:0}
.rv-faq-item-new .faq-tab a{color:#356eff;text-decoration:none}
.rv-faq-item-new .faq-tab a:hover{text-decoration:underline}
.rv-faq-item-new.open .faq-title,.rv-faq-item-new.open .faq-title *{color:inherit!important}
@media(max-width:860px){
  .rv-faq-sect__inner{grid-template-columns:1fr;gap:36px}
  .rv-faq-sect__left{position:static}
  .rv-faq-sect__heading{font-size:34px}
}
@media(max-width:479px){
  .rv-faq-sect{padding:48px 16px 72px}
  .rv-faq-sect__heading{font-size:28px}
}
</style>
'''

# Toggle JS (id="rv-faq-canonical-js")
FAQ_JS = '''<script id="rv-faq-canonical-js">
(function(){
  function init(){
    document.querySelectorAll('.rv-faq-item-new').forEach(function(item){
      if(item.dataset.faqInit) return;
      item.dataset.faqInit='1';
      var title=item.querySelector('.faq-title');
      var content=item.querySelector('.faq-content');
      if(!title||!content) return;
      title.setAttribute('role','button');
      title.setAttribute('tabindex','0');
      function toggle(){
        var isOpen=item.classList.contains('open');
        var siblings=item.parentElement.querySelectorAll('.rv-faq-item-new.open');
        siblings.forEach(function(o){
          if(o!==item){
            o.classList.remove('open');
            var c=o.querySelector('.faq-content'); if(c) c.style.maxHeight='0px';
          }
        });
        if(isOpen){
          item.classList.remove('open');
          content.style.maxHeight='0px';
        } else {
          item.classList.add('open');
          content.style.maxHeight=content.scrollHeight+'px';
        }
      }
      title.addEventListener('click', function(e){ e.preventDefault(); toggle(); });
      title.addEventListener('keydown', function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); } });
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
'''

def find_section_bounds(s, anchor_pos):
    """Find <section ...>...</section> enclosing anchor_pos."""
    sec_start = s.rfind('<section', 0, anchor_pos)
    if sec_start < 0:
        return None, None
    # scan forward, tracking depth
    depth = 1
    i = sec_start + len('<section')
    while i < len(s):
        m = re.search(r'<section\b|</section>', s[i:])
        if not m:
            return None, None
        tag_pos = i + m.start()
        if s[tag_pos:tag_pos+9].startswith('<section'):
            depth += 1
            i = tag_pos + len('<section')
        else:
            depth -= 1
            i = tag_pos + len('</section>')
            if depth == 0:
                return sec_start, i
    return None, None

# Extract Q&A from a block of HTML (legacy `faq w-dropdown` format).
# Question may be in <h2> OR <div>; answer may have multiple <p> tags.
LEGACY_FAQ_RE = re.compile(
    r'<div\s+[^>]*class="faq w-dropdown"[^>]*>(?P<inner>.*?)</nav>\s*</div>',
    re.S
)
Q_RE = re.compile(r'<div class="faq-title-wrapper">\s*<(?:h2|h3|div)[^>]*>(.*?)</(?:h2|h3|div)>', re.S)
TAB_RE = re.compile(r'<div class="faq-tab">(.*?)</div>\s*</nav>', re.S)
P_RE = re.compile(r'<p[^>]*>(.*?)</p>', re.S)

def clean_q(q):
    q = re.sub(r'<br\s*/?>', ' ', q)
    q = re.sub(r'<[^>]+>', '', q)
    q = re.sub(r'\s+', ' ', q).strip()
    # strip leading numbering like "1. " or "1) "
    q = re.sub(r'^\d+[\.\)]\s*', '', q)
    return q

def clean_a_para(p):
    p = re.sub(r'\s*aria-current="page"', '', p)
    p = re.sub(r'\s*class="[^"]*"', '', p)
    p = re.sub(r'<br\s*/?>', '<br>', p)
    return re.sub(r'\s+', ' ', p).strip()

def extract_qa(block):
    qas = []
    for m in LEGACY_FAQ_RE.finditer(block):
        inner = m.group('inner')
        qm = Q_RE.search(inner)
        if not qm: continue
        q = clean_q(qm.group(1))
        # find faq-tab (use a broader search since structure varies)
        tab_match = re.search(r'<div class="faq-tab">(.*?)</div>', inner, re.S)
        if not tab_match: continue
        tab_html = tab_match.group(1)
        paras = [clean_a_para(pm.group(1)) for pm in P_RE.finditer(tab_html)]
        paras = [p for p in paras if p]
        if not paras: continue
        a = ' '.join(paras)
        qas.append((q, a))
    return qas

def build_canonical(qas, talk_url='contact.html'):
    items = []
    for q, a in qas:
        items.append(
            '        <div class="faq rv-faq-item-new">\n'
            '          <div class="faq-title"><div class="faq-title-wrapper">'
            f'<span class="rv-faq-q">{q}</span>'
            '<div class="rv-faq-icon"><svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg></div>'
            '</div></div>\n'
            '          <div class="faq-content"><div class="faq-tab">'
            f'<p>{a}</p>'
            '</div></div>\n'
            '        </div>'
        )
    items_html = '\n'.join(items)
    return (
        '  <section class="rv-faq-sect rv-reveal">\n'
        '    <div class="rv-faq-sect__inner">\n'
        '      <div class="rv-faq-sect__left">\n'
        '        <span class="rv-faq-sect__tag">Got Questions?</span>\n'
        '        <h2 class="rv-faq-sect__heading">Frequently<br><em>Asked Questions</em></h2>\n'
        '        <p class="rv-faq-sect__sub">Can\'t find what you\'re looking for? We\'re happy to help — get in touch and we\'ll guide you through.</p>\n'
        f'        <a href="{talk_url}" class="rv-faq-sect__cta">Talk to Us<svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></a>\n'
        '      </div>\n'
        '      <div class="rv-faq-sect__list">\n'
        f'{items_html}\n'
        '      </div>\n'
        '    </div>\n'
        '  </section>'
    )

def inject_assets(s):
    if 'id="rv-faq-canonical-css"' not in s:
        s = s.replace('</head>', FAQ_CSS + '</head>', 1)
    if 'id="rv-faq-canonical-js"' not in s:
        s = s.replace('</body>', FAQ_JS + '</body>', 1)
    return s

RV_FAQ_ITEM_RE = re.compile(
    r'<div class="rv-faq-item">\s*'
    r'<div class="rv-faq-item__q">\s*<h3[^>]*>(?P<q>.*?)</h3>.*?'
    r'<div class="rv-faq-item__a-inner">\s*<p[^>]*>(?P<a>.*?)</p>',
    re.S
)

def extract_qa(block):
    qas = []
    for m in LEGACY_FAQ_RE.finditer(block):
        inner = m.group('inner')
        qm = Q_RE.search(inner)
        if not qm: continue
        q = clean_q(qm.group(1))
        tab_match = re.search(r'<div class="faq-tab">(.*?)</div>', inner, re.S)
        if not tab_match: continue
        tab_html = tab_match.group(1)
        paras = [clean_a_para(pm.group(1)) for pm in P_RE.finditer(tab_html)]
        paras = [p for p in paras if p]
        if not paras: continue
        a = ' '.join(paras)
        qas.append((q, a))
    # also try rv-faq-item format (used on index.html)
    if not qas:
        for m in RV_FAQ_ITEM_RE.finditer(block):
            q = clean_q(m.group('q'))
            a = clean_a_para(m.group('a'))
            if q and a:
                qas.append((q, a))
    return qas

def process(p):
    s = open(p).read()
    # Match "Frequently" followed by anything then "Asked" within ~80 chars (handles inline tags)
    m = re.search(r'Frequently[\s\S]{0,80}?Asked', s, re.I)
    if not m:
        return f'{p}: NO FAQ heading — skipped'
    sec_start, sec_end = find_section_bounds(s, m.start())
    if sec_start is None:
        return f'{p}: could not find enclosing <section>'
    block = s[sec_start:sec_end]
    qas = extract_qa(block)
    if not qas:
        return f'{p}: section bounds [{sec_start}-{sec_end}] but 0 Q&A extracted'
    new_section = build_canonical(qas)
    new_s = s[:sec_start] + new_section + s[sec_end:]
    new_s = inject_assets(new_s)
    open(p,'w').write(new_s)
    return f'{p}: replaced section ({sec_end-sec_start}B) with {len(qas)} Q&A → {len(new_section)}B'

if __name__ == '__main__':
    for p in PAGES:
        if not os.path.exists(p):
            print(f'{p}: file not found'); continue
        print(process(p))
    # also ensure services.html has the JS (CSS already there)
    sp='services.html'
    s=open(sp).read()
    if 'id="rv-faq-canonical-js"' not in s:
        s=s.replace('</body>', FAQ_JS + '</body>', 1)
        open(sp,'w').write(s)
        print(f'{sp}: injected toggle JS')
    else:
        print(f'{sp}: JS already present')
