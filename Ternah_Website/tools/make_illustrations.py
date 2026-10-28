"""Draws the blue product illustrations used by the case studies.

Run:  python tools/make_illustrations.py
Writes assets/img/art/<product-key>.svg (800 x 500). Each one shares the same
shiny blue backdrop and glass panel; only the motif in the middle changes.
"""
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'img' / 'art'
W = 'rgba(255,255,255,'  # white with alpha, closed by the caller

def backdrop(key):
    return f'''<defs>
  <linearGradient id="bg-{key}" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#0B1F4D"/><stop offset=".55" stop-color="#1D4ED8"/><stop offset="1" stop-color="#3B82F6"/>
  </linearGradient>
  <radialGradient id="glow-{key}" cx=".78" cy=".18" r=".55">
    <stop offset="0" stop-color="#93C5FD" stop-opacity=".55"/><stop offset="1" stop-color="#93C5FD" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="sheen-{key}" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".5" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <pattern id="dots-{key}" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#fff" fill-opacity=".12"/></pattern>
</defs>
<rect width="800" height="500" fill="url(#bg-{key})"/>
<rect width="800" height="500" fill="url(#dots-{key})"/>
<rect width="800" height="500" fill="url(#glow-{key})"/>
<circle cx="80" cy="470" r="160" fill="#60A5FA" fill-opacity=".18"/>
<rect x="120" y="70" width="560" height="360" rx="28" fill="#fff" fill-opacity=".10" stroke="#fff" stroke-opacity=".35" stroke-width="1.5"/>
<rect x="121" y="71" width="558" height="150" rx="27" fill="url(#sheen-{key})"/>'''

def chip(x, y, w, label_w=60, bar=None):
    """Small floating glass card with a label line and an optional progress bar."""
    s = (f'<g><rect x="{x}" y="{y}" width="{w}" height="64" rx="16" fill="#fff" fill-opacity=".92"/>'
         f'<rect x="{x+16}" y="{y+16}" width="{label_w}" height="8" rx="4" fill="#94A3B8"/>')
    if bar is not None:
        s += (f'<rect x="{x+16}" y="{y+36}" width="{w-32}" height="10" rx="5" fill="#DBEAFE"/>'
              f'<rect x="{x+16}" y="{y+36}" width="{(w-32)*bar:.0f}" height="10" rx="5" fill="#2563EB"/>')
    return s + '</g>'

L = 'fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"'
T = 'fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"'

