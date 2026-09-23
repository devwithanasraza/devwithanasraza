"""
gen_terminal.py
===============
Generates TWO SVG files, side-by-side in the README:

  terminal-card.svg  (840 × 875)
    • GitHub avatar converted to ASCII art
    • Each row sweeps left→right with white cursor block
    • macOS chrome:  devwithanasraza@github: ~$ ./portrait.sh
    • Footer:  devwithanasraza@github:~$ whoami  Anas Raza

  info-card.svg  (480 × 420)
    • neofetch-style info card
    • Staggered slide-up + fade-in per row
    • macOS chrome:  devwithanasraza@github: ~$ neofetch
    • Sections: identity header, About, Stack, Highlights

Run:
    pip install Pillow
    python gen_terminal.py
"""

import sys, os, html as _html
from urllib.request import urlopen, Request
from io import BytesIO

# ─── CONFIG ──────────────────────────────────────────────────────────────────
USERNAME     = "devwithanasraza"
DISPLAY_NAME = "Anas Raza"
ROLE         = "Full Stack Developer · Software Engineer"

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def xe(s): return _html.escape(str(s), quote=True)

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1 — terminal-card.svg  (ASCII art portrait)
# ═══════════════════════════════════════════════════════════════════════════════

from PIL import Image, ImageEnhance
import numpy as np

PHOTO_PATH = os.path.join(OUT_DIR, "assets", "anas_photo.jpg")

print(f"[..] Loading uploaded portrait: {PHOTO_PATH}")
if os.path.exists(PHOTO_PATH):
    img = Image.open(PHOTO_PATH)
    print(f"[OK] Loaded local photo: {img.size}")
