"""
Unify FAQ across all pages to use the canonical home-page (index.html) FAQ
section design (.rv-faq / .rv-faq__cta-card / .rv-faq-item / .rv-faq-item__q etc).

For each target page:
  1. Find the existing FAQ section and extract Q&A pairs.
  2. Replace the section with the canonical markup.
  3. Inject canonical CSS into <head> (id="rv-faq-canonical-css") if absent.
  4. Inject canonical JS scripts before </body> (id="rv-faq-canonical-js") if absent.
  5. Ensure Cal.com init script is present.

index.html and pages without an FAQ section are skipped.
"""
import os, re, sys

CSS = r'''<style id="rv-faq-canonical-css">
.rv-faq{padding:100px 0;background:linear-gradient(180deg,#ffffff 0%,#f4f8ff 100%);font-family:'Inter','Helvetica Neue',Arial,sans-serif;color:#0a1f3d;}
.rv-faq *{box-sizing:border-box}
.rv-faq__head{max-width:1200px;width:92%;margin:0 auto 56px}
.rv-faq__label{display:inline-flex;align-items:center;gap:10px;margin-bottom:40px}
.rv-faq__label-sq{width:14px;height:14px;background:#356eff;border-radius:4px}
.rv-faq__label-text{font-size:14px;font-weight:400;color:#0a1f3d}
.rv-faq__label-text strong{font-weight:700}
.rv-faq__headline{font-size:clamp(40px,5.5vw,72px);font-weight:800;line-height:1.05;letter-spacing:-0.03em;color:#0a1f3d;margin:0}
.rv-faq__body{max-width:1200px;width:92%;margin:0 auto;display:grid;grid-template-columns:420px 1fr;gap:48px;align-items:start}
.rv-faq__cta-card{background:linear-gradient(145deg,#5a85ff 0%,#356EFF 55%,#1e50d8 100%);border-radius:24px;padding:40px;display:flex;flex-direction:column;gap:0;position:relative;isolation:isolate;overflow:hidden}
.rv-faq__cta-card::before{content:'';position:absolute;inset:0;background:radial-gradient(circle 220px at var(--mx,50%) var(--my,-20%),rgba(255,255,255,.22) 0%,rgba(255,255,255,.06) 45%,transparent 70%);opacity:0;transition:opacity .4s ease;pointer-events:none;z-index:0;border-radius:inherit}
.rv-faq__cta-card:hover::before{opacity:1}
.rv-faq__cta-card>*{position:relative;z-index:1}
.rv-faq__cta-avatar{width:72px;height:72px;border-radius:50%;overflow:hidden;background:#f5c842;margin-bottom:28px;flex-shrink:0;position:relative}
.rv-faq__cta-avatar img,.rv-faq__cta-avatar video{width:100%;height:100%;object-fit:cover;display:block}
.rv-faq__cta-title{font-size:clamp(36px,4vw,52px);font-weight:800;color:#fff;line-height:1.1;letter-spacing:-0.02em;margin:0 0 16px}
.rv-faq__cta-sub{font-size:16px;color:rgba(255,255,255,.75);margin:0 0 32px;line-height:1.5}
.rv-faq__cta-btn{display:flex;align-items:center;justify-content:space-between;background:#111;color:#fff;border-radius:100px;padding:10px 10px 10px 28px;font-size:16px;font-weight:600;text-decoration:none;border:none;cursor:pointer;transition:background .25s;width:100%;text-align:left}
.rv-faq__cta-btn:hover{background:#000}
.rv-faq__cta-btn-circ{width:44px;height:44px;border-radius:50%;background:#fff;display:grid;place-items:center;flex-shrink:0;overflow:hidden;position:relative}
.rv-faq__cta-btn-circ .arr-out{width:18px;height:18px;stroke:#111;fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round;transition:transform .3s cubic-bezier(.4,0,.2,1);transform:translate(0,0);display:block}
.rv-faq__cta-btn:hover .rv-faq__cta-btn-circ .arr-out{transform:translate(130%,-130%)}
.rv-faq__cta-btn-circ .arr-in{position:absolute;inset:0;display:grid;place-items:center;transform:translate(-130%,130%);transition:transform .3s cubic-bezier(.4,0,.2,1)}
.rv-faq__cta-btn:hover .rv-faq__cta-btn-circ .arr-in{transform:translate(0,0)}
.rv-faq__cta-btn-circ .arr-in svg{width:18px;height:18px;stroke:#111;fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}
.rv-faq__cta-email{display:flex;align-items:center;gap:12px;margin-top:28px;padding-top:28px;border-top:1px solid rgba(255,255,255,.2)}
.rv-faq__cta-email-icon{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.15);display:grid;place-items:center;flex-shrink:0}
.rv-faq__cta-email-icon svg{width:16px;height:16px;stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.rv-faq__cta-email-label{font-size:12px;color:rgba(255,255,255,.65);margin:0 0 2px}
.rv-faq__cta-email-addr{font-size:14px;font-weight:700;color:#fff;margin:0;text-decoration:none}
.rv-faq__list{display:flex;flex-direction:column}
.rv-faq-item{border-bottom:1px solid #e5e7eb;overflow:hidden}
.rv-faq-item:first-child{border-top:1px solid #e5e7eb}
.rv-faq-item__q{display:flex;justify-content:space-between;align-items:center;padding:24px 0;cursor:pointer;gap:16px}
.rv-faq-item__q h3{font-size:17px;font-weight:700;color:#111827;margin:0;line-height:1.4}
.rv-faq-item__icon{width:28px;height:28px;min-width:28px;display:flex;align-items:center;justify-content:center;transition:transform .3s cubic-bezier(.4,0,.2,1);flex-shrink:0}
.rv-faq-item.active .rv-faq-item__icon{transform:rotate(180deg)}
.rv-faq-item__icon svg{width:20px;height:20px;stroke:#111827;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.rv-faq-item__a{max-height:0;overflow:hidden;transition:max-height .35s cubic-bezier(.4,0,.2,1)}
.rv-faq-item__a-inner{padding:0 40px 24px 0}
.rv-faq-item__a p{font-size:15px;line-height:1.75;color:#4b5563;margin:0 0 12px}
.rv-faq-item__a p:last-child{margin-bottom:0}
.rv-faq-item__a a{color:#356eff;text-decoration:underline;text-underline-offset:3px}
@media(max-width:1024px){.rv-faq__body{grid-template-columns:1fr}}
@media(max-width:768px){.rv-faq{padding:80px 0}.rv-faq__cta-card{padding:32px}}
</style>
'''

