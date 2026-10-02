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

def t_mark(size, radius_ratio=0.25, pad=0):
    """Navy rounded tile with a white T, drawn geometrically to match favicon.svg."""
    s = 4 * size  # supersample
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    p = pad * 4
    d.rounded_rectangle([p, p, s - p - 1, s - p - 1], radius=int((s - 2 * p) * radius_ratio), fill=NAV)
    u = (s - 2 * p) / 64
    d.rectangle([p + 18 * u, p + 18 * u, p + 46 * u, p + 25 * u], fill='white')
    d.rectangle([p + 28.5 * u, p + 18 * u, p + 35.5 * u, p + 48 * u], fill='white')
    return img.resize((size, size), Image.LANCZOS)

assets = ROOT / 'assets'
t_mark(32).save(assets / 'favicon-32.png')
apple = Image.new('RGB', (180, 180), NAV)   # iOS adds its own rounding; fill edge to edge
apple.paste(t_mark(180, radius_ratio=0), (0, 0), t_mark(180, radius_ratio=0))
apple.save(assets / 'apple-touch-icon.png')

og = Image.new('RGB', (1200, 630), BG)
d = ImageDraw.Draw(og)
og.paste(t_mark(88), (96, 96), t_mark(88))
d.text((204, 108), 'Ternah', font=font(52), fill=INK)
d.text((96, 280), 'Keep it simple.', font=font(72), fill=INK)
d.text((96, 368), 'We build software that works.', font=font(72), fill=MUTED)
d.line([(96, 520), (1104, 520)], fill=BORDER, width=2)
d.text((96, 545), 'Ternah Software Company Ltd  ·  Built in Kampala, Uganda', font=font(30, bold=False), fill=MUTED)
og.save(assets / 'og-image.png', optimize=True)
print('wrote favicon-32.png, apple-touch-icon.png, og-image.png')
