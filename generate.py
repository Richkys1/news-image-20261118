#!/usr/bin/env python3
"""Draw the front page for Wednesday 18 November 2026.

One 1024x1024 PNG summing up the day's world news as a dense,
dramatic newspaper front page: a masthead, a drawn two-scene lead
illustration (missiles over the Gulf, the Kerch bridge falling),
a two-line lead headline, six more stories in a 2x3 grid and an
ALSO TODAY strip. Everything is drawn with Pillow; no photo, no
network and no randomness, so two runs write byte-identical files.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 239, 220)
INK = (20, 20, 20)
RED = (163, 22, 22)
NAVY = (15, 42, 68)
GOLD = (201, 162, 39)
CREAM = (248, 244, 231)
NIGHT = (11, 53, 66)
SEA = (16, 66, 92)
PALE_SKY = (214, 210, 198)
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def _font(name, size):
    return ImageFont.truetype("%s/%s" % (FONT_DIR, name), size)


def serif_b(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans_b(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centre_block(draw, lines, fnt, cx, y, fill, leading):
    """Draw lines centred on cx, starting at y; returns the next y."""
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += leading
    return y


def burst(draw, cx, cy, r_out, r_in, points, fill):
    """A starburst polygon (explosion flash) centred on cx, cy."""
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def star(draw, cx, cy, r, fill):
    """A small four-point star (a distant light or spark)."""
    pts = [(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
           (cx + r * 0.28, cy + r * 0.28), (cx, cy + r),
           (cx - r * 0.28, cy + r * 0.28), (cx - r, cy),
           (cx - r * 0.28, cy - r * 0.28)]
    draw.polygon(pts, fill=fill)


def draw_masthead(draw):
    """Black nameplate band plus the red date strip."""
    draw.rectangle((26, 22, 998, 90), fill=INK)
    line = "ONE DAY  ·  ONE IMAGE  ·  THE WORLD'S NEWS"
    f_small = sans(15)
    w = draw.textlength(line, font=f_small)
    draw.text(((1024 - w) / 2, 29), line, font=f_small, fill=GOLD)
    name = "THE WORLD IN ONE PAGE"
    f_name = serif_b(44)
    w = draw.textlength(name, font=f_name)
    draw.text(((1024 - w) / 2, 48), name, font=f_name, fill=CREAM)
    draw.rectangle((26, 94, 998, 120), fill=RED)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    f_date = sans_b(23)
    w = draw.textlength(date, font=f_date)
    draw.text(((1024 - w) / 2, 98), date, font=f_date, fill=(255, 255, 255))


def draw_gulf(draw):
    """Left lead panel: night over the Strait of Hormuz."""
    x0, x1, y0, y1 = 26, 596, 130, 428
    for i, shade in enumerate([(11, 53, 66), (9, 44, 56), (8, 36, 48)]):
        draw.rectangle((x0, y0 + i * 67, x1, y0 + (i + 1) * 67), fill=shade)
    for (sx, sy, sr) in [(70, 155, 2), (150, 180, 3), (240, 148, 2),
                         (330, 170, 2), (470, 145, 3), (540, 200, 2),
                         (110, 230, 2), (400, 205, 2), (280, 215, 2)]:
        star(draw, sx, sy, sr, (220, 220, 200))
    draw.ellipse((528, 146, 566, 184), fill=(232, 226, 200))
    draw.ellipse((540, 156, 550, 166), fill=(205, 198, 170))
    draw.arc((80, 150, 330, 330), 200, 340, fill=(255, 255, 255), width=3)
    draw.arc((300, 120, 520, 300), 210, 330, fill=(255, 150, 60), width=3)
    draw.ellipse((318, 152, 330, 164), fill=(255, 240, 180))
    draw.ellipse((505, 122, 517, 134), fill=(255, 180, 90))
    burst(draw, 180, 292, 30, 13, 10, (255, 130, 40))
    burst(draw, 180, 292, 16, 7, 10, (255, 205, 60))
    burst(draw, 440, 252, 38, 16, 10, (255, 130, 40))
    burst(draw, 440, 252, 20, 9, 10, (255, 210, 70))
    draw.rectangle((x0, 330, x1, 398), fill=SEA)
    for wy in (344, 362, 380):
        draw.arc((x0 + 20, wy, x1 - 20, wy + 34), 200, 340,
                 fill=(40, 110, 140), width=2)
    draw.rectangle((310, 368, 520, 392), fill=INK)
    draw.rectangle((470, 350, 505, 368), fill=INK)
    draw.rectangle((330, 352, 348, 368), fill=INK)
    burst(draw, 410, 360, 24, 11, 9, (255, 130, 40))
    burst(draw, 410, 360, 12, 5, 9, (255, 210, 70))
    draw.rectangle((x0, 398, x1, y1), fill=INK)
    cap = "MISSILES AND DRONES OVER THE GULF"
    f_cap = sans_b(14)
    w = draw.textlength(cap, font=f_cap)
    draw.text(((x0 + x1 - w) / 2, 406), cap, font=f_cap, fill=(255, 255, 255))


def draw_kerch(draw):
    """Right lead panel: the Kerch bridge with its road arch down."""
    x0, x1, y0, y1 = 604, 998, 130, 428
    draw.rectangle((x0, y0, x1, 320), fill=PALE_SKY)
    draw.ellipse((950, 148, 982, 180), fill=(240, 225, 190))
    for (ex, ey, er) in [(700, 150, 26), (736, 168, 20), (820, 158, 30),
                         (856, 176, 22), (884, 146, 18)]:
        draw.ellipse((ex - er, ey - er // 2, ex + er, ey + er // 2),
                     fill=(150, 148, 142))
    draw.rectangle((x0, 300, 830, 312), fill=(60, 60, 60))
    draw.rectangle((960, 300, x1, 312), fill=(60, 60, 60))
    draw.arc((640, 210, 790, 312), 180, 360, fill=(60, 60, 60), width=6)
    for (ax, ay) in [(660, 300), (700, 300), (740, 300)]:
        draw.line((ax, 300, ax, 312), fill=(60, 60, 60), width=3)
    # The fallen span is drawn after the water, so it stays visible.
    draw.rectangle((x0, 312, x1, 398), fill=(90, 120, 140))
    for wy in (330, 352, 374):
        draw.arc((x0 + 16, wy, x1 - 16, wy + 30), 200, 340,
                 fill=(140, 165, 185), width=2)
    for (dx, dy, dw, dh) in [(868, 356, 22, 8), (905, 378, 30, 9),
                             (940, 360, 18, 7), (890, 392, 24, 6)]:
        draw.rectangle((dx, dy, dx + dw, dy + dh), fill=(60, 60, 60))
    draw.line((838, 296, 874, 342), fill=(60, 60, 60), width=10)
    draw.line((874, 342, 928, 394), fill=(60, 60, 60), width=10)
    draw.polygon([(856, 356), (918, 378), (938, 398), (876, 384)],
                 fill=(60, 60, 60))
    burst(draw, 928, 392, 20, 9, 8, (220, 235, 245))
    draw.arc((900, 384, 960, 404), 180, 360, fill=(220, 235, 245), width=3)
    draw.rectangle((x0, 398, x1, y1), fill=INK)
    cap = "KERCH STRAIT — THE ROAD ARCH IS DOWN"
    f_cap = sans_b(14)
    w = draw.textlength(cap, font=f_cap)
    draw.text(((x0 + x1 - w) / 2, 406), cap, font=f_cap, fill=(255, 255, 255))


def draw_lead_visual(draw):
    """Both lead panels with their ink frames."""
    draw_gulf(draw)
    draw_kerch(draw)
    draw.rectangle((26, 130, 596, 428), outline=INK, width=3)
    draw.rectangle((604, 130, 998, 428), outline=INK, width=3)


def draw_lead_headline(draw):
    """The two-line lead headline and its three-line deck."""
    lines = ["MISSILES OVER THE GULF,", "THE BRIDGE FALLS"]
    centre_block(draw, lines, serif_b(56), 512, 422, INK, 58)
    deck = ("US jets hit an Iranian missile site on Qeshm Island; Iran "
            "answers with drones over Bahrain and Kuwait, and a Houthi "
            "missile is shot down over Riyadh. On day two of the strikes, "
            "Ukraine drops the Kerch bridge's 227-metre road arch into "
            "the strait.")
    wrapped = wrap(draw, deck, serif(20), 920)
    centre_block(draw, wrapped, serif(20), 512, 540, (40, 40, 40), 24)
    draw.line((26, 616, 998, 616), fill=INK, width=2)
    draw.line((26, 621, 998, 621), fill=INK, width=1)


def draw_icon(draw, kind, x, y):
    """A tiny drawn glyph in a 44x44 box at (x, y)."""
    draw.rectangle((x, y, x + 44, y + 44), outline=INK, width=2,
                   fill=(238, 228, 205))
    cx, cy = x + 22, y + 22
    if kind == "summit":
        for bx, bh, col in ((x + 8, 26, NAVY), (x + 19, 32, RED),
                            (x + 30, 24, GOLD)):
            draw.rectangle((bx, y + 38 - bh, bx + 8, y + 38), fill=col)
    elif kind == "ebola":
        draw.rectangle((cx - 4, y + 10, cx + 4, y + 34), fill=RED)
        draw.rectangle((x + 10, cy - 4, x + 34, cy + 4), fill=RED)
    elif kind == "measles":
        for (dx, dy, dr) in ((-10, -8, 5), (8, -10, 4), (0, 0, 6),
                             (-8, 10, 4), (10, 8, 5)):
            draw.ellipse((cx + dx - dr, cy + dy - dr, cx + dx + dr,
                          cy + dy + dr), fill=RED)
    elif kind == "cyclone":
        for r in (6, 11, 16):
            draw.arc((cx - r, cy - r, cx + r, cy + r), 40, 300,
                     fill=NAVY, width=3)
    elif kind == "senate":
        star(draw, cx, cy, 16, GOLD)
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=RED)
    elif kind == "crash":
        draw.polygon([(cx, cy + 14), (cx - 14, cy - 8), (cx + 14, cy - 8)],
                     fill=(60, 60, 60))
        for (dx, dy) in ((-8, -14), (2, -17), (10, -13)):
            draw.ellipse((cx + dx - 2, cy + dy - 2, cx + dx + 2,
                          cy + dy + 2), fill=(150, 148, 142))


STORIES = [
    ("SUMMIT", "Trump, Xi and Putin to meet in Shenzhen",
     "First-ever trilateral talks on Thursday, on the APEC sidelines; "
     "Xi hosted Putin as the summit opened.", "summit"),
    ("EBOLA", "Ebola passes 11,000 cases in Congo",
     "More than 5,400 dead; nearly three in four infected children "
     "under five do not survive.", "ebola"),
    ("MEASLES", "US loses its measles-free status",
     "Elimination status held for 26 years ends; 5,400 cases and "
     "10 deaths reported this year.", "measles"),
    ("CYCLONE", "Category 5 Xavier lashes Cook Islands",
     "Gusts to 315 km/h in the Northern Cook Islands as the storm "
     "makes landfall.", "cyclone"),
    ("SENATE", "Peltola flips Alaska's Senate seat",
     "Democrat beats Dan Sullivan; Democrats reach 56 seats in "
     "the Senate.", "senate"),
    ("CRASH", "Russian military plane crashes, 19 dead",
     "An An-12 transport comes down in Siberia's Kemerovo region; "
     "all aboard are killed.", "crash"),
]


def draw_card(draw, x, y, w, h, kicker, headline, deck, icon):
    """One story cell: kicker, headline, deck, small icon at right."""
    draw.line((x, y, x + w, y), fill=INK, width=2)
    draw.text((x, y + 5), kicker, font=sans_b(13), fill=RED)
    head_lines = wrap(draw, headline, sans_b(20), w - 58)
    hy = y + 23
    for line in head_lines:
        draw.text((x, hy), line, font=sans_b(20), fill=INK)
        hy += 22
    deck_lines = wrap(draw, deck, sans(14), w - 58)[:2]
    dy = hy + 3
    for line in deck_lines:
        draw.text((x, dy), line, font=sans(14), fill=(50, 50, 50))
        dy += 17
    draw_icon(draw, icon, x + w - 46, y + 26)


def draw_grid(draw):
    """The 2x3 grid of stories below the lead."""
    card_w, card_h, gap_x, gap_y = 478, 100, 16, 8
    for i, (kicker, headline, deck, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = 26 + col * (card_w + gap_x)
        y = 630 + row * (card_h + gap_y)
        draw_card(draw, x, y, card_w, card_h, kicker, headline, deck, icon)


def draw_also_today(draw):
    """Navy strip with the rest of the day's news."""
    draw.rectangle((26, 954, 998, 1000), fill=NAVY)
    draw.text((40, 969), "ALSO TODAY", font=sans_b(15), fill=GOLD)
    items = ("Romania hit by a 5.3 quake  •  Cold kills displaced people "
             "in Gaza tents  •  Eisenkot asked to form Israel's next "
             "government  •  Cyclone Akvan nears the Andhra coast, "
             "landfall due Nov 20")
    lines = wrap(draw, items, sans(15), 814)
    y = 959
    for line in lines:
        draw.text((170, y), line, font=sans(15), fill=CREAM)
        y += 19


def draw_footer(draw):
    """One small line owning up to the drawing and dating the page."""
    note = ("Wednesday 18 November 2026  ·  The world's news in one image  ·  "
            "Every scene is drawn, not photographed")
    f = sans(12)
    w = draw.textlength(note, font=f)
    draw.text(((1024 - w) / 2, 1005), note, font=f, fill=(90, 90, 90))


def build(out_path="entry.png"):
    """Compose the whole front page and save it as a PNG."""
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead_visual(draw)
    draw_lead_headline(draw)
    draw_grid(draw)
    draw_also_today(draw)
    draw_footer(draw)
    img.save(out_path, format="PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(target)
    print("wrote", target)
