#!/usr/bin/env python3
"""Builds the multi-page Ternah site: standalone .html files sharing one CSS + JS."""

import os, pathlib
OUT = str(pathlib.Path(__file__).parent)  # writes next to this script

MARK_PATHS = ('<path d="M27 14 L45 14 C47 14 48 16 47 18 L38 41 C37 43 34 43 33 41 L24 19 C23 16 24 14 27 14 Z"/>'
              '<path d="M58 14 L84 14 C86 14 87 16 87 18 L87 34 C87 37 84 38 82 36 L74 30 L34 78 C33 79 31 80 29 80 L18 80 C15 80 14 77 16 75 L58 14 Z"/>'
              '<path d="M73 78 L55 78 C53 78 52 76 53 74 L62 51 C63 49 66 49 67 51 L76 73 C77 76 76 78 73 78 Z"/>')

def MK(color, cls="mk", style=""):
    return f'<svg class="{cls}" viewBox="0 0 100 94"{f" style=\"{style}\"" if style else ""}><g fill="{color}">{MARK_PATHS}</g></svg>'

ARROW = ('<svg class="arrow" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" '
         'stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>')

ICONS = {
 'code':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
 'layers':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
 'flow':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M9 6h6a2 2 0 0 1 2 2v7"/></svg>',
 'chart':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
 'cloud':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>',
 'support':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></svg>',
 'edu':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>',
 'health':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
 'truck':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
 'cart':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>',
 'globe':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
 'bank':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>',
 'gov':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6"/></svg>',
 'mail':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
 'phone':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
 'pin':'<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
}

# ---------------- shared shell ----------------
NAV_ITEMS = [('index','Home'),('about','About'),('solutions','Solutions'),
             ('industries','Industries'),('products','Products'),('insights','Insights'),('contact','Contact')]

def nav_links():
    out=[]
    for slug,label in NAV_ITEMS:
        href = 'index.html' if slug=='index' else f'{slug}.html'
        out.append(f'<a href="{href}" data-nav="{slug}">{label}</a>')
    return "\n      ".join(out)

def header_html():
    return f'''<header id="hdr">
  <div class="nav">
    <a class="brand" href="index.html">
      {MK('#fff')}
      <span class="wm">TERNAH</span>
    </a>
    <nav class="navlinks" id="navlinks">
      {nav_links()}
    </nav>
    <a class="nav-cta" href="contact.html">Start a Project</a>
    <div class="burger" id="burger"><span></span><span></span><span></span></div>
  </div>
</header>'''

def footer_html():
    return f'''<footer>
  <div class="foot">
    <div>
      <a class="brand" href="index.html">{MK('#fff','mk','width:34px;height:32px')}<span class="wm">TERNAH</span></a>
      <p style="margin-top:20px">Software Company Ltd. Building Africa's digital future: practical, scalable, reliable software, crafted to fit.</p>
    </div>
    <div>
      <h4>Company</h4>
      <a href="about.html">About</a><a href="solutions.html">Solutions</a>
      <a href="industries.html">Industries</a><a href="products.html">Products</a><a href="insights.html">Insights</a>
    </div>
    <div>
      <h4>Solutions</h4>
      <a href="solutions.html">Custom Software</a><a href="solutions.html">ERP &amp; Business Systems</a>
      <a href="solutions.html">Automation</a><a href="solutions.html">Data &amp; Analytics</a><a href="solutions.html">Cloud Solutions</a>
    </div>
    <div>
      <h4>Get in touch</h4>
      <a href="mailto:ternah22@gmail.com">ternah22@gmail.com</a>
      <a href="https://wa.me/256787770007" target="_blank" rel="noopener noreferrer">WhatsApp</a>
      <a href="contact.html">Start a Project</a>
    </div>
  </div>
  <div class="foot-bot">
    <span>© <span id="yr"></span> Ternah Software Company Ltd. All rights reserved.</span>
    <span class="slg">Keep it simple.</span>
  </div>
</footer>'''

SITE_URL  = 'https://ternah.onrender.com'   # update to your custom domain when ready
OG_IMAGE  = f'{SITE_URL}/assets/og-image.svg'

def page(slug, title, desc, body):
    canonical = f'{SITE_URL}/{slug}.html' if slug != 'index' else SITE_URL
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">

<!-- canonical -->
<link rel="canonical" href="{canonical}">

<!-- favicon -->
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="shortcut icon" href="assets/favicon.svg">
<meta name="theme-color" content="#2f4cff">

<!-- open graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Ternah Software Company Ltd">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">

<!-- twitter / x card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMAGE}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body data-page="{slug}">

{header_html()}

<main class="fade-in">
{body}
</main>

{footer_html()}

<!-- floating contact buttons -->
<div class="fab-group">
  <a class="fab fab-wa" href="https://wa.me/256787770007" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp" data-tip="WhatsApp">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="#fff" xmlns="http://www.w3.org/2000/svg">
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
    </svg>
  </a>
  <a class="fab fab-email" href="mailto:ternah22@gmail.com" aria-label="Send us an email" data-tip="Email us">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>
    </svg>
  </a>
  <a class="fab fab-call" href="tel:+256787770007" aria-label="Call us" data-tip="Call us">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.13 12.6a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L7.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>
    </svg>
  </a>
</div>

