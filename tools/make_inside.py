"""Read inside: turn a book PDF into page images for the gated reader at /inside/<book>/ on rainingcad.com.
Usage (repo root): python3 tools/make_inside.py BOOK-ID BOOK.pdf      (BOOK-ID as in tools/books.json)
         python3 tools/make_inside.py BOOK-ID BOOK.pdf --find   lists the pages that look like chapter openers, to fill STARTS
Writes tools/inside/BOOK-ID/inside.json and pages/pNNN.webp. Then run tools/build_rcd.py.
Pages before the first chapter are the opening pages (contents, introduction). They and chapter 1 are free. The rest needs a code."""
import io, json, os, re, sys
from PIL import Image
import pymupdf as fitz
# first page of each chapter (1-based) and its name, per book
STARTS = {"cat-breeds": [[9, "Breeds 50 to 41"], [29, "Breeds 40 to 31"], [49, "Breeds 30 to 21"], [69, "Breeds 20 to 11"], [89, "Breeds 10 to 1"]],
 "dog-breeds": [[11, "Breeds 50 to 41"], [32, "Breeds 40 to 31"], [52, "Breeds 30 to 21"], [72, "Breeds 20 to 11"], [92, "Breeds 10 to 1"]],
 "every-dog-has-his-day": [[14, "It Shouldn't Happen to a Dog"], [32, "Between Bark and Bite"], [50, "Love Me, Love My Dog"], [68, "Dog Star Rising"], [86, "Hungry as a Dog"], [104, "Who Let the Dogs Out?"], [122, "Fighting Dogs"], [140, "Dog-Eared"], [158, "Doggie Bag"]],
 "the-cats-pajamas": [[13, "Pure Class"], [27, "Sitting Pretty"], [41, "Reading the Room"], [55, "The Waiting Game"], [69, "Always Land"], [83, "Need to Know"], [97, "How It Falls"], [111, "Off the Leash"], [127, "9 Lives"], [147, "Claws Out"], [161, "The Big Cats"]],
 "every-bitch-has-her-way": [[11, "Scent of a Bitch"], [17, "Every Bitch Needs a Job"], [23, "Bitches Off the Leash"], [29, "The Underbitch"], [35, "The Bitch on the Line"], [41, "The House Bitch"], [47, "Big Bitch Energy"], [53, "Season of the Bitch"], [59, "Beware of the Bitch"], [65, "The Lap Bitch"], [71, "Bitching Up the Wrong Tree"], [77, "Son of a Bitch"], [83, "Lucky Bitch"], [89, "Desperate Bitches"], [95, "The Alpha Bitch"], [101, "Every Bitch Has Her Day"]]}
W = 1000
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
    im.save(f'{OUT}pages/p{i:03d}.webp', 'WEBP', quality=72); pages.append(f'p{i:03d}.webp')
st = [s for s, _ in cfg]
chs = [{'n': 0, 'name': 'Opening pages', 'pages': pages[:st[0] - 1]}]
for k, (s, name) in enumerate(cfg):
    chs.append({'n': k + 1, 'name': name, 'pages': pages[s - 1:(st[k + 1] - 1 if k + 1 < len(st) else len(pages))]})
json.dump({'id': bid, 'chapters': chs}, open(OUT + 'inside.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(bid, len(pages), 'pages', [(c['n'], c['name'], len(c['pages'])) for c in chs])
