#!/usr/bin/env python3
"""Draw the front page for 18 November 2026 and save it as entry.png.

Everything is drawn with Pillow primitives: a navy masthead, a dramatic
lead scene (the Kerch bridge with its road arch down, missiles over the
Gulf), a two-line lead headline, a six-cell story grid and an ALSO TODAY
strip. No network, no timestamps, no randomness: running this script twice
writes byte-identical output.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (22, 22, 22)
NAVY = (13, 29, 56)
NAVY_LIGHT = (24, 48, 88)
RED = (176, 32, 32)
RED_SOFT = (196, 64, 48)
GOLD = (214, 164, 62)
GREY = (104, 100, 92)
CARD = (255, 255, 255)
CARD_EDGE = (216, 210, 196)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_BIG = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
F_REG = lambda s: font("DejaVuSans.ttf", s)


def wrap_text(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    """Draw a list of lines top to bottom; returns the y after the last."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def blend(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def v_gradient(draw, box, top, bottom, steps=28):
    """Fill box with a vertical gradient in a few flat bands (keeps the
    PNG small while looking smooth at a glance)."""
    x0, y0, x1, y1 = box
    span = max(1, y1 - y0)
    for i in range(steps):
        t0 = i / steps
        t1 = (i + 1) / steps
        col = blend(top, bottom, (t0 + t1) / 2)
        draw.rectangle([x0, y0 + int(span * t0), x1, y0 + int(span * t1)],
                       fill=col)


def soft_disc(base, cx, cy, r, colour, alpha=110):
    """Paint a translucent disc onto base (an RGBA overlay) for glows."""
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour + (alpha,))
    base.alpha_composite(layer)


def smoke_puff(base, cx, cy, r, alpha=90):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    grey = (150, 148, 142)
    d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7],
              fill=grey + (alpha,))
    d.ellipse([cx - r * 0.6, cy - r, cx + r * 0.7, cy + r * 0.5],
              fill=(170, 168, 160, alpha))
    base.alpha_composite(layer)


# ---------------------------------------------------------------- icons
# Small drawn marks for the story grid: simple, bold, readable at 300px.