<script src="assets/js/main.js"></script>
</body>
</html>'''

# ---------------- content data ----------------
SOLUTIONS = [
 ('code','Custom Software Development','Enterprise systems, web applications, and business platforms engineered around your exact processes.',['Enterprise Software','Web Applications','Business Management Systems','E-Commerce Platforms']),
 ('layers','ERP & Business Systems','Unified ERP, CRM, inventory, school and healthcare information systems that connect every part of your operation.',['ERP Systems','CRM Systems','Inventory Management','School & Healthcare Systems']),
 ('flow','Automation','Replace manual work with intelligent workflows, approvals, and digital documentation that run themselves.',['Business Process Automation','Workflow Management','Digital Documentation','Org Digitization']),
 ('chart','Data & Analytics','Turn raw data into decisions with dashboards, reporting, and decision-support built for clarity.',['BI Dashboards','Data Analytics','Reporting Systems','Decision Support']),
 ('cloud','Cloud Solutions','Business email, collaboration, migration, and infrastructure that scale with your team.',['Business Email','Cloud Collaboration','Google Workspace','Data Migration']),
 ('support','Support & Managed Services','Maintenance, monitoring, security updates and optimization that keep everything running.',['Software Maintenance','System Monitoring','Security Updates','Performance Optimization']),
]
INDUSTRIES = [
 ('edu','Education','School management, e-learning, and student information systems for institutions of every size.'),
 ('health','Healthcare','Patient records, clinic operations, and health information systems built for reliability.'),
 ('truck','Logistics','Fleet, supply chain, and delivery platforms that track and optimize every movement.'),
 ('cart','Retail & Commerce','POS, inventory, and e-commerce systems that connect storefronts to the cloud.'),
 ('globe','NGOs & Development','Field data collection, M&E dashboards, and donor reporting for impact organizations.'),
 ('gov','Government','Digital public services, monitoring platforms, and secure institutional systems.'),
 ('bank','Financial Services','Secure platforms for payments, lending, and member management at scale.'),
 ('layers','Enterprises & SMEs','Operational platforms that help growing businesses move faster with less friction.'),
]
VALUES = [
 ('Innovation','We continuously seek better ways to solve complex challenges through technology.'),
 ('Excellence','We maintain the highest standards in everything we design, develop, and deliver.'),
 ('Integrity','We operate with honesty, accountability, and professionalism.'),
 ('Reliability','We build systems and partnerships that our clients can depend upon.'),
 ('Collaboration','Great solutions are achieved through teamwork and strong client relationships.'),
 ('Impact','We measure success by the positive transformation our solutions create.'),
]
OBJECTIVES = [
 ('01','Deliver Excellence','Fast, secure, reliable, scalable software that lets organizations operate efficiently and grow confidently.'),
 ('02','Accelerate Transformation','Move businesses from manual processes to intelligent digital systems that improve decision-making.'),
 ('03','African-Centered Solutions','Technology designed to solve the unique challenges and opportunities of African markets.'),
 ('04','Foster Innovation','A culture of continuous innovation using emerging technologies for practical, sustainable solutions.'),
 ('05','Support Growth','Contributing to economic development through technology, skills, and digital empowerment.'),
 ('06','Lasting Partnerships','Trusted relationships built on consistent value, reliability, and measurable results.'),
]
WHY = [
 ('01','Built to fit you','Software shaped around your exact processes, not a rigid template you bend to.'),
 ('02','African insight','Local understanding of the markets, constraints, and opportunities you operate in.'),
 ('03','Fast delivery','Pragmatic engineering that ships in weeks, not quarters.'),
 ('04','Scalable by design','Architecture that grows the moment your business does.'),
 ('05','End-to-end ownership','From strategy to deployment to support: one accountable team.'),
]
PROJECTS = [
 ('Real Estate · SaaS','Property Management Platform','Multi-tenant SaaS for property businesses with double-entry accounting, automated accruals, supplier ledgers, and VAT reporting.',['Django','SaaS','Accounting']),
 ('Retail · SaaS','Mykashop','One platform for stock, sales, debtors, expenses, and business performance. Built for shops, supermarkets, pharmacies, hardware stores, restaurants, and any growing retail business that needs real control.',['POS','Inventory','Multi-tenant'],'http://mykashop.online/'),
 ('Healthcare · EMR','Medical Records & Inventory','Electronic medical records with prescriptions, dispensing, automatic stock deduction, and lab management.',['EMR','Inventory','Compliance']),
 ('Web · Development','Static and Dynamic Websites','Professional static and dynamic websites for businesses, institutions, and organizations — fast to deploy, built to convert, and easy to manage.',['HTML/CSS','React','CMS']),
 ('Hospitality · Multi-tenant','Hospitality Operations Suite','Bar, restaurant, lodge, gym and service-queue modules under a super-admin licensing model.',['Multi-tenant','POS','Licensing']),
 ('Operations · Workflow','Queue & Workflow System','Kanban-style operator boards and multi-tenant queue management for service businesses.',['Kanban','Workflow','Realtime']),
 ('Healthcare · Pharmacy','Pharmacy Management System','End-to-end pharmacy operations covering drug inventory, dispensing, prescriptions, expiry tracking, supplier management, and sales reporting — built for clinics, hospitals, and standalone pharmacies.',['Dispensing','Inventory','Compliance']),
]
TESTIMONIALS = [
 ('Ternah understood our operation before writing a single line of code. The system fits exactly how we work.','Operations Director','SME, Kampala'),
 ('Fast, reliable, and genuinely invested in the outcome. They delivered ahead of schedule and stayed for support.','Program Manager','Development Agency'),
 ('The dashboards changed how our leadership makes decisions. Data we never had visibility into is now front and centre.','Finance Lead','Retail Group'),
]
INSIGHTS = [
 ('Digital Transformation','From manual to intelligent: a practical roadmap','How African organizations can move off spreadsheets and paper without disrupting daily operations.','8 min read'),
 ('Technology Trends','Why offline-first matters in African markets','Designing software that performs where connectivity is intermittent, and why it wins.','6 min read'),
 ('Guides','Choosing between off-the-shelf and custom software','A decision framework for when to buy, when to build, and how to avoid expensive mistakes.','10 min read'),
 ('Data & Analytics','Turning dashboards into decisions','The difference between reporting that informs and reporting that drives action.','7 min read'),
 ('Digital Transformation','Automation that pays for itself','Identifying the workflows where automation delivers the fastest, clearest return.','5 min read'),
 ('Technology Trends','Building for scale from day one','Architecture choices that save you a painful rebuild as your user base grows.','9 min read'),
]

# ---------------- content lists for homepage ----------------
PROCESS_STEPS = [
 ('Discover', 'We learn how your business actually runs before proposing anything.'),
 ('Design',   'We map the system to your exact workflow, simply and intentionally.'),
 ('Build',    'Pragmatic engineering with weekly visible progress you can follow.'),
 ('Ship',     'We deploy, test, and make sure every part lands correctly.'),
 ('Support',  'We stay for maintenance, updates, and growth long after launch.'),
]
INDUSTRIES_TICKER = ['Education','Healthcare','Logistics','Retail','NGOs','Government','Finance','Hospitality','Agriculture','Pharmacy','Real Estate','Manufacturing']

# ---------------- component templates ----------------
SOL_FILTERS = ['software','erp','automation','data','cloud','support']
def sol_card(i, s):
    ic,t,d,items = s
    lis = "".join(f'<li>{x}</li>' for x in items)
    filt = SOL_FILTERS[i] if i < len(SOL_FILTERS) else 'all'
    green = ' green-accent' if filt in ('erp','data','support') else ''
    return f'''    <div class="card{green} reveal" id="sol-{filt}" data-d="{(i%3)+1}" data-filter="{filt}">
      <div class="ico">{ICONS[ic]}</div>
      <h3>{t}</h3><p>{d}</p>
      <ul>{lis}</ul>
    </div>'''

def rows_tpl(arr):
    rows = "".join(f'''
    <div class="row reveal">
      <span class="rn">{n}</span>
      <div><div class="rt">{t}</div></div>
      <div class="rd">{d}</div>
      {ARROW}
    </div>''' for n,t,d in arr)
    return f'<div class="rows">{rows}</div>'

def ind_card(x):
    ic,t,d = x
    return f'''    <div class="ind reveal"><div class="ico">{ICONS[ic]}</div><h3>{t}</h3><p>{d}</p></div>'''

LIVE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'

def proj_card(i,p):
    cat,t,d,tags,*rest = p
    url = rest[0] if rest else None
    lis = "".join(f'<li>{x}</li>' for x in tags)
    heading = f'<h3><a class="card-link-title" href="{url}" target="_blank" rel="noopener noreferrer">{t}</a></h3>' if url else f'<h3>{t}</h3>'
    live = f'<a class="live-link" href="{url}" target="_blank" rel="noopener noreferrer">Visit live site {LIVE_SVG}</a>' if url else ''
    return f'''    <div class="card reveal" data-d="{(i%3)+1}">
      <div class="num">{cat}</div>{heading}<p>{d}</p><ul>{lis}</ul>{live}
    </div>'''

def svc_block(i, s):
    ic,t,d,_ = s
    filt = SOL_FILTERS[i] if i < len(SOL_FILTERS) else 'all'
    num  = str(i+1).zfill(2)
    return f'''    <div class="svc-item reveal" id="sol-{filt}" data-d="{(i%3)+1}" data-filter="{filt}">
      <div class="svc-num">{num}</div>
      <div class="svc-ico">{ICONS[ic]}</div>
      <h3>{t}</h3>
      <p>{d}</p>
    </div>'''

def proj_card_slim(i,p):
    cat,t,d,tags,*rest = p
    url = rest[0] if rest else None
    chips = "".join(f'<span class="chip">{x}</span>' for x in tags)
    heading = f'<h3><a class="card-link-title" href="{url}" target="_blank" rel="noopener noreferrer">{t}</a></h3>' if url else f'<h3>{t}</h3>'
    live = f'<a class="live-link" href="{url}" target="_blank" rel="noopener noreferrer">Visit live site {LIVE_SVG}</a>' if url else ''
    return f'''    <div class="card reveal" data-d="{(i%3)+1}">
      <div class="num">{cat}</div>{heading}<p>{d}</p>
      <div class="chip-row">{chips}</div>{live}
    </div>'''

def cta_band(h2, p, primary=('Start a Project','contact.html'), ghost=None):
    pbtn = f'<a class="btn btn-primary" href="{primary[1]}">{primary[0]} {ARROW}</a>'
    gbtn = f'<a class="btn btn-ghost" href="{ghost[1]}">{ghost[0]}</a>' if ghost else ''
    return f'''<section class="sec">
  <div class="cta-band reveal">
    <div class="mkbg">{MK('#fff')}</div>
    <h2>{h2}</h2><p>{p}</p>
    <div class="row-cta">{pbtn}{gbtn}</div>
  </div>
</section>'''

# ================= PAGE BODIES =================

home_body = f'''<section class="hero">
  <div class="hero-veil"></div>
  <div class="hero-inner">
    <div class="eyebrow reveal in">Ternah Software Company Ltd</div>
    <h1 class="reveal in" data-d="1" style="margin-top:24px">Keep<br>it <span class="kick">simple.</span></h1>
    <div class="sub reveal in" data-d="2">We build software that works.</div>
    <p class="lead reveal in" data-d="3">Custom-built systems, crafted to fit the exact way your business runs, powering teams, organizations, and communities across Africa.</p>
    <div class="hero-cta reveal in" data-d="4">
      <a class="btn btn-primary" href="contact.html">Start a Project {ARROW}</a>
      <a class="btn btn-ghost" href="solutions.html">Explore Solutions</a>
    </div>
    <div class="hero-tags reveal in" data-d="5">
      {"".join(f'<button class="tag" data-scroll="sol-{s}">{x}</button>' for x,s in [('Custom Software','software'),('ERP &amp; CRM','erp'),('Automation','automation'),('Data &amp; Analytics','data'),('Cloud','cloud'),('Support','support')])}
    </div>
  </div>
  <div class="scroll-ind"><div class="line"></div>Scroll</div>
</section>

