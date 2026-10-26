"""Build the access-code pages, Read inside and the book quizzes of rainingcad.com into ./site, in the site's own look.
Usage (repo root): python3 tools/build_rcd.py
Writes: /unlock/, /redeem/, /admin/, /inside/<book>/ (from tools/inside/<book>/inside.json, made by tools/make_inside.py),
/quiz/<book>/ (from tools/quiz/<book>.json) with certificates, and /gate.json for the Worker (worker.js)."""
import os, re, json, shutil, hashlib, html
from PIL import Image
E = lambda s: html.escape(str(s), quote=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site'); T = os.path.join(ROOT, 'tools')
BOOKS = json.load(open(os.path.join(T, 'books.json'), encoding='utf-8'))   # id, key, title, kind, buy links
BY = {b['id']: b for b in BOOKS}
FREE_IN = [0, 1]   # opening pages and chapter 1

# the site's look, taken from a page that already has it
_tp = open(os.path.join(SITE, 'books', 'the-cats-pajamas', 'look-inside', 'index.html'), encoding='utf-8').read()
_css = re.search(r'<style>(.*?)\.book\{', _tp, re.S).group(1)
_nav = _tp[_tp.index('<body>') + 6:_tp.index('<p class="kick">')]
_nav = _nav.replace('<a href="/books/" class="on">Books</a>', '<a href="/books/">Books</a>')
_foot = '<div class="foot">&copy; Richard J. Koret. Raining Cats &amp; Dogs. <a href="/">rainingcad.com</a></div>\n</div></body></html>'
def ver(f): return hashlib.md5(open(os.path.join(SITE, f), 'rb').read()).hexdigest()[:8]
shutil.copy(os.path.join(T, 'cert.js'), os.path.join(SITE, 'cert.js'))
shutil.copy(os.path.join(T, 'rcd.js'), os.path.join(SITE, 'rcd.js'))
EXTRA = open(os.path.join(T, 'rcd.css'), encoding='utf-8').read()
def write(path, title, desc, body, data=None, robots='', og=''):
    d = os.path.join(SITE, path.strip('/')); os.makedirs(d, exist_ok=True)
    js = ''
    if data is not None:
        js = ('<script type="application/json" id="rc-data">' + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + '</script>'
              + f'<script src="/cert.js?v={ver("cert.js")}" defer></script><script src="/rcd.js?v={ver("rcd.js")}" defer></script>')
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{E(title)}</title><meta name="description" content="{E(desc)}">'
        + (f'<meta name="robots" content="{robots}">' if robots else f'<link rel="canonical" href="https://rainingcad.com{path}">')
        + f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">' + (f'<meta property="og:image" content="https://rainingcad.com{og}">' if og else '')
        + '<link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/menu.css">\n<style>' + _css + EXTRA + '</style></head><body>' + _nav + body + _foot.replace('</body>', js + '<script src="/menu.js" defer></script></body>'))
CATALOG = [{'id': b['key'], 'book': b['id'], 'title': b['title'], 'url': f'/inside/{b["id"]}/'} for b in BOOKS]

# ---- the code pages
write('/unlock/', 'Open the full book | Raining Cats & Dogs', 'Enter your access code to read the whole book.',
      '<div id="rc-app" class="rc" aria-live="polite"><p>Loading…</p></div>', {'page': 'unlock', 'books': CATALOG, 'buy': {b['key']: b['links'] for b in BOOKS}}, robots='noindex')
write('/redeem/', 'Have an access code? | Raining Cats & Dogs', 'Enter your access code to read Raining Cats & Dogs books online.',
      '<div id="rc-app" class="rc" aria-live="polite"><p>Loading…</p></div>', {'page': 'redeem', 'books': CATALOG})
write('/admin/', 'Codes admin | Raining Cats & Dogs', 'Access codes.', '<div id="rc-app" class="rc" aria-live="polite"><p>Loading…</p></div>', {'page': 'admin', 'books': CATALOG}, robots='noindex,nofollow')

