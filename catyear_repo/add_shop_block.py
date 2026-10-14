"""Add a 'Shop this breed' and 'In the book' block to each CY2027 week page that has merch. Idempotent. Run from repo root after build_cy_site.py."""
import json,glob,re,html
SITE="site"
CSS='<style id="shopcss">.shop{border-top:3px solid var(--gold);margin:46px 0 0;padding:22px 0 0}.shop h2{font:800 clamp(22px,4vw,28px)/1.1 Spectral,serif;margin:0 0 6px}.shop p.sm{margin:0 0 16px;color:var(--soft);font:italic 400 17px/1.5 Spectral,serif}.shop .g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;align-items:start}.shop .g a{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);padding:8px}.shop .g img{width:100%;height:auto;display:block;background:#fff}.shop .g .bk img{border:1px solid var(--line)}.shop b{display:block;font:800 15px/1.15 Spectral,serif;margin:8px 0 1px}.shop span{display:block;font:11px Hanken,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--soft)}.shop .btns2{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}.shop .btns2 a{font:700 12px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;padding:11px 16px;border:2px solid var(--gold-deep);color:var(--gold-deep)}.shop .btns2 a.m{background:var(--gold-deep);color:#fff}@media(max-width:520px){.shop .g{grid-template-columns:1fr 1fr}.shop .g .bk{grid-column:1/-1;max-width:50%}}</style>'
SL={"norwegian-forest-cat":"VIKING QUEEN","chartreux":"STRONG SILENT TYPE","turkish-angora":"TURKISH DELIGHT","burmese":"IRON IN SILK","siberian":"COLD? WHAT COLD?","abyssinian":"TOP SHELF ENERGY","devon-rex":"MONKEY IN A CATSUIT","birman":"WHITE GLOVE SERVICE","sphynx":"SKIN IN THE GAME","british-shorthair":"TEDDY BEAR IN TWEED","american-shorthair":"ALL-AMERICAN KITTY"}
n_done=0
for f in sorted(glob.glob("catyear_repo/weeks/week*.json")):
    w=json.load(open(f)); n=w['num']; s=w['slug'].replace('_','-'); b=w['breed']
    if s not in SL: continue
    p=f"{SITE}/CY2027/{n}/index.html"; h=open(p,encoding='utf-8').read()
    h=re.sub(r'<!--shop-->.*?<!--/shop-->','',h,flags=re.S)
    sl=html.escape(SL[s])
    blk=(f'<!--shop--><div class="shop"><h2>Shop the {b}</h2><p class="sm">{sl}. A mug and a tee made for the {b} fan.</p>'
      f'<div class="g"><a href="/merch/cats/{s}/"><img loading="lazy" src="/merch/img/c/{s}-mug-1-c.webp" width="640" height="640" alt="{sl} {b} mug"><b>Mug</b><span>11 oz or 15 oz</span></a>'
      f'<a href="/merch/cats/{s}/"><img loading="lazy" src="/merch/img/c/{s}-tee-1-c.webp" width="640" height="640" alt="{sl} {b} tee"><b>T-shirt</b><span>Photos on the front</span></a>'
      f'<a class="bk" href="/books/cat-breeds/"><img loading="lazy" src="/books/cat-breeds/cover.webp" width="300" height="400" alt="Cat Breeds book cover"><b>Cat Breeds</b><span>{html.escape(w["rank_cap"])}</span></a></div>'
      f'<div class="btns2"><a class="m" href="/merch/cats/{s}/">See the {b} mug and tee</a><a href="/books/cat-breeds/">Read about the {b} in Cat Breeds</a></div></div><!--/shop-->')
    h=re.sub(r'<style id="shopcss">.*?</style>','',h,flags=re.S)
    assert h.count('<div class="qr">')==1
    h=h.replace('<div class="qr">',blk+'\n<div class="qr">',1)
    h=h.replace('</head>',CSS+'</head>',1)
    open(p,'w',encoding='utf-8').write(h); n_done+=1
print("pages",n_done)
