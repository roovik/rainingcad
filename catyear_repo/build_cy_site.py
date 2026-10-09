#!/usr/bin/env python3
"""Build site/CY2027 from weeks/*.json and the supplied PNGs. Usage: build_cy_site.py PNGROOT SITEDIR"""
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
    h=h.replace('<a href="/DY2027/">DY2027</a>','<a href="/DY2027/">DY2027</a><a href="/CY2027/">CY2027</a>')
    return h
TOPBAR='<div class="wrap"><div class="top"><a class="mk" href="/" aria-label="Raining Cats &amp; Dogs home"><img src="/img/rcd-mark-96.webp" srcset="/img/rcd-mark-96.webp 1x,/img/rcd-mark-192.webp 2x" width="48" height="31" alt="Raining Cats &amp; Dogs"></a><a href="/CY2027/">Cat Year 2027 &middot; Every Day a Cat</a></div>\n'
def fix_script(s):
    s=s.replace("dy27:","cy27:").replace("MY DOG YEAR 2027 NOTES","MY CAT YEAR 2027 NOTES").replace("my-dog-year-notes","my-cat-year-notes")
    s=s.replace("Dog Year 2027 &middot; Every Day Has Its Dog","Cat Year 2027 &middot; Every Day Has Its Cat")
    return s
def md(d): return d.strftime("%b ")+str(d.day)
def mdl(d): return d.strftime("%a, ").replace("Sun","Sunday").replace("Mon","Monday").replace("Tue","Tuesday").replace("Wed","Wednesday").replace("Thu","Thursday").replace("Fri","Friday").replace("Sat","Saturday")+md(d)
def save(img,path,size=None,q=80):
    if size: img=img.resize(size,Image.LANCZOS)
    img.convert('RGB').save(path,'WEBP',quality=q,method=6)
