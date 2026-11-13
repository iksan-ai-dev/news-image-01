#!/usr/bin/env python3
"""Draw the news-image-01 entry: a 1024x1024 PNG newspaper front page.

Deterministic: running this script twice produces identical bytes.
All pictograms are drawn with Pillow primitives only (no external images).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (15, 42, 74)       # #0F2A4A
GOLD = (232, 184, 75)     # #E8B84B
RED = (200, 40, 40)
DARKGREY = (51, 51, 51)   # #333
WHITE = (255, 255, 255)

W, H = 1024, 1024


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap_text(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, s, fpath, start_size, min_size, max_w, max_lines):
    """Shrink font until the text wraps to <= max_lines lines."""
    size = start_size
    while size > min_size:
        f = font(fpath, size)
        lines = wrap_text(draw, s, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = font(fpath, min_size)
    return f, wrap_text(draw, s, f, max_w)


def fit_single(draw, s, fpath, start_size, min_size, max_w):
    """Shrink font until the text fits on one line."""
    size = start_size
    while size > min_size:
        f = font(fpath, size)
        if text_w(draw, s, f) <= max_w:
            return f
        size -= 1
    return font(fpath, min_size)


def center_text(draw, cx, y, s, f, fill):
    w = text_w(draw, s, f)
    draw.text((cx - w / 2, y), s, font=f, fill=fill)


# ---------------------------------------------------------------- pictograms
def pic_dove(draw, x0, y0, x1, y1):
    # sky: a few soft clouds
    draw.ellipse([x0 + 20, y0 + 18, x0 + 90, y0 + 48], fill=(255, 255, 255))
    draw.ellipse([x0 + 60, y0 + 10, x0 + 120, y0 + 38], fill=(255, 255, 255))
    draw.ellipse([x1 - 120, y0 + 14, x1 - 50, y0 + 42], fill=(255, 255, 255))
    cx, cy = (x0 + x1) // 2, y0 + 78
    # tail (left, fanned)
    draw.polygon([(cx - 78, cy - 6), (cx - 128, cy - 26), (cx - 124, cy - 8),
                  (cx - 130, cy + 4), (cx - 76, cy + 8)], fill=WHITE)
    # body
    draw.ellipse([cx - 80, cy - 26, cx + 40, cy + 16], fill=WHITE)
    # head
    draw.ellipse([cx + 22, cy - 44, cx + 62, cy - 6], fill=WHITE)
    # beak
    draw.polygon([(cx + 58, cy - 30), (cx + 82, cy - 24), (cx + 58, cy - 20)],
                 fill=(230, 150, 40))
    # eye
    draw.ellipse([cx + 44, cy - 34, cx + 52, cy - 26], fill=(20, 20, 20))
    # raised wing
    draw.polygon([(cx - 55, cy - 18), (cx - 30, cy - 78), (cx + 6, cy - 66),
                  (cx - 12, cy - 30), (cx - 30, cy - 14)], fill=(235, 240, 245))
    draw.line([(cx - 55, cy - 18), (cx - 30, cy - 78)], fill=(200, 210, 220), width=2)
    # olive branch in beak: stem + leaves
    draw.line([(cx + 78, cy - 24), (cx + 108, cy - 8)], fill=(90, 140, 70), width=3)
    for lx, ly in [(88, -16), (96, -22), (102, -12)]:
        draw.ellipse([cx + lx, cy + ly, cx + lx + 14, cy + ly + 7], fill=(90, 160, 70))
    # round table below
    ty = y1 - 34
    draw.ellipse([cx - 70, ty - 12, cx + 70, ty + 8], fill=(150, 100, 55))
    draw.rectangle([cx - 6, ty + 4, cx + 6, y1 - 8], fill=(120, 78, 40))
    draw.rectangle([cx - 46, y1 - 10, cx + 46, y1 - 6], fill=(120, 78, 40))
    # three small flags on the table
    flag_specs = [
        (cx - 62, "ua"), (cx - 14, "us"), (cx + 34, "eu"),
    ]
    for fx, kind in flag_specs:
        draw.line([(fx + 14, ty - 52), (fx + 14, ty - 12)], fill=(60, 60, 60), width=2)
        if kind == "ua":
            draw.rectangle([fx + 14, ty - 52, fx + 42, ty - 38], fill=(0, 90, 180))
            draw.rectangle([fx + 14, ty - 38, fx + 42, ty - 24], fill=(255, 215, 0))
        elif kind == "us":
            for i in range(5):
                col = (180, 30, 30) if i % 2 == 0 else WHITE
                draw.rectangle([fx + 14, ty - 52 + i * 6, fx + 42, ty - 46 + i * 6],
                               fill=col)
            draw.rectangle([fx + 14, ty - 52, fx + 28, ty - 40], fill=(30, 50, 130))
        else:  # eu
            draw.rectangle([fx + 14, ty - 52, fx + 42, ty - 24], fill=(20, 60, 160))
            import math
            for k in range(8):
                a = math.pi * 2 * k / 8
                sx = fx + 28 + int(8 * math.cos(a))
                sy = ty - 38 + int(8 * math.sin(a))
                draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 215, 0))


def pic_chip(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2 - 60, y0 + 88
    # red downward arrow above the chip
    ax = cx
    draw.polygon([(ax - 16, y0 + 8), (ax + 16, y0 + 8), (ax + 16, y0 + 34),
                  (ax + 30, y0 + 34), (ax, y0 + 62), (ax - 30, y0 + 34),
                  (ax - 16, y0 + 34)], fill=RED)
    # chip pins
    for i in range(5):
        px = cx - 52 + i * 26
        draw.rectangle([px - 5, cy - 62, px + 5, cy - 44], fill=(120, 130, 140))
        draw.rectangle([px - 5, cy + 44, px + 5, cy + 62], fill=(120, 130, 140))
        py = cy - 52 + i * 26
        draw.rectangle([cx - 62, py - 5, cx - 44, py + 5], fill=(120, 130, 140))
        draw.rectangle([cx + 44, py - 5, cx + 62, py + 5], fill=(120, 130, 140))
    # chip body
    draw.rounded_rectangle([cx - 46, cy - 46, cx + 46, cy + 46], radius=10,
                           fill=(20, 130, 70))
    draw.rounded_rectangle([cx - 28, cy - 28, cx + 28, cy + 28], radius=6,
                           fill=(15, 105, 55))
    draw.text((cx - 13, cy - 11), "GPU", font=font(BOLD, 20), fill=WHITE)
    # witness chair + desk line (right side)
    dx = x1 - 150
    draw.line([(x0 + 20, y1 - 22), (x1 - 20, y1 - 22)], fill=(120, 78, 40), width=5)
    # chair back + seat + legs
    draw.rectangle([dx, y0 + 62, dx + 10, y1 - 22], fill=(150, 100, 55))
    draw.rectangle([dx, y0 + 62, dx + 78, y0 + 74], fill=(150, 100, 55))
    draw.rectangle([dx, y1 - 52, dx + 78, y1 - 40], fill=(150, 100, 55))
    draw.rectangle([dx + 6, y1 - 40, dx + 14, y1 - 22], fill=(120, 78, 40))
    draw.rectangle([dx + 64, y1 - 40, dx + 72, y1 - 22], fill=(120, 78, 40))


def pic_ship(draw, x0, y0, x1, y1):
    # sea
    draw.rectangle([x0, y1 - 52, x1, y1], fill=(70, 95, 120))
    draw.line([(x0, y1 - 52), (x1, y1 - 52)], fill=(50, 70, 95), width=2)
    for wx in range(x0 + 30, x1 - 20, 70):
        draw.arc([wx, y1 - 40, wx + 34, y1 - 24], 180, 360, fill=(200, 215, 225),
                 width=2)
    cx, cy = (x0 + x1) // 2, y1 - 52
    # smoke plume above funnel (kept inside the scene)
    for i, (sx, sy, r) in enumerate([(-30, -58, 9), (-22, -70, 11),
                                     (-12, -80, 13), (0, -88, 14)]):
        draw.ellipse([cx + sx - r, cy + sy - r, cx + sx + r, cy + sy + r],
                     fill=(150, 155, 160))
    # hull
    draw.polygon([(cx - 150, cy - 6), (cx + 150, cy - 6), (cx + 122, cy + 34),
                  (cx - 128, cy + 34)], fill=(90, 100, 110))
    draw.rectangle([cx - 150, cy - 6, cx + 150, cy + 2], fill=(60, 68, 78))
    # superstructure + funnel + mast
    draw.rectangle([cx - 70, cy - 44, cx + 30, cy - 6], fill=(120, 130, 140))
    draw.rectangle([cx + 48, cy - 40, cx + 72, cy - 6], fill=(100, 110, 120))
    draw.rectangle([cx - 95, cy - 30, cx - 72, cy - 6], fill=(120, 130, 140))
    draw.line([(cx - 10, cy - 44), (cx - 10, cy - 96)], fill=(60, 68, 78), width=5)
    draw.line([(cx - 26, cy - 84), (cx + 6, cy - 84)], fill=(60, 68, 78), width=4)
    # small flag on mast
    draw.polygon([(cx - 10, cy - 96), (cx + 16, cy - 90), (cx - 10, cy - 84)],
                 fill=RED)
    # quadcopter drone above
    dx, dy = x1 - 90, y0 + 34
    draw.line([(dx - 34, dy - 8), (dx + 34, dy - 8)], fill=(40, 40, 40), width=3)
    draw.line([(dx - 34, dy + 8), (dx + 34, dy + 8)], fill=(40, 40, 40), width=3)
    for rx, ry in [(-34, -8), (34, -8), (-34, 8), (34, 8)]:
        draw.ellipse([dx + rx - 12, dy + ry - 3, dx + rx + 12, dy + ry + 3],
                     fill=(90, 90, 90))
    draw.ellipse([dx - 14, dy - 10, dx + 14, dy + 10], fill=(50, 50, 50))
    draw.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=RED)


def pic_radar(draw, x0, y0, x1, y1):
    # sky sun
    draw.ellipse([x1 - 84, y0 + 14, x1 - 44, y0 + 54], fill=(255, 200, 80))
    # desert ground
    draw.rectangle([x0, y1 - 44, x1, y1], fill=(215, 185, 130))
    draw.line([(x0, y1 - 44), (x1, y1 - 44)], fill=(190, 158, 100), width=2)
    # sea strip on the right (coast)
    draw.rectangle([x1 - 150, y1 - 44, x1, y1], fill=(90, 140, 175))
    cx, cy = (x0 + x1) // 2 - 40, y1 - 44
    # radar base + mast
    draw.rectangle([cx - 70, cy - 18, cx + 70, cy], fill=(200, 200, 200))
    draw.rectangle([cx - 34, cy - 34, cx + 34, cy - 18], fill=(220, 220, 220))
    # white dome (hemisphere)
    draw.pieslice([cx - 62, cy - 108, cx + 62, cy + 16], 180, 360, fill=WHITE)
    draw.rectangle([cx - 62, cy - 46, cx + 62, cy - 34], fill=(235, 235, 235))
    # small antenna on dome (kept inside the scene)
    draw.line([(cx, cy - 108), (cx, cy - 116)], fill=(120, 120, 120), width=3)
    draw.ellipse([cx - 4, cy - 120, cx + 4, cy - 112], fill=RED)
    # missile streak across the sky
    draw.line([(x0 + 30, y0 + 30), (x1 - 120, y0 + 78)], fill=(255, 120, 30),
              width=6)
    draw.polygon([(x1 - 120, y0 + 78), (x1 - 96, y0 + 66), (x1 - 100, y0 + 88)],
                 fill=(255, 80, 20))
    # starburst at streak start
    import math
    sx, sy = x0 + 30, y0 + 30
    pts = []
    for k in range(16):
        r = 16 if k % 2 == 0 else 7
        a = math.pi * 2 * k / 16
        pts.append((sx + r * math.cos(a), sy + r * math.sin(a)))
    draw.polygon(pts, fill=(255, 210, 60))


def pic_outage(draw, x0, y0, x1, y1):
    cx, cy = (x0 + x1) // 2, y0 + 78
    # four-pane window
    pane = 44
    gap = 8
    cols = [(43, 140, 210), (0, 110, 190), (80, 170, 225), (20, 125, 200)]
    positions = [(cx - pane - gap // 2, cy - pane - gap // 2),
                 (cx + gap // 2, cy - pane - gap // 2),
                 (cx - pane - gap // 2, cy + gap // 2),
                 (cx + gap // 2, cy + gap // 2)]
    for (px, py), col in zip(positions, cols):
        draw.rectangle([px, py, px + pane, py + pane], fill=col)
    # big red X over the window
    m = 14
    x0b, y0b = cx - pane - gap // 2 - m, cy - pane - gap // 2 - m
    x1b, y1b = cx + pane + gap // 2 + m, cy + pane + gap // 2 + m
    draw.line([(x0b, y0b), (x1b, y1b)], fill=RED, width=12)
    draw.line([(x1b, y0b), (x0b, y1b)], fill=RED, width=12)
    # unplugged cable bottom-right (kept inside the scene)
    draw.arc([x1 - 170, y1 - 62, x1 - 70, y1 - 2], 270, 90, fill=(40, 40, 40),
             width=5)
    draw.rectangle([x1 - 76, y1 - 44, x1 - 52, y1 - 24], fill=(40, 40, 40))
    draw.rectangle([x1 - 52, y1 - 40, x1 - 40, y1 - 34], fill=(180, 180, 180))
    draw.rectangle([x1 - 52, y1 - 30, x1 - 40, y1 - 24], fill=(180, 180, 180))
    # small "no signal" dots bottom-left
    for i, r in enumerate([5, 7, 9]):
        draw.ellipse([x0 + 34 + i * 22 - r, y1 - 40 - r, x0 + 34 + i * 22 + r,
                      y1 - 40 + r], fill=(150, 160, 170))


def pic_hospital(draw, x0, y0, x1, y1):
    cx = (x0 + x1) // 2
    by = y1 - 12
    # main building
    draw.rectangle([cx - 130, y0 + 46, cx + 130, by], fill=(245, 245, 245))
    draw.rectangle([cx - 130, y0 + 46, cx + 130, y0 + 58], fill=(200, 208, 216))
    # roof sign with red cross
    draw.rectangle([cx - 34, y0 + 8, cx + 34, y0 + 46], fill=WHITE)
    draw.rectangle([cx - 34, y0 + 8, cx + 34, y0 + 46], outline=(150, 158, 166),
                   width=2)
    draw.rectangle([cx - 6, y0 + 16, cx + 6, y0 + 38], fill=RED)
    draw.rectangle([cx - 17, y0 + 25, cx + 17, y0 + 31], fill=RED)
    # window rows
    for row in range(3):
        wy = y0 + 72 + row * 30
        for col in range(6):
            wx = cx - 112 + col * 40
            draw.rectangle([wx, wy, wx + 26, wy + 18], fill=(140, 165, 190))
    # entrance
    draw.rectangle([cx - 26, by - 34, cx + 26, by], fill=(120, 135, 150))
    draw.rectangle([cx - 18, by - 26, cx + 18, by], fill=(90, 105, 120))
    # ground line
    draw.line([(x0 + 16, by), (x1 - 16, by)], fill=(120, 128, 136), width=2)


PANELS = [
    ("UKRAINE TALKS: EUROPE JOINS",
     "Europe joins next round; record swap agreed",
     (220, 235, 247), pic_dove),
    ("SENATE SUMMONS EX-NVIDIA CEO",
     "Huang & Lutnick to testify on chips",
     (221, 232, 220), pic_chip),
    ("DRONE HITS RUSSIAN WARSHIP",
     "Corvette Naro-Fominsk hit in Gulf of Finland",
     (211, 220, 227), pic_ship),
    ("IRAN SAYS: US RADAR HIT",
     "US: drones shot down; no damage",
     (240, 228, 200), pic_radar),
    ("MICROSOFT 365 DOWN WORLDWIDE",
     "Outlook & Teams out; not a cyberattack",
     (220, 233, 247), pic_outage),
    ("HOSPITAL STRIKE KILLS SIX",
     "Surgeon among dead at Nasser Hospital",
     (217, 222, 230), pic_hospital),
]


def main():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # ---- masthead band ----
    draw.rectangle([0, 0, W, 112], fill=NAVY)
    center_text(draw, W // 2, 14, "THE WORLD TODAY", font(BOLD, 54), WHITE)
    center_text(draw, W // 2, 74, "FRIDAY 13 NOVEMBER 2026", font(BOLD, 28), GOLD)
    draw.rectangle([0, 112, W, 117], fill=RED)

    # ---- grid: 2 cols x 3 rows ----
    margin, gutter = 16, 12
    top = 124
    col_w = (W - 2 * margin - gutter) // 2          # 490
    row_h = (H - margin - top - 2 * gutter) // 3    # 286
    inner = col_w - 2 * 14                          # text width 462

    for i, (headline, sub, tint, pic) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (col_w + gutter)
        y = top + row * (row_h + gutter)
        # panel frame
        draw.rectangle([x, y, x + col_w, y + row_h], fill=WHITE,
                       outline=NAVY, width=2)
        # pictogram scene
        sx0, sy0, sx1, sy1 = x + 2, y + 2, x + col_w - 2, y + 2 + 165
        draw.rectangle([sx0, sy0, sx1, sy1], fill=tint)
        pic(draw, sx0, sy0, sx1, sy1)
        # headline (max 2 lines, shrink from 30px, floor 24px)
        hf, hlines = fit_lines(draw, headline, BOLD, 30, 24, inner, 2)
        hy = y + 2 + 165 + 10
        for line in hlines:
            draw.text((x + 14, hy), line, font=hf, fill=NAVY)
            hy += int(hf.size * 1.22)
        # sub-line (one line, shrink from 21px, floor 18px)
        sf = fit_single(draw, sub, REG, 21, 18, inner)
        draw.text((x + 14, hy + 4), sub, font=sf, fill=DARKGREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
