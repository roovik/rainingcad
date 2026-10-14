import os,re,json,sys
from PIL import Image,ImageChops
SRC=sys.argv[1]  # Printify_Mockups_Cats dir
SITE="/home/claude/rainingcad/site"
OUT=SITE+"/merch/img/c"; os.makedirs(OUT,exist_ok=True)
sys.path.insert(0,'catyear_repo')
SL={"norwegian-forest-cat":"VIKING QUEEN","chartreux":"STRONG SILENT TYPE","turkish-angora":"TURKISH DELIGHT","burmese":"IRON IN SILK","siberian":"COLD? WHAT COLD?","abyssinian":"TOP SHELF ENERGY","devon-rex":"MONKEY IN A CATSUIT","birman":"WHITE GLOVE SERVICE","sphynx":"SKIN IN THE GAME","british-shorthair":"TEDDY BEAR IN TWEED","american-shorthair":"ALL-AMERICAN KITTY"}
B=[]
for n in range(1,12):
    import glob
    f=glob.glob(f"catyear_repo/weeks/week{n:02d}_*.json")[0]; d=json.load(open(f))
    B.append((n,d['slug'].replace('_','-'),d['breed']))
def crop(p,size,pad=0.04):
    im=Image.open(p).convert('RGB'); bg=Image.new('RGB',im.size,(255,255,255))
    bb=ImageChops.difference(im,bg).point(lambda v:255 if v>14 else 0).getbbox()
    im=im.crop(bb); s=max(im.size); s=int(s*(1+2*pad))
    c=Image.new('RGB',(s,s),'white'); c.paste(im,((s-im.width)//2,(s-im.height)//2)); return c.resize((size,size),Image.LANCZOS)
for n,s,b in B:
    crop(f"{SRC}/{s}-MUG/01_front.jpg",640).save(f"{OUT}/{s}-mug-1-c.webp",quality=82)
    crop(f"{SRC}/{s}-TEE/01_front.jpg",640).save(f"{OUT}/{s}-tee-1-c.webp",quality=82)
    Image.open(f"{SRC}/{s}-TEE/02_back.jpg").convert('RGB').resize((900,900),Image.LANCZOS).save(f"{OUT}/{s}-tee-2.webp",quality=82)
# templates
dog=open(SITE+"/merch/dogs/beagle/index.html").read()
dogi=open(SITE+"/merch/dogs/index.html").read()
def head(html,title,desc,url,og):
    h=re.sub(r'<title>.*?</title><meta name="description" content=".*?">',f'<title>{title} | Raining Cats &amp; Dogs</title><meta name="description" content="{desc}">',html,1,re.S)
    h=re.sub(r'<link rel="canonical" href=".*?">',f'<link rel="canonical" href="https://rainingcad.com{url}">',h,1)
    h=re.sub(r'<meta property="og:title" content=".*?"><meta property="og:description" content=".*?"><meta property="og:image" content=".*?">',
      f'<meta property="og:title" content="{title} | Raining Cats &amp; Dogs"><meta property="og:description" content="{desc}"><meta property="og:image" content="https://rainingcad.com{og}">',h,1)
    return h
SUB2='<nav class="sub2" aria-label="Merch"><a href="/merch/t-shirts/">T-shirts</a><a href="/merch/mugs/">Mugs</a><a href="/merch/dogs/">Dogs</a><a href="/merch/cats/"%s>Cats</a></nav>'
def sub3(cur):
    return '<nav class="sub3" aria-label="Breeds"><em>Breeds</em>'+''.join(f'<a href="/merch/cats/{s}/"'+(' class=on aria-current=page' if s==cur else '')+f'>{b}</a>' for n,s,b in B)+'</nav>'
SOON='<a class="btn off" href="#">Coming soon on Etsy</a>'
def esc(t): return t.replace('&','&amp;').replace('"','&quot;')
pre=dog[:dog.find('<p class="kick">')]; post=dog[dog.find('<div class="foot">'):]
for n,s,b in B:
    sl=esc(SL[s])
    body=f'<p class="kick">Merch &middot; Cats</p><h1>{b}</h1><p class="lead">A mug and a tee for the {b} fan.</p>'+SUB2%' class=on aria-current=page'+sub3(s)
    body+=f'<div class="bp"><div><h2>{sl}</h2><img src="/merch/img/c/{s}-mug-1-c.webp" width="640" height="640" alt="{sl} {b} mug"></div><div><h2>{sl}</h2><div class="two"><img src="/merch/img/c/{s}-tee-1-c.webp" width="640" height="640" alt="Front of the {b} tee"><img src="/merch/img/c/{s}-tee-2.webp" width="900" height="900" alt="Back of the {b} tee" loading="lazy"></div></div></div>'
    body+=f'<div class="cta">{SOON}<a class="btn" href="/CY2027/{n}/">Meet the {b}</a></div>\n'
    h=head(pre,b,f"{b} mug and tee from Raining Cats &amp; Dogs. Coming soon on Etsy.",f"/merch/cats/{s}/",f"/merch/img/c/{s}-mug-1-c.webp")
    os.makedirs(f"{SITE}/merch/cats/{s}",exist_ok=True)
    open(f"{SITE}/merch/cats/{s}/index.html","w").write(h+body+post)
# index
pre=dogi[:dogi.find('<p class="kick">')]; post=dogi[dogi.find('<div class="foot">'):]
body='<p class="kick">Merch</p><h1>Cats</h1><p class="lead">Pick your breed. Each one has a mug and a tee.</p>'+SUB2%' class=on aria-current=page'+sub3('')
body+='<div class="grid dogs">'+''.join(f'<a class="card" href="/merch/cats/{s}/"><div class="pair"><img src="/merch/img/c/{s}-mug-1-c.webp" width="640" height="640" alt="{esc(SL[s])} {b} mug" loading="lazy"><img src="/merch/img/c/{s}-tee-1-c.webp" width="640" height="640" alt="{esc(SL[s])} {b}" loading="lazy"></div><b>{b}</b><span>{esc(SL[s])}</span><i>View</i></a>' for n,s,b in B)+'</div>\n'
h=head(pre,"Cats","Cat breed mugs and tees by breed from Raining Cats &amp; Dogs. Coming soon on Etsy.","/merch/cats/","/merch/img/c/norwegian-forest-cat-mug-1-c.webp")
open(f"{SITE}/merch/cats/index.html","w").write(h+body+post)
print("ok")
