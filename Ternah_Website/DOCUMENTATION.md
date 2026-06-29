# Ternah Website Build Playbook

A reusable system for building fast, no-build-step marketing websites — one Python script generates every HTML page from shared templates and a content list. Built once for the Ternah site; designed to be copied and reused for any client project.

**This document covers:**
1. The reusable architecture (works for any client)
2. How to spin up a new site from this template
3. The design system framework (colors/fonts/spacing — swap per client)
4. A complete font-size reference
5. The component menu (what you can offer a client, and what each costs to build)
6. A pricing framework for quoting website projects
7. Deployment

---

## 1. The architecture (reusable for any client)

```
client-site/
├── build_pages.py          ← single source of truth — generates every .html file
├── index.html               ← generated (never hand-edit)
├── about.html                ← generated
├── ...other-pages.html        ← generated
└── assets/
    ├── css/styles.css        ← hand-edited (the only stylesheet)
    ├── js/main.js              ← hand-edited (the only script)
    ├── favicon.svg
    └── og-image.svg
```

**Golden rule: never hand-edit a generated `.html` file.** Edit `build_pages.py`, then re-run it. Every page rebuilds from the same shared header, footer, and nav — change those once, every page updates everywhere.

### Why this system is worth reusing
- Zero dependencies, zero build pipeline, zero version drift — works on any static host
- One content list per content type (services, projects, testimonials, articles) — no copy-pasting the same card markup across files
- A client's entire site is one `.py` file + one `.css` file + one `.js` file — easy to hand off, easy to maintain, easy to price (see section 6)
- Ships in days, not weeks, once the design system (section 3) is set

### Rebuild command (same for every project)
```bash
python build_pages.py
```

---

## 2. Spinning up a new client site from this template

1. **Copy the folder structure** above into a new project directory
2. **Strip the content lists** (`SOLUTIONS`, `INDUSTRIES`, `PROJECTS`, `TESTIMONIALS`, `INSIGHTS`, etc.) and replace with the new client's content
3. **Set the design tokens** (section 3) to the client's brand colors and pick a font
4. **Update `NAV_ITEMS` and `PAGES`** to match the pages this client actually needs (not every project needs all 7 — a 3-page brochure site is valid)
5. **Update `SITE_URL`**, contact details (WhatsApp number, email, phone), and social meta image
6. **Run `python build_pages.py`**, review locally, then deploy (section 7)

### Adding a new page to any project built on this system
1. Write a `<slug>_body = f'''...'''` string following the pattern of existing `*_body` variables
2. Add `('<slug>', 'Page Title | Client Name', 'meta description', <slug>_body)` to `PAGES`
3. Add `('<slug>', 'Nav Label')` to `NAV_ITEMS` if it belongs in the nav
4. Rebuild

---

## 3. Design system framework (customize per client)

Every visual decision is a CSS variable in `assets/css/styles.css :root` — change these eight lines and the whole site re-skins:

```css
:root{
  --navy:#0a0f2c;        /* primary text + dark surfaces */
  --ink:#070a1f;          /* darkest tone, hero gradients */
  --blue:#2f4cff;          /* primary brand accent */
  --blue-soft:#4d68ff;      /* secondary accent shade */
  --green:#15803d;          /* optional second accent */
  --green-soft:#22c55e;
  --bg:#f5f7ff;              /* page background */
  --mute:rgba(10,15,44,.58); /* body text */
  --border:rgba(10,15,44,.10);
  --sf:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
}
```

**To re-skin for a new client:** swap `--navy`/`--blue`/`--green` for their brand colors, swap `--sf` for their chosen font (load it via Google Fonts `<link>` in the page template), keep every other rule untouched. The type scale, spacing, and component shapes are brand-agnostic by design.

### Typography voice — two presets

| Preset | Weight | Letter-spacing | Feel | Use for |
|---|---|---|---|---|
| **Refined** (current Ternah setting) | 500 | tight/negative (-0.04 to -0.06em) | Quiet, premium, SaaS-like | Tech, consulting, professional services |
| **Bold/Maximalist** | 800 | wider/neutral (-0.02 to -0.03em) | Loud, confident, attention-grabbing | Retail, events, youth brands |

Switch between them by changing `h1,h2,h3{font-weight:...;letter-spacing:...}` — one line decides the entire site's personality.

---

## 4. Font-size reference (reusable scale)

This scale works at any brand's font — only the `font-family` changes, the proportions don't need to.

| Element | Size (mobile → desktop, `clamp()`) | Weight | Letter-spacing |
|---|---|---|---|
| Hero headline | 44px → 88px | 500 | -0.06em |
| Hero subheading | 20px → 32px | 500 | -0.03em |
| Inner page `<h1>` | 40px → 80px | 500 | -0.05em |
| Section heading (`.h2`) | 30px → 56px | 500 | -0.04em |
| Lead paragraph | 17px → 21px | 500 | -0.01em |
| Eyebrow/label | 12px fixed | 500 | +0.06em uppercase |
| Card heading | 24px fixed | 500 | -0.05em |
| Card body text | 16px fixed | 400 | — |
| Stat number | 38px → 58px | 500 | -0.04em |
| Nav links | 14.5px fixed | 500 | — |
| Buttons | 15px fixed | 500 | -0.02em |
| Footer text | 15px fixed | 400 | — |

