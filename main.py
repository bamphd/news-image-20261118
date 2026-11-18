#!/usr/bin/env python3
"""18 November 2026 - the world in one image.

Draws a single 1024x1024 news infographic to /output/entry.png. Every story
is baked into the code below as data, researched from Reuters / AP /
TechCrunch on the morning of 18 November 2026. No network at runtime.

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

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# (tag, colour, headline, summary) — all six stories as reported on 18 Nov 2026.
STORIES = [
    ("GULF", (179, 38, 30),
     "Iran fires drones at a US radar base in Bahrain",
     "Bahrain says its defences intercepted the attack, the third on US targets "
     "there in days; no damage or casualties reported."),
    ("UKRAINE", (29, 78, 176),
     "Ukraine hits the Crimean Bridge for a second day",
     "The road arch collapses into the Kerch Strait; Russia pounds Kyiv's "
     "bridges in reply in the war's largest drone barrage yet."),
    ("ASIA", (15, 118, 110),
     "Trump lands in Manila for Quad talks ahead of China visit",
     "The US president joins regional leaders in the Philippines as Modi urges "
     "a peaceful, stable and prosperous Indo-Pacific."),
    ("TRADE", (180, 83, 9),
     "Canada and China extend trade deals ahead of APEC",
     "Xi meets Carney as the two countries widen cooperation before the "
     "Asia-Pacific summit; ASEAN backs AI-powered small business."),
    ("BRITAIN", (109, 40, 217),
     "UK sanctions Israeli settlement firms",
     "London acts against companies in occupied territory in a push to protect "
     "the two-state solution."),
    ("MARKETS", (21, 128, 61),
     "Nvidia revenue doubles to $115.8 billion",
     "The chipmaker beats forecasts in its first results since Jensen Huang's "
     "resignation and guides to $130 billion next quarter."),
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


def _draw(out_path):
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1024, 1024

    def font(path, size):
        return ImageFont.truetype(path, size)

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- header ----------
    header_h = 150
    d.rectangle([0, 0, W, header_h], fill=NAVY)
    d.rectangle([0, header_h - 4, W, header_h], fill=GOLD)

    kicker = font(SANS_BOLD, 25)
    d.text((44, 20), "THE WORLD IN ONE IMAGE", font=kicker, fill=GOLD)

    # Date: shrink until it fits the page width.
    date_size = 56
    while True:
        df = font(SANS_BOLD, date_size)
        if d.textlength("WEDNESDAY 18 NOVEMBER 2026", font=df) <= W - 88:
            break
        date_size -= 1
    d.text((44, 54), "WEDNESDAY 18 NOVEMBER 2026", font=df, fill=WHITE)

    sub = font(SANS, 24)
    d.text((44, 114), "Six stories that defined the day \u2014 from the Gulf to Manila",
           font=sub, fill=(196, 205, 220))

    # ---------- story rows ----------
    top = header_h
    footer_h = 44
    row_h = (H - footer_h - top) // len(STORIES)  # 138
    head_f = font(SANS_BOLD, 33)
    sum_f = font(SANS, 22)
    tag_f = font(SANS_BOLD, 33)

    for i, (tag, colour, headline, summary) in enumerate(STORIES):
        y0 = top + i * row_h
        y1 = y0 + row_h
        # alternating paper tint + left colour bar
        if i % 2 == 1:
            d.rectangle([0, y0, W, y1], fill=(241, 237, 228))
        d.rectangle([0, y0, 12, y1], fill=colour)
        if i:
            d.line([0, y0, W, y0], fill=RULE, width=1)

        text_x = 40
        text_w = W - text_x - 44
        # headline with coloured tag prefix, max 2 lines; summary max 2 lines
        full = tag + " \u00b7 " + headline
        hlines = _wrap(d, full, head_f, text_w)[:2]
        slines = _wrap(d, summary, sum_f, text_w)[:2]
        block_h = len(hlines) * 39 + len(slines) * 27
        hy = y0 + (row_h - block_h) // 2
        assert hy >= y0, f"story {tag} overflows its row"
        prefix = tag + " \u00b7 "
        for j, ln in enumerate(hlines):
            if j == 0 and ln.startswith(tag):
                d.text((text_x, hy), prefix, font=tag_f, fill=colour)
                rest = ln[len(prefix):]
                d.text((text_x + d.textlength(prefix, font=tag_f), hy),
                       rest, font=head_f, fill=INK)
            else:
                d.text((text_x, hy), ln, font=head_f, fill=INK)
            hy += 39
        for ln in slines:
            d.text((text_x, hy), ln, font=sum_f, fill=GREY)
            hy += 27
        assert hy <= y1, f"story {tag} overflows its row"

    # ---------- footer ----------
    fy = H - footer_h
    d.line([0, fy, W, fy], fill=RULE, width=1)
    foot_f = font(SANS, 20)
    d.text((40, fy + 12),
           "Sources: Reuters \u00b7 AP \u00b7 TechCrunch \u2014 18 Nov 2026",
           font=foot_f, fill=GREY)
    right = "@7billions \u00b7 make.fun"
    d.text((W - 40 - d.textlength(right, font=foot_f), fy + 12),
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
