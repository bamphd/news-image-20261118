# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/bamphd/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/bamphd/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

**18 November 2026 — the world in one image.** A Python program that draws a
single 1024×1024 newspaper-style infographic summing up Wednesday 18 November
2026: Iran's drone attack on a US radar base in Bahrain, Ukraine's second-day
strike on the Crimean Bridge, Trump in Manila for Quad talks, the Canada–China
trade extension ahead of APEC, the UK's sanctions on Israeli settlement firms,
and Nvidia's $115.8B quarter. All news text is baked into the code as data —
no network at runtime — and the program draws the image with Pillow + DejaVu,
falling back to the pre-rendered `entry.png` shipped in the repo if Pillow is
unavailable. Two runs write byte-identical output.

## Run it

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7billions&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
