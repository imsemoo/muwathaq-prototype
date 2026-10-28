# موثّق MUWATHAQ — design prototype

Arabic (RTL) theme prototype for موثّق, a platform that documents crimes by perpetrators of the Israeli
occupation, verifies the evidence and links it to international law. Identity «الحِرْز»: every record is a
sealed exhibit — tied with cord, sealed in wax, opened in front of the reader.

## Build

```
python -I tools/fonts.py      # WOFF2 subsets of Vazirmatn and Red Hat Mono (sources in research/font-src, gitignored)
python -I tools/brand.py      # logo, seal mark and favicon, outlined from the type
python -I tools/photos.py     # Commons photos in tools/photos.json -> assets/img/photo/*.webp + CREDITS.md
python tools/build.py         # every page + assets/js/index.js (search index)
python -I tools/links.py      # internal link and anchor check
```

Content lives in `research/*.json` (sourced research) and `tools/picks.json` (hand choices: which photo
goes with which record, the illustrative verification states, the featured records). Never edit the built
HTML; bump `V` in `tools/shell.py` after any CSS or JS change.

## What is real and what is illustrative

Real and linked to the original: court, UN and rights documents; incidents as reported, with each account
attributed; legal statuses of persons with issuing body and date; official texts of legal provisions;
photographs with place, date, author and licence. Illustrative: the platform's own verification states
(the seals), custody logs and their dates, reference numbers, and the submission, correction and donation
flows (nothing is sent anywhere).

## QA

`node --experimental-websocket tools/qa.mjs http://localhost:8329/ tools/probe.js out.json 375,768,1280 index.html …`
runs the visual-QA probe; `tools/shot.mjs` takes screenshots through headless Chrome.

## Direction B, for the client to choose

`directions.html` sets the two directions side by side. Direction A, «الحِرْز», is the whole site above.
Direction B, «المتن والحاشية», is a home page and an identity page in `b/`, built on the same records:
every sentence of the text is numbered to its source in the margin, the luhaq (the copyist's hooked line)
runs from the sentence being read to its source, and verification states are the copyists' collation signs
(صح، معا، كذا، بلغ، خ). Its inner links still open direction A's pages.

```
python tools/b_brand.py      # wordmark, tile, the six signs (b/assets/brand)
python tools/b_fonts.py      # Noto Naskh Arabic, Noto Kufi Arabic, Fragment Mono (b/assets/fonts)
python tools/b_home.py       # b/index.html, b/identity.html
python tools/directions.py   # directions.html
```