JS = r'''<script id="rv-faq-canonical-js">
(function(){
  function init(){
    var card=document.querySelector('.rv-faq__cta-card');
    if(card && !card.dataset.rvSpot){
      card.dataset.rvSpot='1';
      card.addEventListener('mousemove',function(e){var r=card.getBoundingClientRect();card.style.setProperty('--mx',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');card.style.setProperty('--my',((e.clientY-r.top)/r.height*100).toFixed(1)+'%')});
      card.addEventListener('mouseleave',function(){card.style.setProperty('--mx','50%');card.style.setProperty('--my','-20%')});
    }
    var items=document.querySelectorAll('.rv-faq-item');
    items.forEach(function(item){
      if(item.dataset.rvFaq) return; item.dataset.rvFaq='1';
      var q=item.querySelector('.rv-faq-item__q'),a=item.querySelector('.rv-faq-item__a');
      if(!q||!a) return;
      q.addEventListener('click',function(){
        var open=item.classList.contains('active');
        items.forEach(function(o){o.classList.remove('active');var oa=o.querySelector('.rv-faq-item__a');if(oa) oa.style.maxHeight=null;});
        if(!open){item.classList.add('active');a.style.maxHeight=a.scrollHeight+'px';}
      });
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init); else init();
  window.Webflow=window.Webflow||[]; window.Webflow.push(init);
})();
</script>
'''

CAL_INIT = r'''<script id="rv-cal-init">
(function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if(typeof namespace === "string"){cal.ns[namespace] = cal.ns[namespace] || api;p(cal.ns[namespace], ar);p(cal, ["initNamespace", namespace]);} else p(cal, ar); return;} p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "Cal");
Cal("init","30min",{origin:"https://cal.com"});
Cal.ns["30min"]("ui",{"hideEventTypeDetails":false,"layout":"month_view"});
</script>
'''

# ---------------- helpers ----------------
TAG_RE = re.compile(r'<[^>]+>')

def strip_tags_keep_a(html):
    out=[]; i=0
    while i<len(html):
        if html[i]=='<':
            j=html.find('>',i)
            if j==-1: break
            tag=html[i:j+1]
            low=tag.lower()
            if re.match(r'<a\b', low) or low.startswith('</a'):
                # strip Webflow-specific attrs but keep href
                m=re.match(r'<a\b([^>]*)>', tag, re.I)
                if m:
                    attrs=m.group(1)
                    href_m=re.search(r'href="([^"]*)"', attrs)
                    href=href_m.group(1) if href_m else '#'
                    out.append(f'<a href="{href}">')
                else:
                    out.append('</a>')
            i=j+1
        else:
            out.append(html[i]); i+=1
    return ''.join(out)

def clean_text(s):
    return re.sub(r'\s+',' ', s).strip()

def clean_q(s):
    s=re.sub(TAG_RE,'', s)
    s=clean_text(s)
    s=re.sub(r'^\d+\.\s*','', s)
    # Remove leading numbering "01" "02" etc that appears as <span>
    s=re.sub(r'^\d{2}\s+','', s)
    return s

