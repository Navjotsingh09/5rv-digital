#!/usr/bin/env python3
"""
Generate 12 case study pages from the Hilston Park template.
Writes to disk via plain file I/O (per file-persistence note in memory).
"""
import os, pathlib

ROOT = pathlib.Path(__file__).parent

# ---------------------------------------------------------------------------
# Per-client content
# ---------------------------------------------------------------------------
CLIENTS = [
    {
        "slug": "bt-sports",
        "name": "BT Sports",
        "title_meta": "BT Sports — 5RV Digital | Case Study",
        "desc_meta": "BT Sports vendor case study — strategic product launch consultancy for UK market entry by 5RV Digital.",
        "tags": ["Strategy", "Product Launch", "Consultancy"],
        "lead": "We partnered with a BT Sport vendor to shape a strategic UK market launch — sharpening positioning, mapping the audience and giving the team a clear playbook for entering a competitive digital category with confidence.",
        "industry": "Sports &amp; Broadcast",
        "services_short": "Strategy · Launch",
        "engagement": "Project engagement",
        "hero_img": "BT-Sports-Hero",
        "gallery": ["BT-Sports-Hero", "Rectangle-6-1", "Rectangle-7-1"],
        "challenge": [
            "Entering the UK sports-tech market meant cutting through a noisy, crowded category dominated by household names. Our partner had a strong product but no clear positioning, no go-to-market playbook and limited visibility in the territory.",
            "The brief: define who they were for, sharpen the message and give the leadership team a launch plan they could actually execute against.",
        ],
        "approach": [
            "We ran a focused discovery — competitor mapping, audience interviews and a positioning workshop with the leadership team. From there we shaped the campaign architecture, channel mix and messaging framework.",
            "The result is a launch strategy built on insight, not guesswork — with a clear target, a memorable message and a measurable plan for the first 90 days.",
        ],
        "services": [
            ("strategy", "Campaign Planning", "Objectives, audience insights and messaging hierarchy — packaged into a clear go-to-market plan."),
            ("digital", "Digital Strategy", "Platform selection, targeting and content recommendations to maximise launch impact and reach."),
            ("brand", "Brand Consultation", "Creative direction on visuals, messaging and positioning so every channel feels like one product."),
        ],
    },
    {
        "slug": "contello",
        "name": "Contello",
        "title_meta": "Contello — 5RV Digital | Case Study",
        "desc_meta": "Contello case study — website redevelopment, SEO and content strategy for a high-end home automation and cinema brand by 5RV Digital.",
        "tags": ["Web Design", "SEO", "Content"],
        "lead": "Contello delivers bespoke home automation and cinema solutions for premium homes. To match the calibre of the product, we rebuilt their digital presence from the ground up — site, content and search.",
        "industry": "Home Automation &amp; Cinema",
        "services_short": "Web · SEO · Content",
        "engagement": "Ongoing partner",
        "hero_img": "Contello-Hero",
        "gallery": ["Contello-Hero", "Rectangle-6-5", "Rectangle-7-5"],
        "challenge": [
            "Contello had a premium product but a digital presence that didn't quite show it. The old site was dated, service pages were thin and the content wasn't earning the search visibility a brand of this calibre deserves.",
            "The brief: a modern, high-end site that mirrors the craftsmanship of the product, plus a content and SEO foundation built to attract qualified, intent-led leads.",
        ],
        "approach": [
            "We rebuilt the website around clear, image-led service pages for Home Automation and Home Cinema, layered in trust signals — testimonials, certifications, project stories — and shaped a content plan designed to rank for the searches that actually matter.",
            "The outcome is a digital presence that genuinely reflects the brand: confident, considered and built to convert.",
        ],
        "services": [
            ("web", "Web Design &amp; Development", "A modern, image-led site with clear navigation and service pages built around the customer journey."),
            ("seo", "SEO &amp; Service Pages", "Optimised pages for Home Automation and Home Cinema, structured to rank and to convert."),
            ("content", "Content Strategy", "Blogs, guides and project stories — an SEO-focused content plan that showcases real expertise."),
        ],
    },
    {
        "slug": "halesowen-dental",
        "name": "Halesowen Dental",
        "title_meta": "Halesowen Dental — 5RV Digital | Case Study",
        "desc_meta": "Halesowen Dental case study — local SEO, social campaigns and PPC delivered by 5RV Digital to grow patient enquiries.",
        "tags": ["Local SEO", "PPC", "Social"],
        "lead": "A trusted local practice that wasn't being found by the patients on its doorstep — we partnered with Halesowen Dental on a local SEO, social and PPC programme designed to put them top-of-mind in the area.",
        "industry": "Healthcare &amp; Dentistry",
        "services_short": "Local SEO · PPC",
        "engagement": "Ongoing partner",
        "hero_img": "Dental-Hero",
        "gallery": ["Dental-Hero", "Rectangle-6-2_1", "Rectangle-7-2_1"],
        "challenge": [
            "Halesowen Dental had a strong reputation in the chair but limited online visibility — local patients searching for cosmetic dentistry, Invisalign and routine care simply weren't finding them.",
            "The brief: lift local search rankings, sharpen the Invisalign campaign, and turn more website visits into booked consultations.",
        ],
        "approach": [
            "We started with local SEO foundations — Google Business Profile, citations, on-page work — then ran tightly-targeted Facebook and Google Ads campaigns alongside a refreshed Invisalign landing page and improved enquiry form.",
            "Online flyers, social content and offline collateral all kept a consistent look and feel, so the brand felt unified across every patient touchpoint.",
        ],
        "services": [
            ("seo", "Local SEO for Dentists", "On-page work, Google Business optimisation and locally-focused content to dominate the area's searches."),
            ("ppc", "Paid Ads (Google &amp; Facebook)", "Targeted campaigns built around real patient intent — Invisalign, cosmetic, routine care."),
            ("design", "Creative &amp; Print", "Flyers, banners and social templates to keep the brand consistent online and offline."),
        ],
    },
    {
        "slug": "halle-properties",
        "name": "Halle Properties",
        "title_meta": "Halle Properties — 5RV Digital | Case Study",
        "desc_meta": "Halle Properties case study — real estate SEO, paid ads and brand work delivered by 5RV Digital for a UK estate agency.",
        "tags": ["SEO", "Paid Ads", "Strategy"],
        "lead": "A trusted local estate agency in need of a digital presence that matched its on-the-ground reputation — we built a focused SEO and paid programme designed to put properties in front of the right buyers and sellers.",
        "industry": "Real Estate &amp; Property",
        "services_short": "SEO · Paid Ads",
        "engagement": "Ongoing partner",
        "hero_img": "HALLE-HERO",
        "gallery": ["HALLE-HERO", "Rectangle-6-7", "Rectangle-7-11"],
        "challenge": [
            "Halle Properties helps clients buy, sell and rent across the area — but their digital presence wasn't reflecting the strength of their local reputation. Listings were getting lost, enquiries were inconsistent and the brand voice felt scattered across channels.",
            "The brief: a joined-up SEO and paid strategy that drives qualified buyer and vendor enquiries, plus a brand voice that feels professional and unmistakably Halle.",
        ],
        "approach": [
            "We tightened SEO foundations across the property pages, layered in targeted Google and social ads, and gave the team a brand voice guide they could lean on for listings, social posts and enquiry follow-ups.",
            "Performance is reviewed monthly so spend follows what's actually generating enquiries — not vanity clicks.",
        ],
        "services": [
            ("seo", "Real Estate SEO", "On-page optimisation across listings and service pages, with a focus on local intent searches."),
            ("ppc", "Targeted Digital Ads", "Google and social campaigns built around buyer and vendor intent, optimised in real time."),
            ("brand", "Brand Voice", "A consistent, professional tone across listings, social and follow-ups."),
        ],
    },
    {
        "slug": "iv-land",
        "name": "IV Land",
        "title_meta": "IV Land — 5RV Digital | Case Study",
        "desc_meta": "IV Land case study — brand identity, website and digital strategy for a strategic land development consultancy by 5RV Digital.",
        "tags": ["Branding", "Web Design", "Strategy"],
        "lead": "A strategic land development consultancy entering the market — we shaped the brand from logo to website to social, positioning IV Land as a trusted, forward-thinking partner in sustainable development.",
        "industry": "Land &amp; Development",
        "services_short": "Branding · Web",
        "engagement": "Launch partner",
        "hero_img": "IVLAND-HERO",
        "gallery": ["IVLAND-HERO", "Rectangle-6-8", "Rectangle-7-8"],
        "challenge": [
            "IV Land needed a brand and digital presence that could open doors with landowners, developers and local authorities — credible, considered and clearly different from the typical land consultancy.",
            "The brief: build the brand identity and digital toolkit from scratch, ready to support business development from day one.",
        ],
        "approach": [
            "We worked closely with the founders on positioning, then designed a logo, brand system and supporting collateral — business cards, deck templates, a launch website and a social rollout.",
            "The outcome is a cohesive, credible identity that reflects IV Land's values and gives the team the confidence to pitch at any level.",
        ],
        "services": [
            ("brand", "Brand Identity", "Logo, colour, typography and a complete brand system — designed to feel premium without being precious."),
            ("web", "Website Design &amp; Build", "A clear, credible launch site that tells the story and supports business development conversations."),
            ("social", "Social &amp; Strategy", "A practical social plan and tone-of-voice guide so the team can show up consistently."),
        ],
    },
    {
        "slug": "klassic-trade-frames",
        "name": "Klassic Trade Frames",
        "title_meta": "Klassic Trade Frames — 5RV Digital | Case Study",
        "desc_meta": "Klassic Trade Frames case study — website redesign and SEO for a Birmingham aluminium fabrication specialist, by 5RV Digital.",
        "tags": ["Web Design", "SEO", "Branding"],
        "lead": "A respected Birmingham fabricator with deep technical heritage — we rebuilt their website and SEO foundation to turn that expertise into qualified trade enquiries.",
        "industry": "Manufacturing &amp; Fabrication",
        "services_short": "Web · SEO",
        "engagement": "Project engagement",
        "hero_img": "Klassic-Frames-Hero",
        "gallery": ["Klassic-Frames-Hero", "Rectangle-6-9", "Rectangle-7-9"],
        "challenge": [
            "Klassic Trade Frames specialises in high-quality aluminium doors, windows, conservatories and REHAU profile fabrication — but the existing website didn't carry the weight of that expertise or surface in trade searches.",
            "The brief: modernise the digital presence, sharpen the SEO foundations and make it easier for trade buyers to get in touch.",
        ],
        "approach": [
            "We rebuilt the site around clear product and capability pages, mapped content to the searches trade buyers actually use, and tightened the technical SEO so the team could compete on local fabrication keywords.",
            "The outcome is a professional digital platform that does justice to the manufacturing pedigree — and starts conversations with the right buyers.",
        ],
        "services": [
            ("web", "Website Design &amp; Build", "A modern, trade-led site that showcases capability and makes enquiry effortless."),
            ("seo", "SEO Strategy", "Local, trade-focused keyword mapping plus on-page and technical optimisation."),
            ("brand", "Brand Integration", "Consistent identity across the site, content and customer-facing materials."),
        ],
    },
    {
        "slug": "lightologist",
        "name": "Lightologist",
        "title_meta": "Lightologist — 5RV Digital | Case Study",
        "desc_meta": "Lightologist case study — e-commerce build, SEO and paid ads for a premium UK lighting retailer by 5RV Digital.",
        "tags": ["E-commerce", "SEO", "Paid Ads"],
        "lead": "The lighting division of Sunny Electrical Supplies — 20+ years of expertise in premium lighting for homes and businesses. We rebuilt the e-commerce experience and growth engine behind it.",
        "industry": "E-commerce &amp; Retail",
        "services_short": "E-commerce · SEO",
        "engagement": "Ongoing partner",
        "hero_img": "Contello-Hero",
        "gallery": ["Rectangle-6-6", "Rectangle-7-6", "Rectangle-6-1_1"],
        "challenge": [
            "Lightologist had two decades of expertise but an online store that wasn't pulling its weight — product discovery was clunky, search visibility was thin and paid spend wasn't translating into sales.",
            "The brief: a modern e-commerce platform with stock integration, plus an SEO and paid programme built to drive measurable growth.",
        ],
        "approach": [
            "We rebuilt the e-commerce site with proper stock integration and a much cleaner browsing experience, then layered in a focused SEO programme and paid campaigns aligned to the highest-intent searches.",
            "The result is a store that converts, supported by a search and paid engine that keeps qualified traffic flowing.",
        ],
        "services": [
            ("web", "E-commerce Development", "A modern store with integrated stock, faster product discovery and a smoother checkout."),
            ("seo", "SEO Strategy", "Keyword research, technical optimisation and content built around real buyer intent."),
            ("ppc", "Paid Advertising", "Google and social campaigns aligned to high-intent search and shopping behaviours."),
        ],
    },
    {
        "slug": "national-health-services",
        "name": "NHS",
        "title_meta": "NHS Vaccine Campaign — 5RV Digital | Case Study",
        "desc_meta": "NHS case study — multi-channel vaccine uptake campaign across digital and print, delivered by 5RV Digital.",
        "tags": ["Strategy", "Social", "Print"],
        "lead": "A multi-channel campaign to lift vaccine uptake in underserved communities — we blended digital, social and print to deliver inclusive, accessible communications people could trust.",
        "industry": "Healthcare &amp; Public Sector",
        "services_short": "Strategy · Social",
        "engagement": "Project engagement",
        "hero_img": "NHS-Hero",
        "gallery": ["NHS-Hero", "Rectangle-6-2", "Rectangle-7-2"],
        "challenge": [
            "Vaccine uptake in some communities sat well below the national average. Trust, language and access were all factors — and a one-size-fits-all message wasn't going to move the needle.",
            "The brief: a tailored, multi-channel campaign that meets people where they are, in language and formats they trust.",
        ],
        "approach": [
            "We combined audience research, targeted social campaigns and printed flyers distributed through schools, pharmacies and community venues — every asset reviewed for inclusivity, accessibility and clinical accuracy.",
            "The result is a clear digital roadmap and a strengthened, consistent message across every channel that touches the community.",
        ],
        "services": [
            ("strategy", "Campaign Planning", "Audience research, KPIs and a messaging framework built for sensitivity and reach."),
            ("social", "Social Strategy", "Facebook and Instagram campaigns designed for the specific communities being reached."),
            ("design", "Print &amp; Distribution", "Flyer design and distribution through schools, pharmacies and community venues."),
        ],
    },
    {
        "slug": "pass-11-plus",
        "name": "Pass 11+",
        "title_meta": "Pass 11+ — 5RV Digital | Case Study",
        "desc_meta": "Pass 11+ case study — website build, content and local SEO for an 11+ tuition specialist by 5RV Digital.",
        "tags": ["Web Design", "Content", "SEO"],
        "lead": "An 11+ tuition specialist that needed a digital home for parents to discover, trust and engage — we built the website, sharpened the content and laid the SEO groundwork.",
        "industry": "Education &amp; Tuition",
        "services_short": "Web · Content · SEO",
        "engagement": "Ongoing partner",
        "hero_img": "Pass-11-hero",
        "gallery": ["Pass-11-hero", "Copy-of-Untitled-1", "Rectangle-7-3_1"],
        "challenge": [
            "Pass 11+ had a strong reputation among local families but no proper digital home — parents searching for trusted 11+ tuition were landing on competitors instead.",
            "The brief: a clear, parent-friendly website that showcases credibility, plus the SEO and Google Business work to make sure the right families actually find it.",
        ],
        "approach": [
            "We built a bespoke, easy-to-navigate site, wrote content that speaks directly to parents (not students), and optimised local search and Google Business Profile so the practice surfaces for the right enquiries.",
            "The outcome is a brand that finally feels as credible online as it is in person.",
        ],
        "services": [
            ("web", "Website Development", "A bespoke, parent-friendly site that highlights teaching credibility and student outcomes."),
            ("content", "Content &amp; Copy", "Clear, reassuring copy written for the parents making the decision."),
            ("seo", "Local SEO", "On-page work and Google Business optimisation to capture local family searches."),
        ],
    },
    {
        "slug": "qcom-ltd",
        "name": "Qcom Ltd",
        "title_meta": "Qcom Ltd — 5RV Digital | Case Study",
        "desc_meta": "Qcom Ltd case study — brand, website and SEO for a managed IT and digital transformation specialist by 5RV Digital.",
        "tags": ["Branding", "Web Design", "SEO"],
        "lead": "A managed IT and digital transformation specialist helping businesses innovate — we sharpened the brand, rebuilt the website and gave the search and paid presence room to grow.",
        "industry": "IT &amp; Technology",
        "services_short": "Brand · Web · SEO",
        "engagement": "Ongoing partner",
        "hero_img": "QCOM-HERO",
        "gallery": ["QCOM-HERO", "Rectangle-6-2_2", "Rectangle-7_2"],
        "challenge": [
            "Qcom delivers serious technical capability but the brand and digital presence weren't carrying that authority. Service pages were generic, the brand felt undefined and search wasn't doing the team any favours.",
            "The brief: a sharper brand, a website that actually sells the offering, and SEO plus paid built to pull in qualified IT buyers.",
        ],
        "approach": [
            "We refined the brand identity, rebuilt the site around clear service pillars — IT support, consultancy and digital transformation — and ran focused SEO and paid programmes aligned to high-intent buyer searches.",
            "The result is a digital presence that finally matches the technical credibility the team has earned.",
        ],
        "services": [
            ("brand", "Brand Identity", "A sharper, more credible identity that reflects Qcom's technical authority."),
            ("web", "Website Design &amp; Build", "Clear service pages structured around how IT buyers actually evaluate providers."),
            ("seo", "SEO &amp; Paid Ads", "Focused campaigns and on-page work that pull in qualified IT decision-makers."),
        ],
    },
    {
        "slug": "university-of-birmingham",
        "name": "University of Birmingham",
        "title_meta": "University of Birmingham — 5RV Digital | Case Study",
        "desc_meta": "University of Birmingham case study — student engagement campaign across web, social and print delivered by 5RV Digital.",
        "tags": ["Strategy", "Social", "Print"],
        "lead": "A student engagement campaign that needed to land on a busy campus — we combined a custom campaign hub, student-led social and printed materials to drive measurable digital engagement.",
        "industry": "Higher Education",
        "services_short": "Strategy · Web · Social",
        "engagement": "Project engagement",
        "hero_img": "UOB-Hero",
        "gallery": ["UOB-Hero", "uni-bir-student", "Rectangle-7-3"],
        "challenge": [
            "The University needed a clearer way to connect students with key services and events — competing with the constant noise of campus life and a saturated student inbox.",
            "The brief: a campaign hub students would actually use, supported by social and print that meet them where they already are.",
        ],
        "approach": [
            "We built a custom campaign hub, ran organic and paid social tuned for a student audience, and designed printed materials placed in the right corners of campus — all stitched together with a clear creative through-line.",
            "The campaign drove measurable engagement and traffic, and gave the University a repeatable playbook for future student campaigns.",
        ],
        "services": [
            ("web", "Campaign Hub Build", "A custom microsite designed around student user-flows, not corporate templates."),
            ("social", "Student-Led Social", "Organic and paid campaigns tuned to the platforms and tone students actually engage with."),
            ("design", "Print &amp; On-Campus", "Printed flyers and on-campus materials designed to cut through the noise."),
        ],
    },
    {
        "slug": "w13",
        "name": "W13",
        "title_meta": "W13 — 5RV Digital | Case Study",
        "desc_meta": "W13 case study — content, social and paid strategy for a West Midlands sustainable architecture and development firm, by 5RV Digital.",
        "tags": ["Content", "Social", "Paid Ads"],
        "lead": "A West Midlands building and development firm with 20+ years creating sustainable spaces — we lifted the digital presence with focused content, cross-platform social and paid built around real intent.",
        "industry": "Architecture &amp; Development",
        "services_short": "Content · Social · Paid",
        "engagement": "Ongoing partner",
        "hero_img": "w13-Hero",
        "gallery": ["w13-Hero", "Rectangle-6-10", "Rectangle-7-10"],
        "challenge": [
            "W13 had genuinely impressive work and strong values around sustainability and community — but the digital presence wasn't telling that story. Inconsistent social, generic content and no real paid strategy meant the brand felt smaller online than on the ground.",
            "The brief: a content and social rhythm that surfaces the work, reinforces the values and drives qualified enquiries.",
        ],
        "approach": [
            "We shaped a content strategy around the portfolio, expertise and community focus — then ran cross-platform social on LinkedIn, Instagram and X, supported by Google Ads tuned for retargeting and high-intent keywords.",
            "The result is a digital presence that finally reflects the calibre of the work — and positions W13 as a leader in sustainable, socially responsible architecture.",
        ],
        "services": [
            ("content", "Content Strategy", "Portfolio-led content that surfaces the work, expertise and community values."),
            ("social", "Cross-Platform Social", "LinkedIn, Instagram and X — tuned for the audiences that actually commission this work."),
            ("ppc", "Paid Ads &amp; Retargeting", "Google Ads built around high-intent keywords and audience retargeting."),
        ],
    },
]