<section class="sec">
  <div class="stats">
    <div class="stat reveal"><div class="n">100%</div><div class="l">Custom-built to fit</div></div>
    <div class="stat reveal" data-d="1"><div class="n">9+</div><div class="l">Industries served</div></div>
    <div class="stat green reveal" data-d="2"><div class="n">Weeks</div><div class="l">Not quarters to ship</div></div>
    <div class="stat reveal" data-d="3"><div class="n">Africa</div><div class="l">Built for the future</div></div>
  </div>
</section>

<section class="sec" style="padding-top:20px">
  <div class="sec-head">
    <span class="eyebrow">What we build</span>
    <h2 class="h2">Six ways we<br>move you forward.</h2>
    <p class="lead">From a single tool to a full platform: design, build, and support — under one accountable team.</p>
  </div>
  <div class="svc-grid">
{chr(10).join(svc_block(i,s) for i,s in enumerate(SOLUTIONS))}
  </div>
  <div class="center mt-cta"><a class="btn btn-ghost" href="solutions.html">All solutions {ARROW}</a></div>
</section>

<section class="sec">
  <div class="sec-head">
    <span class="eyebrow">How we work</span>
    <h2 class="h2">Simple process.<br>Real delivery.</h2>
    <p class="lead">Five steps from your first conversation to a running system.</p>
  </div>
  <div class="process-track">
{chr(10).join(f"""    <div class="process-step reveal" data-d="{i+1}">
      <div class="process-dot">{i+1}</div>
      <h4>{t}</h4>
      <p>{d}</p>
    </div>""" for i,(t,d) in enumerate(PROCESS_STEPS))}
  </div>
</section>

<div class="marquee-section">
  <div class="marquee-track">
    {"".join(f'<span class="marquee-item">{ind}</span><span class="marquee-sep">&nbsp;·&nbsp;</span>' for ind in INDUSTRIES_TICKER * 2)}
  </div>
</div>

<section class="sec">
  <div class="sec-head">
    <span class="eyebrow">Why Ternah</span>
    <h2 class="h2">A partner, not<br>just a vendor.</h2>
  </div>
  <div class="why-grid">
    <div class="why-block reveal">
      <div class="bn">01</div>
      <div class="accent-line"></div>
      <h3>Built to fit you</h3>
      <p>Software shaped around your exact processes, not a rigid template you bend to fit. We start by understanding how you already work.</p>
    </div>
    <div class="why-block reveal" data-d="1">
      <div class="bn">02</div>
      <div class="accent-line"></div>
      <h3>African insight</h3>
      <p>Local understanding of the markets, constraints, connectivity, and opportunities you actually operate in. Not imported assumptions.</p>
    </div>
    <div class="why-block reveal" data-d="2">
      <div class="bn">03</div>
      <div class="accent-line"></div>
      <h3>Scalable by design</h3>
      <p>Architecture that grows the moment your business does, without painful rebuilds or migrations six months in.</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="sec-head">
    <span class="eyebrow">Featured products</span>
    <h2 class="h2">Work that ships.</h2>
    <p class="lead">A selection of platforms and systems we have designed and delivered.</p>
  </div>
  <div class="grid g3">
{chr(10).join(proj_card_slim(i,p) for i,p in enumerate(PROJECTS[:3]))}
  </div>
  <div class="center mt-cta"><a class="btn btn-ghost" href="products.html">See all products {ARROW}</a></div>
</section>

{cta_band("Let's build something that fits.", "Tell us how your business runs. We'll turn it into software that keeps it simple.", ghost=('ternah22@gmail.com','mailto:ternah22@gmail.com'))}'''

about_body = f'''<section class="phead">
  <span class="eyebrow">About Ternah</span>
  <h1>More than code.<br>A digital partner.</h1>
  <p class="lead">TERNAH Software Company Ltd is an African software development and digital transformation company building innovative, reliable, and scalable technology for businesses, institutions, and communities.</p>
</section>

<section class="sec" style="padding-top:20px">
  <div class="split">
    <div>
      <span class="eyebrow">Our story</span>
      <h2 class="h2" style="margin:20px 0 24px">Software, crafted to fit.</h2>
      <p class="lead" style="margin-bottom:18px">We started Ternah on a simple conviction: technology should fit the way you already work, not force you to work the way it wants.</p>
      <p class="lead">We combine technical depth, business understanding, and local insight to create software that solves real problems across Africa. We help organizations embrace digital transformation, improve efficiency, and unlock new opportunities, and we stay for the long term.</p>
    </div>
    <div class="visual reveal">{MK('#cdd6ff')}</div>
  </div>
</section>

<section class="sec">
  <div class="grid g2">
    <div class="card feat reveal"><div class="num">Our Vision</div><h3 style="font-size:30px;line-height:1.25">To become Africa's leading software company, driving digital transformation through innovative, reliable, locally relevant technology.</h3></div>
    <div class="card reveal" data-d="1"><div class="num">Our Mission</div><h3 style="font-size:30px;line-height:1.25">To empower businesses, institutions, and communities across Africa with affordable, scalable, impactful digital solutions, fostering innovation and indigenous technology.</h3></div>
  </div>
</section>

<section class="sec">
  <div class="sec-head"><span class="eyebrow">Strategic objectives</span><h2 class="h2">What drives us.</h2></div>
  {rows_tpl(OBJECTIVES)}
</section>

<section class="sec">
  <div class="sec-head"><span class="eyebrow">Our values</span><h2 class="h2">What we stand on.</h2></div>
  <div class="grid g3">
{chr(10).join(f'''    <div class="card reveal" data-d="{(i%3)+1}"><div class="ico">{MK('#7c92ff')}</div><h3>{t}</h3><p>{d}</p></div>''' for i,(t,d) in enumerate(VALUES))}
  </div>
</section>

{cta_band("Ready when you are.", "Let's talk about where your organization wants to go, and how software gets it there.", primary=('Get in touch','contact.html'))}'''

solutions_body = f'''<section class="phead">
  <span class="eyebrow">Solutions</span>
  <h1>From idea to<br>deployment.</h1>
  <p class="lead">A complete toolkit for digital transformation, designed, built, and supported by one accountable team.</p>
</section>
<section class="sec" style="padding-top:20px">
  <div class="filter-bar" id="solFilter">
    <button class="pill active" data-filter="all">All</button>
    <button class="pill" data-filter="software">Custom Software</button>
    <button class="pill green-pill" data-filter="erp">ERP &amp; Systems</button>
    <button class="pill" data-filter="automation">Automation</button>
    <button class="pill green-pill" data-filter="data">Data &amp; Analytics</button>
    <button class="pill" data-filter="cloud">Cloud</button>
    <button class="pill green-pill" data-filter="support">Support</button>
  </div>
  <div class="grid g3" id="solGrid">
{chr(10).join(sol_card(i,s) for i,s in enumerate(SOLUTIONS))}
  </div>
</section>
<section class="sec">
  <div class="split">
    <div>
      <span class="eyebrow">How we work</span>
      <h2 class="h2" style="margin:20px 0 30px">A process built<br>around clarity.</h2>
      {rows_tpl([('01','Discover','We learn how your business actually runs before proposing anything.'),('02','Design','We map the system to your processes: simple, scalable, intentional.'),('03','Build','Pragmatic engineering with progress you can see, week by week.'),('04','Support','We deploy, monitor, and keep improving long after launch.')])}
    </div>
    <div class="visual reveal">{MK('#cdd6ff')}</div>
  </div>
</section>
{cta_band("Not sure where to start?", "Tell us the problem. We'll help you find the simplest path to solving it.", primary=('Book a consultation','contact.html'))}'''

industries_body = f'''<section class="phead">
  <span class="eyebrow">Industries</span>
  <h1>Built for how<br>Africa works.</h1>
  <p class="lead">We bring sector-specific understanding to every build, so the software fits the realities of your field, not a generic template.</p>
</section>
<section class="sec" style="padding-top:20px">
  <div class="ind-grid">
{chr(10).join(ind_card(x) for x in INDUSTRIES)}
  </div>
</section>
{cta_band("Don't see your sector?", "If your organization runs on processes, we can build software for it. Let's talk.", primary=('Start a conversation','contact.html'))}'''

products_body = f'''<section class="phead">
  <span class="eyebrow">Products</span>
  <h1>Work that ships.</h1>
  <p class="lead">A selection of products, platforms, and systems we've designed and built across industries and markets.</p>
</section>
<section class="sec" style="padding-top:20px">
  <div class="grid g3">
{chr(10).join(proj_card(i,p) for i,p in enumerate(PROJECTS))}
  </div>
</section>
<section class="sec">
  <div class="sec-head"><span class="eyebrow">Client testimonials</span><h2 class="h2">What clients say.</h2></div>
  <div class="grid g3">
{chr(10).join(f'''    <div class="quote reveal" data-d="{i+1}">
      <div class="q">&ldquo;{q}&rdquo;</div>
      <div class="who"><div class="av">{n[0]}</div><div><div class="nm">{n}</div><div class="rl">{r}</div></div></div>
    </div>''' for i,(q,n,r) in enumerate(TESTIMONIALS))}
  </div>