else:
    print("[..] Local photo not found, falling back to GitHub avatar …")
    try:
        req = Request(
            f"https://avatars.githubusercontent.com/{USERNAME}?size=400",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        img_bytes = urlopen(req, timeout=20).read()
        img = Image.open(BytesIO(img_bytes))
        print(f"[OK] Avatar fetched ({len(img_bytes):,} bytes)")
    except Exception as e:
        sys.exit(f"[ERR] Image load failed: {e}")

from PIL import ImageEnhance
import numpy as np

# Crop to center portrait if larger image
if img.size[0] > 300 and img.size[1] > 300:
    w, h = img.size
    crop_box = (int(w * 0.05), int(h * 0.02), int(w * 0.95), int(h * 0.96))
    img = img.crop(crop_box)

img_gray = img.convert("L")
img_enh = ImageEnhance.Contrast(img_gray).enhance(1.45)
img_enh = ImageEnhance.Brightness(img_enh).enhance(1.15)

# Background cleaning for upper shoulders and head background
arr = np.array(img_enh)
H_arr, W_arr = arr.shape
for y in range(H_arr):
    for x in range(W_arr):
        ny = y / H_arr
        nx = x / W_arr
        if ny < 0.42:
            dist_x = abs(nx - 0.5)
            if dist_x > 0.22 and arr[y, x] > 90:
                arr[y, x] = 255
            elif dist_x > 0.32:
                arr[y, x] = 255

cleaned_img = Image.fromarray(arr)

# Density ramp: space = bright pixel, @ = dark pixel
ASCII_CHARS = "  `.-':=+*csS%#@"
ART_W, ART_H = 100, 53

img_resized = cleaned_img.resize((ART_W, ART_H), Image.Resampling.LANCZOS)

rows = []
for r in range(ART_H):
    row = ""
    for c in range(ART_W):
        px = img_resized.getpixel((c, r))
        idx = int((255 - px) / 255 * (len(ASCII_CHARS) - 1))
        row += ASCII_CHARS[idx]
    rows.append(row)

print(f"[OK] ASCII art generated ({ART_W}×{ART_H})")

# Layout constants — identical to reference avi-ascii.svg
W1      = 840
ROW_H   = 15
ROW_Y0  = 37
FONT_SZ = 12.9
ROW_DUR = 0.11
TEXT_W  = 800
TEXT_X  = 20

FOOTER_LINE_Y = ROW_Y0 + ART_H * ROW_H   # 832
FOOTER_TEXT_Y = FOOTER_LINE_Y + 19        # 851
H1            = FOOTER_LINE_Y + 43        # 875

WHOAMI_TEXT = f"{USERNAME}@github:~$ whoami "
CURSOR_X    = TEXT_X + len(WHOAMI_TEXT) * 7.73

# Build rows SVG
rows_svg = ""
for i, row in enumerate(rows):
    begin  = i * ROW_DUR
    y_top  = ROW_Y0 + i * ROW_H
    y_text = y_top + 11.1
    safe   = xe(row)

    rows_svg += (
        f'<clipPath id="r{i}">'
        f'<rect x="{TEXT_X}" y="{y_top:.1f}" height="{ROW_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{TEXT_W}" '
        f'begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
        f'</rect></clipPath>\n'
        f'<g clip-path="url(#r{i})">'
        f'<text xml:space="preserve" x="{TEXT_X}" y="{y_text:.1f}" '
        f'fill="#c9d1d9" font-size="{FONT_SZ}" '
        f'textLength="{TEXT_W}" lengthAdjust="spacing">{safe}</text>'
        f'</g>\n'
        f'<rect y="{y_top+1:.1f}" width="8" height="13" fill="#c9d1d9" opacity="0">'
        f'<animate attributeName="x" from="{TEXT_X}" to="{TEXT_X+TEXT_W}" '
        f'begin="{begin:.3f}s" dur="{ROW_DUR}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{begin:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{begin+ROW_DUR:.3f}s"/>'
        f'</rect>\n'
    )

svg1 = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W1}" height="{H1}" viewBox="0 0 {W1} {H1}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<rect width="{W1}" height="{H1}" rx="12" fill="url(#bg)"/>
<rect x="0.5" y="0.5" width="{W1-1}" height="{H1-1}" rx="12" fill="none" stroke="#30363d" stroke-width="1"/>
<line x1="0" y1="30" x2="{W1}" y2="30" stroke="#30363d"/>
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<text x="{W1/2:.1f}" y="19.0" fill="#7d8590" font-size="12" text-anchor="middle">{USERNAME}@github: ~$ ./portrait.sh</text>
{rows_svg}
<line x1="0" y1="{FOOTER_LINE_Y:.1f}" x2="{W1}" y2="{FOOTER_LINE_Y:.1f}" stroke="#30363d"/>
<text x="20" y="{FOOTER_TEXT_Y:.1f}" fill="#7d8590" font-size="13">{USERNAME}@github:~$ whoami <tspan fill="#c9d1d9">{DISPLAY_NAME}</tspan></text>
<rect x="{CURSOR_X:.0f}" y="{FOOTER_TEXT_Y-13:.1f}" width="8" height="14" fill="#c9d1d9">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/>
</rect>
</svg>"""

out1 = os.path.join(OUT_DIR, "terminal-card.svg")
with open(out1, "w", encoding="utf-8") as f:
    f.write(svg1)
print(f"[OK] terminal-card.svg written  ({W1}×{H1}px, {os.path.getsize(out1)//1024} KB)")


# ═══════════════════════════════════════════════════════════════════════════════
# PART 2 — info-card.svg  (neofetch-style, matching Avi's info-card.svg)
# ═══════════════════════════════════════════════════════════════════════════════

W2, H2 = 480, 420

# Info rows: (label_color, label, value)
# Colors matching reference exactly
C_ORANGE = "#ffa657"
C_BLUE   = "#58a6ff"
C_GREEN  = "#3fb950"
C_CYAN   = "#22d3ee"
C_WHITE  = "#c9d1d9"
C_DIM    = "#30363d"
C_GRAY   = "#7d8590"

# Build rows: each is a dict describing what to render
# type: "header" | "section" | "field" | "bullet"
INFO_ROWS = [
    # identity header
    {"type": "header"},
    # About section
    {"type": "section",  "label": "— About"},
    {"type": "field",    "label": "Role",        "value": "Full Stack Developer"},
    {"type": "field",    "label": "Company",     "value": "Bissbay Solutions"},
    {"type": "field",    "label": "Education",   "value": "MCA Scholar, COER University"},
    {"type": "field",    "label": "Focus",       "value": "Scalable ERP & Web Apps"},
    # Stack section
    {"type": "section",  "label": "— Stack"},
    {"type": "field",    "label": "Backend",     "value": "PHP 8 (OOP/MVC), MySQL, Node"},
    {"type": "field",    "label": "Frontend",    "value": "React.js, Tailwind, Bootstrap"},
    {"type": "field",    "label": "Database",    "value": "MySQL, PostgreSQL, Redis, Mongo"},
    {"type": "field",    "label": "CMS & DevOps","value": "WordPress, Docker, Linux, Git"},
    # Highlights section
    {"type": "section",  "label": "— Highlights"},
    {"type": "bullet",   "value": "Full Stack Dev at Bissbay Solutions"},
    {"type": "bullet",   "value": "Engineered Karobar Bazar (Business ERP)"},
    {"type": "bullet",   "value": "MCA (2024-26) · BCA Graduate, COER Univ"},
    {"type": "bullet",   "value": "Specialized in PHP, MySQL, React & WP"},
]

# Animation timing (matches reference: each row starts 0.06s after previous)
SLIDE_DUR  = 0.4    # s — duration of each row's animation
STEP       = 0.06   # s — stagger between rows

# Y positions
TOP_Y    = 60.0    # first row (identity header) text y
LINE_H   = 20.5   # between rows

parts = []
cur_t = 0.15
cur_y = TOP_Y

for row in INFO_ROWS:
    t     = cur_t
    ks    = "0.2 0.8 0.2 1"    # easing

    if row["type"] == "header":
        # "devwithanasraza@github" bold header + horizontal rule
        ulen = len(USERNAME)
        rule_x1 = 20 + (ulen + 1 + 6) * 8.2   # rough char width
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<text x="20" y="{cur_y}" font-size="14" font-weight="700">'
            f'<tspan fill="{C_GREEN}">{xe(USERNAME)}</tspan>'
            f'<tspan fill="{C_GRAY}">@</tspan>'
            f'<tspan fill="{C_CYAN}">github</tspan>'
            f'</text>'
            f'<line x1="{rule_x1:.0f}" y1="{cur_y-4:.1f}" x2="460" y2="{cur_y-4:.1f}" stroke="{C_DIM}" stroke-opacity="0.8"/>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H * 1.1
        cur_t += STEP

    elif row["type"] == "section":
        # blue section header + horizontal rule
        label   = row["label"]
        rule_x1 = 20 + len(label) * 7.5
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<text x="20" y="{cur_y}" fill="{C_BLUE}" font-size="12.5" font-weight="700">{xe(label)}</text>'
            f'<line x1="{rule_x1:.0f}" y1="{cur_y-4:.1f}" x2="460" y2="{cur_y-4:.1f}" stroke="{C_DIM}" stroke-opacity="0.8"/>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H * 1.5
        cur_t += STEP * 2

    elif row["type"] == "field":
        # orange label + white value, label column at x=20, value at x=112
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<text x="20" y="{cur_y}" fill="{C_ORANGE}" font-size="12.5" font-weight="700">{xe(row["label"])}</text>'
            f'<text x="112" y="{cur_y}" fill="{C_WHITE}" font-size="12.5">{xe(row["value"])}</text>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H
        cur_t += STEP

    elif row["type"] == "bullet":
        # green dot + white text
        dot_cy = cur_y - 4
        parts.append(
            f'<g opacity="0" transform="translate(0,5)">'
            f'<circle cx="23" cy="{dot_cy:.1f}" r="2.5" fill="{C_GREEN}"/>'
            f'<text x="34" y="{cur_y}" fill="{C_WHITE}" font-size="12.5">{xe(row["value"])}</text>'
            f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" begin="{t:.2f}s" dur="{SLIDE_DUR}s" fill="freeze" calcMode="spline" keySplines="{ks}"/>'
            f'</g>'
        )
        cur_y += LINE_H
        cur_t += STEP

# Adjust H2 to fit content
H2 = max(420, int(cur_y) + 30)

info_parts_svg = "\n".join(parts)

svg2 = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
<defs>
  <linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#111722"/>
    <stop offset="1" stop-color="#0d1117"/>
  </linearGradient>
</defs>
<rect width="{W2}" height="{H2}" rx="12" fill="url(#ibg)"/>
<rect x="0.5" y="0.5" width="{W2-1}" height="{H2-1}" rx="12" fill="none" stroke="#30363d"/>
<line x1="0" y1="30" x2="{W2}" y2="30" stroke="#30363d"/>
<circle cx="20" cy="15.0" r="5" fill="#ff5f56"/>
<circle cx="36" cy="15.0" r="5" fill="#ffbd2e"/>
<circle cx="52" cy="15.0" r="5" fill="#27c93f"/>
<text x="{W2/2:.1f}" y="19.0" fill="{C_GRAY}" font-size="12" text-anchor="middle">{USERNAME}@github: ~$ neofetch</text>
{info_parts_svg}
</svg>"""

out2 = os.path.join(OUT_DIR, "info-card.svg")
with open(out2, "w", encoding="utf-8") as f:
    f.write(svg2)
print(f"[OK] info-card.svg written       ({W2}×{H2}px, {os.path.getsize(out2)//1024} KB)")

print()
print("Done! SVGs generated for Anas Raza.")