weeks=[json.load(open(f,encoding='utf-8')) for f in sorted(glob.glob('weeks/week*.json'))]
start=datetime.date(2027,1,3)
hW,qW,tW,fW=split(tpl_week); hD,qD,tD,fD=split(tpl_day)
os.makedirs(OUT,exist_ok=True)
cards=[]
for w in weeks:
    n=w['num']; wd=f"{OUT}/{n}"; os.makedirs(wd,exist_ok=True)
    d0=start+datetime.timedelta(days=7*(n-1)); d6=d0+datetime.timedelta(days=6)
    src=glob.glob(f"{PNG}/**/w{n:02d}_*",recursive=True)
    def find(k): 
        m=[p for p in src if f"_{k}_" in os.path.basename(p)]; assert len(m)==1,(k,m); return m[0]
    save(Image.open(find('hero')),f"{wd}/hero.webp",(1086,1448))
    for i,dn in enumerate(DAYS+['lastwalk'],1):
        im=Image.open(find(dn))
        save(im,f"{wd}/{i}.webp",(1086,1448)); save(im,f"{wd}/t{i}.webp",(480,640),75)
    B=w['breed']; B_e=esc(B)
    url=f"{BASE}/CY2027/{n}/"
    # week page
    h=fix_head(hW,f"{B} · Week {n} · Cat Year 2027",w['positioning'],url,f"{url}hero.webp")
    story=''.join(f"<p>{esc(curly(p))}</p>" for p in w['story'])
    facts=''.join(f"<div><dt>{esc(a)}</dt><dd>{esc(curly(b))}</dd></div>" for a,b in w['glance'])
    blks=''.join(f"<div class=blk><h3>{esc(a)}</h3><p>{esc(curly(b))}</p></div>" for a,b in w['fblocks'])
    rank=f"<div class=rank><b>{w['rank_num']}</b><span>{esc(w['rank_cap'])} &middot; {esc(w['season_line'])}</span></div>"
    cap=f"<p class=cap>{esc(curly(w.get('cap','')))}</p>" if w.get('cap') else ""
    thumbs=''.join(f'<a href="/CY2027/{n}/{i}/"><img loading=lazy src="/CY2027/{n}/t{i}.webp" alt="{attr(B)} on {dn}"><b>{dn}</b><small>{md(d0+datetime.timedelta(days=i-1))}</small></a>' for i,dn in enumerate(["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],1))
    thumbs+=f'<a href="/CY2027/{n}/8/"><img loading=lazy src="/CY2027/{n}/t8.webp" alt="Last walk of the week"><b>Last Walk</b><small>Week close</small></a>'
    body=(TOPBAR+f'<div class=kick>Week {n} &middot; {md(d0)} &ndash; {md(d6)}</div>\n<h1>{B_e}</h1><p class=pos>{esc(curly(w["positioning"]))}</p>\n'
      f'<img class=big src="/CY2027/{n}/hero.webp" alt="{attr(B)}">\n<div class=story style="margin-top:28px">{story}</div>\n'
      f'<div class=facts>{rank}{cap}<dl>{facts}</dl>{blks}</div>\n<div class=kick>The week</div><div class=days>{thumbs}</div>\n')
    open(f"{wd}/index.html","w",encoding='utf-8').write(h+body+qW+qr(url)+tW+fix_script(fW))
    # day pages
    for i in range(1,9):
        durl=f"{url}{i}/"
        if i<=7:
            day,beat,text=w['days'][i-1]; dd=d0+datetime.timedelta(days=i-1)
            title=f"{mdl(dd)} · {B} · Cat Year 2027"; desc=text
            kick=f"Week {n} &middot; {mdl(dd)}"; main=f'<p class=daytxt>{esc(curly(text))}</p>'; dt=mdl(dd)
            prev=f'<a href="/CY2027/{n}/{i-1 if i>1 else ""}">&larr; {"Previous" if i>1 else "Week %d"%n}</a>'.replace('/"','/"')
            prev=f'<a href="/CY2027/{n}/{i-1}/">&larr; Previous</a>' if i>1 else f'<a href="/CY2027/{n}/">&larr; Week {n}</a>'
            nxt=f'<a href="/CY2027/{n}/{i+1}/">Next &rarr;</a>'
        else:
            lead,rest=w['last_walk'].split("\n",1)
            title=f"Last Walk · {B} · Cat Year 2027"; desc=lead
            kick=f"Week {n} &middot; Last Walk of the Week"
            main=f'<div class=lw><p class=lead>{esc(curly(lead))}</p><p>{esc(curly(rest))}</p></div>'; dt=f"Last Walk of Week {n}"
            prev=f'<a href="/CY2027/{n}/7/">&larr; Previous</a>'; nxt=f'<a href="/CY2027/{n}/">Week {n} &rarr;</a>'
        h=fix_head(hD,title,desc,durl,f"{url}{i}.webp")
        body=(TOPBAR+f'<div class=kick>{kick}</div><img class=big src="/CY2027/{n}/{i}.webp" alt="{attr(B)}">{main}\n'
          f'<div class="notes" id="notes" data-key="{n}/{i}" data-title="{attr(dt)}"><h2>My notes</h2><textarea rows="7" placeholder="What did your cat do today?" aria-label="My notes"></textarea><p class="saved">Notes are saved on this device only.</p><button type="button" class="dl">Download all my notes</button></div>\n'
          f'<div class=nav>{prev}<a href="/CY2027/{n}/">All of week {n}</a>{nxt}</div>\n')
        os.makedirs(f"{wd}/{i}",exist_ok=True)
        open(f"{wd}/{i}/index.html","w",encoding='utf-8').write(h+body+qD+qr(durl)+tD+fix_script(fD))
    cards.append(f'<a href="/CY2027/{n}/"><img loading=lazy src="/CY2027/{n}/hero.webp" alt="{attr(B)}"><small>Week {n}</small><b>{B_e}</b></a>')
# index
hI,qI,tI,fI=split(tpl_idx)
h=fix_head(hI,"Cat Year 2027 · Every Day a Cat","Cat Year 2027. A week with a breed, a page for every day, and a last walk.",f"{BASE}/CY2027/",f"{BASE}/CY2027/1/hero.webp")
body=(TOPBAR+'<div class=kick>2027</div><h1>Cat Year 2027</h1><p class=pos>Every Day a Cat.</p>\n<p>Scan any date in the book and it opens here. Pick a week to meet the breed.</p><div class=grid>'+''.join(cards)+'</div>\n')
open(f"{OUT}/index.html","w",encoding='utf-8').write(h+body+qI+qr(f"{BASE}/CY2027/")+tI+fix_script(fI))
print("built",len(weeks),"weeks")