</section>
{cta_band("Your product could be next.", "Bring us a challenge. We'll bring the simplest software that solves it.")}'''

BUY_VS_BUILD_SLUG = 'buy-vs-build'
ARTICLE_SLUGS = {
    'Choosing between off-the-shelf and custom software': 'buy-vs-build',
    'Why offline-first matters in African markets':       'offline-first',
    'From manual to intelligent: a practical roadmap':   'manual-to-intelligent',
    'Turning dashboards into decisions':                  'dashboards-to-decisions',
    'Automation that pays for itself':                    'automation-roi',
    'Building for scale from day one':                    'scale-from-day-one',
}
READ_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>'

def insight_card(i, ins):
    cat,t,d,meta = ins
    slug = ARTICLE_SLUGS.get(t)
    extra_cls = ' clickable' if slug else ''
    read_link = f'<div class="art-read">Read article {READ_SVG}</div>' if slug else ''
    open_attr = f' data-open="{slug}"' if slug else ''
    return f'''    <article class="art{extra_cls} reveal" data-d="{(i%3)+1}"{open_attr}>
      <div class="thumb">{MK('#fff')}</div>
      <div class="body"><div class="cat">{cat}</div><h3>{t}</h3><p>{d}</p><div class="meta">{meta}</div>{read_link}</div>
    </article>'''

BUY_VS_BUILD_MODAL = f'''
<div class="modal-overlay" id="modal-{BUY_VS_BUILD_SLUG}" role="dialog" aria-modal="true" aria-labelledby="modal-title-bvb">
  <div class="modal">
    <button class="modal-close" aria-label="Close article">
      <svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
    <div class="modal-eyebrow">Guides &nbsp;·&nbsp; Decision Frameworks</div>
    <h1 id="modal-title-bvb">Buy vs. Build:<br>A Framework for Smarter Decisions</h1>
    <div class="modal-byline">
      <div class="modal-av">J</div>
      <div>
        <div class="name">Jonathan N.</div>
        <div class="role">Software Engineer, Ternah</div>
      </div>
      <div class="read-time">10 min read</div>
    </div>
    <div class="article-body">
      <p>Choosing between off-the-shelf software and a custom build is one of the highest-stakes technology decisions a business makes. Get it right and you move fast, spend efficiently, and stay focused on what makes you competitive. Get it wrong and you spend 3–10x more than expected, delay operations by months, and end up maintaining a system that was never quite right.</p>
      <p>This framework cuts through the noise.</p>

      <h2>First, Define Your Terms</h2>
      <p><strong>Off-the-shelf software</strong> (also called commercial off-the-shelf, or COTS) is pre-built software sold to many customers. Think QuickBooks, Salesforce, SAP, or any SaaS product you pay a subscription for. It is designed to handle common business needs and is ready to deploy in days or weeks.</p>
      <p><strong>Custom software</strong> is built specifically for your organization, from the ground up, to match your exact processes, data structures, and workflows. It takes months to build, requires ongoing maintenance, and only you own it.</p>
      <p>Neither is inherently better. The right answer depends entirely on your context.</p>

      <h2>The 5-Question Framework</h2>
      <p>Before writing a single line of code or signing a vendor SLA, answer these five questions honestly.</p>

      <h3>1. Is this a competitive advantage?</h3>
      <ul>
        <li><strong>Yes (Core differentiator):</strong> A unique workflow, proprietary process, or capability that competitors cannot easily replicate. Build.</li>
        <li><strong>No (Standard business function):</strong> Payroll, basic CRM, email, file storage. Buy. Everyone does this the same way, and that is fine.</li>
      </ul>

      <h3>2. What is your real timeline?</h3>
      <p>Need something working within three months? Buy. Custom software realistically takes six to eighteen months from discovery to deployment — and that is for a well-run project with clear requirements. If you have external deadlines, compliance dates, or a market window to hit, off-the-shelf is the only sane choice.</p>

      <h3>3. Can you afford total ownership?</h3>
      <ul>
        <li><strong>Off-the-shelf:</strong> Predictable subscription cost. Vendor handles infrastructure, security patches, and feature updates.</li>
        <li><strong>Custom:</strong> Build cost, plus roughly 20% of that cost every year in maintenance, bug fixes, documentation, and onboarding new developers who need to understand the codebase.</li>
      </ul>
      <p>A system that costs $50,000 to build costs $10,000/year to maintain indefinitely. Factor this in before you start.</p>

      <h3>4. Does your team have the expertise to own this?</h3>
      <p>Custom software without a dedicated product manager and at least one senior architect on the client side almost always fails — not because the code is bad, but because requirements drift, priorities shift, and no one is accountable for the product decisions that need to be made every week.</p>
      <div class="danger"><p>No internal product leadership? Do not build custom. You will regret it.</p></div>

      <h3>5. How stable are your requirements?</h3>
      <ul>
        <li><strong>Changing every quarter:</strong> Buy. Off-the-shelf vendors absorb market changes into their product. You benefit without rebuilding.</li>
        <li><strong>Frozen and well-understood for two or more years:</strong> Custom may be worth it. Stable requirements are the single biggest predictor of a successful custom build.</li>
      </ul>

      <h2>The Golden Rule</h2>
      <blockquote><p>Buy commodity. Build differentiators. Integrate everything else.</p></blockquote>
      <p>This is not a compromise. It is a strategy. The best technology organizations in the world buy aggressively for anything that is not their core business, and build only where they can win.</p>

      <h2>When to Buy</h2>
      <ul>
        <li>Standard business functions: accounting, HR, payroll, file storage, basic project management</li>
        <li>You are paying for features you do not use — that is fine, because you are also paying for security, compliance, and a team of engineers maintaining it</li>
        <li>Compliance is the vendor's problem (SOC 2, HIPAA, GDPR) — this alone can justify the subscription cost</li>
        <li>You are early stage and your processes are still evolving</li>
      </ul>
      <div class="callout"><p>Rule of thumb: if ten other companies in your industry use the same tool, buy it.</p></div>

      <h2>When to Build</h2>
      <ul>
        <li>The software is your product — you are a SaaS company or technology platform</li>
        <li>Off-the-shelf forces dangerous workarounds: manual re-entry between systems, shadow spreadsheets, staff inventing unofficial processes</li>
        <li>You have dedicated product leadership and a 12+ month budget</li>
        <li>Your workflow is genuinely unique — not "we do things slightly differently," but fundamentally incompatible with any existing tool</li>
      </ul>

      <h2>The Dangerous Middle (Where Money Dies)</h2>
      <p><strong>Trap 1: "We are special, so we need to build."</strong> Most organizations are not as operationally unique as they think. Eighty percent of companies that build custom software could have bought something, configured it well, and moved faster. Challenge your team: have you actually exhausted the market?</p>
      <p><strong>Trap 2: "We bought it and now we are hacking it to death."</strong> If your team has built more than 20% custom functionality on top of a commercial product, you are now maintaining a custom system anyway — one with the worst of both worlds. Stop. Evaluate whether you should migrate to a proper custom build or a different off-the-shelf product.</p>

      <h2>Decision Matrix</h2>
      <table>
        <tr><th>Your Situation</th><th>Verdict</th></tr>
        <tr><td>Startup, pre-product-market fit</td><td class="verdict">Buy everything. Iterate fast.</td></tr>
        <tr><td>Scale-up with a truly unique core workflow</td><td class="verdict">Build core. Buy the rest.</td></tr>
        <tr><td>Enterprise with 50+ Salesforce customizations</td><td class="verdict">You built already — just poorly. Evaluate migration.</td></tr>
        <tr><td>"No tool can do what we need"</td><td class="verdict">90% chance you have not looked hard enough.</td></tr>
        <tr><td>Requirements change every quarter</td><td class="verdict">Buy. No debate.</td></tr>
        <tr><td>Software is your product</td><td class="verdict">Build. That is your job.</td></tr>
      </table>

      <h2>The Bottom Line</h2>
      <p>When in doubt, buy. Most custom software projects fail not because of bad engineering, but because requirements change faster than delivery. The graveyard of failed software projects is full of systems that were beautifully built for a problem that no longer existed by the time they launched.</p>
      <p>Save your build budget for what makes you genuinely different. Buy everything else, and buy it fast.</p>

      <div class="article-cta">
        <a class="btn btn-primary" href="contact.html">Get a second opinion {ARROW}</a>
        <a class="btn btn-ghost" href="solutions.html">Explore our solutions</a>
      </div>
    </div>
  </div>
