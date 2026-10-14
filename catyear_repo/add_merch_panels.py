"""Add merch panels. Idempotent. Run from repo root after the site is built.
 - Cat Year week and day pages (CY2027/N/ and CY2027/N/D/) for breeds with merch: Shop the breed (mug, tee, Cat Breeds book)
 - Dog Year week and day pages for the 12 breeds with merch: same, with the Dog Breeds book
 - Book pages and their sample (look inside) pages: a Merch strip
"""
import json,glob,re,html,os
SITE="site"
CSS='<style id="shopcss">.shop{border-top:3px solid var(--gold);margin:46px 0 0;padding:22px 0 0}.shop h2{font:800 clamp(22px,4vw,28px)/1.1 Spectral,serif;margin:0 0 6px}.shop p.sm{margin:0 0 16px;color:var(--soft);font:italic 400 17px/1.5 Spectral,serif}.shop .g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start}.shop .g a{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);padding:8px}.shop .g img{width:100%;height:auto;display:block;background:#fff}.shop .g a:not(.bk) img{aspect-ratio:1/1;object-fit:contain}.shop .g .bk img{border:1px solid var(--line)}.shop b{display:block;font:800 15px/1.15 Spectral,serif;margin:8px 0 1px}.shop span{display:block;font:11px Hanken,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}.shop .btns2{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}.shop .btns2 a{font:700 12px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;padding:11px 16px;border:2px solid var(--gold-deep);color:var(--gold-deep)}.shop .btns2 a.m{background:var(--gold-deep);color:#fff}@media(max-width:520px){.shop .g{grid-template-columns:1fr 1fr}.shop .g .bk{grid-column:1/-1;max-width:50%}}</style>'
MPCSS='<style id="mpcss">.mp{border-top:3px solid #B0822B;margin:46px 0 0;padding:22px 0 8px}.mp h2{font:800 clamp(22px,4vw,28px)/1.1 Spectral,Georgia,serif;margin:0 0 6px}.mp p.sm{margin:0 0 16px;color:#6F6F74;font:italic 400 17px/1.5 Spectral,Georgia,serif}.mp .g{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}.mp .g a{display:block;text-decoration:none;color:#2A2A2D;background:#fff;border:1px solid rgba(42,42,45,.16);padding:8px}.mp .g img{width:100%;height:auto;aspect-ratio:1/1;object-fit:contain;display:block;background:#fff}.mp .g b{display:block;font:800 15px/1.15 Spectral,Georgia,serif;margin:8px 0 1px}.mp .g span{display:block;font:11px Hanken,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#6F6F74}.mp .btns2{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}.mp .btns2 a{font:700 12px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;padding:11px 16px;border:2px solid #876217;color:#876217}.mp .btns2 a.m{background:#876217;color:#fff}</style>'
E=html.escape
def put(path,blk,anchor,css=CSS,cid='shopcss',mark='shop'):
    h=open(path,encoding='utf-8').read()
    h=re.sub(rf'<!--{mark}-->.*?<!--/{mark}-->','',h,flags=re.S)
    h=re.sub(rf'<style id="{cid}">.*?</style>','',h,flags=re.S)
    if h.count(anchor)!=1: return False
    h=h.replace(anchor,f'<!--{mark}-->{blk}<!--/{mark}-->\n'+anchor,1).replace('</head>',css+'</head>',1)
    open(path,'w',encoding='utf-8').write(h); return True
def breed_block(name,url,slogan,mug,tee,book_url,book_cover,book_title,rank):
    sl=E(slogan)
    return (f'<div class="shop"><h2>Shop the {E(name)}</h2><p class="sm">{sl}. A mug and a tee made for the {E(name)} fan.</p>'
      f'<div class="g"><a href="{url}"><img loading="lazy" src="{mug}" width="640" height="640" alt="{sl} {E(name)} mug"><b>Mug</b><span>11 oz or 15 oz</span></a>'
      f'<a href="{url}"><img loading="lazy" src="{tee}" width="640" height="640" alt="{sl} {E(name)} tee"><b>T-shirt</b><span>Photos on the front</span></a>'
      f'<a class="bk" href="{book_url}"><img loading="lazy" src="{book_cover}" width="300" height="400" alt="{E(book_title)} book cover"><b>{E(book_title)}</b><span>{E(rank)}</span></a></div>'
      f'<div class="btns2"><a class="m" href="{url}">See the {E(name)} mug and tee</a><a href="{book_url}">Read about the {E(name)} in {E(book_title)}</a></div></div>')
