# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/bamphd/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/bamphd/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

**18 November 2026 — the world in one image (v2).** A Python program that draws a
single 1024×1024 newspaper-style infographic summing up Wednesday 18 November
2026: **45 verified stories** — 6 illustrated lead panels (Iran's drones on US
bases in Bahrain and Kuwait, the Crimean Bridge arch collapse, Voyager 1's
one-light-day milestone, Trump leaving Manila for the Shenzhen summit with Xi
and Putin, Nvidia's $115.8B quarter, the EU's €45bn Ukraine loan proposal),
a schematic world map with 12 story locations, a figures strip, and 39 more
one-line briefs across the Gulf, Europe, Asia, the Americas and Africa — plus
a date-check note (the Kerch strike began overnight 17 Nov; the arch collapse
was confirmed 18 Nov). All news text is baked into the code as data — no
network at runtime — and the program draws the image with Pillow + DejaVu,
falling back to the pre-rendered `entry.png` shipped in the repo if Pillow is
unavailable. Two runs write byte-identical output.

## Run it

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7billions&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