</div>'''

OFFLINE_FIRST_MODAL = f'''
<div class="modal-overlay" id="modal-offline-first" role="dialog" aria-modal="true" aria-labelledby="modal-title-off">
  <div class="modal">
    <button class="modal-close" aria-label="Close article">
      <svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
    <div class="modal-eyebrow">Technology Trends &nbsp;·&nbsp; African Markets</div>
    <h1 id="modal-title-off">Why Offline-First Matters<br>in African Markets</h1>
    <div class="modal-byline">
      <div class="modal-av">J</div>
      <div>
        <div class="name">Jonathan N.</div>
        <div class="role">Software Engineer, Ternah</div>
      </div>
      <div class="read-time">6 min read</div>
    </div>
    <div class="article-body">
      <p><strong>Build for the connection you don't have, not the one you might get.</strong></p>
      <p>Across Africa, connectivity is real but intermittent. Reliable fiber in Lagos, patchy 3G in Kisumu, no signal at all in rural depots. Apps that assume always-on internet fail. Offline-first software wins.</p>

      <h2>What "Offline-First" Actually Means</h2>
      <p>Not "works offline sometimes." Offline-first means the app is designed so that offline is the default state, and online is simply when it syncs.</p>
      <ul>
        <li><strong>User opens app:</strong> works instantly, no spinner</li>
        <li><strong>Data saved locally first:</strong> syncs automatically when connection returns</li>
        <li><strong>Conflicts resolved automatically:</strong> no "error: no network" dead ends</li>
      </ul>

      <h2>Why It Matters in African Markets</h2>
      <table>
        <tr><th>Reality on the Ground</th><th>Offline-First Advantage</th></tr>
        <tr><td>Mobile data is expensive</td><td>Syncs once, not hundreds of tiny requests</td></tr>
        <tr><td>Power outages reset routers</td><td>No lost work — everything cached locally</td></tr>
        <tr><td>Users switch networks (WiFi to 4G to 2G)</td><td>Seamless handoff, no crash</td></tr>
        <tr><td>Morning sync window before field work</td><td>Preload data, then work all day offline</td></tr>
      </table>
      <div class="callout"><p>Result: Your app feels 10x faster and more reliable than competitors who assume constant connectivity.</p></div>

      <h2>Where Offline-First Wins Most</h2>
      <ul>
        <li><strong>Logistics and delivery:</strong> Drivers enter waypoints and delivery updates without needing a signal</li>
        <li><strong>Healthcare:</strong> Community health workers register patients in villages with no coverage</li>
        <li><strong>Agriculture:</strong> Farmers log yields and inputs with no tower for miles</li>
        <li><strong>Fintech:</strong> Agent banking transactions are queued locally and reconciled when connectivity returns</li>
        <li><strong>Education:</strong> Students complete quizzes on a tablet, syncing results when they reach school WiFi</li>
      </ul>

      <h2>The Technical Reality (Kept Simple)</h2>
      <p>You do not need a decentralized database. You need four things:</p>
      <ul>
        <li><strong>Local-first storage:</strong> IndexedDB for web apps, SQLite for mobile apps</li>
        <li><strong>Sync engine:</strong> Background, resumable, and conflict-aware</li>
        <li><strong>Optimistic UI:</strong> The interface updates instantly and retries in the background</li>
        <li><strong>Smart sync policies:</strong> Prioritize critical data, defer large media files</li>
      </ul>
      <div class="danger"><p>Anti-pattern: "We will add offline support later." You will not. Offline-first must be a day-one architectural decision, not a feature added at the end.</p></div>

      <h2>The Business Case</h2>
      <ul>
        <li><strong>Higher retention:</strong> When something breaks, users blame your app. Offline-first removes the most common failure point.</li>
        <li><strong>Lower data costs:</strong> Apps that batch sync use a fraction of the data of always-online apps, reducing churn in price-sensitive markets.</li>
        <li><strong>Better trust:</strong> "It just works" builds a reputation that spreads by word of mouth in low-connectivity regions.</li>
        <li><strong>Regulatory edge:</strong> Some government and NGO tenders now specifically require offline capability for rural deployment. This is a growing requirement.</li>
      </ul>

      <h2>Common Mistakes to Avoid</h2>
      <ul>
        <li>Building online-first, then bolting on a "save for later" button at the end</li>
        <li>Assuming users will patiently wait for a sync spinner to complete</li>
        <li>Using "last writer wins" conflict resolution — this causes silent data loss</li>
        <li>Testing only on office WiFi, even with network throttling in developer tools</li>
      </ul>

      <h2>Offline-First vs. Traditional: A Direct Comparison</h2>
      <table>
        <tr><th>Feature</th><th>Traditional App</th><th>Offline-First App</th></tr>
        <tr><td>First load</td><td>Spinner, timeout, error</td><td class="verdict">Instant</td></tr>
        <tr><td>Weak or no signal</td><td>"No connection"</td><td class="verdict">Works fine</td></tr>
        <tr><td>Data usage</td><td>5 to 10x higher</td><td class="verdict">Minimal</td></tr>
        <tr><td>User frustration</td><td>High</td><td class="verdict">Low</td></tr>
      </table>

      <h2>The Bottom Line</h2>
      <p>Do not design for 100% uptime. Design for 60% uptime and degrade gracefully.</p>
      <p>Offline-first is not a technical niche. It is a competitive advantage in African markets. Build it correctly from day one, and you win the users that always-online software consistently leaves behind.</p>

      <div class="article-cta">
        <a class="btn btn-primary" href="contact.html">Talk to us about offline-first {ARROW}</a>
        <a class="btn btn-ghost" href="solutions.html">Explore our solutions</a>
      </div>
    </div>
  </div>
