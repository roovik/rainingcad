#!/usr/bin/env python3
"""Build the Cat Year holiday pages (holiday1, holiday2) from xmas/*.json and the courtyard images. Usage: build_cy_holiday.py IMGROOT SITEDIR"""
import json,glob,re,sys,os,html,datetime,io
from PIL import Image
import qrcode,qrcode.image.svg
PNG=sys.argv[1]; SITE=sys.argv[2]
DY=f"{SITE}/DY2027"; OUT=f"{SITE}/CY2027"
BASE="https://rainingcad.com"
DAYS=["sun","mon","tue","wed","thu","fri","sat"]
def esc(s): return html.escape(s,quote=False).replace("'","&rsquo;") if False else html.escape(s,quote=False)
def curly(s): return s.replace("'", "’")
def attr(s): return html.escape(curly(s),quote=True)
def qr(url):
    q=qrcode.QRCode(border=1,error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url);q.make(fit=True)
    img=q.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    s=img.to_string().decode() if hasattr(img,'to_string') else ''
    return re.search(r'<path[^>]*\bd="([^"]+)"',s).group(1)
tpl_week=open(f"{DY}/1/index.html",encoding='utf-8').read()
tpl_day=open(f"{DY}/1/1/index.html",encoding='utf-8').read()
tpl_idx=open(f"{DY}/index.html",encoding='utf-8').read()
def split(t):
    i=t.index('<div class="wrap">'); j=t.index('<div class="qr">'); k=t.index('<div class="foot">')
    head=t[:i]; qrhead=t[j:t.index('<path d="')+9]; tail=t[t.index('" id="qr-path"'):k]
    foot_and_script=t[k:]
    return head,qrhead,tail,foot_and_script
def fix_head(h,title,desc,canon,og):
    h=re.sub(r'<title>.*?</title>',f'<title>{attr(title)}</title>',h)
    h=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{attr(desc)}">',h)
    h=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{canon}">',h)
    h=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{attr(title)}">',h)
    h=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{attr(desc)}">',h)
    h=re.sub(r'<meta property="og:image" content="[^"]*">',f'<meta property="og:image" content="{og}">',h)
    h=h.replace('<span class="q"><a href="/DY2027/" class="on">Dog Year</a><a href="/CY2027/">Cat Year</a></span>','<span class="q"><a href="/DY2027/">Dog Year</a><a href="/CY2027/" class="on">Cat Year</a></span>').replace('<a href="/DY2027/" class="on">Dog Year 2027</a><a href="/CY2027/">Cat Year 2027</a>','<a href="/DY2027/">Dog Year 2027</a><a href="/CY2027/" class="on">Cat Year 2027</a>')
    h=h.replace('<a href="/DY2027/">DY2027</a>','<a href="/DY2027/">DY2027</a><a href="/CY2027/">CY2027</a>')
    return h
TOPBAR='<div class="wrap"><div class="top"><a class="mk" href="/" aria-label="Raining Cats &amp; Dogs home"><img src="/img/rcd-mark-96.webp" srcset="/img/rcd-mark-96.webp 1x,/img/rcd-mark-192.webp 2x" width="48" height="31" alt="Raining Cats &amp; Dogs"></a><a href="/CY2027/">Cat Year 2027 &middot; Every Day Has Its Cat</a></div>\n'
def fix_script(s):
    s=s.replace("dy27:","cy27:").replace("MY DOG YEAR 2027 NOTES","MY CAT YEAR 2027 NOTES").replace("my-dog-year-notes","my-cat-year-notes")
    s=s.replace("Dog Year 2027 &middot; Every Day Has Its Dog","Cat Year 2027 &middot; Every Day Has Its Cat")
    return s
def md(d): return d.strftime("%b ")+str(d.day)
def mdl(d): return d.strftime("%a, ").replace("Sun","Sunday").replace("Mon","Monday").replace("Tue","Tuesday").replace("Wed","Wednesday").replace("Thu","Thursday").replace("Fri","Friday").replace("Sat","Saturday")+md(d)
def save(img,path,size=None,q=80):
    if size: img=img.resize(size,Image.LANCZOS)
    img.convert('RGB').save(path,'WEBP',quality=q,method=6)