# Service icon SVGs (paths only, used inside the cs-svc-card icon)
SVC_ICON = {
    "strategy": '<svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
    "digital":  '<svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>',
    "brand":    '<svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
    "web":      '<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>',
    "seo":      '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "ppc":      '<svg viewBox="0 0 24 24"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    "content":  '<svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
    "social":   '<svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>',
    "design":   '<svg viewBox="0 0 24 24"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>',
}


# ---------------------------------------------------------------------------
# Read the master template (Hilston Park) so we inherit any future tweaks
# ---------------------------------------------------------------------------
TEMPLATE_PATH = ROOT / "hilstonpark.html"
TEMPLATE = TEMPLATE_PATH.read_text(encoding="utf-8")


def render_meta_cells(c):
    return (
        f'<div class="cs-meta__cell"><p class="cs-meta__label">Client</p><p class="cs-meta__value">{c["name"]}</p></div>\n'
        f'        <div class="cs-meta__cell"><p class="cs-meta__label">Industry</p><p class="cs-meta__value">{c["industry"]}</p></div>\n'
        f'        <div class="cs-meta__cell"><p class="cs-meta__label">Services</p><p class="cs-meta__value">{c["services_short"]}</p></div>\n'
        f'        <div class="cs-meta__cell"><p class="cs-meta__label">Engagement</p><p class="cs-meta__value">{c["engagement"]}</p></div>'
    )


