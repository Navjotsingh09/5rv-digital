# =============================================================================
# DO NOT RUN — SUPERSEDED
# This script has been archived and is kept for historical reference only.
# Running it may overwrite production files or undo current work.
# See RUNBOOK.md in the project root for the list of active scripts.
# =============================================================================

"""
Unify FAQ across all pages with the new "Questions? We've got answers." design.
- Replaces canonical CSS block (id=rv-faq-canonical-css)
- Replaces the <section class="rv-faq-sect ...">...</section> markup
- Extracts existing Q&A from each page and re-emits them
- Also handles legacy `.faq w-dropdown` markup if any remain
- Keeps the existing canonical JS toggle (rv-faq-canonical-js) untouched
"""
import os, re, sys

NEW_CSS = '''<style id="rv-faq-canonical-css">
/* ============ 5RV CANONICAL FAQ (v2) ============ */
.rv-faq-sect{position:relative;padding:120px 0 140px;background:#fff;color:#0a1f3d;font-family:'Inter','Helvetica Neue',Arial,sans-serif;}
.rv-faq-sect__inner{max-width:1280px;margin:0 auto;padding:0 32px;}
.rv-faq-sect__top{display:flex;flex-direction:column;gap:18px;margin-bottom:56px;}
.rv-faq-sect__tag{display:inline-flex;align-items:center;gap:10px;font-size:14px;font-weight:500;color:#0a1f3d;letter-spacing:.01em;}
.rv-faq-sect__tag::before{content:"";display:block;width:14px;height:14px;background:#356eff;border-radius:3px;flex:0 0 auto;}
.rv-faq-sect__tag b{font-weight:700;}
.rv-faq-sect__heading{font-family:'Inter','Helvetica Neue',Arial,sans-serif;font-size:clamp(40px,6.4vw,84px);line-height:1.02;font-weight:800;letter-spacing:-.03em;color:#0a1f3d;margin:0;}
.rv-faq-sect__grid{display:grid;grid-template-columns:minmax(280px,360px) 1fr;gap:48px;align-items:start;}
@media (max-width:900px){.rv-faq-sect{padding:80px 0 90px;}.rv-faq-sect__grid{grid-template-columns:1fr;gap:32px;}.rv-faq-sect__top{margin-bottom:40px;}}

/* Left CTA card */
.rv-faq-cta{position:sticky;top:120px;background:linear-gradient(155deg,#5b8bff 0%,#2a5cf0 60%,#1d44c4 100%);border-radius:24px;padding:32px 30px 30px;color:#fff;box-shadow:0 30px 60px -30px rgba(45,92,240,.5);overflow:hidden;}
.rv-faq-cta__avatar{width:64px;height:64px;border-radius:50%;background:#ffd84d;display:flex;align-items:center;justify-content:center;overflow:hidden;margin-bottom:60px;box-shadow:0 4px 14px rgba(0,0,0,.15);}
.rv-faq-cta__avatar svg{width:100%;height:100%;display:block;}
.rv-faq-cta__title{font-size:38px;line-height:1.05;font-weight:800;letter-spacing:-.02em;margin:0 0 12px;color:#fff;}
.rv-faq-cta__sub{font-size:14.5px;line-height:1.55;color:rgba(255,255,255,.78);margin:0 0 26px;max-width:280px;}
.rv-faq-cta__btn{display:inline-flex;align-items:center;gap:10px;background:#0a0e1a;color:#fff;border:none;border-radius:999px;padding:8px 8px 8px 26px;font-size:15px;font-weight:500;cursor:pointer;text-decoration:none;transition:transform .25s ease,box-shadow .25s ease;}
.rv-faq-cta__btn:hover{transform:translateY(-2px);box-shadow:0 12px 24px rgba(0,0,0,.25);}
.rv-faq-cta__btn-circ{width:36px;height:36px;border-radius:50%;background:#fff;color:#0a0e1a;display:flex;align-items:center;justify-content:center;flex:0 0 auto;}
.rv-faq-cta__btn-circ svg{width:16px;height:16px;}
.rv-faq-cta__btn-circ svg path{stroke:#0a0e1a;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round;}
.rv-faq-cta__divider{height:1px;background:rgba(255,255,255,.22);margin:28px 0 18px;}
.rv-faq-cta__email{display:flex;align-items:center;gap:12px;color:#fff;text-decoration:none;}
.rv-faq-cta__email-icon{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.14);display:flex;align-items:center;justify-content:center;flex:0 0 auto;}
.rv-faq-cta__email-icon svg{width:16px;height:16px;stroke:#fff;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round;}
.rv-faq-cta__email-txt{display:flex;flex-direction:column;line-height:1.25;}
.rv-faq-cta__email-txt span:first-child{font-size:12px;color:rgba(255,255,255,.7);}
.rv-faq-cta__email-txt span:last-child{font-size:14.5px;font-weight:500;color:#fff;}
@media (max-width:900px){.rv-faq-cta{position:static;}}

/* Right list */
.rv-faq-sect__list{display:flex;flex-direction:column;}
.rv-faq-item-new{border-top:1px solid #e5e7eb;}
.rv-faq-item-new:last-child{border-bottom:1px solid #e5e7eb;}
.rv-faq-item-new .faq-title{padding:24px 8px 24px 4px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;user-select:none;}
.rv-faq-item-new .faq-title-wrapper{display:flex;align-items:center;justify-content:space-between;gap:16px;width:100%;}
.rv-faq-item-new .rv-faq-q{font-size:16.5px;font-weight:500;color:#0a1f3d;line-height:1.4;}
.rv-faq-item-new .rv-faq-icon{width:24px;height:24px;flex:0 0 auto;display:flex;align-items:center;justify-content:center;transition:transform .35s cubic-bezier(.4,0,.2,1);}
.rv-faq-item-new .rv-faq-icon svg{width:18px;height:18px;}
.rv-faq-item-new .rv-faq-icon svg path{stroke:#0a1f3d;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round;}
.rv-faq-item-new.open .rv-faq-icon{transform:rotate(180deg);}
.rv-faq-item-new .faq-content{max-height:0;overflow:hidden;transition:max-height .45s cubic-bezier(.4,0,.2,1);}
.rv-faq-item-new .faq-tab{padding:0 8px 24px 4px;}
.rv-faq-item-new .faq-tab p{font-size:15px;line-height:1.65;color:#4a5878;margin:0 0 12px;}
.rv-faq-item-new .faq-tab p:last-child{margin-bottom:0;}
.rv-faq-item-new .faq-tab a{color:#356eff;text-decoration:underline;}
</style>
'''