hW,qW,tW,fW=split(tpl_week); hD,qD,tD,fD=split(tpl_day)
IMG=PNG
# part -> start date, hero file, the 8 slot files (7 days plus last walk), alternates for the last walk
PARTS={
 'holiday1':dict(json='xmas/week_m1_twelve_cats_part1.json',start=datetime.date(2026,12,20),hero='day07.png',
   slots=['day01.png','day02.png','day03.png','day04.png','day05.png','day06.png','day07.png','lastwalk1.png|day07_alt1.png']),
 'holiday2':dict(json='xmas/week_00_twelve_cats_part2.json',start=datetime.date(2026,12,27),hero='day12.png',
   slots=['day08.png','day09.png','day10.png','day11.png','day12.png','N3.png','N4.png','N5.png|day12_alt1.png']),
}
def pick(spec):
    for f in spec.split('|'):
        p=os.path.join(IMG,f)
        if os.path.exists(p): return p
    return None
built=[]
for slug,P in PARTS.items():
    w=json.load(open(P['json'],encoding='utf-8'))
    files=[pick(s) for s in P['slots']]; hero=pick(P['hero'])
    if hero is None or any(f is None for f in files):
        print("SKIP",slug,"missing:",[s for s,f in zip(P['slots'],files) if f is None]); continue
    wd=f"{OUT}/{slug}"; os.makedirs(wd,exist_ok=True)
    d0=P['start']; d6=d0+datetime.timedelta(days=6)
    save(Image.open(hero),f"{wd}/hero.webp",(1086,1448))
    for i,f in enumerate(files,1):
        im=Image.open(f); save(im,f"{wd}/{i}.webp",(1086,1448)); save(im,f"{wd}/t{i}.webp",(480,640),75)
    # optional close-ups: closeNN.png where NN is the carol day number of that slot
    cl0=1 if slug=='holiday1' else 8
    closes={}
    for i in range(1,8):
        cf=pick(f"close{cl0+i-1:02d}.png")
        if cf and (slug=='holiday1' or i<=5):
            im_c=Image.open(cf); save(im_c,f"{wd}/c{i}.webp",(1086,1448)); save(im_c,f"{wd}/ct{i}.webp",(480,640),75); closes[i]=True
    hc=pick('close07.png' if slug=='holiday1' else 'close12.png')
    if hc: save(Image.open(hc),f"{wd}/hero.webp",(1086,1448))
    base=pick('day00_base.png')
    if base and closes: save(Image.open(base),f"{wd}/e.webp",(1086,1448))
    B=' '.join(w['name_lines']); B_e=esc(' '.join(w['name_lines'])); title_b=f"{B}, {md(d0)} to {md(d6)}"
    url=f"{BASE}/CY2027/{slug}/"
    h=fix_head(hW,f"{title_b} · Holiday Season · Cat Year 2027",w['positioning'],url,f"{url}hero.webp")
    story=''.join(f"<p>{esc(curly(p))}</p>" for p in w['story'])
    facts=''.join(f"<div><dt>{esc(a)}</dt><dd>{esc(curly(b))}</dd></div>" for a,b in w['glance'])
    blks=''.join(f"<div class=blk><h3>{esc(a)}</h3><p>{esc(curly(b))}</p></div>" for a,b in w['fblocks'])
    rank=f"<div class=rank><b>{w['rank_num']}</b><span>{esc(w['rank_cap'])} &middot; {esc(w['season_line'])}</span></div>"
    names=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    thumbs=''.join(f'<a href="/CY2027/{slug}/{i}/"><img loading=lazy src="/CY2027/{slug}/{'ct' if i in closes else 't'}{i}.webp" alt="{attr(B)}, {dn}"><b>{dn}</b><small>{md(d0+datetime.timedelta(days=i-1))}</small></a>' for i,dn in enumerate(names,1))
    thumbs+=f'<a href="/CY2027/{slug}/8/"><img loading=lazy src="/CY2027/{slug}/t8.webp" alt="Last walk of the holiday week"><b>Last Walk</b><small>Week close</small></a>'
    body=(TOPBAR+f'<div class=kick>{esc(w["kicker"])} &middot; {md(d0)} &ndash; {md(d6)}</div>\n<h1>{B_e}</h1><p class=pos>{esc(curly(w["positioning"]))}</p>\n'
      f'<p><a href="/CY2027/twelve-cats/" style="font:700 12px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase">See all twelve days in one place &rarr;</a></p>\n<img class=big src="/CY2027/{slug}/hero.webp" alt="{attr(B)}">\n<div class=story style="margin-top:28px">{story}</div>\n'
      f'<div class=facts>{rank}<dl>{facts}</dl>{blks}</div>\n<div class=kick>The week</div><div class=days>{thumbs}</div>\n')
    open(f"{wd}/index.html","w",encoding='utf-8').write(h+body+qW+qr(url)+tW+fix_script(fW))
    for i in range(1,9):
        durl=f"{url}{i}/"
        if i<=7:
            day,beat,text=w['days'][i-1]; dd=d0+datetime.timedelta(days=i-1)
            title=f"{mdl(dd)} · {B} · Cat Year 2027"; desc=text
            nth=i if slug=='holiday1' else i+7
            ordn=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth","eleventh","twelfth"]
            cap_day=f'</div><div class=kick style="margin-top:2px">The {ordn[nth-1]} day of Christmas' if nth<=12 else ""
            kick=f"{esc(w['kicker'])} &middot; {mdl(dd)}{cap_day}"; main=f'<p class=daytxt>{esc(curly(text))}</p>'; dt=mdl(dd)
            prev=f'<a href="/CY2027/{slug}/{i-1}/">&larr; Previous</a>' if i>1 else f'<a href="/CY2027/{slug}/">&larr; {esc(w["weekhead"])}</a>'
            nxt=f'<a href="/CY2027/{slug}/{i+1}/">Next &rarr;</a>'
        else:
            lead,rest=w['last_walk'].split("\n",1)
            title=f"Last Walk · {B} · Cat Year 2027"; desc=lead
            kick=f"{esc(w['kicker'])} &middot; Last Walk"
            main=f'<div class=lw><p class=lead>{esc(curly(lead))}</p><p>{esc(curly(rest))}</p></div>'; dt=f"Last Walk, {w['weekhead']}"
            prev=f'<a href="/CY2027/{slug}/7/">&larr; Previous</a>'; nxt=f'<a href="/CY2027/{slug}/">{esc(w["weekhead"])} &rarr;</a>'
        h=fix_head(hD,title,desc,durl,f"{url}{i}.webp")
        cap=lambda t: f'<div class=kick style="margin-top:24px">{t}</div>'
        if i in closes:
            media=(f'<img class=big src="/CY2027/{slug}/e.webp" alt="The empty courtyard, before the cats arrive">'
                   +cap('Up close')+f'<img class=big src="/CY2027/{slug}/c{i}.webp" alt="{attr(B)}, up close" loading=lazy>'
                   +cap('The whole courtyard')+f'<img class=big src="/CY2027/{slug}/{i}.webp" alt="{attr(B)}, the whole courtyard" loading=lazy>')
            media=cap('The courtyard, waiting').replace('margin-top:24px','margin-top:0')+media
        else:
            media=f'<img class=big src="/CY2027/{slug}/{i}.webp" alt="{attr(B)}">'
        body=(TOPBAR+f'<div class=kick>{kick}</div>{media}{main}\n'
          f'<div class="notes" id="notes" data-key="{slug}/{i}" data-title="{attr(dt)}"><h2>My Cat-Eared Notes</h2><textarea rows="7" placeholder="What did your cat do today?" aria-label="My Cat-Eared Notes"></textarea><p class="saved">Notes are saved on this device only.</p><button type="button" class="dl">Download all my notes</button></div>\n'
          f'<div class=nav>{prev}<a href="/CY2027/{slug}/">All of this week</a>{nxt}</div>\n')
        os.makedirs(f"{wd}/{i}",exist_ok=True)
        open(f"{wd}/{i}/index.html","w",encoding='utf-8').write(h+body+qD+qr(durl)+tD+fix_script(fD))
    built.append(slug)