def icon_flags(d, x, y, s):
    """Three meeting flags: red, navy, white poles with pennants."""
    for i, col in enumerate((RED, NAVY_LIGHT, GOLD)):
        px = x + 8 + i * (s // 3)
        d.line([px, y + 6, px, y + s - 6], fill=INK, width=3)
        d.polygon([(px, y + 6), (px + s // 3 - 2, y + 12),
                   (px, y + 18)], fill=col)


def icon_virus(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    r = s // 4
    for k in range(10):
        ang = 2 * math.pi * k / 10
        d.line([cx + int(r * math.cos(ang)), cy + int(r * math.sin(ang)),
                cx + int((r + 9) * math.cos(ang)),
                cy + int((r + 9) * math.sin(ang))], fill=RED, width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    d.ellipse([cx - r // 2, cy - r // 2, cx, cy], fill=PAPER)


def icon_bars(d, x, y, s):
    """Rising bars: a chart climbing up."""
    base = y + s - 8
    for i, h in enumerate((s // 4, s // 2, 3 * s // 4)):
        bx = x + 8 + i * (s // 3)
        d.rectangle([bx, base - h, bx + s // 5, base], fill=NAVY_LIGHT)
    d.line([x + 6, base - 3 * s // 4 - 6, x + s - 6, y + 6],
           fill=RED, width=4)


def icon_cyclone(d, x, y, s):
    cx, cy = x + s // 2, y + s // 2
    for k, r in enumerate((s // 2 - 4, s // 3, s // 5)):
        start = k * 40
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 250,
              fill=NAVY_LIGHT, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def icon_ballot(d, x, y, s):
    d.rectangle([x + 8, y + s // 2, x + s - 8, y + s - 8],
                outline=INK, width=3)
    d.rectangle([x + s // 3, y + s // 3, x + 2 * s // 3, y + s // 2],
                fill=INK)
    d.line([x + s // 4, y + s // 2, x + s // 2 - 2, y + 3 * s // 4,
            x + 3 * s // 4, y + s // 4], fill=RED, width=5)


def icon_plane(d, x, y, s):
    """A transport plane in side view, nose down."""
    cx, cy = x + s // 2, y + s // 2
    # fuselage: long thin diamond, nose to the lower left
    d.polygon([(cx - s // 2 + 4, cy + 2), (cx - s // 6, cy - 6),
               (cx + s // 3, cy - 2), (cx + s // 2, cy + 4),
               (cx + s // 6, cy + 10), (cx - s // 4, cy + 10)],
              fill=NAVY_LIGHT)
    # main wing, swept back
    d.polygon([(cx - s // 8, cy + 2), (cx + s // 10, cy + s // 3),
               (cx + s // 4, cy + s // 3 - 6), (cx + s // 12, cy + 4)],
              fill=NAVY_LIGHT)
    # tail fin
    d.polygon([(cx + s // 4, cy - 2), (cx + s // 3, cy - s // 4),
               (cx + 5 * s // 12, cy - s // 4 + 4), (cx + s // 3, cy + 2)],
              fill=NAVY_LIGHT)


# ------------------------------------------------------------- lead art
# Dusk over the strait: a bridge with its road arch down on the left,
# missiles and a burning tanker over the Gulf on the right.

def draw_lead_art(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img, "RGBA")
    horizon = y0 + int((y1 - y0) * 0.62)
    v_gradient(d, (x0, y0, x1, horizon), (11, 28, 51), (232, 122, 74))
    v_gradient(d, (x0, horizon, x1, y1), (18, 48, 58), (10, 26, 34))

    # low sun glow behind the smoke, kept small so it never reads as a
    # second fireball on the bridge
    soft_disc(img, x0 + int((x1 - x0) * 0.60), horizon - 10, 46,
              (255, 170, 90), 110)
    soft_disc(img, x0 + int((x1 - x0) * 0.60), horizon - 10, 22,
              (255, 220, 150), 140)

    # missile streaks, upper right
    for (sx, sy, ex, ey) in ((760, 150, 830, 196), (820, 132, 890, 180),
                             (700, 178, 770, 220)):
        d.line([sx, sy, ex, ey], fill=(255, 240, 200, 230), width=4)
        d.ellipse([ex - 4, ey - 4, ex + 4, ey + 4],
                  fill=(255, 220, 140, 255))

    # smoke over the gap and over the tanker, hugging the deck line
    smoke_puff(img, x0 + 462, y0 + 84, 40, 95)
    smoke_puff(img, x0 + 500, y0 + 62, 30, 75)
    smoke_puff(img, x0 + 880, y0 + 96, 26, 85)

    # sea glints
    for gy in (horizon + 14, horizon + 30, horizon + 48):
        for gx in range(x0 + 30, x1 - 60, 90):
            d.line([gx, gy, gx + 42, gy], fill=(214, 164, 62, 120),
                   width=2)

    deck_y = horizon - 42
    # bridge deck: two standing spans, a gap where the arch fell
    d.rectangle([x0, deck_y, x0 + 400, deck_y + 12], fill=(16, 22, 30))
    d.rectangle([x0 + 560, deck_y, x1, deck_y + 12], fill=(16, 22, 30))
    # pillars
    for px in (x0 + 60, x0 + 220, x0 + 350, x0 + 640, x0 + 800, x0 + 940):
        d.rectangle([px, deck_y + 12, px + 14, horizon + 26],
                    fill=(16, 22, 30))
    # standing arch ribs on the two spans
    d.arc([x0 + 60, deck_y - 58, x0 + 340, deck_y + 10], 180, 360,
          fill=(16, 22, 30), width=10)
    d.arc([x0 + 620, deck_y - 58, x0 + 900, deck_y + 10], 180, 360,
          fill=(16, 22, 30), width=10)
    # the fallen arch: a tilted slab half in the water, mid-gap
    d.polygon([(x0 + 428, deck_y + 6), (x0 + 520, deck_y + 30),
               (x0 + 500, deck_y + 62), (x0 + 412, deck_y + 40)],
              fill=(28, 36, 46))
    d.polygon([(x0 + 470, deck_y + 58), (x0 + 540, deck_y + 78),
               (x0 + 528, deck_y + 96), (x0 + 462, deck_y + 78)],
              fill=(20, 28, 38))
    # splash ring where it hit
    d.ellipse([x0 + 440, horizon + 18, x0 + 540, horizon + 34],
              outline=(220, 225, 225, 180), width=3)

    # tanker on the right, burning
    tx, ty = x0 + 830, horizon + 34
    d.polygon([(tx, ty), (tx + 130, ty), (tx + 118, ty + 18),
               (tx + 12, ty + 18)], fill=(10, 14, 20))
    d.rectangle([tx + 30, ty - 16, tx + 58, ty], fill=(10, 14, 20))
    soft_disc(img, tx + 44, ty - 20, 18, (255, 140, 40), 170)
    soft_disc(img, tx + 44, ty - 20, 8, (255, 220, 120), 200)

    # dark frame around the picture
    d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(10, 10, 10), width=3)


# -------------------------------------------------------------- stories

LEAD_HEAD = ["MISSILES OVER THE GULF,", "THE BRIDGE FALLS"]
LEAD_TEXT = (
    "US jets struck an Iranian missile site on Qeshm Island. Iran answered "
    "with drones at Bahrain \u2014 its third attack there this week \u2014 and "
    "at the American base in Kuwait, while a Houthi missile aimed at Riyadh "
    "was shot down and a gas tanker burned in the Strait of Hormuz. In the "
    "Black Sea, Ukraine dropped the Kerch bridge\u2019s 227-metre road arch "
    "into the strait; the road is closed and two people were killed."
)

# (kicker, headline, summary, icon function)
GRID = [
    ("SUMMIT", "Trump, Xi and Putin to meet in Shenzhen",
     "The three leaders hold their first trilateral talks on Thursday, "
     "on the APEC sidelines.", icon_flags),
    ("HEALTH", "Ebola outbreak passes 11,000 cases",
     "More than 5,400 dead in Congo; nearly three in four infected "
     "children under five do not survive.", icon_virus),
    ("HEALTH", "US loses its measles-free status",
     "Elimination status held for 26 years ends; 5,400 cases and "
     "10 deaths reported this year.", icon_bars),
    ("WEATHER", "Category 5 cyclone hits Cook Islands",
     "Cyclone Xavier lashes the Northern Cook Islands with gusts "
     "up to 315 km/h.", icon_cyclone),
    ("POLITICS", "Peltola flips Alaska\u2019s Senate seat",
     "Democrat Mary Peltola beats Dan Sullivan; Democrats reach "
     "56 seats in the Senate.", icon_ballot),
    ("DISASTER", "Russian military plane crashes",
     "An An-12 transport comes down in Siberia\u2019s Kemerovo region; "
     "all 19 aboard are killed.", icon_plane),
]

ALSO = (
    "Romania: a 5.3 quake is felt in Bucharest and across south-eastern "
    "Europe, with no casualties reported  \u2022  Cold kills displaced "
    "people in tents in Gaza as four nations demand aid access  \u2022  "
    "Israel\u2019s president asks Gadi Eisenkot to form the next government  "
    "\u2022  Cyclone Akvan bears down on India\u2019s Andhra coast, landfall "
    "expected on 20 November"
)


# -------------------------------------------------------------- layout

def draw_masthead(d):
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((20, 20), "THE WORLD TODAY", font=F_SERIF_BIG(52), fill=(255, 255, 255))
    d.text((1004, 16), "WEDNESDAY", font=F_BOLD(26),
           fill=(255, 255, 255), anchor="ra")
    d.text((1004, 50), "18 NOVEMBER 2026", font=F_BOLD(26),
           fill=GOLD, anchor="ra")
    d.rectangle([0, 96, W, 102], fill=RED)


def draw_lead(d, y):
    f_head = F_BOLD(48)
    y = draw_lines(d, LEAD_HEAD, f_head, 20, y, INK, 54)
    y += 4
    f_body = F_REG(19)
    lines = wrap_text(LEAD_TEXT, f_body, W - 40)
    y = draw_lines(d, lines, f_body, 20, y, (40, 40, 40), 25)
    return y


def draw_grid(d, y):
    d.text((20, y), "MORE OF THE DAY", font=F_BOLD(16), fill=RED)
    d.line([210, y + 11, W - 20, y + 11], fill=CARD_EDGE, width=2)
    y += 24
    cell_w, cell_h, gap = 488, 112, 6
    for row in range(3):
        for col in range(2):
            kicker, head, summ, icon = GRID[row * 2 + col]
            x = 20 + col * (cell_w + 8)
            cy = y + row * (cell_h + gap)
            d.rectangle([x, cy, x + cell_w, cy + cell_h], fill=CARD,
                        outline=CARD_EDGE, width=1)
            d.rectangle([x, cy, x + 5, cy + cell_h], fill=RED)
            icon(d, x + 16, cy + 24, 64)
            tx = x + 92
            d.text((tx, cy + 10), kicker, font=F_BOLD(13), fill=RED)
            f_h = F_BOLD(21)
            hl = wrap_text(head, f_h, cell_w - 108)[:2]
            hy = draw_lines(d, hl, f_h, tx, cy + 30, INK, 25)
            f_s = F_REG(15)
            sl = wrap_text(summ, f_s, cell_w - 108)[:2]
            draw_lines(d, sl, f_s, tx, hy + 2, (60, 60, 60), 19)
    return y + 3 * cell_h + 2 * gap


def draw_also_today(d, y):
    band_h = 82
    d.rectangle([0, y, W, y + band_h], fill=NAVY)
    d.text((20, y + 6), "ALSO TODAY", font=F_BOLD(16), fill=GOLD)
    f = F_REG(15)
    lines = wrap_text(ALSO, f, W - 40)[:3]
    draw_lines(d, lines, f, 20, y + 26, (235, 235, 235), 19)
    return y + band_h


def build():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    draw_masthead(d)
    draw_lead_art(img, 20, 112, W - 20, 330)
    y = draw_lead(d, 344)
    y = draw_grid(d, y + 10)
    draw_also_today(d, y + 6)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().convert("RGB").save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
