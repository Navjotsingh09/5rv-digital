#!/usr/bin/env python3
"""Replace the redundant 'Clear steps for growing brands' section on services.html
with three new sections: How We Work (4 steps), Industries We Serve, Tools & Tech."""
import pathlib

P = pathlib.Path('services.html')
s = P.read_text()
MARKER_START = '<!-- rv-svc-extras-start -->'
MARKER_END = '<!-- rv-svc-extras-end -->'

if MARKER_START in s:
    print('services.html: already migrated')
    raise SystemExit

# Locate the fsv-wrap section
needle = 'Clear steps for growing brands'
i = s.find(needle)
if i < 0:
    raise SystemExit('needle not found')
sec_start = s.rfind('<section class="fsv-wrap">', 0, i)
sec_end = s.find('</section>', i) + len('</section>')
assert sec_start > 0 and sec_end > sec_start, 'bounds bad'

NEW = MARKER_START + '''
<style id="rv-svc-extras-css">
.rv-svc-extras{font-family:var(--font-primary,Urbanist,sans-serif)}
.rv-svc-extras__container{width:min(1280px,calc(100% - 48px));margin:0 auto}

/* HOW WE WORK */
.rv-process{background:#f5f5f5;padding:96px 0 80px}
.rv-process__head{display:flex;justify-content:space-between;align-items:flex-end;flex-wrap:wrap;gap:24px;margin-bottom:56px}
.rv-process__eyebrow{display:inline-flex;align-items:center;gap:8px;background:#262a36;color:#fff;border-radius:100px;padding:6px 16px;font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.rv-process__eyebrow::before{content:"";width:6px;height:6px;border-radius:50%;background:#5a85ff}
.rv-process__title{font-size:clamp(32px,4vw,52px);font-weight:700;color:#0B1739;margin:18px 0 0;line-height:1.05;max-width:680px;letter-spacing:-0.02em}
.rv-process__lede{font-family:Plus Jakarta Sans,sans-serif;font-size:15px;color:#4b5563;line-height:1.6;max-width:340px;margin:0}
.rv-process__grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
.rv-process__step{background:#fff;border:1px solid rgba(11,23,57,.06);border-radius:18px;padding:28px 24px;transition:transform .25s ease,box-shadow .25s ease;display:flex;flex-direction:column;gap:14px;position:relative;overflow:hidden}
.rv-process__step:hover{transform:translateY(-4px);box-shadow:0 16px 40px rgba(11,23,57,.08)}
.rv-process__num{font-size:13px;font-weight:700;color:#356EFF;letter-spacing:.1em}
.rv-process__step h3{font-size:20px;font-weight:700;color:#0B1739;margin:0;letter-spacing:-0.01em}
.rv-process__step p{font-family:Plus Jakarta Sans,sans-serif;font-size:14px;line-height:1.6;color:#4b5563;margin:0}
.rv-process__icon{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,rgba(90,133,255,.12),rgba(53,110,255,.18));display:grid;place-items:center;color:#356EFF}
.rv-process__icon svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
@media(max-width:1024px){.rv-process__grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.rv-process__grid{grid-template-columns:1fr}}

/* INDUSTRIES */
.rv-industries{background:#fff;padding:88px 0}
.rv-industries__head{text-align:center;margin-bottom:48px}
.rv-industries__eyebrow{display:inline-block;background:rgba(53,110,255,.1);color:#356EFF;border-radius:100px;padding:5px 14px;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;margin-bottom:16px}
.rv-industries__title{font-size:clamp(28px,3.4vw,42px);font-weight:700;color:#0B1739;margin:0;letter-spacing:-0.02em}
.rv-industries__sub{font-family:Plus Jakarta Sans,sans-serif;font-size:15px;color:#4b5563;line-height:1.6;max-width:560px;margin:14px auto 0}
.rv-industries__grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-top:8px}
.rv-industries__item{background:#f7f8fb;border:1px solid rgba(11,23,57,.05);border-radius:14px;padding:22px 16px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;text-align:center;min-height:120px;transition:background .2s ease,transform .25s ease,border-color .2s ease}
.rv-industries__item:hover{background:#fff;border-color:rgba(53,110,255,.25);transform:translateY(-3px)}
.rv-industries__item-icon{width:36px;height:36px;color:#356EFF}
.rv-industries__item-icon svg{width:100%;height:100%;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.rv-industries__item-name{font-size:13.5px;font-weight:600;color:#0B1739;line-height:1.25}
@media(max-width:1024px){.rv-industries__grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:560px){.rv-industries__grid{grid-template-columns:repeat(2,1fr)}}

/* TOOLS */
.rv-tools{background:#0a0e1a;padding:88px 0;color:#fff;position:relative;overflow:hidden}
.rv-tools::before{content:"";position:absolute;inset:0;background:radial-gradient(ellipse at top,rgba(53,110,255,.18),transparent 55%);pointer-events:none}
.rv-tools__head{text-align:center;margin-bottom:48px;position:relative}
.rv-tools__eyebrow{display:inline-block;background:rgba(255,255,255,.08);color:#a8b8e0;border-radius:100px;padding:5px 14px;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;margin-bottom:16px}
.rv-tools__title{font-size:clamp(28px,3.4vw,42px);font-weight:700;margin:0;letter-spacing:-0.02em;color:#fff}
.rv-tools__sub{font-family:Plus Jakarta Sans,sans-serif;font-size:15px;color:rgba(255,255,255,.65);line-height:1.6;max-width:560px;margin:14px auto 0}
.rv-tools__grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;position:relative}
.rv-tools__item{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:22px 16px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;min-height:118px;text-align:center;transition:background .2s ease,border-color .2s ease,transform .25s ease}
.rv-tools__item:hover{background:rgba(255,255,255,.07);border-color:rgba(90,133,255,.4);transform:translateY(-3px)}
.rv-tools__item-mark{font-size:22px;font-weight:800;color:#fff;letter-spacing:-0.03em;line-height:1}
.rv-tools__item-name{font-size:12px;font-weight:500;color:rgba(255,255,255,.65);line-height:1.3}
@media(max-width:1024px){.rv-tools__grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:560px){.rv-tools__grid{grid-template-columns:repeat(2,1fr)}}
</style>

<!-- HOW WE WORK -->
<section class="rv-svc-extras rv-process">
  <div class="rv-svc-extras__container">
    <div class="rv-process__head">
      <div>
        <span class="rv-process__eyebrow">Our process</span>
        <h2 class="rv-process__title">A clear, repeatable path to growth</h2>
      </div>
      <p class="rv-process__lede">Every engagement follows the same four-step rhythm — built to remove guesswork and deliver measurable results.</p>
    </div>
    <div class="rv-process__grid">
      <div class="rv-process__step">
        <div class="rv-process__icon"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></div>
        <span class="rv-process__num">01</span>
        <h3>Discover</h3>
        <p>We audit your brand, market and competitors, then map every channel to opportunity.</p>
      </div>
      <div class="rv-process__step">
        <div class="rv-process__icon"><svg viewBox="0 0 24 24"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-6"/></svg></div>
        <span class="rv-process__num">02</span>
        <h3>Strategy</h3>
        <p>A focused plan that pairs the right channels, content and KPIs with your business goals.</p>
      </div>
      <div class="rv-process__step">
        <div class="rv-process__icon"><svg viewBox="0 0 24 24"><path d="m4 12 5 5L20 6"/></svg></div>
        <span class="rv-process__num">03</span>
        <h3>Execute</h3>
        <p>We ship campaigns, websites and content quickly — without sacrificing craft or detail.</p>
      </div>
      <div class="rv-process__step">
        <div class="rv-process__icon"><svg viewBox="0 0 24 24"><path d="M3 12a9 9 0 1 0 9-9"/><path d="M3 4v5h5"/></svg></div>
        <span class="rv-process__num">04</span>
        <h3>Optimise</h3>
        <p>We measure what works, double-down on winners and report transparently every month.</p>
      </div>
    </div>
  </div>
</section>

<!-- INDUSTRIES -->
<section class="rv-svc-extras rv-industries">
  <div class="rv-svc-extras__container">
    <div class="rv-industries__head">
      <span class="rv-industries__eyebrow">Who we work with</span>
      <h2 class="rv-industries__title">Industries we serve</h2>
      <p class="rv-industries__sub">From local service businesses to growing e-commerce brands, we adapt our playbook to your sector.</p>
    </div>
    <div class="rv-industries__grid">
      <div class="rv-industries__item">
        <div class="rv-industries__item-icon"><svg viewBox="0 0 24 24"><path d="M3 9l9-6 9 6v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg></div>
        <div class="rv-industries__item-name">Local Services</div>
      </div>
      <div class="rv-industries__item">
        <div class="rv-industries__item-icon"><svg viewBox="0 0 24 24"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"/></svg></div>
        <div class="rv-industries__item-name">E-commerce</div>
      </div>
      <div class="rv-industries__item">
        <div class="rv-industries__item-icon"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/></svg></div>
        <div class="rv-industries__item-name">SaaS &amp; Tech</div>
      </div>
      <div class="rv-industries__item">
        <div class="rv-industries__item-icon"><svg viewBox="0 0 24 24"><path d="M3 21h18"/><path d="M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/></svg></div>
        <div class="rv-industries__item-name">Hospitality</div>
      </div>
      <div class="rv-industries__item">
        <div class="rv-industries__item-icon"><svg viewBox="0 0 24 24"><path d="M19 14V8a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6"/><path d="M3 14h18v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M7 6V4a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2"/></svg></div>
        <div class="rv-industries__item-name">Professional Services</div>
      </div>
      <div class="rv-industries__item">
        <div class="rv-industries__item-icon"><svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
        <div class="rv-industries__item-name">Health &amp; Wellness</div>
      </div>
    </div>
  </div>
</section>

<!-- TOOLS & TECH -->
<section class="rv-svc-extras rv-tools">
  <div class="rv-svc-extras__container">
    <div class="rv-tools__head">
      <span class="rv-tools__eyebrow">Tools &amp; tech we use</span>
      <h2 class="rv-tools__title">A modern stack, built for performance</h2>
      <p class="rv-tools__sub">We work with industry-standard platforms so your data, ads and websites are always on solid ground.</p>
    </div>
    <div class="rv-tools__grid">
      <div class="rv-tools__item"><span class="rv-tools__item-mark">GA4</span><span class="rv-tools__item-name">Google Analytics</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">GSC</span><span class="rv-tools__item-name">Search Console</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">Ads</span><span class="rv-tools__item-name">Google Ads</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">Meta</span><span class="rv-tools__item-name">Meta Ads Manager</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">SEM</span><span class="rv-tools__item-name">Semrush</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">Ahr</span><span class="rv-tools__item-name">Ahrefs</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">WF</span><span class="rv-tools__item-name">Webflow</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">WP</span><span class="rv-tools__item-name">WordPress</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">Sh</span><span class="rv-tools__item-name">Shopify</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">Fig</span><span class="rv-tools__item-name">Figma</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">HS</span><span class="rv-tools__item-name">HubSpot</span></div>
      <div class="rv-tools__item"><span class="rv-tools__item-mark">Mc</span><span class="rv-tools__item-name">Mailchimp</span></div>
    </div>
  </div>
</section>
''' + MARKER_END

s2 = s[:sec_start] + NEW + s[sec_end:]
P.write_text(s2)
print(f'services.html: replaced {sec_end-sec_start} chars with {len(NEW)} chars')