NEW_JS = '''<script id="rv-faq-canonical-js">
(function(){
  function init(){
    document.querySelectorAll('.rv-faq-item-new').forEach(function(item){
      if(item.dataset.faqInit==='3') return;
      item.dataset.faqInit='3';
      var oldTitle=item.querySelector('.faq-title');
      if(!oldTitle) return;
      var title=oldTitle.cloneNode(true);
      oldTitle.parentNode.replaceChild(title, oldTitle);
      var content=item.querySelector('.faq-content');
      if(!content) return;
      title.setAttribute('role','button');
      title.setAttribute('tabindex','0');
      title.style.cursor='pointer';
      function toggle(){
        var isOpen=item.classList.contains('open');
        item.parentElement.querySelectorAll('.rv-faq-item-new.open').forEach(function(o){
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
      title.addEventListener('click', function(e){
        if(e.target.closest('a,button')) return;
        e.preventDefault(); e.stopPropagation();
        toggle();
      });
      title.addEventListener('keydown', function(e){
        if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); }
      });
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init);
  else init();
  window.Webflow=window.Webflow||[]; window.Webflow.push(init);
})();
</script>
'''

CTA_INNER = '''      <aside class="rv-faq-cta">
        <div class="rv-faq-cta__avatar" aria-hidden="true">
          <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <circle cx="32" cy="32" r="32" fill="#FFD84D"/>
            <path d="M14 56c2-10 10-16 18-16s16 6 18 16" fill="#fff"/>
            <path d="M22 28c0-7 4-13 10-13s10 6 10 13v3H22v-3z" fill="#5a3a22"/>
            <ellipse cx="32" cy="33" rx="9" ry="11" fill="#f5d3b0"/>
            <rect x="22" y="29" width="20" height="6" rx="3" fill="#1a1a1a"/>
            <ellipse cx="27" cy="32" rx="3" ry="2.4" fill="#1a1a1a"/>
            <ellipse cx="37" cy="32" rx="3" ry="2.4" fill="#1a1a1a"/>
          </svg>
        </div>
        <h3 class="rv-faq-cta__title">Book a 30 min<br>free call</h3>
        <p class="rv-faq-cta__sub">Got more questions? Let's chat about your goals.</p>
        <button type="button" class="rv-faq-cta__btn" data-cal-namespace="30min" data-cal-link="navjot-singh-gfjevp/30min" data-cal-config='{"layout":"month_view"}' aria-label="Schedule a 30 minute free call">
          <span>Schedule a call</span>
          <span class="rv-faq-cta__btn-circ"><svg viewBox="0 0 24 24"><path d="M5 12h14"/><path d="M13 6l6 6-6 6"/></svg></span>
        </button>
        <div class="rv-faq-cta__divider"></div>
        <a class="rv-faq-cta__email" href="mailto:hello@5rv.digital">
          <span class="rv-faq-cta__email-icon"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></span>
          <span class="rv-faq-cta__email-txt"><span>Do you prefer email?</span><span>hello@5rv.digital</span></span>
        </a>
      </aside>
'''