# ---- Read inside
gate = {}
for b in BOOKS:
    f = os.path.join(T, 'inside', b['id'], 'inside.json')
    if not os.path.exists(f): continue
    I = json.load(open(f, encoding='utf-8')); P = f'/inside/{b["id"]}/'; CH = I['chapters']; NP = sum(len(c['pages']) for c in CH)
    gate[b['key']] = {'re': rf'^/inside/{b["id"]}/(\d+)/', 'free': FREE_IN}
    if os.path.isdir(os.path.join(SITE, 'inside', b['id'])): shutil.rmtree(os.path.join(SITE, 'inside', b['id']))
    lbl = lambda c: 'Opening pages' if c['n'] == 0 else f'Chapter {c["n"]}'
    buy = ''.join(f'<a class="btn" href="{E(u)}" rel="noopener">{E(t)}</a>' for t, u in b['links'])
    code = f'<p class="rc-code">Have an access code? <a href="/unlock/?c={b["key"]}&amp;l=2&amp;next={P}2/">Open the full book</a></p>'
    toc = ''.join(f'<li><a href="{P}{c["n"]}/"><span class="n">{lbl(c)}</span><b>{E(c["name"]) if c["n"] else "Contents and introduction"}</b><span class="pp">{len(c["pages"])} pages</span>'
                  + ('<i class="fr">Free</i>' if c['n'] in FREE_IN else '<i class="lk">Full book</i>') + '</a></li>' for c in CH)
    write(P, f'Read inside {b["title"]} | Raining Cats & Dogs', f'Read the opening pages and the first chapter of {b["title"]} free.',
          f'<div class="rc-in"><img class="cv" src="/books/{b["id"]}/cover.webp" alt="{E(b["title"])} cover" width="220"><div><p class="kick">Read inside</p><h1>{E(b["title"])}</h1>'
          f'<p>{NP} pages. The opening pages and chapter 1 are free to read.</p><div class="btns"><a class="btn main" href="{P}0/">Start reading</a>{buy}</div>{code}</div></div>'
          f'<h2>Contents</h2><ol class="rc-toc">{toc}</ol>', og=f'/books/{b["id"]}/cover.webp')
    for k, c in enumerate(CH):
        d = os.path.join(SITE, 'inside', b['id'], str(c['n'])); os.makedirs(d, exist_ok=True); figs = ''
        for pg in c['pages']:
            src = os.path.join(T, 'inside', b['id'], 'pages', pg); shutil.copy(src, os.path.join(d, pg)); w, h = Image.open(src).size
            figs += f'<figure class="rc-pg"><img src="{P}{c["n"]}/{pg}" alt="Page {int(pg[1:4])}" width="{w}" height="{h}" loading="{"lazy" if figs else "eager"}" draggable="false"></figure>'
        pv = CH[k - 1] if k else None; nx = CH[k + 1] if k + 1 < len(CH) else None
        nav = (f'<a href="{P}{pv["n"]}/"><small>Back</small>{lbl(pv)}</a>' if pv else f'<a href="{P}"><small>Back</small>Contents</a>')
        nav += (f'<a class="nx" href="{P}{nx["n"]}/"><small>Next{" &middot; full book" if nx["n"] not in FREE_IN else ""}</small>{lbl(nx)}: {E(nx["name"])}</a>' if nx else f'<a class="nx" href="/books/{b["id"]}/"><small>The end</small>Get the book</a>')
        end = f'<div class="rc-end"><p>The next chapter is in the full book.</p><div class="btns">{buy}</div>{code}</div>' if nx and nx['n'] not in FREE_IN and c['n'] in FREE_IN else ''
        write(f'{P}{c["n"]}/', f'{b["title"]}: {lbl(c)} | Read inside', f'Read inside {b["title"]}.',
              f'<p class="kick"><a href="{P}">{E(b["title"])}</a> &middot; read inside</p><h1>{lbl(c)}{": " + E(c["name"]) if c["n"] else ""}</h1><div class="rc-pages" oncontextmenu="return false">{figs}</div>{end}<nav class="rc-nav">{nav}</nav>', robots='noindex')

# ---- book quizzes and certificates
for b in BOOKS:
    f = os.path.join(T, 'quiz', b['id'] + '.json')
    if not os.path.exists(f): continue
    Z = json.load(open(f, encoding='utf-8')); P = f'/quiz/{b["id"]}/'
    _src = os.path.join(T, 'quiz', b['id'], 'img'); _dst = os.path.join(SITE, 'quiz', b['id'], 'img')
    if os.path.isdir(_src): shutil.rmtree(_dst, ignore_errors=True); shutil.copytree(_src, _dst)
    data = {'page': 'quiz', 'book': b['id'], 'key': b['key'], 'title': b['title'], 'kind': b['kind'], 'cover': f'/books/{b["id"]}/cover.webp', 'cert': Z.get('cert') or b['cert'], 'pass': Z.get('pass', 70),
            'rounds': Z['rounds'], 'links': b['links'], 'inside': f'/inside/{b["id"]}/' if b['key'] in gate else ''}
    write(P, f'The {b["title"]} Quiz | Raining Cats & Dogs', Z['blurb'], '<div id="rc-app" class="rc rc-quiz" aria-live="polite"><p>Loading…</p></div>', data, og=f'/books/{b["id"]}/cover.webp')
    write(P + 'certificate/', f'A {(Z.get("cert") or b["cert"])["title"]} certificate | Raining Cats & Dogs', f'Certified by the {b["title"]} quiz. Take it yourself.', '<div id="rc-app" class="rc" aria-live="polite"><p>Loading…</p></div>',
          dict(data, page='certview'), og=f'/books/{b["id"]}/cover.webp')
json.dump(gate, open(os.path.join(SITE, 'gate.json'), 'w'))
# Read inside and quiz buttons on each book's own page (hand-made pages: the line between the markers is replaced on every build)
for b in BOOKS:
    f = os.path.join(SITE, 'books', b['id'], 'index.html')
    if not os.path.exists(f) or b['key'] not in gate: continue
    h = open(f, encoding='utf-8').read(); h = re.sub(r'<!--rc-in-->.*?<!--/rc-in-->', '', h, flags=re.S)
    row = (f'<!--rc-in--><div class="btns"><a class="btn" href="/inside/{b["id"]}/">Read inside</a>'
           + (f'<a class="btn" href="/quiz/{b["id"]}/">Take the quiz</a>' if os.path.exists(os.path.join(T, 'quiz', b['id'] + '.json')) else '') + '</div><!--/rc-in-->')
    i = h.find('<div class="btns">')
    if i < 0: continue
    j = h.find('</div>', i) + 6
    open(f, 'w', encoding='utf-8').write(h[:j] + row + h[j:])
print('built: code pages,', len(gate), 'books inside,', sum(os.path.exists(os.path.join(T, 'quiz', b['id'] + '.json')) for b in BOOKS), 'quizzes')