# ---------------- bounds ----------------
def section_bounds_at(html, start):
    """Given the index of '<section', return (start, end) of the matching </section>."""
    depth=0; i=start
    while i < len(html):
        ot = re.match(r'<section\b', html[i:], re.I)
        ct = re.match(r'</section\s*>', html[i:], re.I)
        if ot: depth += 1; i += 8
        elif ct:
            depth -= 1; i += ct.end()
            if depth == 0: return (start, i)
        else:
            i += 1
    return None

def find_faq_section(html):
    """Return (start, end, kind) of the FAQ <section>.
    Searches for: rv-faq-sect, then heading 'Frequently Asked Questions' inside a <section>."""
    # 1) services-style
    m = re.search(r'<section[^>]*class="[^"]*rv-faq-sect[^"]*"', html, re.I)
    if m:
        b = section_bounds_at(html, m.start())
        if b: return (*b, 'rv-faq-sect')
    # 2) heading-based: scan all <section> blocks
    for sm in re.finditer(r'<section\b', html, re.I):
        b = section_bounds_at(html, sm.start())
        if not b: continue
        body = html[b[0]:b[1]]
        if re.search(r'Frequently\s*Asked\s*Questions?', body, re.I) and ('class="faq w-dropdown' in body or 'class="rv-faq-item' in body):
            return (*b, 'webflow')
    return None

# ---------------- extractors ----------------
def extract_qa_webflow(section_html):
    """Extract from Webflow `.faq w-dropdown` items."""
    items=[]
    for m in re.finditer(r'<div[^>]*class="[^"]*\bfaq\b[^"]*w-dropdown[^"]*"[^>]*>([\s\S]*?</nav>)', section_html, re.I):
        block = m.group(1)
        # question - inside .faq-title-wrapper
        wm = re.search(r'<div[^>]*class="[^"]*faq-title-wrapper[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>', block, re.I)
        q = ''
        if wm:
            inner = wm.group(1)
            # take first heading or text up to faq-icon
            hm = re.search(r'<(?:h\d|p|span|div)[^>]*>([\s\S]*?)</(?:h\d|p|span|div)>', inner, re.I)
            if hm: q = clean_q(hm.group(1))
            else: q = clean_q(inner)
        # answer paragraphs from <nav> ... </nav>
        nm = re.search(r'<nav[^>]*>([\s\S]*?)</nav>', block, re.I)
        paras = []
        if nm:
            for pm in re.finditer(r'<p[^>]*>([\s\S]*?)</p>', nm.group(1), re.I):
                t = clean_text(strip_tags_keep_a(pm.group(1)))
                if t: paras.append(t)
            if not paras:
                t = clean_text(strip_tags_keep_a(nm.group(1)))
                if t: paras.append(t)
        if q and paras: items.append((q, paras))
    return items

def extract_qa_rv_item_new(section_html):
    """Extract from earlier `.rv-faq-item-new` markup."""
    items=[]
    pos = 0
    while True:
        m = re.search(r'<div[^>]*class="[^"]*rv-faq-item-new', section_html[pos:])
        if not m: break
        start = pos + m.start()
        depth=0; i=start
        while i < len(section_html):
            ot = re.match(r'<div\b', section_html[i:], re.I)
            ct = re.match(r'</div\s*>', section_html[i:], re.I)
            if ot: depth += 1; i += 4
            elif ct:
                depth -= 1; i += ct.end()
                if depth == 0: break
            else:
                i += 1
        block = section_html[start:i]
        qm = re.search(r'<span[^>]*class="[^"]*rv-faq-q[^"]*"[^>]*>([\s\S]*?)</span>', block, re.I)
        q = clean_q(qm.group(1)) if qm else ''
        cm = re.search(r'<div[^>]*class="[^"]*faq-content[^"]*"[^>]*>([\s\S]*?)</div>\s*</div>\s*</div>', block, re.I)
        if not cm:
            cm = re.search(r'<div[^>]*class="[^"]*faq-tab[^"]*"[^>]*>([\s\S]*?)</div>', block, re.I)
        paras=[]
        if cm:
            content = cm.group(1)
            for pm in re.finditer(r'<p[^>]*>([\s\S]*?)</p>', content, re.I):
                t = clean_text(strip_tags_keep_a(pm.group(1)))
                if t: paras.append(t)
            if not paras:
                t = clean_text(strip_tags_keep_a(content))
                if t: paras.append(t)
        if q and paras: items.append((q, paras))
        pos = i
    return items

def extract_qa(section_html, kind):
    if kind == 'rv-faq-sect':
        items = extract_qa_rv_item_new(section_html)
        if items: return items
    return extract_qa_webflow(section_html)