# ---------- Q&A extraction ----------
TAG_RE = re.compile(r'<[^>]+>')

def strip_tags_keep_a(html):
    # keep <a> tags so they remain clickable
    out=[]; i=0
    while i<len(html):
        if html[i]=='<':
            j=html.find('>',i)
            if j==-1: break
            tag=html[i:j+1]
            low=tag.lower()
            if low.startswith('<a ') or low.startswith('<a>') or low.startswith('</a'):
                out.append(tag)
            i=j+1
        else:
            out.append(html[i]); i+=1
    return ''.join(out)

def clean_text(s):
    s=re.sub(r'\s+',' ', s).strip()
    return s

def extract_from_rv_items(section_html):
    items=[]
    item_re=re.compile(r'<div[^>]*class="[^"]*rv-faq-item-new[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>\s*</div>', re.I)
    # Simpler depth-aware extraction
    pos=0
    while True:
        m=re.search(r'<div[^>]*class="[^"]*rv-faq-item-new', section_html[pos:])
        if not m: break
        start=pos+m.start()
        # find balanced div
        depth=0; i=start
        while i<len(section_html):
            t=re.match(r'<div\b', section_html[i:], re.I)
            ct=re.match(r'</div\s*>', section_html[i:], re.I)
            if t: depth+=1; i+=4; 
            elif ct: 
                depth-=1; i+=ct.end()
                if depth==0: break
            else:
                i+=1
        block=section_html[start:i]
        # extract Q
        qm=re.search(r'<span[^>]*class="[^"]*rv-faq-q[^"]*"[^>]*>([\s\S]*?)</span>', block, re.I)
        q=clean_text(re.sub(TAG_RE,'', qm.group(1))) if qm else ''
        # extract content paragraphs
        cm=re.search(r'<div[^>]*class="[^"]*faq-content[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>', block, re.I)
        paras=[]
        if cm:
            content=cm.group(1)
            for pm in re.finditer(r'<p[^>]*>([\s\S]*?)</p>', content, re.I):
                txt=clean_text(strip_tags_keep_a(pm.group(1)))
                if txt: paras.append(txt)
            if not paras:
                txt=clean_text(strip_tags_keep_a(content))
                if txt: paras.append(txt)
        if q and paras: items.append((q,paras))
        pos=i
    return items

def extract_from_legacy(section_html):
    items=[]
    pat=re.compile(r'<div[^>]*class="[^"]*\bfaq\b[^"]*w-dropdown[^"]*"[\s\S]*?</nav>\s*</div>', re.I)
    for m in pat.finditer(section_html):
        block=m.group(0)
        # question
        qm=re.search(r'<div[^>]*class="[^"]*faq-title-wrapper[^"]*"[^>]*>([\s\S]*?)</div>', block, re.I)
        q=''
        if qm:
            inner=qm.group(1)
            hm=re.search(r'<(?:h\d|div|span)[^>]*>([\s\S]*?)</(?:h\d|div|span)>', inner, re.I)
            if hm: q=clean_text(re.sub(TAG_RE,'', hm.group(1)))
            else: q=clean_text(re.sub(TAG_RE,'', inner))
        q=re.sub(r'^\d+\.\s*','', q)
        # content paragraphs
        nav=re.search(r'<nav[^>]*>([\s\S]*?)</nav>', block, re.I)
        paras=[]
        if nav:
            for pm in re.finditer(r'<p[^>]*>([\s\S]*?)</p>', nav.group(1), re.I):
                txt=clean_text(strip_tags_keep_a(pm.group(1)))
                if txt: paras.append(txt)
            if not paras:
                txt=clean_text(strip_tags_keep_a(nav.group(1)))
                if txt: paras.append(txt)
        if q and paras: items.append((q,paras))
    return items

# ---------- Section bounds ----------
def find_section_bounds(html, anchor_re):
    # Find a <section ...> tag whose contents contain the anchor.
    for sm in re.finditer(r'<section\b', html, re.I):
        seek_start=sm.start()
        # find matching </section>
        depth=0; i=seek_start; end=None
        while i<len(html):
            ot=re.match(r'<section\b', html[i:], re.I)
            ct=re.match(r'</section\s*>', html[i:], re.I)
            if ot: depth+=1; i+=8
            elif ct:
                depth-=1; i+=ct.end()
                if depth==0: end=i; break
            else: i+=1
        if end is None: continue
        body=html[seek_start:end]
        if anchor_re.search(body):
            return (seek_start, end)
    return None
