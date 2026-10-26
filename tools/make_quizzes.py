"""Book quizzes for rainingcad.com, made from the book text (the BookText_AllFour text pack) and the pictures in the book PDFs.
Usage (repo root): python3 tools/make_quizzes.py TEXTPACK_DIR PDF_DIR
Writes tools/quiz/<book>.json and tools/quiz/<book>/img/*.webp. Then run tools/build_rcd.py.
Breed books: five rounds of ten breeds (the countdown 50 to 1). Idiom books: one round per chapter.
The text pack page numbers are two less than the PDF pages: a breed's photo is on pdf_page + 1, an idiom's picture on page + 1."""
import io, json, os, random, re, sys
from PIL import Image
import pymupdf as fitz
TP, PD = sys.argv[1], sys.argv[2]
OFF = 2
def first(paras, n=2):
    t = ' '.join(p for p in paras if p and not p.isupper())
    s = re.split(r'(?<=[.!?])\s+', t); return ' '.join(s[:n])[:320]
def save_img(doc, page, out):
    xs = doc[page - 1].get_images(full=True)
    if not xs: return False
    x = max(xs, key=lambda x: x[2] * x[3]); im = Image.open(io.BytesIO(doc.extract_image(x[0])['image'])).convert('RGB')
    im.thumbnail((720, 900)); im.save(out, 'WEBP', quality=78); return True
def opts(right, pool, rnd, n=4):
    o = [right] + rnd.sample([p for p in pool if p != right], n - 1); rnd.shuffle(o); return o, o.index(right)
def write(bid, rounds, blurb):
    json.dump({'blurb': blurb, 'pass': 70, 'rounds': rounds}, open(f'tools/quiz/{bid}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(bid, len(rounds), 'rounds', sum(len(r['qs']) for r in rounds), 'questions')

def breeds(bid, js, pdf, animal):
    B = json.load(open(os.path.join(TP, js), encoding='utf-8')); B.sort(key=lambda b: -b['rank'])
    doc = fitz.open(os.path.join(PD, pdf)); rnd = random.Random(bid); os.makedirs(f'tools/quiz/{bid}/img', exist_ok=True)
    fact = lambda b, k: (dict(b['facts']) if isinstance(b['facts'], list) else b['facts']).get(k, '')
    origins = sorted({fact(b, 'Origin') for b in B if fact(b, 'Origin')})
    rounds = []
    for r in range(5):
        grp = B[r * 10:(r + 1) * 10]; names = [b['name'] for b in grp]; qs = []
        for k, b in enumerate(grp):
            slug = re.sub(r'[^a-z0-9]+', '-', b['name'].lower()).strip('-'); img = f'/quiz/{bid}/img/{slug}.webp'
            have = save_img(doc, b['pdf_page'] + OFF - 1, f'tools/quiz/{bid}/img/{slug}.webp')
            why = f'The {b["name"]}, number {b["rank"]} in the countdown. ' + first(b['story'], 1)
            kind = ['photo', 'tagline', 'photo', 'origin', 'photo'][k % 5]
            if kind == 'origin' and (not fact(b, 'Origin') or len(origins) < 4): kind = 'tagline'
            if kind == 'photo' and not have: kind = 'tagline'
            if kind == 'photo':
                o, a = opts(b['name'], names, rnd); qs.append({'q': f'Which breed is this?', 'img': img, 'o': o, 'a': a, 'x': why})
            elif kind == 'tagline':
                o, a = opts(b['name'], names, rnd); qs.append({'q': f'Which breed is “{b["tagline"].rstrip(".")}”?', 'o': o, 'a': a, 'x': why})
            else:
                o, a = opts(fact(b, 'Origin'), origins, rnd); qs.append({'q': f'Where does the {b["name"]} come from?', 'img': img if have else None, 'o': o, 'a': a, 'x': why})
        rounds.append({'name': f'{animal} {grp[0]["rank"]} to {grp[-1]["rank"]}', 'qs': qs})
    write(bid, rounds, f'Fifty {animal.lower()} breeds in five rounds. Name the breed from its photo, its description and where it comes from.')

def idioms(bid, chapters, pdf, art_off, animal):
    doc = fitz.open(os.path.join(PD, pdf)); rnd = random.Random(bid); os.makedirs(f'tools/quiz/{bid}/img', exist_ok=True)
    allnames = [i['title'] for c in chapters for i in c['idioms']]; rounds = []
    for c in chapters:
        names = [i['title'] for i in c['idioms']]; pool = names if len(names) >= 4 else allnames; qs = []
        for k, i in enumerate(c['idioms']):
            slug = re.sub(r'[^a-z0-9]+', '-', i['title'].lower()).strip('-'); img = f'/quiz/{bid}/img/{slug}.webp'
            have = bool(i.get('page')) and save_img(doc, int(i['page']) + art_off, f'tools/quiz/{bid}/img/{slug}.webp')
            mean = (i.get('tagline') or i.get('subtitle') or '').rstrip('.')
            why = f'{i["title"]}: {mean}. ' + first(i['paras'], 1)
            if k % 2 == 0 and have:
                o, a = opts(i['title'], pool, rnd); qs.append({'q': 'Which idiom does this picture show?', 'img': img, 'o': o, 'a': a, 'x': why})
            else:
                o, a = opts(i['title'], pool, rnd); qs.append({'q': f'Which idiom means “{mean}”?', 'o': o, 'a': a, 'x': why})
        rounds.append({'name': c['title'], 'qs': qs})
    write(bid, rounds, f'How well do you know your {animal} idioms? One round per chapter of the book. Name the idiom from its picture and its meaning.')

breeds('cat-breeds', 'catbreeds.json', 'CatBreeds_Book_Distributable.pdf', 'Cats')
breeds('dog-breeds', 'dogbreeds.json', 'DogBreeds_Book_Final.pdf', 'Dogs')
ed = json.load(open(os.path.join(TP, 'everydog.json'), encoding='utf-8'))
idioms('every-dog-has-his-day', ed['chapters'], 'EveryDogHasHisDay_Book_Final.pdf', 1, 'dog')
cp = json.load(open(os.path.join(TP, 'catspajamas.json'), encoding='utf-8'))
# The Cat's Pajamas text pack has printed page numbers only: find each idiom's text page in the PDF, its picture is the page before
doc = fitz.open(os.path.join(PD, 'CatsPajamas_INTERIOR_print.pdf'))
heads = {}
for n, pg in enumerate(doc, 1):
    t = pg.get_text().strip().split('\n'); heads.setdefault(t[0].strip().lower(), n) if t and t[0].strip() else None
for c in cp['chapters']:
    for i in c['idioms']: i['page'] = heads.get(i['title'].strip().lower(), 0)
idioms('the-cats-pajamas', cp['chapters'], 'CatsPajamas_INTERIOR_print.pdf', -1, 'cat')
