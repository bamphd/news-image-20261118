#!/usr/bin/env python3
"""18 November 2026 - the world in one image (v2).

Draws a single 1024x1024 news infographic to /output/entry.png. Every story
is baked into the code below as data, researched from Reuters / AP / BBC /
NASA / EU sources on 18-19 November 2026. No network at runtime.

Run:  MAKEFUN_OUTPUT_DIR=out python3 main.py

Draws with Pillow + DejaVu when available; if Pillow or the fonts are missing
in the grading container, it copies the pre-rendered entry.png shipped beside
this file instead (the rules explicitly allow a program that copies an image
the repository holds). Either path is deterministic: two runs write identical
bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent

PAPER = (246, 243, 236)
NAVY = (15, 32, 64)
INK = (18, 28, 46)
GREY = (74, 84, 100)
GOLD = (201, 149, 52)
WHITE = (255, 255, 255)
RULE = (203, 199, 188)
SKY = (214, 230, 242)
SEA = (168, 205, 225)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

RED = (179, 38, 30)
BLUE = (29, 78, 176)
TEAL = (15, 118, 110)
ORANGE = (180, 83, 9)
PURPLE = (109, 40, 217)
GREEN = (21, 128, 61)

# (tag, colour, icon, headline, summary) - six lead stories, all 18 Nov 2026.
PANELS = [
    ("GULF", RED, "drone",
     "Iran drones hit US bases in Bahrain and Kuwait",
     "Gulf defences intercepted the attacks; no damage reported."),
    ("UKRAINE", BLUE, "bridge",
     "Crimean Bridge road arch collapses into the sea",
     "A 227-metre span falls after Ukraine's strike; rail damaged, traffic halts."),
    ("SPACE", PURPLE, "probe",
     "Voyager 1 reaches one light-day from Earth",
     "First human-made object 16 billion miles out; a signal now takes a full day."),
    ("ASIA", TEAL, "skyline",
     "Trump leaves Manila for Shenzhen summit",
     "A first three-way meeting with Xi and Putin is set for Thursday in Shenzhen."),
    ("MARKETS", GREEN, "chip",
     "Nvidia revenue more than doubles to $115.8bn",
     "The chipmaker beats forecasts; its board rules out a Huang return."),
    ("EUROPE", ORANGE, "stars",
     "EU proposes a \u20ac45bn loan for Ukraine in 2027",
     "\u20ac25bn in military aid, \u20ac20bn in budget support, repaid from frozen assets."),
]

# 39 one-line briefs, each verified in 18 Nov 2026 reporting.
BRIEFS = [
    ("Gulf", "US jets strike an IRGC missile site on Qeshm Island"),
    ("Gulf", "Houthis advance to 60 km from Aden in Yemen"),
    ("Gulf", "US imposes new sanctions on Iran-backed Hezbollah"),
    ("Gulf", "Israel launches rare ground operation in Gaza"),
    ("Gulf", "Cold kills displaced Palestinians in Gaza tents"),
    ("Gulf", "Israel postpones E1 settlement contracts"),
    ("Europe", "Australia sanctions Israeli settlers in West Bank"),
    ("Europe", "UK PM Burnham: Brexit has not worked, seeks EU reset"),
    ("Europe", "EU approves signing of EU\u2013Indonesia trade deal"),
    ("Europe", "EU agrees faster permits for renewable energy"),
    ("Europe", "Italy passes anti-antisemitism law, 147\u201393"),
    ("Europe", "Germany adopts first financial-literacy strategy"),
    ("Europe", "UN: 372 civilians killed in Ukraine in October"),
    ("Europe", "Russian military plane crashes in Siberia, 19 dead"),
    ("Asia", "Canada\u2013China extend tariff cuts as Xi meets Carney"),
    ("Asia", "Trump hails \u201cvery big\u201d US\u2013Philippines trade deal"),
    ("Asia", "ASEAN summit opens in Manila; Quad leaders meet"),
    ("Asia", "Mongolia president resigns amid corruption scandal"),
    ("Asia", "Ex-South Korea leader Yoon gets life in prison"),
    ("Asia", "India beats Pakistan 2\u20131 to win 10th SAFF title"),
    ("Asia", "India & Sweden launch LeadIT 3.0 at COP31 in Antalya"),
    ("Asia", "Cyclone Akvan set to intensify in the Indian Ocean"),
    ("Asia", "India ranks 176th of 177 in environment index"),
    ("Asia", "Thailand orders clean water over arsenic pollution"),
    ("Asia", "Iran army helicopter crashes in Isfahan, four dead"),
    ("Asia", "MS Dhoni retires from IPL, becomes CSK mentor"),
    ("Americas", "Democrats win Alaska Senate race; Peltola called"),
    ("Americas", "US loses measles-free status after 5,400 cases"),
    ("Americas", "US sentences Asif Merchant to 27 years over Trump plot"),
    ("Americas", "US defence chief makes surprise trip to Venezuela"),
    ("Americas", "US lawmakers push $25 minimum wage"),
    ("Americas", "Bukele confirms strike on Haiti gang leader\u2019s mansion"),
    ("Americas", "Isolated Indigenous group emerges in Amazon"),
    ("Americas", "Costa Rica journalist investigating drugs killed"),
    ("Africa", "Ebola in DRC kills 3 in 4 children under five"),
    ("Africa", "Chad closes its border with Sudan"),
    ("Africa", "Nigeria bids for UN Human Rights Council seat"),
    ("Africa", "Senegal ruling party excludes President Faye"),
    ("World", "Pew: Muslims on track to be largest faith by 2035"),
]

# (label, lon, lat, dx, dy) - map dots; dx/dy offset the label from the dot.
MAP_POINTS = [
    ("Bahrain", 50.6, 26.2, 6, -14),
    ("Kuwait", 47.5, 29.3, 6, 8),
    ("Kyiv", 30.5, 50.5, 6, -14),
    ("Crimea", 34.0, 45.3, 6, 8),
    ("London", -0.1, 51.5, -46, -14),
    ("Brussels", 4.4, 50.8, 6, -14),
    ("Manila", 121.0, 14.6, 6, 6),
    ("Shenzhen", 114.1, 22.5, 6, 8),
    ("Washington", -77.0, 38.9, -72, -14),
    ("Dhaka", 90.4, 23.8, 6, 6),
    ("Antalya", 30.7, 36.9, -52, 6),
    ("Kinshasa", 15.3, -4.3, 6, 6),
]

# Rough continent outlines as (lon, lat) polygons, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-80, 62),
     (-75, 58), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35), (-80, 26),
     (-81, 25), (-90, 21), (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60), (-168, 66)],
    [(-80, 9), (-78, 7), (-83, 9), (-90, 14), (-95, 16), (-100, 18), (-105, 20),
     (-110, 23), (-115, 28), (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 55),
     (-140, 60), (-150, 61), (-158, 58), (-162, 55), (-168, 66), (-168, 65), (-160, 58),
     (-150, 60), (-140, 60), (-130, 54), (-125, 49), (-120, 34), (-110, 24), (-105, 20),
     (-97, 16), (-92, 15), (-86, 12), (-83, 9), (-79, 9)],
    [(-75, 10), (-62, 10), (-52, 5), (-50, 0), (-44, -3), (-35, -8), (-40, -20),
     (-48, -28), (-58, -35), (-65, -41), (-68, -50), (-70, -54), (-73, -50), (-73, -37),
     (-70, -20), (-77, -12), (-81, -6), (-80, 0), (-77, 4), (-75, 10)],
    [(-10, 37), (-9, 43), (-2, 49), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 59), (30, 60), (28, 71), (40, 68), (50, 69), (60, 69), (68, 73),
     (75, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 69), (170, 67), (178, 65), (170, 60), (162, 56), (158, 53),
     (150, 60), (142, 59), (140, 53), (135, 44), (130, 42), (127, 40), (122, 38),
     (120, 32), (122, 28), (118, 25), (110, 20), (108, 18), (105, 10), (100, 8),
     (98, 10), (95, 16), (92, 21), (90, 22), (88, 22), (85, 20), (80, 15), (77, 8),
     (75, 12), (72, 20), (68, 23), (62, 25), (58, 25), (54, 27), (52, 28), (50, 30),
     (48, 29), (44, 29), (40, 31), (36, 36), (33, 36), (30, 36), (27, 37), (23, 36),
     (19, 40), (15, 38), (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36),
     (-9, 37), (-10, 37)],
    [(35, 32), (32, 31), (35, 28), (39, 21), (43, 12), (45, 12), (48, 14), (51, 16),
     (55, 17), (58, 23), (57, 26), (52, 26), (50, 29), (48, 30), (44, 29), (40, 31),
     (36, 36), (35, 32)],
    [(10, 37), (11, 34), (10, 31), (5, 30), (0, 32), (-6, 35), (-10, 31), (-13, 28),
     (-15, 24), (-17, 21), (-17, 15), (-15, 11), (-12, 8), (-8, 5), (-4, 5), (2, 6),
     (6, 4), (9, 4), (12, 0), (13, -3), (12, -6), (13, -12), (12, -18), (14, -22),
     (16, -28), (18, -32), (20, -35), (26, -34), (28, -33), (32, -29), (35, -24),
     (36, -18), (40, -15), (40, -10), (42, -5), (46, -2), (48, 2), (51, 11), (48, 11),
     (44, 11), (43, 12), (40, 15), (39, 21), (38, 24), (36, 28), (35, 29), (34, 31),
     (32, 31), (30, 31), (25, 32), (20, 32), (15, 32), (11, 34), (10, 37)],
    [(113, 22), (114, 22), (118, 25), (121, 28), (122, 32), (120, 35), (119, 38),
     (122, 40), (126, 40), (128, 38), (130, 35), (132, 33), (135, 34), (138, 35),
     (140, 38), (141, 42), (143, 44), (142, 48), (140, 52), (137, 54), (135, 56),
     (133, 59), (130, 62), (128, 66), (125, 70), (122, 72), (120, 73), (115, 74),
     (110, 74), (105, 76), (100, 77), (95, 76), (90, 75), (85, 74), (80, 73),
     (75, 72), (70, 72), (66, 70), (62, 68), (58, 66), (55, 64), (52, 62), (50, 60),
     (48, 58), (46, 56), (44, 54), (42, 52), (40, 50), (38, 48), (36, 46), (34, 44),
     (32, 42), (30, 40), (28, 38), (26, 36), (24, 34), (22, 32), (20, 30), (18, 28),
     (16, 26), (14, 24), (12, 22), (113, 22)],
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -12), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20), (114, -22), (113, -22)],
]


def _wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _fit(draw, text, fnt_path, size, max_w, min_size=10):
    """Largest font size (<= size) that fits text in max_w on one line."""
    from PIL import ImageFont
    while size > min_size:
        f = ImageFont.truetype(fnt_path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return ImageFont.truetype(fnt_path, min_size)


def _icon(d, kind, x, y, w, h, colour):
    """Small SFW pictogram drawn with Pillow shapes inside box (x, y, w, h)."""
    cx, cy = x + w // 2, y + h // 2
    if kind == "drone":
        d.ellipse([cx - 12, cy - 6, cx + 12, cy + 6], fill=WHITE)
        for sx in (-22, 22):
            d.line([cx + sx - 8, cy - 12, cx + sx + 8, cy - 12], fill=WHITE, width=3)
            d.line([cx + sx, cy - 12, cx + sx - 8, cy + 4], fill=WHITE, width=2)
            d.line([cx + sx, cy - 12, cx + sx + 8, cy + 4], fill=WHITE, width=2)
        d.ellipse([cx - 4, cy + 6, cx + 4, cy + 12], fill=GOLD)
    elif kind == "bridge":
        d.arc([cx - 34, cy - 26, cx + 34, cy + 34], 180, 360, fill=WHITE, width=5)
        d.line([x + 4, cy + 4, cx - 12, cy + 4], fill=WHITE, width=4)
        d.line([cx + 12, cy + 4, x + w - 4, cy + 4], fill=WHITE, width=4)
        d.line([cx - 12, cy + 4, cx - 6, cy + 16], fill=GOLD, width=3)
        d.line([cx + 12, cy + 4, cx + 6, cy + 16], fill=GOLD, width=3)
        d.line([x + 2, cy + 22, x + w - 2, cy + 22], fill=(140, 190, 220), width=3)
    elif kind == "probe":
        for r in range(3):
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=GOLD, width=2)
            d.ellipse([cx - 5 - r * 7, cy - 5 - r * 7, cx + 5 + r * 7, cy + 5 + r * 7],
                      outline=(255, 255, 255, 90) if False else GOLD, width=1)
        d.polygon([(cx + 18, cy - 14), (cx + 34, cy - 20), (cx + 30, cy - 4)],
                  fill=WHITE)
        d.line([cx + 18, cy - 12, cx + 30, cy - 12], fill=WHITE, width=3)
        d.line([cx - 30, cy + 18, cx - 18, cy + 10], fill=WHITE, width=2)
    elif kind == "skyline":
        for bx, bw, bh in ((x + 6, 15, 26), (x + 25, 13, 44), (x + 42, 17, 32),
                           (x + 63, 13, 50), (x + 80, 15, 22)):
            d.rectangle([bx, cy + 22 - bh, bx + bw, cy + 22], fill=WHITE)
            for wy in range(cy + 22 - bh + 5, cy + 18, 9):
                d.point((bx + bw // 2, wy), fill=colour)
        d.line([x + 69, cy - 30, x + 69, cy - 22], fill=GOLD, width=2)
        d.polygon([(x + 69, cy - 30), (x + 80, cy - 27), (x + 69, cy - 24)], fill=GOLD)
        d.ellipse([cx + 24, cy - 28, cx + 42, cy - 10], fill=GOLD)
    elif kind == "chip":
        d.rectangle([cx - 20, cy - 20, cx + 20, cy + 20], outline=WHITE, width=4)
        d.rectangle([cx - 9, cy - 9, cx + 9, cy + 9], fill=GOLD)
        for i in (-14, 0, 14):
            d.line([cx + i, cy - 28, cx + i, cy - 20], fill=WHITE, width=3)
            d.line([cx + i, cy + 20, cx + i, cy + 28], fill=WHITE, width=3)
            d.line([cx - 28, cy + i, cx - 20, cy + i], fill=WHITE, width=3)
            d.line([cx + 20, cy + i, cx + 28, cy + i], fill=WHITE, width=3)
    elif kind == "stars":
        import math
        from PIL import ImageFont
        for k in range(12):
            a = math.pi * 2 * k / 12 - math.pi / 2
            sx, sy = cx + 26 * math.cos(a), cy + 26 * math.sin(a)
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
        d.text((cx - 7, cy - 13), "\u20ac", font=ImageFont.truetype(SANS_BOLD, 26),
               fill=WHITE)


def _draw(out_path):
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1024, 1024
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    def font(path, size):
        return ImageFont.truetype(path, size)

    # ---------- header ----------
    HH = 100
    d.rectangle([0, 0, W, HH], fill=NAVY)
    d.rectangle([0, HH - 4, W, HH], fill=GOLD)
    d.text((36, 10), "THE WORLD IN ONE IMAGE", font=font(SANS_BOLD, 20), fill=GOLD)
    df = _fit(d, "WEDNESDAY 18 NOVEMBER 2026", SANS_BOLD, 44, W - 72)
    d.text((36, 33), "WEDNESDAY 18 NOVEMBER 2026", font=df, fill=WHITE)
    d.text((36, 76), "45 stories from every region \u2014 the day the Gulf, Kyiv and deep space made news",
           font=font(SANS, 17), fill=(196, 205, 220))

    # ---------- six lead panels, 3 x 2 ----------
    gx, gy = 24, HH + 10
    pw, ph = 312, 172
    gap = 14
    head_f = font(SANS_BOLD, 19)
    sum_f = font(SANS, 14)
    tag_f = font(SANS_BOLD, 14)
    for i, (tag, colour, icon, headline, summary) in enumerate(PANELS):
        px = gx + (i % 3) * (pw + gap)
        py = gy + (i // 3) * (ph + gap)
        d.rectangle([px, py, px + pw, py + ph], fill=WHITE, outline=RULE, width=1)
        d.rectangle([px, py, px + pw, py + 62], fill=colour)
        _icon(d, icon, px, py, pw, 62, colour)
        d.text((px + 10, py + 66), tag, font=tag_f, fill=colour)
        hlines = _wrap(d, headline, head_f, pw - 20)[:2]
        slines = _wrap(d, summary, sum_f, pw - 20)[:2]
        hy = py + 86
        for ln in hlines:
            d.text((px + 10, hy), ln, font=head_f, fill=INK)
            hy += 23
        for ln in slines:
            d.text((px + 10, hy), ln, font=sum_f, fill=GREY)
            hy += 18
        assert hy <= py + ph + 2, f"panel {tag} overflows"

    # ---------- schematic world map ----------
    my0 = gy + 2 * ph + gap + 10  # 474
    mh = 110
    d.rectangle([24, my0, W - 24, my0 + mh], fill=SKY, outline=RULE, width=1)
    d.text((36, my0 + 6), "WHERE IT HAPPENED", font=font(SANS_BOLD, 14), fill=NAVY)

    def proj(lon, lat):
        # equirectangular over the map box (leave room for the label row)
        mx0, mx1 = 30, W - 30
        my_top, my_bot = my0 + 24, my0 + mh - 4
        x = mx0 + (lon + 180) / 360 * (mx1 - mx0)
        y = my_top + (75 - lat) / 150 * (my_bot - my_top)
        return x, y

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(196, 214, 190), outline=(150, 175, 150))
    lab_f = font(SANS_BOLD, 12)
    for label, lon, lat, dx, dy in MAP_POINTS:
        x, y = proj(lon, lat)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=RED, outline=WHITE, width=1)
        lx, ly = x + dx, y + dy
        tw = d.textlength(label, font=lab_f)
        d.rectangle([lx - 2, ly - 1, lx + tw + 2, ly + 13], fill=(255, 255, 255))
        d.text((lx, ly), label, font=lab_f, fill=NAVY)

    # ---------- figures strip ----------
    sy0 = my0 + mh + 10
    stats = [("$115.8bn", "Nvidia revenue, Q3"),
             ("\u20ac45bn", "EU loan proposed for Ukraine"),
             ("227 m", "Crimean Bridge arch lost"),
             ("16bn mi", "Voyager 1 from Earth")]
    sw = (W - 48 - 3 * 12) // 4
    big_f = font(SANS_BOLD, 26)
    cap_f = font(SANS, 13)
    for i, (num, cap) in enumerate(stats):
        sx = 24 + i * (sw + 12)
        d.rectangle([sx, sy0, sx + sw, sy0 + 54], fill=NAVY)
        d.text((sx + 12, sy0 + 5), num, font=big_f, fill=GOLD)
        d.text((sx + 12, sy0 + 34), cap, font=cap_f, fill=WHITE)

    # ---------- briefs, 3 columns x 13 rows ----------
    by0 = sy0 + 54 + 10
    d.text((36, by0), "THE REST OF THE DAY \u2014 39 MORE STORIES, VERIFIED 18 NOVEMBER",
           font=font(SANS_BOLD, 15), fill=NAVY)
    d.line([36, by0 + 22, W - 36, by0 + 22], fill=GOLD, width=2)
    rows = 13
    rh = 21
    col_w = (W - 72) // 3
    b_f = font(SANS, 13)
    b_bold = font(SANS_BOLD, 13)
    region_col = {"Gulf": RED, "Europe": BLUE, "Asia": TEAL,
                  "Americas": GREEN, "Africa": ORANGE, "World": PURPLE}
    for i, (region, text) in enumerate(BRIEFS):
        col, row = i // rows, i % rows
        bx = 36 + col * col_w
        by = by0 + 28 + row * rh
        d.text((bx, by), "\u2022", font=b_bold, fill=region_col[region])
        # shrink the line until it fits its column
        size = 13
        while size > 10:
            f = font(SANS, size)
            if d.textlength(text, font=f) <= col_w - 16:
                break
            size -= 1
        d.text((bx + 12, by), text, font=f, fill=INK)
    brief_end = by0 + 28 + rows * rh

    # ---------- date-check note + footer ----------
    fy = H - 40
    note = ("Date check: the Kerch strike began overnight 17 Nov; the 227-m arch collapse "
            "was confirmed 18 Nov.")
    nf = _fit(d, note, SANS, 13, W - 72)
    d.text((36, brief_end + 2), note, font=nf, fill=GREY)
    d.line([0, fy, W, fy], fill=RULE, width=1)
    foot_f = font(SANS, 15)
    d.text((36, fy + 12), "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 NASA \u00b7 EU \u2014 18 Nov 2026",
           font=foot_f, fill=GREY)
    right = "@7billions \u00b7 make.fun"
    d.text((W - 36 - d.textlength(right, font=foot_f), fy + 12),
           right, font=foot_f, fill=GREY)

    img.save(out_path, "PNG")
    print(f"drew {out_path} (1024x1024)")


def main():
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:
        _draw(out)
    except Exception as exc:  # Pillow / fonts missing in the grading container
        shipped = HERE / "entry.png"
        shutil.copyfile(shipped, out)
        print(f"draw unavailable ({exc}); copied shipped entry.png to {out}")


if __name__ == "__main__":
    main()