# ---- one landing page for the whole twelve-day sequence ----
TWELVE=[("Maine Coon","Maine Coon"),("Siamese","Siamese"),("Manx","Manx"),("Scottish Folds","Scottish Fold"),("Sphynx","Sphynx"),
        ("Bengals","Bengal"),("Korats","Korat"),("Ragdolls","Ragdoll"),("Persians","Persian"),("Munchkins","Munchkin"),("Devon Rex","Devon Rex"),("Abyssinians","Abyssinian")]
if all(os.path.isdir(f"{OUT}/{x}") for x in ('holiday1','holiday2')):
    wd=f"{OUT}/twelve-cats"; os.makedirs(wd,exist_ok=True)
    hc=pick('close12.png')
    if hc: save(Image.open(hc),f"{wd}/hero.webp",(1086,1448))
    url=f"{BASE}/CY2027/twelve-cats/"
    d0=datetime.date(2026,12,20)
    title="The Twelve Cats of Christmas"
    desc="Twelve days. Twelve breeds. Seventy-eight cats. One pear tree."
    h=fix_head(hW,f"{title} · Holiday Season · Cat Year 2027",desc,url,f"{url}hero.webp")
    cards=''; tot=0
    for n,(plural,_b) in enumerate(TWELVE,1):
        tot+=n
        dd=d0+datetime.timedelta(days=n-1)
        part,k=('holiday1',n) if n<=7 else ('holiday2',n-7)
        label=f"{n} {plural}" if n>1 else plural
        cards+=f'<a href="/CY2027/{part}/{k}/"><img loading=lazy src="/CY2027/{part}/ct{k}.webp" alt="Day {n}, {attr(label)}"><b>Day {n}, {esc(plural)}</b><small>{md(dd)} &middot; {tot} in all</small></a>'
    after=''.join(f'<a href="/CY2027/holiday2/{k}/"><img loading=lazy src="/CY2027/holiday2/t{k}.webp" alt="{a}"><b>{a}</b><small>{b}</small></a>' for k,a,b in ((6,"New Year&rsquo;s Day","Fri Jan 1"),(7,"The rescue cat","Sat Jan 2"),(8,"Last Walk","Week close")))
    body=(TOPBAR+'<div class=kick>Holiday Season &middot; Dec 20 &ndash; Jan 2</div>\n<h1>The Twelve Cats of Christmas</h1><p class=pos>Twelve days. Twelve breeds. Seventy-eight cats. One pear tree.</p>\n'
      f'<img class=big src="/CY2027/twelve-cats/hero.webp" alt="Twelve Abyssinians in a pyramid">\n'
      '<div class=story style="margin-top:28px"><p>Every carol has a list. This one has cats. The old song counts twelve days of gifts. Ours counts twelve days of cats in one snowy courtyard, starting on Sunday, December 20. A Maine Coon sits in the pear tree. Every day after that, a bigger group of a new breed joins her, until the courtyard holds all seventy-eight on New Year&rsquo;s Eve.</p><p>The days run in order below. Tap a day for its close-up, its wide view and a place for your notes.</p></div>\n'
      '<div class=kick>The twelve days</div><div class=days>'+cards+'</div>\n'
      '<div class=kick>After the twelfth day</div><div class=days>'+after+'</div>\n'
      '<div class=nav><a href="/CY2027/">&larr; All weeks</a><a href="/CY2027/holiday1/">Dec 20 to 26</a><a href="/CY2027/holiday2/">Dec 27 to Jan 2</a></div>\n')
    open(f"{wd}/index.html","w",encoding='utf-8').write(h+body+qW+qr(url)+tW+fix_script(fW))
    built.append('twelve-cats')
print("built",built)