</div>'''

MANUAL_INTEL_MODAL = f'''
<div class="modal-overlay" id="modal-manual-to-intelligent" role="dialog" aria-modal="true" aria-labelledby="modal-title-mti">
  <div class="modal">
    <button class="modal-close" aria-label="Close article">
      <svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
    <div class="modal-eyebrow">Digital Transformation &nbsp;·&nbsp; Practical Roadmap</div>
    <h1 id="modal-title-mti">From Manual to Intelligent:<br>A Practical Roadmap</h1>
    <div class="modal-byline">
      <div class="modal-av">J</div>
      <div>
        <div class="name">Jonathan N.</div>
        <div class="role">Software Engineer, Ternah</div>
      </div>
      <div class="read-time">8 min read</div>
    </div>
    <div class="article-body">
      <p>Spreadsheets and paper are not the enemy. They are survivors. They work. But they do not scale, they hide important insights, and they bleed time. The goal is not to rip them out overnight. It is to migrate without creating chaos.</p>

      <h2>The Three-Phase Roadmap</h2>
      <p>Skip the "big bang" ERP disaster. Instead, move through three deliberate phases: digitize, connect, then make it intelligent.</p>

      <h3>Phase 1: Stabilize and Digitize (Months 0 to 6)</h3>
      <p>No new processes. No optimization yet. Just replace paper with digital equivalents.</p>
      <ul>
        <li>Identify your top three pain points: stock cards, attendance registers, invoice approvals</li>
        <li>Pick one workflow and digitize it exactly as it already works — same fields, same steps</li>
        <li>Use simple tools: mobile forms, Google Sheets with validation, or a lightweight workflow tool</li>
        <li>Train one champion per team. Avoid mass training sessions at this stage.</li>
      </ul>
      <div class="callout"><p>Success metric: Same process, 50% less time, zero manual data re-entry.</p></div>
      <div class="danger"><p>Avoid: Automating a broken process. Digitize first, then improve. Putting broken workflows into software just makes them break faster.</p></div>

      <h3>Phase 2: Connect and Automate (Months 6 to 12)</h3>
      <p>Now you can remove redundancy and add intelligent rules.</p>
      <ul>
        <li>Connect your digitized forms to a central database — stop emailing CSV files between departments</li>
        <li>Set basic business rules: "Alert when stock falls below 10 units"</li>
        <li>Automate reminders and approvals: managers get a notification instead of a paper form</li>
        <li>Introduce one simple dashboard showing today's exceptions — the things that need attention</li>
      </ul>
      <div class="callout"><p>Success metric: Three workflows fully integrated, manual steps reduced by 70%.</p></div>
      <div class="danger"><p>Avoid: Building custom integrations for every edge case. Use tools like Zapier, n8n, or built-in connectors first. Only build custom when you have exhausted existing options.</p></div>

      <h3>Phase 3: Intelligent and Predictive (Months 12 to 18)</h3>
      <p>Now the system starts working for you, not the other way around.</p>
      <ul>
        <li>Forecast demand based on historical patterns in your own data</li>
        <li>Flag anomalies automatically: "This month's procurement is twice the usual — review before approving"</li>
        <li>Surface suggested next actions: "Reorder now to avoid a stockout in five days"</li>
        <li>Optional: Add document capture via camera for receipts, IDs, and field reports</li>
      </ul>
      <div class="callout"><p>Success metric: At least one operational decision made by the system without requiring human review.</p></div>
      <div class="danger"><p>Avoid: Adding AI for its own sake. Only introduce intelligence where the decisions are repetitive and the underlying data is already clean and structured.</p></div>

      <h2>The "No Disruption" Rule</h2>
      <table>
        <tr><th>Do This</th><th>Not This</th></tr>
        <tr><td>Run old and new systems in parallel for two weeks</td><td>Flip a switch on a Friday afternoon</td></tr>
        <tr><td>Keep spreadsheets available as a backup export</td><td>Delete the master spreadsheet on day one</td></tr>
        <tr><td>Digitize after the daily rush, such as an end-of-day sync</td><td>Require real-time entry during peak operating hours</td></tr>
        <tr><td>Let users still print reports if they need to</td><td>Force tablets onto resistant staff immediately</td></tr>
      </table>
      <p>You are not replacing people. You are replacing friction.</p>

      <h2>Why This Works for African Organizations Specifically</h2>
      <ul>
        <li><strong>Power and internet gaps:</strong> Offline-first mobile forms handle this — see our offline-first guide for details</li>
        <li><strong>Mixed literacy levels:</strong> Use voice input, icons, and local language interfaces wherever possible</li>
        <li><strong>Low IT budget:</strong> Start with free tiers of Airtable, AppSheet, or Trello — they are powerful enough for Phase 1</li>
        <li><strong>Resistance to change:</strong> Find the one person already using a shadow spreadsheet to solve a real problem. That person is your internal champion and your ally.</li>
      </ul>

      <h2>The Spreadsheet Trap and How to Escape It</h2>
      <p>Spreadsheets are not evil. They are just fragile once you have more than 50 rows and five users editing simultaneously.</p>
      <p><strong>Signs you have outgrown them:</strong></p>
      <ul>
        <li>"Which version of this file is the latest?"</li>
        <li>Emailing files back and forth between people</li>
        <li>Accidental deletions with no audit trail to recover from</li>
        <li>Copy-paste errors appearing in monthly reports</li>
      </ul>
      <p><strong>Escape path:</strong> Move the spreadsheet into a database without changing the visual layout. Users see the same columns and rows they are used to, but the data is now in a real system with proper access controls, history, and validation.</p>

      <h2>Realistic Budget Ranges</h2>
      <table>
        <tr><th>Phase</th><th>Monthly Cost (USD)</th><th>Example Tools</th></tr>
        <tr><td>Digitize</td><td>$0 to $200</td><td>Google Workspace, Google Forms, AppSheet free tier</td></tr>
        <tr><td>Connect</td><td>$200 to $800</td><td>Airtable, n8n cloud, Microsoft Power Apps</td></tr>
        <tr><td>Intelligent</td><td>$800 to $3,000</td><td>Retool, Supabase, basic ML APIs</td></tr>
      </table>
      <p>Compare this to the hidden cost of paper: printing, physical storage, lost documents, and an average of two hours per day per person searching for information that should take seconds.</p>

      <h2>The Bottom Line</h2>
      <p>Do not try to digitize everything at once. Digitize the three workflows that cause the most firefighting in your organization right now.</p>
      <p>Start with procurement approvals, stock reconciliation, or daily field reports. Get those working without disruption. Then expand to the next three. Spreadsheets are not your enemy. Undertrained staff forced into complex software they do not understand is the real problem. Keep it simple. Keep it parallel. Keep it running.</p>
      <p><strong>Your first 30-day action item:</strong> Pick one paper form your team uses today. Turn it into a mobile form by the end of this week. Run it alongside the paper version for two weeks. No disruption. Just proof that it works.</p>

      <div class="article-cta">
        <a class="btn btn-primary" href="contact.html">Start your digitization {ARROW}</a>
        <a class="btn btn-ghost" href="solutions.html">Explore automation solutions</a>
      </div>
    </div>
  </div>
</div>'''

DASHBOARDS_MODAL = f'''
<div class="modal-overlay" id="modal-dashboards-to-decisions" role="dialog" aria-modal="true" aria-labelledby="modal-title-dash">
  <div class="modal">
    <button class="modal-close" aria-label="Close article">
      <svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
    <div class="modal-eyebrow">Data &amp; Analytics &nbsp;·&nbsp; Decision Intelligence</div>
    <h1 id="modal-title-dash">Turning Dashboards<br>into Decisions</h1>
    <div class="modal-byline">
      <div class="modal-av" style="background:linear-gradient(135deg,var(--green-soft),var(--green))">S</div>
      <div>
        <div class="name">Sheronah A.</div>
        <div class="role">IT Consultant, Ternah</div>
      </div>
      <div class="read-time">7 min read</div>
    </div>
    <div class="article-body">
      <p><strong>The difference between reporting that informs and reporting that drives action.</strong></p>
      <p>Most dashboards are digital wallpaper. Everyone nods at the charts, then walks away and does the same thing they always did. A good dashboard does not just inform — it demands a next step.</p>

      <h2>The Three Questions Every Dashboard Must Answer</h2>
      <p>Before you build a single chart, answer these three questions.</p>
      <h3>1. Who is looking at this?</h3>
      <ul>
        <li><strong>Executive:</strong> one number — "Are we on track?"</li>
        <li><strong>Manager:</strong> exceptions — "What needs my attention?"</li>
        <li><strong>Operator:</strong> actions — "What do I do next?"</li>
      </ul>
      <h3>2. What decision does this enable?</h3>
      <p>If the answer is "just awareness," delete the metric. Every number on a dashboard should map to a specific decision: approve, reorder, escalate, or pause. If it cannot trigger a decision, it is noise.</p>
      <h3>3. When will they act?</h3>
      <ul>
        <li><strong>Real-time data:</strong> alert — a red light that cannot be ignored</li>
        <li><strong>Daily data:</strong> a checklist reviewed each morning</li>
        <li><strong>Weekly data:</strong> a trend review for planning</li>
      </ul>

      <h2>Reporting Dashboard vs. Action Dashboard</h2>
      <table>
        <tr><th>Feature</th><th>Reporting Dashboard</th><th>Action Dashboard</th></tr>
        <tr><td>Purpose</td><td>What happened</td><td class="verdict">What to do now</td></tr>
        <tr><td>Typical content</td><td>Trend lines, averages</td><td class="verdict">Exceptions, queues, alerts</td></tr>
        <tr><td>User response</td><td>"Hmm, interesting"</td><td class="verdict">Opens a task or approval</td></tr>
        <tr><td>Update frequency</td><td>Daily or weekly</td><td class="verdict">Real-time or hourly</td></tr>
        <tr><td>Success metric</td><td>"Viewed"</td><td class="verdict">"Clicked through"</td></tr>
      </table>

      <h2>The Actionable Dashboard Checklist</h2>
      <ul>
        <li>Each card has a named owner — a person or team who is responsible</li>
        <li>Each number has a target with red, yellow, and green thresholds</li>
        <li>Each exception has a suggested action — for example, "Review 5 overdue invoices"</li>
        <li>Each action is one click away, not behind a separate login</li>
        <li>No pie charts — they describe, they do not drive action</li>
      </ul>

      <h2>A Simple Framework: The OODA Loop</h2>
      <p><strong>Observe, Orient, Decide, Act.</strong></p>
      <ul>
        <li><strong>Observe:</strong> One screen shows today's exceptions — stock below minimum, payments overdue by more than 30 days</li>
        <li><strong>Orient:</strong> Color coding shows severity — red means act now, yellow means plan, green means fine</li>
        <li><strong>Decide:</strong> The dashboard suggests "Reorder 100 units from Supplier X"</li>
        <li><strong>Act:</strong> A button creates the purchase order or assigns the task directly</li>
      </ul>
      <div class="danger"><p>If your dashboard does not reach the Act step, it is a report, not a tool.</p></div>

      <h2>Common Mistakes and Their Fixes</h2>
      <table>
        <tr><th>Mistake</th><th>Fix</th></tr>
        <tr><td>Too many metrics — analysis paralysis</td><td>Limit to top 3 Key Performance Indicators (KPIs) per role</td></tr>
        <tr><td>Historical data only — yesterday's news</td><td>Add real-time alerts for critical thresholds</td></tr>
        <tr><td>Static PDF exported monthly</td><td>Live link with filters for each user type</td></tr>
        <tr><td>No alerting rules configured</td><td>Push notification when stock falls below safety level</td></tr>
        <tr><td>Dashboard treated as a trophy</td><td>Dashboard treated as a to-do list</td></tr>
      </table>

      <h2>What Action Dashboards Look Like in Practice</h2>
      <ul>
        <li><strong>Procurement:</strong> "10 items below reorder point. Click to generate orders."</li>
        <li><strong>Finance:</strong> "5 invoices overdue by more than 30 days. Click to send reminder."</li>
        <li><strong>Logistics:</strong> "3 deliveries delayed by more than 2 hours. Click to reassign driver."</li>
        <li><strong>Sales:</strong> "Leads not contacted in 48 hours. Click to assign to rep."</li>
      </ul>

      <h2>The Bottom Line</h2>
      <blockquote><p>Do not build a dashboard that answers questions. Build one that starts work.</p></blockquote>
      <p>After a user looks at your dashboard, they should know exactly what to do next and be able to do it in two clicks. If they close the tab and nothing changes, you built a report, not a decision tool.</p>
      <p><strong>One-page audit:</strong> Pick your most-used dashboard. Delete half the charts. Add one action button. Test for a week and measure whether anything changes in response time or task completion.</p>

      <div class="article-cta">
        <a class="btn btn-primary" href="contact.html">Get a dashboard audit {ARROW}</a>
        <a class="btn btn-ghost" href="solutions.html">Explore data solutions</a>
      </div>
    </div>
  </div>
