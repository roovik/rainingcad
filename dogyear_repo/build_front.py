import base64,io,sys,os
from PIL import Image
from playwright.sync_api import sync_playwright
SP='npm/node_modules/@fontsource/spectral/files/'
HG='npm/node_modules/@fontsource-variable/hanken-grotesk/files/hanken-grotesk-latin-wght-normal.woff2'
b64=lambda p:base64.b64encode(open(p,'rb').read()).decode()
def face(fam,st,w,p): return f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{w};src:url(data:font/woff2;base64,{b64(p)}) format('woff2');font-display:block}}"
fonts="\n".join([face('Spectral','normal',w,f'{SP}spectral-latin-{w}-normal.woff2') for w in (400,600,700,800)]+[face('Spectral','italic',w,f'{SP}spectral-latin-{w}-italic.woff2') for w in (400,600)]+[face('Hanken Grotesk','normal','100 900',HG)])
maxw=int(sys.argv[2]) if len(sys.argv)>2 else 0
im=Image.open('winter.png').convert('RGB')
if maxw and im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
bb=io.BytesIO(); im.save(bb,'JPEG',quality=92 if not maxw else 76); winter='data:image/jpeg;base64,'+base64.b64encode(bb.getvalue()).decode()
CSS=open('house.css').read()
intro=["Dogs do not keep calendars. They keep appointments. Breakfast, the morning walk, the sound of a key in the door at six o’clock. A dog’s year is made of small, faithful hours, and none of them is wasted.",
"This book follows that example. Dog Year 2027 gives every week its own breed, fifty in all, from giants of the mountain passes to lapdogs of royal courts. Each week opens with a portrait, then a page of history, character, and fact. Seven short thoughts follow, one for each day, with room beside every one to write down your own. A Last Walk closes each week.",
"The year moves through four seasons, and so does the book. Each chapter has its own light, its own weather, and its own Dog of the season. Special weeks open and close the calendar, to welcome the year in and to see it out.",
"Every date carries a small photograph and a QR code. Scan it, and that day opens online at rainingcad.com, where the dog of the week is waiting with more.",
"Turn the page. The first dog is already at the door."]
seasons=[("Winter","Weeks 1&ndash;11","Jan 3 &ndash; Mar 20","11 breeds"),("Spring","Weeks 12&ndash;24","Mar 21 &ndash; Jun 19","13 breeds"),("Summer","Weeks 25&ndash;37","Jun 20 &ndash; Sep 18","13 breeds"),("Fall","Weeks 38&ndash;50","Sep 19 &ndash; Dec 18","13 breeds")]
sc="".join(f'<div class="sn"><div class="nm">{n}</div><div class="wk">{w}</div><div class="dt">{d}</div><div class="ct">{c}</div></div>' for n,w,d,c in seasons)
wint=["For a dog, winter arrives as news. The air has a new smell. The ground makes a new sound. Overnight, the familiar yard becomes a place worth investigating again, and a dog who was tired of the same old walk is suddenly a puppy.",
"Some dogs were built for this. The Saint Bernard, the Newfoundland, and the Bernese Mountain Dog wear coats that laugh at the cold. The Siberian Husky and the Akita run happiest when the temperature falls. For them, snow is not weather. It is home.",
"Others have different plans. The Maltese, the Pomeranian, and the Cavalier would like a sweater, a lap, and a fire. The Bulldog would like all three, plus a ruling on whether the walk is strictly necessary. Winter, it turns out, has a place for every dog.",
"For those who love them, winter is the season of closeness. The days shorten. The evenings lengthen. The couch fills up. In the dark months a dog asks for nothing but company, and offers everything in return. Warmth against your feet. A head on your knee. A reason to go outside when you would rather not, and a reason to come back in, glad of home.",
"Every cold morning with a dog holds a small lesson. Put on the coat. Step into the weather. Notice the snow. Then come home to the fire together.",
"These are the Dogs of Winter 2027. Eleven weeks. Eleven breeds. 99 new friends. And one long, bright season for them to warm your heart."]
P=lambda L:"".join(f"<p>{t}</p>" for t in L)
folio='<div class="folio"><span>A Dog Year &middot; Every Day Has Its Dog</span><span class="pageno">[ # ]</span></div>'
html=f'''<!doctype html><meta charset=utf-8><style>{fonts}\n{CSS}
@page{{size:8in 10in;margin:0}} body{{margin:0}} .page{{page-break-after:always}}
.fm .pad{{padding:.9in .95in}}
.fm .kicker{{margin-bottom:16px}}
.fm h1{{font-family:Spectral,serif;font-weight:800;font-size:50px;line-height:.98;margin:0;letter-spacing:-.01em}}
.fm .pos{{font-style:italic;font-weight:600;font-size:20px;color:var(--gold-deep);margin:14px 0 22px;line-height:1.3}}
.fm .rule{{width:100%;border-top:3px solid var(--gold);margin:0 0 22px}}
.fm .body{{font-size:17px;line-height:1.62;text-align:justify;hyphens:auto}}
.fm .body p{{margin:0 0 11px}}
.fm .body p:first-child:first-letter{{font-weight:800;float:left;font-size:64pt;line-height:.66;padding:8px 12px 0 0;color:var(--gold)}}
.fm .body p:last-child{{font-style:italic;font-weight:600;color:var(--gold-deep);margin-top:16px}}
.seasons{{position:absolute;left:.95in;right:.95in;bottom:1.05in;display:grid;grid-template-columns:repeat(4,1fr);gap:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.sn{{padding:14px 12px;border-left:1px solid var(--line)}} .sn:first-child{{border-left:0;padding-left:0}}
.sn .nm{{font-weight:800;font-size:22px}} .sn .wk{{font-family:"Hanken Grotesk";font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-deep);margin-top:6px}}
.sn .dt,.sn .ct{{font-family:"Hanken Grotesk";font-size:10.5px;color:var(--ink-soft);margin-top:4px;letter-spacing:.04em}}
.hero.w .holder{{inset:.75in}}
</style><div class=deck>
<section class="page fm"><div class=pad><div class=kicker>Introduction</div><h1>Every Day a Dog</h1><p class=pos>A year lived at the speed of a wagging tail.</p><div class=rule></div><div class=body>{P(intro)}</div></div>
<div class=seasons>{sc}</div>{folio}</section>
<section class="page hero w"><div class=holder><img src="{winter}" alt="The Dogs of Winter"></div></section>
<section class="page fm"><div class=pad><div class=kicker>Winter &middot; Weeks 1&ndash;11</div><h1>What Winter Means</h1><p class=pos>To dogs, and to those who love them.</p><div class=rule></div><div class=body>{P(wint)}</div></div>{folio}</section>
</div>'''
open('front.html','w').write(html)
with sync_playwright() as p:
    br=p.chromium.launch();pg=br.new_page();pg.goto('file://'+os.path.abspath('front.html')+'');pg.wait_for_timeout(600)
    pg.pdf(path=sys.argv[1],width='8in',height='10in',print_background=True);br.close()