Layout constants that travel with the scale: max content width `1280px`, section padding `40px → 32px → 24px → 16px` across 4 breakpoints (`1280 / 1024 / 768 / 480`), border-radius `100px` pills / `24px` cards.

---

## 5. Component menu — what you can offer a client

Each row is a feature module already built and proven on the Ternah site. Use this as a build menu when scoping a new project — tick what the client needs, price accordingly (section 6).

| Component | What it does | Build complexity |
|---|---|---|
| Sticky nav + mobile burger menu | Scroll-blur header, active-page indicator, auto-closing mobile drawer | Low |
| Animated canvas hero (waves) | Looping generative background animation behind the headline | Medium |
| Scroll-reveal animations | Content fades/slides in as it enters the viewport | Low |
| Filterable grid (pills) | Click a category, grid filters + scrolls to match | Medium |
| Article/content modal system | Full-screen reading view for long-form content, no page reload | Medium |
| Floating contact buttons (FABs) | WhatsApp / Email / Call, fixed corner, hover tooltips | Low |
| Scroll-driven color grading | Ambient brand-color blobs shift as the page scrolls | Medium |
| Contact form (client-side) | Opens user's email client pre-filled — no backend/server needed | Low |
| Contact form (server-side) | Actually sends email via a backend — requires hosting with server support | High (extra cost — see add-ons) |
| SEO + social preview tags | Canonical URLs, Open Graph image, Twitter Card, favicon | Low |
| Multi-page content system (this whole architecture) | Everything generated from one script — no duplicated markup | Foundational (included in every quote) |

---

## 6. Pricing framework

A starting framework for quoting projects built on this system. **Adjust the numbers to your market and currency** — these are relative tiers, not fixed prices.

### Tier 1 — Starter / Brochure site
**3–5 pages** (Home, About, Services, Contact). No custom interactive components beyond nav + contact form + responsive layout.
- Best for: small businesses, solo professionals, simple service listings
- Timeline: 3–5 working days
- What's included: design system setup, all pages, mobile responsive, basic SEO tags, client-side contact form

### Tier 2 — Standard Business site
**5–8 pages** + 2–3 components from the menu above (e.g. filterable grid, FABs, scroll-reveal animations).
- Best for: growing businesses, multi-service companies, anyone needing a "real" site with personality
- Timeline: 1–2 weeks
- What's included: everything in Tier 1, plus chosen components, custom illustration/icon work, content structuring for multiple service/product lines

### Tier 3 — Premium / Full-feature site
**8+ pages** + most/all components from the menu, including modals, scroll-driven color grading, custom animation, article/insights system.
- Best for: companies positioning as premium/tech-forward, content-heavy sites, platforms with ongoing articles/updates
- Timeline: 2–4 weeks
- What's included: everything in Tier 2, plus full component menu, performance tuning, detailed SEO/social setup, a documentation handoff (like this file) so the client's team can maintain it

### Add-ons (quote separately, on top of any tier)
| Add-on | Why it costs extra |
|---|---|
| Server-side contact form / backend integration | Requires server hosting, not just static hosting |
| CMS or admin panel for non-technical content edits | Significant extra engineering beyond the static-generator model |
| Custom logo / full brand identity design | Separate design discipline from web build |
| Copywriting (all page text written from scratch) | Separate skill, billed by word count or page count |
| Ongoing maintenance retainer | Recurring monthly fee — content updates, security patches, monitoring |
| Domain + hosting setup and first-year cost | Pass-through cost from registrar/host, plus setup time |
| Rush delivery (compressed timeline) | Premium for working outside normal pace |

### How to scope a quote quickly
1. Count the pages the client actually needs (don't default to 7 — some need 3, some need 12)
2. Walk the component menu (section 5) and mark what they want
3. Pick the tier that matches page count + component count
4. Add any add-ons separately, itemized, so the client sees what's optional
5. State the timeline clearly — this system is fast, and that speed is part of the value being sold

---

## 7. Deployment (generic — works for any static host)

This system needs nothing but a place to run one Python script and serve static files. Tested settings for Render:

| Setting | Value |
|---|---|
| Root Directory | the folder containing `build_pages.py` |
| Build Command | `python build_pages.py` |
| Publish Directory | `./` |

The same two facts (run the script, serve the output folder) apply to Netlify, Vercel (static mode), GitHub Pages (via Actions), or a plain VPS with a cron job. Nothing about this system is host-specific.

Update `SITE_URL` in `build_pages.py` to the live domain once one is confirmed, then rebuild — canonical URLs and Open Graph image URLs update automatically across every page.

---

## 8. Local development

```bash
# 1. Edit build_pages.py (content) or assets/css/styles.css (design)
# 2. Regenerate HTML
python build_pages.py
# 3. Preview
python -m http.server 8000
```