def render_tags(tags):
    return "\n        ".join(f'<span class="cs-tag">{t}</span>' for t in tags)


def render_hero_media(c):
    img = c["hero_img"]
    return (
        f'<img src="images/{img}.webp"\n'
        f'             srcset="images/{img}-p-800.webp 800w, images/{img}-p-1080.webp 1080w"\n'
        f'             sizes="(max-width:960px) 92vw, 1180px"\n'
        f'             alt="{c["name"]} case study" loading="eager" fetchpriority="high">'
    )


def render_overview(c):
    challenge = "\n          ".join(f"<p>{p}</p>" for p in c["challenge"])
    approach  = "\n          ".join(f"<p>{p}</p>" for p in c["approach"])
    return f"""<div class="cs-overview__col">
          <h2>The Challenge</h2>
          {challenge}
        </div>
        <div class="cs-overview__col">
          <h2>Our Approach</h2>
          {approach}
        </div>"""


def render_services(services):
    cards = []
    for icon_key, title, body in services:
        icon = SVC_ICON.get(icon_key, SVC_ICON["strategy"])
        cards.append(f"""<div class="cs-svc-card">
          <div class="cs-svc-card__icon">
            {icon}
          </div>
          <h3>{title}</h3>
          <p>{body}</p>
        </div>""")
    return "\n        ".join(cards)