</div>'''

AUTOMATION_ROI_MODAL = f'''
<div class="modal-overlay" id="modal-automation-roi" role="dialog" aria-modal="true" aria-labelledby="modal-title-auto">
  <div class="modal">
    <button class="modal-close" aria-label="Close article">
      <svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
    <div class="modal-eyebrow">Digital Transformation &nbsp;·&nbsp; ROI</div>
    <h1 id="modal-title-auto">Automation That<br>Pays for Itself</h1>
    <div class="modal-byline">
      <div class="modal-av" style="background:linear-gradient(135deg,var(--green-soft),var(--green))">S</div>
      <div>
        <div class="name">Sheronah A.</div>
        <div class="role">IT Consultant, Ternah</div>
      </div>
      <div class="read-time">5 min read</div>
    </div>
    <div class="article-body">
      <p><strong>Identifying the workflows where automation delivers the fastest, clearest return.</strong></p>
      <p>Not every automation makes money. Some just digitize inefficiency. The trick is finding the workflows where the Return on Investment (ROI) is obvious, fast, and hard to argue with.</p>

      <h2>The Self-Funding Automation Formula</h2>
      <p>A workflow is a good candidate when it meets this test:</p>
      <blockquote><p>High frequency multiplied by high manual effort, divided by low rule complexity, equals fast payback.</p></blockquote>

      <h2>Where to Look First: The Top Five</h2>
      <table>
        <tr><th>Workflow</th><th>Typical Monthly Hours</th><th>Payback Period</th></tr>
        <tr><td>Data entry (paper to digital)</td><td>40 to 100 hours</td><td class="verdict">1 to 2 months</td></tr>
        <tr><td>Approval routing (emails and signatures)</td><td>30 to 60 hours</td><td class="verdict">2 to 3 months</td></tr>
        <tr><td>Report generation (copy-paste from multiple sources)</td><td>20 to 40 hours</td><td class="verdict">1 month</td></tr>
        <tr><td>Inventory reconciliation (spreadsheet vs. physical count)</td><td>15 to 30 hours</td><td class="verdict">2 months</td></tr>
        <tr><td>Customer follow-up (reminders, payment chasing)</td><td>25 to 50 hours</td><td class="verdict">1 to 2 months</td></tr>
      </table>

      <h2>The Three Types of ROI — Calculate All of Them</h2>
      <h3>1. Hard ROI (Direct cost savings)</h3>
      <ul>
        <li>Labor hours reduced, multiplied by hourly cost including benefits and overhead</li>
        <li>Overtime eliminated</li>
        <li>Late fees or penalties avoided</li>
      </ul>
      <h3>2. Soft ROI (Productivity gains)</h3>
      <ul>
        <li>Faster turnaround leads to happier customers</li>
        <li>Staff reallocated to higher-value work</li>
        <li>Reduced burnout and lower staff turnover</li>
      </ul>
      <h3>3. Strategic ROI (Risk and compliance)</h3>
      <ul>
        <li>Fewer manual errors such as double payments and misrouted orders</li>
        <li>Audit trail captured automatically without extra effort</li>
        <li>Regulatory reporting completed without last-minute panic</li>
      </ul>

      <h2>The No-Code First Rule</h2>
      <p>You do not need developers to find your first payback. Start with tools that require no programming:</p>
      <ul>
        <li><strong>Zapier or Make (formerly Integromat):</strong> Connect two apps — for example, Google Forms to Google Sheets to an email alert</li>
        <li><strong>Power Automate:</strong> Best for the Microsoft ecosystem — SharePoint approvals, email parsing</li>
        <li><strong>n8n:</strong> Self-hosted, open-source automation — good when your data is sensitive and cannot leave your servers</li>
        <li><strong>Retool or Budibase:</strong> Internal tools built on top of databases you already have</li>
      </ul>

      <h2>The 30-Day Automation Sprint</h2>
      <ul>
        <li><strong>Week 1:</strong> Map the current workflow in detail — every click, every email, every copy-paste step</li>
        <li><strong>Week 2:</strong> Identify the single most repetitive subtask, not the whole process</li>
        <li><strong>Week 3:</strong> Build a prototype using the free tier of an automation tool</li>
        <li><strong>Week 4:</strong> Run old and new in parallel and measure time saved</li>
      </ul>
      <div class="callout"><p>Success metric: At least 10 hours per week saved. If yes, roll out. If no, choose a different workflow and repeat.</p></div>

      <h2>When Not to Automate</h2>
      <ul>
        <li>The process changes every month — automate stability, not chaos</li>
        <li>More than 50% of cases require human judgment or exception handling</li>
        <li>The data source is inconsistent — garbage in, garbage out</li>
        <li>Compliance requires a manual sign-off at every step regardless</li>
      </ul>

      <h2>Real Example: African Retail Chain</h2>
      <p><strong>Before:</strong> 12 store managers emailed daily stock sheets. Head office copy-pasted everything into a master spreadsheet. Three hours every morning. Frequent errors from manual entry.</p>
      <p><strong>After:</strong> Google Form on each manager's phone. Data writes directly to Google Sheets. Automated alert fires if any item falls below reorder point.</p>
      <div class="callout"><p>Result: 15 hours per week saved at head office. Stockouts reduced by 40%. Full payback in 22 days.</p></div>

      <h2>The Bottom Line</h2>
      <blockquote><p>Do not automate everything. Automate the boring, the repetitive, and the frequent.</p></blockquote>
      <p>Start with a workflow that annoys someone every single day. If you can save that person one hour daily, that is 250 hours a year — roughly six full work weeks. That pays for itself before the first month is over.</p>
      <p><strong>Your Monday morning test:</strong> Ask your team, "What task do you dread doing every day?" That is your first automation target.</p>

      <div class="article-cta">
        <a class="btn btn-primary" href="contact.html">Find your first automation {ARROW}</a>
        <a class="btn btn-ghost" href="solutions.html">Explore automation solutions</a>
      </div>
    </div>
  </div>