n=0
# ---- cats
SL={"norwegian-forest-cat":"VIKING QUEEN","chartreux":"STRONG SILENT TYPE","turkish-angora":"TURKISH DELIGHT","burmese":"IRON IN SILK","siberian":"COLD? WHAT COLD?","abyssinian":"TOP SHELF ENERGY","devon-rex":"MONKEY IN A CATSUIT","birman":"WHITE GLOVE SERVICE","sphynx":"SKIN IN THE GAME","british-shorthair":"TEDDY BEAR IN TWEED","american-shorthair":"ALL-AMERICAN KITTY"}
for f in sorted(glob.glob("catyear_repo/weeks/week*.json")):
    w=json.load(open(f)); k=w['num']; s=w['slug'].replace('_','-')
    if s not in SL: continue
    blk=breed_block(w['breed'],f"/merch/cats/{s}/",SL[s],f"/merch/img/c/{s}-mug-1-c.webp",f"/merch/img/c/{s}-tee-1-c.webp","/books/cat-breeds/","/books/cat-breeds/cover.webp","Cat Breeds",w['rank_cap'])
    for p in [f"{SITE}/CY2027/{k}/index.html"]+[f"{SITE}/CY2027/{k}/{d}/index.html" for d in range(1,9)]:
        if os.path.exists(p) and put(p,blk,'<div class="qr">'): n+=1
print("cat pages",n); n=0
# ---- dogs
for f in sorted(glob.glob(f"{SITE}/merch/dogs/*/index.html")):
    h=open(f,encoding='utf-8').read(); s=f.split('/')[-2]
    name=re.search(r'<h1>(.*?)</h1>',h).group(1); slg=re.search(r'<h2><a href="[^"]*">(.*?)</a></h2>',h).group(1)
    wk=re.search(r'href="/DY2027/(\d+)/"',h).group(1)
    bp=re.search(r'<div class="bp">.*?<div class="cta">',h,re.S).group(0); im=re.findall(r'<img src="([^"]+)"',bp)
    d=open(f"{SITE}/DY2027/{wk}/index.html",encoding='utf-8').read(); rn=re.search(r'<div class=rank><b>(\d+)</b>',d).group(1)
    blk=breed_block(name,f"/merch/dogs/{s}/",html.unescape(slg),im[0],im[1],"/books/dog-breeds/","/books/dog-breeds/cover.webp","Dog Breeds",f"No. {rn} of 50")
    for p in [f"{SITE}/DY2027/{wk}/index.html"]+[f"{SITE}/DY2027/{wk}/{x}/index.html" for x in range(1,9)]:
        if os.path.exists(p) and put(p,blk,'<div class="qr">'): n+=1