MOTIFS = {
 'ternah-health': f'''
<polyline points="160,260 270,260 300,200 340,330 380,170 420,290 450,260 640,260" {L}/>
<g transform="translate(560,120)"><rect width="76" height="76" rx="18" fill="#fff"/>
<path d="M38 18v40M18 38h40" stroke="#1D4ED8" stroke-width="10" stroke-linecap="round"/></g>
<g fill="#fff">{''.join(f'<circle cx="{190+i*44}" cy="370" r="14" fill-opacity="{1-i*.18:.2f}"/>' for i in range(5))}</g>
{chip(560, 340, 170, 70, .7)}''',
 'pharmacy': f'''
<g transform="rotate(-30 300 250)"><rect x="200" y="215" width="200" height="70" rx="35" fill="#fff"/>
<path d="M300 215h65a35 35 0 0 1 0 70h-65z" fill="#93C5FD"/></g>
<g transform="rotate(25 470 300)"><rect x="420" y="275" width="130" height="46" rx="23" fill="#fff" fill-opacity=".9"/>
<path d="M485 275h42a23 23 0 0 1 0 46h-42z" fill="#60A5FA"/></g>
<g transform="translate(560,110)"><rect x="12" y="0" width="56" height="22" rx="6" fill="#fff"/>
<rect x="0" y="26" width="80" height="110" rx="16" fill="#fff" fill-opacity=".9"/>
<path d="M40 60v40M20 80h40" stroke="#1D4ED8" stroke-width="8" stroke-linecap="round"/></g>
{chip(160, 340, 190, 80, .35)}''',
 'ternah-factories': f'''
<path d="M170 380V240l90 50v-50l90 50v-50l90 50V150h60v230z" fill="#fff" fill-opacity=".92"/>
<g fill="#1D4ED8">{''.join(f'<rect x="{200+i*70}" y="320" width="34" height="30" rx="5"/>' for i in range(4))}</g>
<g transform="translate(590,190)" {T}><circle r="42"/><circle r="14"/>
{''.join(f'<line x1="0" y1="-42" x2="0" y2="-58" transform="rotate({a})"/>' for a in range(0,360,45))}</g>
{chip(530, 330, 160, 60, .82)}''',
 'mykashop': f'''
<path d="M190 200h300l-20 50H210z" fill="#fff"/>
<path d="M210 250h260v120H210z" fill="#fff" fill-opacity=".85"/>
<g fill="#93C5FD">{''.join(f'<path d="M{190+i*60} 200h30l-6 50h-30z"/>' for i in range(5))}</g>
<rect x="300" y="290" width="70" height="80" rx="6" fill="#1D4ED8"/>
<g transform="translate(540,150)" {T}><path d="M0 0h22l20 90h80l16-60H34"/><circle cx="52" cy="112" r="10"/><circle cx="112" cy="112" r="10"/></g>
<g fill="#fff">{''.join(f'<rect x="{545+i*12}" y="320" width="{4 if i%3 else 7}" height="50"/>' for i in range(10))}</g>''',
 'pearl-educate': f'''
<path d="M400 140l170 70-170 70-170-70z" fill="#fff"/>
<path d="M300 250v60c0 25 200 25 200 0v-60l-100 40z" fill="#fff" fill-opacity=".85"/>
<path d="M560 214v80" {T}/><circle cx="560" cy="304" r="12" fill="#93C5FD"/>
<g fill="#FDE68A">{''.join(f'<path transform="translate({x},{y}) scale({s})" d="M0-14l4 9 10 1-7 7 2 10-9-5-9 5 2-10-7-7 10-1z"/>' for x,y,s in [(200,150,1.2),(620,140,.9),(230,360,.8)])}</g>
{chip(500, 350, 170, 50, 1)}''',
 'sacco': f'''
<g>{''.join(f'<ellipse cx="260" cy="{360-i*26}" rx="70" ry="20" fill="#fff" fill-opacity="{.95-i*.08:.2f}" stroke="#93C5FD" stroke-width="3"/>' for i in range(6))}</g>
<g fill="#fff">{''.join(f'<rect x="{400+i*46}" y="{360-h}" width="30" height="{h}" rx="6" fill-opacity="{.6+i*.1:.1f}"/>' for i,h in enumerate([60,95,130,175]))}</g>
<polyline points="400,260 450,230 500,240 600,150" {T}/><polyline points="575,150 600,150 600,175" {T}/>
<g fill="#fff"><circle cx="560" cy="380" r="0"/></g>''',
 'property': f'''
<path d="M220 250l130-100 130 100v130H220z" fill="#fff"/>
<rect x="320" y="300" width="60" height="80" rx="6" fill="#1D4ED8"/>
<rect x="250" y="270" width="44" height="40" rx="6" fill="#93C5FD"/><rect x="406" y="270" width="44" height="40" rx="6" fill="#93C5FD"/>
<g transform="translate(540,160)" {T}><circle cx="30" cy="30" r="28"/><path d="M52 50l70 70M100 98l14-14M86 84l12-12"/></g>
{chip(530, 330, 160, 70, .55)}''',
 'hospitality': f'''
<path d="M220 330a130 130 0 0 1 260 0z" fill="#fff"/>
<rect x="200" y="330" width="300" height="20" rx="10" fill="#fff"/>
<circle cx="350" cy="190" r="12" fill="#fff"/>
<g transform="translate(540,170)"><path d="M0 0h90v70a45 45 0 0 1-90 0z" fill="#fff" fill-opacity=".9"/>
<path d="M90 20h18a18 18 0 0 1 0 36h-18" {T}/><path d="M25-30c0-15 15-15 15-30M55-30c0-15 15-15 15-30" stroke="#fff" stroke-opacity=".7" stroke-width="5" fill="none" stroke-linecap="round"/></g>
{chip(530, 330, 160, 60, .9)}''',
 'queueflow': f'''
<g>{''.join(f'<rect x="{170+c*160}" y="120" width="140" height="270" rx="16" fill="#fff" fill-opacity=".14"/>'
            f'<rect x="{186+c*160}" y="136" width="70" height="8" rx="4" fill="#fff" fill-opacity=".7"/>' for c in range(3))}</g>
<g>{''.join(f'<rect x="{184+c*160}" y="{160+r*62}" width="112" height="50" rx="10" fill="#fff"/>'
            f'<rect x="{196+c*160}" y="{174+r*62}" width="{40+((c+r)%3)*18}" height="8" rx="4" fill="#94A3B8"/>'
            f'<rect x="{196+c*160}" y="{190+r*62}" width="30" height="8" rx="4" fill="#2563EB"/>'
            for c,n in enumerate([3,2,1]) for r in range(n))}</g>
<path d="M300 300c20 0 30-20 50-20" {T} stroke-dasharray="2 12"/>''',
 # industries without a product of their own
 'logistics': f'''
<path d="M170 210h230v150H170z" fill="#fff"/><path d="M400 250h80l50 55v55H400z" fill="#fff" fill-opacity=".85"/>
<path d="M420 265h50l30 35h-80z" fill="#93C5FD"/>
<circle cx="230" cy="368" r="30" fill="#1E3A8A" stroke="#fff" stroke-width="8"/><circle cx="470" cy="368" r="30" fill="#1E3A8A" stroke="#fff" stroke-width="8"/>
<path d="M560 330c40-60 60-110 110-130" {T} stroke-dasharray="4 16"/>
<g transform="translate(640 150)"><path d="M0 0c-26 0-44 20-44 44 0 32 44 76 44 76s44-44 44-76C44 20 26 0 0 0z" fill="#fff"/><circle cy="44" r="16" fill="#2563EB"/></g>
{chip(170, 120, 170, 60, .65)}''',
 'ngos': f'''
<g transform="translate(300 250)" {T}><circle r="120"/><ellipse rx="50" ry="120"/><path d="M-120 0h240M-104 -60h208M-104 60h208"/></g>
<g transform="translate(470 120)"><rect width="150" height="190" rx="12" fill="#fff"/><rect x="45" y="-10" width="60" height="22" rx="6" fill="#93C5FD"/>
<path d="M28 60l12 12 22-24M28 110l12 12 22-24M28 160l12 12 22-24" fill="none" stroke="#22C55E" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M80 66h44M80 116h44M80 166h34" stroke="#94A3B8" stroke-width="8" stroke-linecap="round"/></g>
{chip(520, 340, 160, 70, .8)}''',
 'government': f'''
<path d="M190 200L350 130L510 200Z" fill="#fff"/><rect x="200" y="200" width="300" height="20" fill="#fff"/>
<g fill="#fff" fill-opacity=".85">{''.join(f'<rect x="{220+i*62}" y="232" width="34" height="120" rx="4"/>' for i in range(5))}</g>
<rect x="180" y="352" width="340" height="28" rx="6" fill="#fff"/>
<g transform="translate(600 170)"><circle cx="40" cy="40" r="40" fill="#22C55E"/><path d="M22 40l12 12 26-26" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></g>
{chip(540, 310, 160, 80, .5)}''',
}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for key, motif in MOTIFS.items():
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" role="img">'
               f'{backdrop(key)}{motif}</svg>\n')
        (OUT / f'{key}.svg').write_text(svg, encoding='utf-8')
        print('wrote', OUT / f'{key}.svg')

if __name__ == '__main__':
    main()
