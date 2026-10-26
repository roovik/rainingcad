"""Read inside: turn a book PDF into page images for the gated reader at /inside/<book>/ on rainingcad.com.
Usage (repo root): python3 tools/make_inside.py BOOK-ID BOOK.pdf      (BOOK-ID as in tools/books.json)
         python3 tools/make_inside.py BOOK-ID BOOK.pdf --find   lists the pages that look like chapter openers, to fill STARTS
Writes tools/inside/BOOK-ID/inside.json and pages/pNNN.webp. Then run tools/build_rcd.py.
Pages before the first chapter are the opening pages (contents, introduction). They and chapter 1 are free. The rest needs a code."""
import io, json, os, re, sys
from PIL import Image
import pymupdf as fitz
# first page of each chapter (1-based) and its name, per book
STARTS = {}
W = 1100
bid, src = sys.argv[1], sys.argv[2]
d = fitz.open(src)
if '--find' in sys.argv:
    for i, pg in enumerate(d, 1):
        t = pg.get_text().strip()
        if re.match(r'^(chapter|part)\b', t, re.I) or re.search(r'^\s*chapter\s+\w+', t[:200], re.I | re.M): print(i, repr(t[:90]))
    sys.exit()
cfg = STARTS[bid]
OUT = f'tools/inside/{bid}/'
os.makedirs(OUT + 'pages', exist_ok=True)
for f in os.listdir(OUT + 'pages'): os.remove(OUT + 'pages/' + f)
pages = []
for i, pg in enumerate(d, 1):
    im = Image.open(io.BytesIO(pg.get_pixmap(dpi=150).tobytes('png'))).convert('RGB')
    if im.width > W: im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    im.save(f'{OUT}pages/p{i:03d}.webp', 'WEBP', quality=78); pages.append(f'p{i:03d}.webp')
st = [s for s, _ in cfg]
chs = [{'n': 0, 'name': 'Opening pages', 'pages': pages[:st[0] - 1]}]
for k, (s, name) in enumerate(cfg):
    chs.append({'n': k + 1, 'name': name, 'pages': pages[s - 1:(st[k + 1] - 1 if k + 1 < len(st) else len(pages))]})
json.dump({'id': bid, 'chapters': chs}, open(OUT + 'inside.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(bid, len(pages), 'pages', [(c['n'], c['name'], len(c['pages'])) for c in chs])
