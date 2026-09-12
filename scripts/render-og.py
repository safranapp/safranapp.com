#!/usr/bin/env python3
"""
Render the cards link previews show (WhatsApp, iMessage, Slack, X, LinkedIn).

The default was the bare app icon on cream, which reads as a placeholder in a
chat thread. This puts the product on it: brand mesh, wordmark, the promise in
one line, and a real screen from the app - one card per language.

    python3 scripts/render-og.py   ->  assets/og-image.png  (en)
                                       assets/og-image-nl.png

Stops match app/src/components/ui/MeshBackground.tsx (and the email header),
so every brand surface is the same gradient.

Needs numpy, Pillow, cairosvg and the Google Fonts package (Linux paths).
"""
import io
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, 'assets')

W, H = 1200, 630
BASE = (0xFD, 0xF7, 0xE7)
PEAK = 0.92
INK = (0x52, 0x51, 0x4C)
MUTED = (0x84, 0x82, 0x7E)
L = 88                                  # left margin for all text

STOPS = [
    ('#DECDEC', 0.5, 0.5, 0.60),
    ('#E5FAFB', -0.2, -0.2, 0.50),
    ('#E6DFF1', 0.9, 0.1, 0.50),
    ('#FEF8DC', -0.1, 0.8, 0.55),
    ('#FFDCE9', 0.85, 0.9, 0.50),
]

COPY = {
    'en': {
        'out': 'og-image.png',
        'shot': 'include-1-en.webp',
        'head': ['Your AI', 'health coach'],
        'sub': ['Chat what you ate, snap a photo, import',
                'recipes. Safran plans the rest and adjusts',
                'every week.'],
    },
    'nl': {
        'out': 'og-image-nl.png',
        'shot': 'include-1-nl.webp',
        'head': ['Je AI', 'health coach'],
        'sub': ['Typ wat je at, stuur een foto, importeer',
                'recepten. Safran regelt de rest en stuurt',
                'elke week bij.'],
    },
}

FONT_DIR = '/usr/share/fonts/truetype/google-fonts'


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def hex_rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float64)


def render_mesh():
    """The brand gradient: alpha-over each bloom, three-stop falloff."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float64)
    canvas = np.zeros((H, W, 3), dtype=np.float64) + np.array(BASE, dtype=np.float64)
    span = max(W, H)
    for colour, cx, cy, r in STOPS:
        d = np.hypot(xx - cx * W, yy - cy * H) / (r * span)
        a = np.where(
            d < 0.55,
            PEAK + (PEAK * 0.55 - PEAK) * (d / 0.55),
            np.where(d < 1.0, PEAK * 0.55 * (1 - (d - 0.55) / 0.45), 0.0),
        )
        a = np.clip(a, 0, 1)[..., None]
        canvas = canvas * (1 - a) + hex_rgb(colour) * a
    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')


MARK = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <path d="M 76,120 L 76,104 C 76,98 46,100 46,78 C 46,58 62,50 69,53 C 73,36 87,30 100,30
           C 113,30 127,36 131,53 C 138,50 154,58 154,78 C 154,100 124,98 124,104 L 124,120
           Q 124,128 116,128 L 84,128 Q 76,128 76,120 Z"
        fill="none" stroke="#52514C" stroke-width="11" stroke-linejoin="round" stroke-linecap="round"/>
  <rect x="78" y="143" width="44" height="14" rx="7" fill="none" stroke="#52514C" stroke-width="9"/>
  <path d="M 84,166.5 A 16,16 0 0 0 116,166.5 Z" fill="#52514C"/>
</svg>'''


def phone(shot_name):
    """The app screenshot in a black frame, sized to bleed off the bottom."""
    PHONE_W, BEZEL, RADIUS = 330, 9, 52
    shot = Image.open(os.path.join(ASSETS, shot_name)).convert('RGB')
    inner_w = PHONE_W - BEZEL * 2
    shot = shot.resize((inner_w, int(inner_w * shot.height / shot.width)), Image.LANCZOS)
    h = shot.height + BEZEL * 2

    body = Image.new('RGBA', (PHONE_W, h), (0, 0, 0, 0))
    ImageDraw.Draw(body).rounded_rectangle([0, 0, PHONE_W - 1, h - 1], RADIUS, fill=(28, 28, 30, 255))
    mask = Image.new('L', (inner_w, shot.height), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, inner_w - 1, shot.height - 1], RADIUS - BEZEL, fill=255)
    screen = shot.convert('RGBA')
    screen.putalpha(mask)
    body.alpha_composite(screen, (BEZEL, BEZEL))
    return body, RADIUS


def render(lang, c, mesh, mark):
    img = mesh.copy()

    body, radius = phone(c['shot'])
    px, py = 760, 96
    shadow = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [px + 10, py + 24, px + body.width + 10, py + body.height + 24], radius, fill=(0, 0, 0, 60))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(26)))
    img.alpha_composite(body, (px, py))

    img.alpha_composite(mark, (L - 6, 92))
    d = ImageDraw.Draw(img)
    d.text((L + 66, 108), 'SAFRAN', font=font('Poppins-Bold.ttf', 34), fill=INK)
    for i, line in enumerate(c['head']):
        d.text((L, 214 + i * 78), line, font=font('Poppins-Bold.ttf', 72), fill=INK)
    for i, line in enumerate(c['sub']):
        d.text((L, 404 + i * 40), line, font=font('Poppins-Regular.ttf', 27), fill=MUTED)

    out = os.path.join(ASSETS, c['out'])
    img.convert('RGB').save(out, 'PNG', optimize=True)
    print(f"{lang}: {out} ({os.path.getsize(out) // 1024} KB)")


mesh = render_mesh()
mark = Image.open(io.BytesIO(cairosvg.svg2png(
    bytestring=MARK.encode(), output_width=64, output_height=64))).convert('RGBA')
for lang, c in COPY.items():
    render(lang, c, mesh, mark)