def _unused_find(html, anchor_re):
    m=anchor_re.search(html)
    if not m: return None
    seek_start=html.rfind('<section', 0, m.start())
    if seek_start==-1: return None
    # walk forward to matching </section>
    depth=0; i=seek_start
    while i<len(html):
        ot=re.match(r'<section\b', html[i:], re.I)
        ct=re.match(r'</section\s*>', html[i:], re.I)
        if ot: depth+=1; i+=8
        elif ct:
            depth-=1; i+=ct.end()
            if depth==0: return (seek_start, i)
        else:
            i+=1
    return None

def build_section(items):
    if not items: return ''
    qa_html=[]
    for q,paras in items:
        ps=''.join(f'<p>{p}</p>' for p in paras)
        qa_html.append(f'''        <div class="faq rv-faq-item-new">
          <div class="faq-title"><div class="faq-title-wrapper"><span class="rv-faq-q">{q}</span><div class="rv-faq-icon"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></div></div></div>
          <div class="faq-content"><div class="faq-tab">{ps}</div></div>
        </div>''')
    list_html='\n'.join(qa_html)
    return f'''  <!-- FAQ (canonical v2) -->
  <section class="rv-faq-sect rv-reveal">
    <div class="rv-faq-sect__inner">
      <div class="rv-faq-sect__top">
        <span class="rv-faq-sect__tag">Frequently <b>Asked Questions</b></span>
        <h2 class="rv-faq-sect__heading">Questions? We've got answers.</h2>
      </div>
      <div class="rv-faq-sect__grid">
{CTA_INNER}        <div class="rv-faq-sect__list">
{list_html}
        </div>
      </div>
    </div>
  </section>
'''

CSS_RE=re.compile(r'<style id="rv-faq-canonical-css">[\s\S]*?</style>\s*', re.I)
JS_RE =re.compile(r'<script id="rv-faq-canonical-js">[\s\S]*?</script>\s*', re.I)

def inject_assets(html):
    # remove existing canonical CSS/JS
    html=CSS_RE.sub('', html)
    html=JS_RE.sub('', html)
    # inject CSS before </head>
    html=html.replace('</head>', NEW_CSS + '</head>', 1)
    # inject JS before </body>
    html=html.replace('</body>', NEW_JS + '</body>', 1)
    return html

CAL_INLINE_RE=re.compile(r'\(function\s*\(C,\s*A,\s*L\)[\s\S]*?Cal\("init"[\s\S]*?\}\)\(\);?', re.I)

def ensure_cal_init(html):
    # Cal.com init script needs to be present for data-cal-* buttons to work.
    if 'Cal("init"' in html and '"30min"' in html:
        return html
    snippet='''<script>
(function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if(typeof namespace === "string"){cal.ns[namespace] = cal.ns[namespace] || api;p(cal.ns[namespace], ar);p(cal, ["initNamespace", namespace]);} else p(cal, ar); return;} p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "Cal");
Cal("init", "30min", {origin:"https://cal.com"});
Cal.ns["30min"]("ui", {"hideEventTypeDetails":false,"layout":"month_view"});
</script>
'''
    html=html.replace('</body>', snippet + '</body>', 1)
    return html

ANCHOR_RE = re.compile(r'(class="[^"]*rv-faq-sect|class="faq w-dropdown|<h2[^>]*>\s*Frequently[\s\S]{0,80}?Asked|class="[^"]*rv-faq-item-new)', re.I)

def process(path):
    s=open(path).read()
    bounds=find_section_bounds(s, ANCHOR_RE)
    if not bounds:
        return f'{path}: no FAQ section found'
    section=s[bounds[0]:bounds[1]]
    items=extract_from_rv_items(section)
    if not items:
        items=extract_from_legacy(section)
    if not items:
        return f'{path}: no Q&A extracted (skipped)'
    new_section=build_section(items)
    new_html=s[:bounds[0]] + new_section + s[bounds[1]:]
    new_html=inject_assets(new_html)
    new_html=ensure_cal_init(new_html)
    open(path,'w').write(new_html)
    return f'{path}: {len(items)} Q&A migrated'

if __name__=='__main__':
    targets=sys.argv[1:] or [f for f in sorted(os.listdir('.')) if f.endswith('.html') and 'backup' not in f]
    for f in targets:
        try:
            print(process(f))
        except Exception as e:
            print(f'{f}: ERROR {e}')
