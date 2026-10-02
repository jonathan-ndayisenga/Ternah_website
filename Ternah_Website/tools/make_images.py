#!/usr/bin/env python3
"""One-off generator for the PNG icons and the Open Graph image.
Needs Pillow (pip install pillow). Run from the site folder: python tools/make_images.py
The outputs are committed, so the Render build does not need Pillow."""
import os, pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAV, BG, INK, MUTED, BORDER = '#14233A', '#F4F3EF', '#15202E', '#5B6472', '#E4E2DB'

def font(size, bold=True):
    for name in (['seguisb.ttf', 'segoeuib.ttf', 'arialbd.ttf'] if bold else ['segoeui.ttf', 'arial.ttf']):
        for d in (os.environ.get('WINDIR', 'C:/Windows') + '/Fonts', '/usr/share/fonts/truetype/dejavu'):
            p = os.path.join(d, name)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

# Ternah mark polygons (from the SVG paths, viewBox 0 0 100 94; curves approximated by their corners).
MARK = [
    [(27,14),(45,14),(47,18),(38,41),(33,41),(24,19)],
    [(58,14),(84,14),(87,18),(87,34),(82,36),(74,30),(34,78),(29,80),(18,80),(16,75)],
    [(73,78),(55,78),(53,74),(62,51),(67,51),(76,73)],
]

def draw_mark(img, x, y, size, color):
    """Draw the mark into img with its 100-unit box at (x, y), size px wide."""
    s = 4
    layer = Image.new('L', (size * s, size * s), 0)
    d = ImageDraw.Draw(layer)
    u = size * s / 100
    for poly in MARK:
        d.polygon([(px * u, py * u) for px, py in poly], fill=255)
    layer = layer.resize((size, size), Image.LANCZOS)
    img.paste(Image.new('RGBA', (size, size), color), (x, y), layer)

def tile(size, bg, fg, radius_ratio=0.22):
    img = Image.new('RGBA', (size * 4, size * 4), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=int(size * 4 * radius_ratio), fill=bg)
    img = img.resize((size, size), Image.LANCZOS)
    m = int(size * .82)
    draw_mark(img, (size - m) // 2, (size - m) // 2 + size // 40, m, fg)
    return img

assets = ROOT / 'assets'
tile(32, NAV, 'white').save(assets / 'favicon-32.png')
apple = Image.new('RGBA', (180, 180), BG)   # iOS adds its own rounding; fill edge to edge
draw_mark(apple, 30, 28, 120, NAV)
apple.convert('RGB').save(assets / 'apple-touch-icon.png')

og = Image.new('RGBA', (1200, 630), BG)
d = ImageDraw.Draw(og)
draw_mark(og, 90, 92, 96, NAV)
d.text((204, 108), 'Ternah', font=font(52), fill=INK)
d.text((96, 280), 'Keep it simple.', font=font(72), fill=INK)
d.text((96, 368), 'We build software that works.', font=font(72), fill=MUTED)
d.line([(96, 520), (1104, 520)], fill=BORDER, width=2)
d.text((96, 545), 'Ternah Software Company Ltd  ·  Built in Kampala, Uganda', font=font(30, bold=False), fill=MUTED)
og.convert('RGB').save(assets / 'og-image.png', optimize=True)
print('wrote favicon-32.png, apple-touch-icon.png, og-image.png')
