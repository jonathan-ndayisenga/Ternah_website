"""Draws the illustrated hero scenes and article covers.

Run:  python tools/make_scenes.py
Writes assets/img/art/hero-<key>.svg (1600 x 900) and assets/img/art/article-<slug>.svg (1200 x 675).
The hero lays a live product screen over the right half of each scene, so people stand on the left.
A real photo at assets/img/hero/<key>.webp or assets/img/articles/<slug>.webp replaces the drawing.
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'img' / 'art'

def person(x, y, s=1.0, skin='#7A4B2A', hair='#1C1917', hair_style='short', top='coat', inner='#3B82F6',
           pants='#1E293B', hat=None, holds=None, steth=False, glasses=False):
    """A flat, faceless figure standing with feet at (x, y); about 690 units tall at s=1."""
    g = [f'<g transform="translate({x} {y}) scale({s})">',
         '<ellipse cx="0" cy="0" rx="120" ry="16" fill="#0F172A" fill-opacity=".10"/>',
         f'<rect x="-62" y="-250" width="52" height="244" rx="22" fill="{pants}"/>',
         f'<rect x="10" y="-250" width="52" height="244" rx="22" fill="{pants}"/>',
         '<ellipse cx="-38" cy="-8" rx="40" ry="14" fill="#111827"/><ellipse cx="38" cy="-8" rx="40" ry="14" fill="#111827"/>',
         f'<path d="M-88 -470Q-88 -525 -40 -530L40 -530Q88 -525 88 -470L92 -232L-92 -232Z" fill="{inner}"/>']
    if top == 'coat':
        g += ['<path d="M-40 -530Q-95 -525 -98 -470L-110 -196L-6 -196L-6 -436Z" fill="#fff" stroke="#CBD5E1" stroke-width="3"/>',
              '<path d="M40 -530Q95 -525 98 -470L110 -196L6 -196L6 -436Z" fill="#fff" stroke="#CBD5E1" stroke-width="3"/>',
              '<rect x="34" y="-280" width="46" height="44" rx="6" fill="none" stroke="#CBD5E1" stroke-width="3"/>',
              '<path d="M46 -280v-18M58 -280v-24" stroke="#2563EB" stroke-width="5" stroke-linecap="round"/>']
        sleeve = '#fff'
    elif top == 'vest':
        g += ['<path d="M-40 -530Q-92 -525 -94 -470L-98 -250L-8 -250L-8 -436Z" fill="#F97316"/>',
              '<path d="M40 -530Q92 -525 94 -470L98 -250L8 -250L8 -436Z" fill="#F97316"/>',
              '<rect x="-94" y="-460" width="86" height="16" fill="#E5E7EB"/><rect x="8" y="-460" width="86" height="16" fill="#E5E7EB"/>',
              '<rect x="-96" y="-280" width="88" height="16" fill="#E5E7EB"/><rect x="8" y="-280" width="88" height="16" fill="#E5E7EB"/>']
        sleeve = inner
    elif top == 'overall':
        g += [f'<path d="M-70 -400H70L92 -232H-92Z" fill="{pants}"/>',
              f'<path d="M-62 -400L-50 -528M62 -400L50 -528" stroke="{pants}" stroke-width="18" stroke-linecap="round"/>']
        sleeve = inner
    else:  # scrubs
        g += ['<path d="M-22 -530L0 -478L22 -530" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="5"/>']
        sleeve = inner
    sk = f'stroke="{sleeve}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    if holds == 'tablet':
        g += [f'<path d="M-82 -482L-104 -344L-62 -330" {sk}/>', f'<path d="M82 -482L104 -344L62 -330" {sk}/>',
              '<rect x="-74" y="-398" width="148" height="104" rx="12" fill="#1E293B"/>',
              '<rect x="-64" y="-388" width="128" height="84" rx="6" fill="#DBEAFE"/>',
              '<rect x="-54" y="-378" width="50" height="10" rx="5" fill="#2563EB"/><rect x="-54" y="-360" width="108" height="8" rx="4" fill="#93C5FD"/>',
              '<rect x="-54" y="-344" width="80" height="8" rx="4" fill="#93C5FD"/><rect x="-54" y="-328" width="96" height="8" rx="4" fill="#93C5FD"/>',
              f'<circle cx="-66" cy="-328" r="17" fill="{skin}"/><circle cx="66" cy="-328" r="17" fill="{skin}"/>']
    elif holds == 'clipboard':
        g += [f'<path d="M-82 -482L-100 -262" {sk}/>', f'<circle cx="-100" cy="-250" r="18" fill="{skin}"/>',
              f'<path d="M82 -482L110 -350L56 -330" {sk}/>',
              '<rect x="-10" y="-420" width="100" height="130" rx="8" fill="#B45309"/>',
              '<rect x="0" y="-408" width="80" height="110" rx="4" fill="#fff"/>',
              '<rect x="22" y="-428" width="36" height="16" rx="4" fill="#64748B"/>',
              '<path d="M12 -386h56M12 -366h44M12 -346h56M12 -326h36" stroke="#94A3B8" stroke-width="6" stroke-linecap="round"/>',
              f'<circle cx="58" cy="-330" r="17" fill="{skin}"/>']
    else:
        g += [f'<path d="M-82 -482L-100 -262" {sk}/>', f'<path d="M82 -482L100 -262" {sk}/>',
              f'<circle cx="-100" cy="-250" r="18" fill="{skin}"/><circle cx="100" cy="-250" r="18" fill="{skin}"/>']
    g += [f'<rect x="-16" y="-566" width="32" height="44" rx="10" fill="{skin}"/>',
          f'<ellipse cx="-44" cy="-604" rx="9" ry="13" fill="{skin}"/><ellipse cx="44" cy="-604" rx="9" ry="13" fill="{skin}"/>',
          f'<ellipse cx="0" cy="-608" rx="44" ry="52" fill="{skin}"/>']
    if steth:
        g += ['<path d="M-28 -528Q-50 -468 -22 -444Q0 -430 22 -444Q50 -468 28 -528" fill="none" stroke="#334155" stroke-width="6"/>',
              '<path d="M0 -436V-420" stroke="#334155" stroke-width="6"/><circle cx="0" cy="-414" r="10" fill="#94A3B8" stroke="#334155" stroke-width="4"/>']
    if hat:
        g += [f'<path d="M-54 -620Q-54 -690 0 -692Q54 -690 54 -620Z" fill="{hat}"/>',
              f'<rect x="-64" y="-626" width="128" height="14" rx="7" fill="{hat}"/>',
              '<path d="M0 -690V-626" stroke="#0F172A" stroke-opacity=".15" stroke-width="8"/>']
    elif hair_style == 'short':
        g += [f'<path d="M-46 -612Q-48 -668 0 -668Q48 -668 46 -612Q40 -642 0 -644Q-40 -642 -46 -612Z" fill="{hair}"/>']
    elif hair_style == 'bun':
        g += [f'<circle cx="0" cy="-676" r="26" fill="{hair}"/>',
              f'<path d="M-47 -598Q-52 -668 0 -670Q52 -668 47 -598Q44 -640 0 -642Q-44 -640 -47 -598Z" fill="{hair}"/>']
    if glasses:
        g += ['<g fill="none" stroke="#0F172A" stroke-width="4"><circle cx="-17" cy="-606" r="12"/><circle cx="17" cy="-606" r="12"/><path d="M-5 -606h10"/></g>']
    g.append('</g>')
    return ''.join(g)

def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" '
            f'role="img">{body}</svg>\n')

def hero_health():
    wall = ''.join(f'<path d="M{x} 0V760"/>' for x in range(200, 1600, 200))
    bg = f'''<defs><linearGradient id="hw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F1F6FF"/><stop offset="1" stop-color="#DCE7FA"/></linearGradient>
<linearGradient id="hsky" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#BFDBFE"/><stop offset="1" stop-color="#EFF6FF"/></linearGradient>
<radialGradient id="hglow" cx=".7" cy=".3" r=".6"><stop offset="0" stop-color="#3B82F6" stop-opacity=".22"/><stop offset="1" stop-color="#3B82F6" stop-opacity="0"/></radialGradient></defs>
<rect width="1600" height="900" fill="url(#hw)"/><rect width="1600" height="900" fill="url(#hglow)"/>
<g stroke="#C7D7F2" stroke-width="2">{wall}</g>
<rect x="70" y="110" width="300" height="330" rx="14" fill="#fff"/><rect x="84" y="124" width="272" height="302" rx="8" fill="url(#hsky)"/>
<path d="M220 124V426M84 275H356" stroke="#fff" stroke-width="10"/>
<g transform="translate(560 110)"><rect width="110" height="110" rx="22" fill="#2563EB"/><path d="M55 28v54M28 55h54" stroke="#fff" stroke-width="16" stroke-linecap="round"/></g>
<rect x="0" y="760" width="1600" height="140" fill="#C3D3EE"/><rect x="0" y="760" width="1600" height="6" fill="#AFC3E6"/>
<g transform="translate(100 770)"><rect x="-40" y="-90" width="80" height="90" rx="10" fill="#1E40AF"/>
<path d="M0 -90C-60 -150 -70 -230 -20 -260C0 -200 10 -150 0 -90ZM0 -90C50 -170 90 -200 110 -190C90 -140 50 -110 0 -90ZM0 -90C-30 -180 -10 -260 30 -280C40 -220 30 -150 0 -90Z" fill="#16A34A"/></g>'''
    people = (person(540, 850, .95, skin='#5C3A21', hair='#111827', hair_style='short', top='scrubs', inner='#0D9488', pants='#0F766E', holds='clipboard', glasses=True) +
              person(280, 875, 1.0, skin='#7A4B2A', hair='#1C1917', hair_style='bun', top='coat', inner='#2563EB', pants='#1E3A8A', holds='tablet', steth=True))
    return svg(1600, 900, bg + people)

def hero_factories():
    windows = ''.join(f'<rect x="{60+i*160}" y="60" width="130" height="150" rx="6"/>' for i in range(10))
    rollers = ''.join(f'<circle cx="{400+i*45}" cy="637" r="10"/>' for i in range(9))
    boxes = ''.join(f'<rect x="{410+i*120}" y="548" width="84" height="72" rx="6" fill="#D97706"/><path d="M{410+i*120} 572h84" stroke="#92400E" stroke-width="5"/>' for i in range(3))
    bg = f'''<defs><linearGradient id="fw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF2F8"/><stop offset="1" stop-color="#DAE2EE"/></linearGradient>
<radialGradient id="fglow" cx=".7" cy=".3" r=".6"><stop offset="0" stop-color="#3B82F6" stop-opacity=".2"/><stop offset="1" stop-color="#3B82F6" stop-opacity="0"/></radialGradient></defs>
<rect width="1600" height="900" fill="url(#fw)"/><rect width="1600" height="900" fill="url(#fglow)"/>
<g fill="#fff" fill-opacity=".8">{windows}</g>
<path d="M0 230H1600" stroke="#94A3B8" stroke-width="14"/>
<g fill="#CBD5E1" stroke="#94A3B8" stroke-width="4"><rect x="40" y="300" width="150" height="460" rx="70"/><rect x="210" y="360" width="130" height="400" rx="60"/></g>
<g stroke="#94A3B8" stroke-width="6"><path d="M115 300V230M275 360V230"/></g>
<rect x="0" y="760" width="1600" height="140" fill="#B8C4D6"/><rect x="0" y="760" width="1600" height="6" fill="#A3B1C6"/>
<rect x="380" y="620" width="400" height="34" rx="17" fill="#334155"/><g fill="#64748B">{rollers}</g>
<rect x="400" y="654" width="16" height="106" fill="#475569"/><rect x="744" y="654" width="16" height="106" fill="#475569"/>
<g>{boxes}</g>'''
    people = (person(545, 880, .9, skin='#4A2E1E', top='overall', inner='#93C5FD', pants='#1D4ED8', hat='#F8FAFC', holds='clipboard') +
              person(260, 885, 1.0, skin='#7A4B2A', top='vest', inner='#1E3A8A', pants='#1E293B', hat='#FACC15', holds='tablet'))
    return svg(1600, 900, bg + people)

# ---- article covers: shiny blue with one white motif ----
def cover(key, motif):
    return svg(1200, 675, f'''<defs><linearGradient id="c-{key}" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0B1F4D"/><stop offset=".55" stop-color="#1D4ED8"/><stop offset="1" stop-color="#3B82F6"/></linearGradient>
<radialGradient id="cg-{key}" cx=".8" cy=".15" r=".6"><stop offset="0" stop-color="#93C5FD" stop-opacity=".5"/><stop offset="1" stop-color="#93C5FD" stop-opacity="0"/></radialGradient>
<pattern id="cd-{key}" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.4" fill="#fff" fill-opacity=".12"/></pattern></defs>
<rect width="1200" height="675" fill="url(#c-{key})"/><rect width="1200" height="675" fill="url(#cd-{key})"/><rect width="1200" height="675" fill="url(#cg-{key})"/>
<circle cx="120" cy="640" r="220" fill="#60A5FA" fill-opacity=".16"/>{motif}''')

W = 'fill="#fff"'
S = 'fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"'

def bars(xs, base, color):
    return ''.join(f'<rect x="{x}" y="{base-h}" width="34" height="{h}" rx="6" fill="{color}"/>' for x, h in xs)

ARTICLES = {
 'manual-to-intelligent': f'''
<g transform="translate(250 200)"><rect x="24" y="-18" width="220" height="280" rx="12" {W} fill-opacity=".45"/><rect width="220" height="280" rx="12" {W}/>
<path d="M30 50h160M30 90h130M30 130h160M30 170h100M30 210h140" stroke="#94A3B8" stroke-width="10" stroke-linecap="round"/></g>
<path d="M530 340h130M630 300l40 40-40 40" {S}/>
<g transform="translate(720 190)"><rect width="300" height="210" rx="18" {W}/><rect x="16" y="16" width="268" height="178" rx="8" fill="#DBEAFE"/>
{bars([(40,50),(96,80),(152,110),(208,140)], 170, '#2563EB')}
<rect x="110" y="210" width="80" height="40" fill="#fff"/><rect x="70" y="248" width="160" height="14" rx="7" fill="#fff"/></g>''',
 'offline-first': f'''
<g transform="translate(420 140)"><rect width="200" height="380" rx="34" fill="#0F172A"/><rect x="14" y="40" width="172" height="300" rx="10" fill="#DBEAFE"/>
<rect x="34" y="70" width="132" height="22" rx="11" fill="#2563EB"/><rect x="34" y="110" width="100" height="14" rx="7" fill="#93C5FD"/><rect x="34" y="138" width="120" height="14" rx="7" fill="#93C5FD"/>
<circle cx="100" cy="270" r="34" fill="#22C55E"/><path d="M84 270l12 12 22-24" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></g>
<g transform="translate(760 220)"><path d="M0 120a70 70 0 0 1 20-136a90 90 0 0 1 170 20a60 60 0 0 1 10 116z" {W} fill-opacity=".92"/>
<path d="M70 70a40 40 0 0 1 60 0M85 92a18 18 0 0 1 30 0" fill="none" stroke="#2563EB" stroke-width="9" stroke-linecap="round"/>
<path d="M50 10L150 120" stroke="#EF4444" stroke-width="10" stroke-linecap="round"/></g>
<path d="M660 480c60 30 120 20 160-30M810 430l16 22 14-26" {S}/>''',
 'buy-vs-build': f'''
<path d="M600 560V170" {S}/>
<g transform="translate(600 210)"><path d="M0 0h230l40 40-40 40H0z" {W}/><path d="M0 110h-230l-40 40 40 40H0z" {W} fill-opacity=".85"/>
<rect x="30" y="28" width="120" height="24" rx="12" fill="#2563EB"/><rect x="-200" y="138" width="120" height="24" rx="12" fill="#1E3A8A"/></g>
<g transform="translate(240 450)">{''.join(f'<rect x="{c*62+r*31}" y="{-r*62}" width="56" height="56" rx="8" {W} fill-opacity="{.95-r*.15:.2f}"/>' for r in range(3) for c in range(3-r))}</g>
<g transform="translate(820 420)"><path d="M0 40L90 0L180 40L90 80Z" {W}/><path d="M0 40V140L90 180V80Z" {W} fill-opacity=".75"/><path d="M180 40V140L90 180V80Z" {W} fill-opacity=".55"/></g>''',
 'dashboards-to-decisions': f'''
<g transform="translate(250 150)"><rect width="520" height="360" rx="22" {W}/><rect x="24" y="24" width="150" height="90" rx="10" fill="#DBEAFE"/>
<rect x="190" y="24" width="150" height="90" rx="10" fill="#DBEAFE"/><rect x="356" y="24" width="140" height="90" rx="10" fill="#DBEAFE"/>
<polyline points="40,300 120,250 200,270 290,190 380,210 480,140" fill="none" stroke="#2563EB" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="44" y="52" width="80" height="14" rx="7" fill="#2563EB"/><rect x="210" y="52" width="60" height="14" rx="7" fill="#2563EB"/><rect x="376" y="52" width="90" height="14" rx="7" fill="#2563EB"/></g>
<g transform="translate(900 330)"><circle r="110" fill="none" stroke="#fff" stroke-width="16"/><circle r="66" fill="none" stroke="#fff" stroke-width="16" stroke-opacity=".7"/><circle r="22" {W}/>
<path d="M150 -150L14 -14" {S}/><path d="M150 -150l-8 46M150 -150l-46 8" {S}/></g>''',
 'automation-roi': f'''
<g transform="translate(400 340)" {S}><circle r="110"/><circle r="40"/>{''.join(f'<path d="M0 -110V-150" transform="rotate({a})"/>' for a in range(0,360,40))}</g>
<g transform="translate(590 210)" {S} stroke-opacity=".8"><circle r="60"/><circle r="22"/>{''.join(f'<path d="M0 -60V-86" transform="rotate({a})"/>' for a in range(0,360,45))}</g>
<g transform="translate(820 520)">{''.join(f'<ellipse cx="0" cy="{-i*30}" rx="90" ry="26" {W} fill-opacity="{.95-i*.1:.2f}" stroke="#93C5FD" stroke-width="4"/>' for i in range(5))}</g>
<path d="M720 330L840 220L890 260L1000 150M960 150h40v40" {S}/>''',
 'scale-from-day-one': f'''
<g transform="translate(260 150)">{''.join(f'<rect y="{i*100}" width="300" height="80" rx="14" {W} fill-opacity="{1-i*.12:.2f}"/><circle cx="40" cy="{40+i*100}" r="10" fill="#22C55E"/><rect x="70" y="{34+i*100}" width="160" height="12" rx="6" fill="#93C5FD"/>' for i in range(4))}</g>
<g fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"><path d="M580 330H700M700 330L800 220M700 330H820M700 330L800 440"/></g>
<g {W}><circle cx="830" cy="210" r="40"/><circle cx="860" cy="330" r="40"/><circle cx="830" cy="450" r="40"/></g>
<g fill="#fff" fill-opacity=".6"><circle cx="960" cy="160" r="24"/><circle cx="990" cy="260" r="24"/><circle cx="1000" cy="380" r="24"/><circle cx="960" cy="490" r="24"/></g>''',
}

def waves():
    """A bundle of flowing light lines on a transparent background, 1600 x 600.
    Every line repeats exactly every 1600 units, so the image tiles left to right without a seam
    and can drift sideways forever (see .waves in styles.css)."""
    import math
    W, H, N = 1600, 600, 34
    paths = []
    for i in range(N):
        t = i / (N - 1)
        base = 150 + t * 300
        a1, a2 = 95 - 30 * t, 26 + 20 * t
        ph1, ph2 = t * 1.1, 1.7 - t * 2.4
        pts = []
        for x in range(0, W + 1, 16):
            y = base + a1 * math.sin(2 * math.pi * x / W + ph1) + a2 * math.sin(2 * math.pi * 2 * x / W + ph2)
            pts.append(f'{x} {y:.1f}')
        r, g, b = (int(29 + (34 - 29) * t), int(78 + (211 - 78) * t), int(216 + (238 - 216) * t))  # #1D4ED8 -> #22D3EE
        bright = i % 7 == 3
        paths.append(f'<path d="M{" L".join(pts)}" stroke="rgb({r},{g},{b})" stroke-opacity="{.95 if bright else .35 + .4 * math.sin(math.pi * t):.2f}" '
                     f'stroke-width="{2.6 if bright else 1.4}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">'
            f'<g fill="none" stroke-linecap="round">{"".join(paths)}</g></svg>\n')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'waves.svg').write_text(waves(), encoding='utf-8')
    (OUT / 'hero-ternah-health.svg').write_text(hero_health(), encoding='utf-8')
    (OUT / 'hero-ternah-factories.svg').write_text(hero_factories(), encoding='utf-8')
    for slug, motif in ARTICLES.items():
        (OUT / f'article-{slug}.svg').write_text(cover(slug, motif), encoding='utf-8')
    print('wrote', 2 + len(ARTICLES), 'files to', OUT)

if __name__ == '__main__':
    main()