# ---------------- canonical builder ----------------
def build_canonical(items):
    qa_html = []
    for q, paras in items:
        ps = ''.join(f'<p>{p}</p>' for p in paras)
        qa_html.append(
            f'        <div class="rv-faq-item">\n'
            f'          <div class="rv-faq-item__q"><h3>{q}</h3><div class="rv-faq-item__icon"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></div></div>\n'
            f'          <div class="rv-faq-item__a"><div class="rv-faq-item__a-inner">{ps}</div></div>\n'
            f'        </div>'
        )
    items_str = '\n'.join(qa_html)
    return f'''  <!-- FAQ (canonical: matches index.html) -->
  <section class="rv-faq">
    <div class="rv-faq__head">
      <div class="rv-faq__label">
        <span class="rv-faq__label-sq"></span>
        <span class="rv-faq__label-text">Frequently <strong>Asked Questions</strong></span>
      </div>
      <h2 class="rv-faq__headline">Questions? We've got answers.</h2>
    </div>
    <div class="rv-faq__body">

      <!-- Left: CTA card -->
      <div class="rv-faq__cta-card">
        <div class="rv-faq__cta-avatar">
          <video class="video-component" autoplay loop playsinline muted width="72" height="72" poster="videos/character-poster.jpg" style="width:100%;height:100%;object-fit:cover;display:block;border-radius:50%;"><source src="videos/ch.mp4" type="video/mp4"></video>
        </div>
        <h3 class="rv-faq__cta-title">Book a 30 min free call</h3>
        <p class="rv-faq__cta-sub">Got more Qs? Let's chat</p>
        <button class="rv-faq__cta-btn" data-cal-namespace="30min" data-cal-link="navjot-singh-gfjevp/30min" data-cal-config='{{"layout":"month_view"}}' style="border:none;">
          <span>Book a Call</span>
          <div class="rv-faq__cta-btn-circ">
            <svg class="arr-out" viewBox="0 0 24 24"><path d="M7 17L17 7"/><path d="M7 7h10v10"/></svg>
            <span class="arr-in"><svg viewBox="0 0 24 24"><path d="M7 17L17 7"/><path d="M7 7h10v10"/></svg></span>
          </div>
        </button>
        <div class="rv-faq__cta-email">
          <div class="rv-faq__cta-email-icon">
            <svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
          </div>
          <div>
            <p class="rv-faq__cta-email-label">Do you prefer email communication?</p>
            <a href="mailto:hello@5rv.digital" class="rv-faq__cta-email-addr">hello@5rv.digital</a>
          </div>
        </div>
      </div>

      <!-- Right: Accordion -->
      <div class="rv-faq__list">
{items_str}
      </div>

    </div>
  </section>
'''

# ---------------- injectors ----------------
CSS_RE = re.compile(r'<style id="rv-faq-canonical-css">[\s\S]*?</style>\s*', re.I)
JS_RE  = re.compile(r'<script id="rv-faq-canonical-js">[\s\S]*?</script>\s*', re.I)
CAL_RE = re.compile(r'<script id="rv-cal-init">[\s\S]*?</script>\s*', re.I)

def inject_before_last_body(html, snippet):
    """Insert snippet before the LAST </body> (avoids </body> trapped in HTML comments)."""
    if '</body>' not in html:
        return html + snippet
    parts = html.rsplit('</body>', 1)
    return parts[0] + snippet + '</body>' + parts[1]

def inject_assets(html):
    html = CSS_RE.sub('', html)
    html = JS_RE.sub('', html)
    html = html.replace('</head>', CSS + '</head>', 1)
    # Only inject canonical JS if no inline FAQ JS already handles .rv-faq-item
    if "querySelectorAll('.rv-faq-item')" not in html:
        html = inject_before_last_body(html, JS)
    if 'Cal("init"' not in html and 'Cal(\\"init\\"' not in html:
        html = CAL_RE.sub('', html)
        html = inject_before_last_body(html, CAL_INIT)
    return html

# ---------------- per-page driver ----------------
def process(path):
    s = open(path).read()
    if path == 'index.html':
        return f'{path}: skipped (canonical source)'
    bounds = find_faq_section(s)
    if not bounds:
        return f'{path}: no FAQ section found (skipped)'
    start, end, kind = bounds
    section = s[start:end]
    items = extract_qa(section, kind)
    if not items:
        return f'{path}: no Q&A extracted (skipped)'
    new_section = build_canonical(items)
    new_html = s[:start] + new_section + s[end:]
    new_html = inject_assets(new_html)
    open(path, 'w').write(new_html)
    return f'{path}: {len(items)} Q&A migrated ({kind})'

if __name__ == '__main__':
    targets = sys.argv[1:] or [f for f in sorted(os.listdir('.'))
                               if f.endswith('.html') and 'backup' not in f]
    for f in targets:
        try:
            print(process(f))
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f'{f}: ERROR {e}')
