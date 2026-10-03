# A Dog Year: Every Day Has Its Dog

Build files for the 2027 dog-breed calendar and journal. One JSON record plus nine role-named photos produces one four-page 8x10 in spread.

## Setup

    pip install qrcode pillow playwright pypdf
    playwright install chromium
    mkdir npm && cd npm && npm init -y && npm install @fontsource/spectral @fontsource-variable/hanken-grotesk && cd ..

## Build a week

    python make_week.py weeks/week11_golden_retriever.json photos/week11 Week11_GoldenRetriever.pdf

The photo folder holds hero, sun, mon, tue, wed, thu, fri, sat and lastwalk images (png or jpg).
`make_week_lite.py` is the same script with photos shrunk to about 100 dpi for screen review.

## Cover and front matter

- `build_cover.py grid.png Cover.pdf` builds the cover over a 7x7 photo grid image.
- `build_front.py Front.pdf` builds the introduction, the season image (`winter.png`) and the winter essay.

## Links

QR codes use `https://rainingcad.com/DY2027/[week 1-50]/[day 1-8]`. Days 1-7 are Sunday to Saturday and day 8 is the Last Walk. Page 2 links to `https://rainingcad.com/DY2027/[week]`. The hero page has no QR.

## Not in this repo

Photos and rendered PDFs are large and are kept out. Add them with Git LFS if needed.