</div>'''

SCALE_MODAL = f'''
<div class="modal-overlay" id="modal-scale-from-day-one" role="dialog" aria-modal="true" aria-labelledby="modal-title-scale">
  <div class="modal">
    <button class="modal-close" aria-label="Close article">
      <svg viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </button>
    <div class="modal-eyebrow">Technology Trends &nbsp;·&nbsp; Architecture</div>
    <h1 id="modal-title-scale">Building for Scale<br>from Day One</h1>
    <div class="modal-byline">
      <div class="modal-av" style="background:linear-gradient(135deg,var(--green-soft),var(--green))">S</div>
      <div>
        <div class="name">Sheronah A.</div>
        <div class="role">IT Consultant, Ternah</div>
      </div>
      <div class="read-time">9 min read</div>
    </div>
    <div class="article-body">
      <p><strong>Architecture choices that save you a painful rebuild as your user base grows.</strong></p>
      <p>"We will rebuild it properly when we grow" is a statement that never comes true. You never have time, and by then your data is a mess, your users are frustrated, and your team is fighting fires instead of shipping features. Scaling is not about expensive hardware. It is about smart architectural decisions from the very first line of code.</p>

      <h2>What "Scale" Actually Means</h2>
      <p>Scaling is not just about more users. It covers four dimensions that often break independently:</p>
      <ul>
        <li><strong>Data volume:</strong> Moving from 1,000 rows to 10 million rows while keeping queries fast</li>
        <li><strong>Concurrency:</strong> Going from 10 simultaneous users to 10,000 without timeouts</li>
        <li><strong>Features:</strong> Expanding from 5 database tables to 50 without the codebase breaking down</li>
        <li><strong>Team size:</strong> Growing from 1 developer to 10 without them constantly blocking each other</li>
      </ul>

      <h2>The Five Non-Negotiable Choices</h2>
      <h3>1. Start with a relational database</h3>
      <p>Use PostgreSQL or MySQL. Avoid flat files, spreadsheets, or JSON blobs as your primary data store. Relational databases give you indexes, joins, and transactions — three capabilities that save you enormous pain as your data grows. NoSQL (Not Only Structured Query Language) databases have their place, but start with SQL (Structured Query Language) until you have a proven reason to move away from it.</p>

      <h3>2. Keep the application layer stateless</h3>
      <p>Do not store user sessions on a specific server. Use a shared cache like Redis or store session state in your database. This lets you add more servers behind a load balancer without running into "sticky session" problems where users get logged out randomly.</p>

      <h3>3. Make operations idempotent</h3>
      <p>An idempotent operation produces the same result whether it runs once or ten times. No duplicate charges, no duplicate orders. Networks fail and users double-click. Idempotency protects your data integrity automatically.</p>

      <h3>4. Use asynchronous processing for anything slow</h3>
      <p>Email sending, report generation, and file processing should go into a queue — tools like RabbitMQ, Amazon SQS (Simple Queue Service), or Bull work well. Your Application Programming Interface (API) returns a fast response, and the slow work happens in the background. Users get a "we will notify you when it is ready" response rather than a spinning wheel.</p>

      <h3>5. Keep environments identical</h3>
      <p>Your development, staging, and production environments should match as closely as possible — same database version, same operating system. "It works on my machine" is the single most common cause of scaling failures in small teams.</p>

      <h2>The "Scale Too Early" Trap</h2>
      <p>Do not build for Google's scale. Build for ten times your current users. That is always enough headroom for the next 18 months.</p>
      <p>Common over-engineering mistakes:</p>
      <ul>
        <li>Microservices architecture for a team of three developers</li>
        <li>Kubernetes for an application handling 500 requests per day</li>
        <li>Database sharding before you have reached 100 gigabytes of data</li>
      </ul>
      <div class="callout"><p>A single well-structured monolith with a properly indexed database can handle millions of users. WhatsApp ran on PostgreSQL for years at massive scale.</p></div>

      <h2>What Breaks First and How to Prevent It</h2>
      <table>
        <tr><th>Breaking Point</th><th>Early Prevention</th></tr>
        <tr><td>Database queries become slow</td><td>Always index foreign keys and columns used in WHERE clauses from day one</td></tr>
        <tr><td>File uploads fill server storage</td><td>Store files in cloud storage (Amazon S3 or Cloudflare R2), never in the database itself</td></tr>
        <tr><td>Third-party API rate limits hit</td><td>Add a queue with retry logic and exponential backoff</td></tr>
        <tr><td>Authentication becomes a bottleneck</td><td>Use token-based authentication (JSON Web Tokens / JWT) from day one rather than server-side session cookies</td></tr>
        <tr><td>Logging becomes unreadable chaos</td><td>Use structured JSON logs with a request ID that traces a single request across all services</td></tr>
      </table>

      <h2>The Real Cost of a Scale Rebuild</h2>
      <p>A "scaling rebuild" at 100,000 users typically costs all of the following at once:</p>
      <ul>
        <li>Six to twelve months of engineering time that could have built new features</li>
        <li>A data migration with real risk of corruption or extended downtime</li>
        <li>Customer churn during the performance problems that triggered the rebuild</li>
        <li>Opportunity cost of every feature you could not ship during that period</li>
      </ul>
      <p>All of this is avoidable with a handful of small decisions made at the beginning.</p>

      <h2>Simple Checklist for Day One</h2>
      <ul>
        <li>Use a relational database with a proper, normalized schema</li>
        <li>Keep business logic in application code, not in database stored procedures</li>
        <li>Make every API endpoint idempotent where possible</li>
        <li>Send email and process files in background jobs, not in the request cycle</li>
        <li>Use environment variables for all configuration — no hardcoded URLs or credentials</li>
        <li>Write database migration scripts from the first commit so schema changes are tracked and reversible</li>
      </ul>

      <h2>The Bottom Line</h2>
      <blockquote><p>Scale is not a feature you add later. It is a set of habits you build from the start.</p></blockquote>
      <p>You do not need Kubernetes or microservices to scale well. You need a clean database schema, stateless application servers, and a queue for slow tasks. That covers 80% of scaling problems. The remaining 20% you will learn when you actually get there — and by then you will have the data and the budget to solve it properly.</p>
      <p><strong>Your one-page action item:</strong> Review your current architecture against the checklist above. For each item you cannot check off, estimate how many users you can handle before it becomes a crisis. Then decide whether that ceiling is acceptable for the next 18 months.</p>

      <div class="article-cta">
        <a class="btn btn-primary" href="contact.html">Book an architecture review {ARROW}</a>
        <a class="btn btn-ghost" href="solutions.html">Explore our solutions</a>
      </div>
    </div>
  </div>
</div>'''

insights_body = f'''<section class="phead">
  <span class="eyebrow">Insights</span>
  <h1>Ideas worth<br>building on.</h1>
  <p class="lead">Articles, technology trends, and practical guides on digital transformation across Africa.</p>
</section>
<section class="sec" style="padding-top:20px">
  <div class="grid g3">
{chr(10).join(insight_card(i,ins) for i,ins in enumerate(INSIGHTS))}
  </div>
</section>
{cta_band("Let's turn insight into action.", "Reading about transformation is one thing. Let's build yours.", primary=('Talk to us','contact.html'))}
{BUY_VS_BUILD_MODAL}
{OFFLINE_FIRST_MODAL}
{MANUAL_INTEL_MODAL}
{DASHBOARDS_MODAL}
{AUTOMATION_ROI_MODAL}
{SCALE_MODAL}'''

contact_body = f'''<section class="phead">
  <span class="eyebrow">Contact</span>
  <h1>Let's keep<br>it simple.</h1>
  <p class="lead">Tell us about your project or challenge. We'll get back to you fast.</p>
</section>
<section class="sec" style="padding-top:20px">
  <div class="contact-wrap">
    <div>
      <div class="field"><label>Name</label><input id="f_name" type="text" placeholder="Your name"></div>
      <div class="field"><label>Email</label><input id="f_email" type="email" placeholder="you@company.com"></div>
      <div class="field"><label>Company / Organization</label><input id="f_co" type="text" placeholder="Optional"></div>
      <div class="field"><label>How can we help?</label><textarea id="f_msg" placeholder="Tell us what you're trying to build or solve…"></textarea></div>
      <button class="btn btn-primary" id="sendBtn">Send message {ARROW}</button>
      <div id="formMsg"></div>
    </div>
    <div class="contact-info">
      <div class="ci"><div class="ico">{ICONS['mail']}</div><div><div class="k">Email</div><a class="v" href="mailto:ternah22@gmail.com">ternah22@gmail.com</a></div></div>
      <div class="ci"><div class="ico"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;stroke:var(--blue)"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.13 12.6a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L7.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg></div><div><div class="k">WhatsApp</div><a class="v" href="https://wa.me/256787770007" target="_blank" rel="noopener noreferrer">Chat with us</a></div></div>
      <div class="ci"><div class="ico">{ICONS['pin']}</div><div><div class="k">Based in</div><div class="v">Africa, serving the continent</div></div></div>
      <div class="ci" style="border:none"><div class="ico">{MK('#7c92ff')}</div><div><div class="k">Brand promise</div><div class="v" style="font-size:16px;font-weight:600">Practical, scalable, reliable.<br>Built for Africa's future.</div></div></div>
    </div>
  </div>
</section>'''

# ================= WRITE FILES =================
PAGES = [
 ('index','Ternah Software Company Ltd | Keep it simple.','Ternah Software Company Ltd builds custom software, ERP, automation, data and cloud solutions for businesses across Africa.',home_body),
 ('about','About | Ternah Software Company Ltd','An African software development and digital transformation company building reliable, scalable technology.',about_body),
 ('solutions','Solutions | Ternah Software Company Ltd','Custom software, ERP & business systems, automation, data & analytics, cloud and support services.',solutions_body),
 ('industries','Industries | Ternah Software Company Ltd','Software built for education, healthcare, logistics, retail, NGOs, government, finance and enterprises across Africa.',industries_body),
 ('products','Products | Ternah Software Company Ltd','Products, platforms, and systems we have designed and built across industries and markets.',products_body),
 ('insights','Insights | Ternah Software Company Ltd','Articles, technology trends, and practical guides on digital transformation across Africa.',insights_body),
 ('contact','Contact | Ternah Software Company Ltd','Get in touch with Ternah Software Company Ltd. Email ternah22@gmail.com or call +256 787 770007.',contact_body),
]

for slug,title,desc,body in PAGES:
    fn = os.path.join(OUT, f'{slug}.html')
    open(fn,'w',encoding='utf-8').write(page(slug,title,desc,body))
    print('wrote', fn)
print('done —', len(PAGES), 'pages')