def render_gallery(gallery):
    big = gallery[0]
    rest = gallery[1:3] if len(gallery) >= 3 else gallery[1:] + [gallery[0]]
    items = [f'<div class="cs-gallery__item cs-gallery__item--big">\n          <img src="images/{big}.webp" alt="Project visual" loading="lazy">\n        </div>']
    for g in rest:
        items.append(f'<div class="cs-gallery__item">\n          <img src="images/{g}.webp" alt="Project visual" loading="lazy">\n        </div>')
    return "\n        ".join(items)


def build_page(c):
    out = TEMPLATE

    # ---- <head> meta ----
    out = out.replace(
        "<title>Hilston Park — 5RV Digital | Case Study</title>",
        f"<title>{c['title_meta']}</title>",
    )
    out = out.replace(
        '<meta name="description" content="Hilston Park case study — branding, social media and digital strategy delivered by 5RV Digital.">',
        f'<meta name="description" content="{c["desc_meta"]}">',
    )
    out = out.replace(
        '<meta property="og:title" content="Hilston Park — Case Study | 5RV Digital">',
        f'<meta property="og:title" content="{c["title_meta"]}">',
    )
    out = out.replace(
        '<meta property="og:description" content="How 5RV Digital approached branding and social for Hilston Park.">',
        f'<meta property="og:description" content="{c["desc_meta"]}">',
    )

    # ---- Hero block (breadcrumb cur, tags, h1, lead, media, meta) ----
    old_hero = """<nav class="cs-hero__crumbs" aria-label="Breadcrumb">
        <a href="index.html">Home</a><span>/</span><a href="work.html">Work</a><span>/</span><span class="cur">Hilston Park</span>
      </nav>
      <div class="cs-hero__tags">
        <span class="cs-tag">Branding</span>
        <span class="cs-tag">Social Media</span>
        <span class="cs-tag">Strategy</span>
      </div>
      <h1 class="cs-hero__title">Hilston Park</h1>
      <p class="cs-hero__lead">A heritage estate stepping into a new chapter — we partnered with Hilston Park to refresh the way the brand looks, sounds and shows up across social, building a visual language that feels timeless without feeling tired.</p>
      <div class="cs-hero__media">
        <img src="images/Hilston-Park-Her0.webp"
             srcset="images/Hilston-Park-Her0-p-800.webp 800w, images/Hilston-Park-Her0-p-1080.webp 1080w, images/Hilston-Park-Her0-p-1600.webp 1600w, images/Hilston-Park-Her0-p-2000.webp 2000w, images/Hilston-Park-Her0-p-2600.webp 2600w"
             sizes="(max-width:960px) 92vw, 1180px"
             alt="Hilston Park brand work" loading="eager" fetchpriority="high">
      </div>
      <div class="cs-meta">
        <div class="cs-meta__cell"><p class="cs-meta__label">Client</p><p class="cs-meta__value">Hilston Park</p></div>
        <div class="cs-meta__cell"><p class="cs-meta__label">Industry</p><p class="cs-meta__value">Hospitality &amp; Events</p></div>
        <div class="cs-meta__cell"><p class="cs-meta__label">Services</p><p class="cs-meta__value">Branding · Social</p></div>
        <div class="cs-meta__cell"><p class="cs-meta__label">Engagement</p><p class="cs-meta__value">Ongoing partner</p></div>
      </div>"""

    new_hero = f"""<nav class="cs-hero__crumbs" aria-label="Breadcrumb">
        <a href="index.html">Home</a><span>/</span><a href="work.html">Work</a><span>/</span><span class="cur">{c['name']}</span>
      </nav>
      <div class="cs-hero__tags">
        {render_tags(c['tags'])}
      </div>
      <h1 class="cs-hero__title">{c['name']}</h1>
      <p class="cs-hero__lead">{c['lead']}</p>
      <div class="cs-hero__media">
        {render_hero_media(c)}
      </div>
      <div class="cs-meta">
        {render_meta_cells(c)}
      </div>"""

    if old_hero not in out:
        raise RuntimeError(f"hero block not matched for {c['slug']}")
    out = out.replace(old_hero, new_hero)

    # ---- Overview block ----
    old_overview = """<div class="cs-overview__col">
          <h2>The Challenge</h2>
          <p>Hilston Park has a story most venues can only dream of — but its visual identity and digital presence weren't doing it justice. Inconsistent imagery, a quiet social feed and messaging that drifted between weddings, corporate events and stays meant the brand felt smaller online than it does in person.</p>
          <p>The brief: tighten the brand, give the team an easy-to-run social rhythm, and make sure every touchpoint feels like the same place.</p>
        </div>
        <div class="cs-overview__col">
          <h2>Our Approach</h2>
          <p>We started with a brand audit and a few quiet conversations — what does Hilston Park really stand for, who is it for, what do guests remember after they leave. From there we shaped a refreshed visual system, a clear social playbook and a content cadence the in-house team could actually maintain.</p>
          <p>The result is a brand that feels confident, consistent and unmistakably Hilston — across every grid, story and stay.</p>
        </div>"""

    if old_overview not in out:
        raise RuntimeError(f"overview block not matched for {c['slug']}")
    out = out.replace(old_overview, render_overview(c))

    # ---- Services grid ----
    old_services = """<div class="cs-svc-card">
          <div class="cs-svc-card__icon">
            <svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
          </div>
          <h3>Brand Refresh</h3>
          <p>Logo lockups, colour, type, photographic direction and a tone-of-voice guide — packaged into a usable mini brand book.</p>
        </div>
        <div class="cs-svc-card">
          <div class="cs-svc-card__icon">
            <svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98"/></svg>
          </div>
          <h3>Social Media</h3>
          <p>Monthly content planning, on-brand templates and a shooting brief — so every post feels like Hilston, not like an afterthought.</p>
        </div>
        <div class="cs-svc-card">
          <div class="cs-svc-card__icon">
            <svg viewBox="0 0 24 24"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
          </div>
          <h3>Digital Strategy</h3>
          <p>A clear plan that ties the website, social and enquiries together — with a simple way to measure what's actually working.</p>
        </div>"""

    if old_services not in out:
        raise RuntimeError(f"services block not matched for {c['slug']}")
    out = out.replace(old_services, render_services(c["services"]))

    # ---- Gallery ----
    old_gallery = """<div class="cs-gallery__item cs-gallery__item--big">
          <img src="images/Hilston-Park-Her0-p-1600.webp" alt="Hilston Park hero visual" loading="lazy">
        </div>
        <div class="cs-gallery__item">
          <img src="images/Rectangle-10.webp" alt="Brand application" loading="lazy">
        </div>
        <div class="cs-gallery__item">
          <img src="images/Rectangle-11.webp" alt="Social content" loading="lazy">
        </div>"""

    if old_gallery not in out:
        raise RuntimeError(f"gallery block not matched for {c['slug']}")
    out = out.replace(old_gallery, render_gallery(c["gallery"]))

    return out


def main():
    written = []
    for c in CLIENTS:
        page = build_page(c)
        path = ROOT / f"{c['slug']}.html"
        path.write_text(page, encoding="utf-8")
        written.append((c["slug"], len(page), path.stat().st_size))
        print(f"  wrote {c['slug']:30s}  {path.stat().st_size:>8d} bytes")

    print(f"\nDone. {len(written)} pages written.")


if __name__ == "__main__":
    main()