print("dog pages",n); n=0
# ---- books
def tile(href,img,title,sub): return f'<a href="{href}"><img loading="lazy" src="{img}" width="400" height="400" alt="{E(title)}"><b>{E(title)}</b><span>{sub}</span></a>'
CAT=[("norwegian-forest-cat","Norwegian Forest Cat","tee"),("chartreux","Chartreux","mug"),("british-shorthair","British Shorthair","tee"),("siberian","Siberian","mug")]
DOG=[("golden-retriever","Golden Retriever","GoldenRetriever","tee"),("beagle","Beagle","Beagle","mug"),("french-bulldog","French Bulldog","FrenchBulldog","tee"),("dachshund","Dachshund","Dachshund","mug")]
def kind(k): return "T-shirt" if k=="tee" else "Mug"
PANELS={
 "cat-breeds":("Cat breed mugs and tees","Each breed has a mug and a tee. Slogans, photos and a little attitude.",[tile(f"/merch/cats/{s}/",f"/merch/img/c/{s}-{k}-1-c.webp",nm,kind(k)) for s,nm,k in CAT],[("/merch/cats/","See all cat merch",1),("/CY2027/","Cat Year 2027",0)]),
 "dog-breeds":("Dog breed mugs and tees","Each breed has a mug and a tee. Slogans, photos and a little attitude.",[tile(f"/merch/dogs/{s}/",f"/merch/img/m/{p}-{k}-1-c.webp",nm,kind(k)) for s,nm,p,k in DOG],[("/merch/dogs/","See all dog merch",1),("/DY2027/","Dog Year 2027",0)]),
 "the-cats-pajamas":("Cat idiom mugs and tees","Cat sayings on mugs and tees.",[tile("/merch/#idioms",f"/merch/img/idiom-{a}.webp",t,k) for a,t,k in [("crazy-cat-lady-tee","Crazy Cat Lady","T-shirt"),("cool-cat-tee","Cool Cat","T-shirt"),("cat-nap-mug","Cat Nap","Mug"),("catnip-mug","Catnip","Mug")]],[("/merch/#idioms","See all idiom merch",1)]),
 "every-dog-has-his-day":("Dog idiom mugs and tees","Dog sayings on mugs and tees.",[tile("/merch/#idioms",f"/merch/img/idiom-{a}.webp",t,k) for a,t,k in [("top-dog-tee","Top Dog","T-shirt"),("top-dog-mug","Top Dog","Mug"),("in-the-doghouse-tee","In the Doghouse","T-shirt"),("hot-dog-mug","Hot Dog","Mug")]],[("/merch/#idioms","See all idiom merch",1)]),
}
for b,(t,sub,tiles,btns) in PANELS.items():
    blk=f'<div class="mp"><h2>{E(t)}</h2><p class="sm">{E(sub)}</p><div class="g">{"".join(tiles)}</div><div class="btns2">'+''.join(f'<a{" class=m" if m else ""} href="{h}">{E(x)}</a>' for h,x,m in btns)+'</div></div>'
    for p in [f"{SITE}/books/{b}/index.html"]+glob.glob(f"{SITE}/books/{b}/sample/**/index.html",recursive=True):
        if put(p,blk,'<div class="foot">',MPCSS,'mpcss','mp'): n+=1
        else: print("skipped",p)
print("book pages",n)
# ---- all four books at the very bottom of every page that has a merch panel
BKCSS='<style id="bkcss">.bks{border-top:3px solid #B0822B;margin:46px 0 0;padding:22px 0 8px}.bks h2{font:800 clamp(22px,4vw,28px)/1.1 Spectral,Georgia,serif;margin:0 0 14px}.bks .g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}.bks .g a{display:block;text-decoration:none;color:#2A2A2D}.bks .g img{width:100%;height:auto;display:block;border:1px solid rgba(42,42,45,.16);box-shadow:0 8px 20px rgba(0,0,0,.14);background:#e9e7df}.bks .g b{display:block;font:800 15px/1.15 Spectral,Georgia,serif;margin:10px 0 1px}.bks .g span{display:block;font:11px Hanken,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#6F6F74}.bks .g.n3{grid-template-columns:repeat(3,minmax(0,1fr))}@media(max-width:560px){.bks .g,.bks .g.n3{grid-template-columns:1fr 1fr}}</style>'
BOOKS=[("cat-breeds","Cat Breeds","Breed guide"),("dog-breeds","Dog Breeds","Breed guide"),("every-dog-has-his-day","Every Dog Has His Day","Idiom book"),("the-cats-pajamas","The Cat&#x27;s Pajamas","Idiom book")]
def strip(cur=None):
    bs=[b for b in BOOKS if b[0]!=cur]
    return f'<div class="bks"><h2>{"More Books" if cur else "The Books"}</h2><div class="g n{len(bs)}">'+''.join(f'<a href="/books/{s}/"><img loading="lazy" src="/books/{s}/cover.webp" width="300" height="400" alt="{t} cover"><b>{t}</b><span>{sub}</span></a>' for s,t,sub in bs)+'</div></div>'
n=0
for p in glob.glob(f"{SITE}/**/index.html",recursive=True):
    h=open(p,encoding='utf-8').read()
    if '<!--shop-->' in h or '<!--mp-->' in h:
        m=re.match(rf'{SITE}/books/([^/]+)/',p)
        cur=m.group(1) if m and m.group(1) in [b[0] for b in BOOKS] else None
        if put(p,strip(cur),'<div class="foot">',BKCSS,'bkcss','bks'): n+=1
        else: print("skipped",p)
print("books strip pages",n)
