#!/usr/bin/env python3
"""Cat Year 2027, full-year print interior in 4 parts (so each part stays small enough to move around)."""
import os, sys, re, json, base64, glob, datetime
sys.path.insert(0, "/tmp/ce/tools/print_pipeline"); sys.path.insert(0, "/tmp/ce")
import make_week as mw
from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from season_cfg_cat import CFG, SEASONS_STRIP, ESSAYS

ROOT="/tmp/ce"; IMG=f"{ROOT}/img"; OUTDIR=sys.argv[1]; os.makedirs(OUTDIR,exist_ok=True)
ORDER=["winter","spring","summer","fall"]
FOLIO='<div class="folio"><span>A Cat Year &middot; Every Day Has Its Cat</span><span class="pageno">[ # ]</span></div>'
P=lambda ps:"".join(f"<p>{t}</p>" for t in ps)
b64=lambda p:"data:image/jpeg;base64,"+base64.b64encode(open(p,"rb").read()).decode()
EXTRA_CSS=open('/tmp/ce/extra.css').read()+r"""
.toc .pad{padding:.85in .95in}
.toc h1{font-size:42px}
.toc .sh{font-family:"Hanken Grotesk",sans-serif;font-weight:700;font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold-deep);margin:14px 0 4px;border-bottom:2px solid var(--gold);padding-bottom:4px;display:flex;justify-content:space-between}
.toc .r{display:flex;align-items:baseline;gap:8px;font-size:13px;line-height:1;padding:4.6px 0}
.toc .r .w{font-family:"Hanken Grotesk",sans-serif;font-weight:600;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft);width:48px}
.toc .r .b{font-weight:600}
.toc .r .l{flex:1;border-bottom:1px dotted rgba(42,42,45,.35);transform:translateY(-3px)}
.toc .r .d{font-family:"Hanken Grotesk",sans-serif;font-size:9px;letter-spacing:.1em;color:var(--ink-soft);text-transform:uppercase}
.toc .r .p{width:26px;text-align:right;font-family:"Hanken Grotesk",sans-serif;font-weight:600;font-size:11px}
.idx .cols{columns:2;column-gap:.4in}
.idx .r{break-inside:avoid;font-size:12.6px;padding:4.3px 0}
.notes .lines{position:absolute;left:.95in;right:.95in;top:1.55in;bottom:1.15in;display:flex;flex-direction:column;justify-content:space-between}
.xd .pad{padding:.8in .95in}
.xd h1{font-size:44px;margin:0}
.xd .pos{margin:10px 0 18px}
.xd .xi{height:3.85in;border-radius:3px;overflow:hidden;margin-bottom:20px}
.xd .xi img{width:100%;height:100%;object-fit:cover;object-position:50% 36%;display:block}
.xd .xb{font-size:14.5px;line-height:1.55;margin:0 0 14px}
.xd .xr{display:flex;gap:16px;align-items:flex-start;margin-top:14px}
.xd .xr .qr img{width:1in;height:1in}
.xd .xr .write{flex:1;display:flex;flex-direction:column;justify-content:space-between;height:1in}
.xd .xr .write span{display:block;border-bottom:1px solid rgba(42,42,45,.26)}
.notes .lines span{display:block;border-bottom:1px solid rgba(42,42,45,.26);flex:0 0 0;height:0}
.notes .lines.full{top:.95in}
.notes .nh{position:absolute;left:.95in;right:.95in;top:.9in}
.notes .nh h1{font-size:40px}
"""

# ---------- structure and page numbers
def slugs(season):
    c=CFG[season]
    return [(int(f[4:6]),f[:-5]) for f in sorted(os.listdir(f"{ROOT}/weeks")) if f.startswith("week") and c["first"]<=int(f[4:6])<=c["last"]]
STRUCT={}   # season -> dict(open=page, weeks={n:heropage})
HOL={-1:6,0:10}; HOLDIR={-1:"holiday1",0:"holiday2"}
p=14
for s in ORDER:
    sl=slugs(s); STRUCT[s]={"open":p,"weeks":{n:p+2+4*i for i,(n,_) in enumerate(sl)}}
    p+=2+4*len(sl)
INDEX_PAGE=p; XDAY=p+1; NOTES=list(range(p+2,p+6)); CLOSE=p+6; TOTAL=CLOSE
assert TOTAL==228,TOTAL
DATA={}
for s in ORDER:
    for n,_ in slugs(s):
        DATA[n]=json.load(open(glob.glob(f"{ROOT}/weeks/week{n:02d}_*.json")[0],encoding="utf-8"))
for n,f in [(-1,"week_m1_twelve_cats_part1.json"),(0,"week_00_twelve_cats_part2.json")]:
    DATA[n]=json.load(open(f"{ROOT}/xmas/{f}",encoding="utf-8"))
for _n in DATA:
    DATA[_n]["base_url"]="https://rainingcad.com/CY2027"
    if _n>0: DATA[_n]["fblocks"]=[b for b in DATA[_n]["fblocks"] if not (b[0].startswith("Coat") or b[0].startswith("By the Numbers"))]
SEAS=[(1,11,"Winter"),(12,24,"Spring"),(25,37,"Summer"),(38,50,"Fall")]
for _n in list(DATA):
    if _n<1: continue
    _a,_b,_se=[t for t in SEAS if t[0]<=_n<=t[1]][0]
    _ann=DATA[_n]["rank_num"]
    DATA[_n]["rank_num"]=str(_b-_n+1)
    DATA[_n]["rank_cap"]=f"annual rank No. {_ann} of 50"
    DATA[_n]["season_line"]=f"Cats of {_se} &middot; countdown {_b-_a+1} to 1"
def sunday(n): return datetime.date(2027,1,3)+datetime.timedelta(days=7*(n-1))
def fmt(d): return d.strftime("%b ")+str(d.day)

# ---------- page builders
def prep(season): pass

def title_page():
    return '''<section class="page fm title"><div class="tpad"><div class="kicker">A Calendar &amp; Journal</div><h1>Cat Year<br>2027</h1><div class="trule"></div>
      <p class="tag">Every Day Has Its Cat</p><p class="span">52 breeds &nbsp;&middot;&nbsp; 365 days &nbsp;&middot;&nbsp; December 20, 2026 to December 19, 2027</p>
      <div class="byline">Richard J. Koret</div><div class="press">Raining Cats &amp; Dogs Press</div></div></section>'''
def copy_page():
    return '''<section class="page fm copy"><div class="cpad"><p class="cb"><strong>A Cat Year: Every Day Has Its Cat</strong><br>2027 Edition</p>
      <p>Copyright &copy; 2026 Richard J. Koret. All rights reserved.</p>
      <p>No part of this book may be reproduced, stored, or transmitted in any form without written permission from the publisher, except for brief quotations in reviews.</p>
      <p>Published by Raining Cats &amp; Dogs Press<br>rainingcad.com</p><p>First edition, 2026.</p><p>Breed rankings are approximate.</p></div></section>'''
def intro_page():
    intro=["Cats do not keep calendars. They keep schedules. The window at dawn, the sunbeam at noon, the exact moment the can opener starts. A cat&rsquo;s year is made of small, particular hours, and none of them is wasted.",
      "This book follows that example. Cat Year 2027 gives every week its own breed: fifty, plus the Burmilla on Day 365 and a rescue cat who belongs to every breed and none. Fifty-two in all. Each week opens with a portrait, then a page of history, character, and fact. Seven short thoughts follow, one for each day, with room beside each to write down your own.",
      "The book opens with a Holiday Season prelude of twelve days of cats, and the year begins on the first Sunday of January. Four seasons follow, each opening with a few words on what it means to a cat.",
      "Every date carries a photograph and a QR code. Write in the book, or scan the code and tap or talk your note online at rainingcad.com. The book or the Kindle edition gives you online access to all of it.",
      "Turn the page. The first cat is already at the window."]
    sc="".join(f'<div class="sn"><div class="nm">{n}</div><div class="wk">{w}</div><div class="dt">{d}</div><div class="ct">{c}</div></div>' for n,w,d,c in SEASONS_STRIP)
    return f'''<section class="page fm"><div class="pad"><div class="kicker">Introduction</div><h1>Every Day Has Its Cat.</h1><p class="pos">A year lived at the speed of a slow blink.</p><div class="rule"></div><div class="body">{P(intro)}</div></div><div class="seasons">{sc}</div>{FOLIO}</section>'''
def toc_page(seasons,first):
    rows=""
    if first:
        rows+='<div class="sh"><span>Holiday Season</span><span>Dec 20, 2026 &middot; Jan 2, 2027</span></div>'
        rows+=f'<div class="r"><span class="w">Holiday</span><span class="b">The Twelve Cats of Christmas</span><span class="l"></span><span class="d">Dec 20 &ndash; 31</span><span class="p">{HOL[-1]}</span></div>'
        rows+=f'<div class="r"><span class="w">2027</span><span class="b">The New Year Begins</span><span class="l"></span><span class="d">Jan 1</span><span class="p">{HOL[-1]+7}</span></div>'
    for s in seasons:
        c=CFG[s]; rng=SEASONS_STRIP[ORDER.index(s)]
        rows+=f'<div class="sh"><span>{c["name"]}</span><span>{rng[1]} &middot; {rng[2]}</span></div>'
        for n,_ in slugs(s):
            d=DATA[n]
            rows+=f'<div class="r"><span class="w">Week {n}</span><span class="b">{d["breed"]}</span><span class="l"></span><span class="d">{fmt(sunday(n))}</span><span class="p">{STRUCT[s]["weeks"][n]}</span></div>'
    if 'fall' in seasons: rows+=f'<div class="r"><span class="w">Day 365</span><span class="b">Burmilla</span><span class="l"></span><span class="d">Dec 19</span><span class="p">{XDAY}</span></div>'
    head='<div class="kicker">Contents</div><h1>The Year at a Glance</h1>' if first else '<div class="kicker">Contents, continued</div><h1>&nbsp;</h1>'
    return f'<section class="page fm toc"><div class="pad">{head}{rows}</div>{FOLIO}</section>'
def opener_pages(season):
    c=CFG[season]; name=c["name"]
    tiles="".join(f'<img src="{b64(f"{IMG}/{sl}/hero.jpg")}" alt="">' for n,sl in slugs(season))
    a=f'''<section class="page hero w"><div class="collage"><div class="ct"><div class="k">Cat Year 2027 &middot; {name}</div><h2>The Cats of {name}</h2><p>{c["Count"]} weeks. {c["Count"]} friends.</p></div>{tiles}</div><div class="folio nofolio"><span></span><span class="pageno">[ # ]</span></div></section>'''
    c=dict(c,essay_title=f"What {name} Means",essay_pos="To cats, and to those who love them.",essay=ESSAYS[season])
    b=f'''<section class="page fm"><div class="pad"><div class="kicker">{c["kicker"]}</div><h1>{c["essay_title"]}</h1><p class="pos">{c["essay_pos"]}</p><div class="rule"></div><div class="body">{P(c["essay"])}</div></div>{FOLIO}</section>'''
    return [a,b]
def week_pages(season):
    out=[]
    for n,slug in slugs(season):
        html=mw.build(DATA[n],f"{IMG}/{slug}")
        secs=re.findall(r'(<section class="page.*?</section>)',html,flags=re.S); assert len(secs)==4
        out+=secs
    return out
def hol_pages(n):
    html=mw.build(DATA[n],f"{IMG}/{HOLDIR[n]}")
    secs=re.findall(r'(<section class="page.*?</section>)',html,flags=re.S); assert len(secs)==4
    return secs
def index_page():
    ents=sorted(((DATA[n]["breed"],STRUCT[s]["weeks"][n]) for s in ORDER for n,_ in slugs(s)),key=lambda x:x[0].lower())
    rows="".join(f'<div class="r"><span class="b">{b}</span><span class="l"></span><span class="p">{pg}</span></div>' for b,pg in ents)
    return f'<section class="page fm toc idx"><div class="pad"><div class="kicker">Index</div><h1>Breeds A to Z</h1><div class="rule" style="margin-top:14px"></div><div class="cols">{rows}</div></div>{FOLIO}</section>'
def notes_page(first):
    if first: return f'<section class="page fm notes"><div class="nh"><div class="kicker">Journal</div><h1>Notes</h1></div><div class="lines">{"<span></span>"*20}</div>{FOLIO}</section>'
    return f'<section class="page fm notes"><div class="lines full">{"<span></span>"*23}</div>{FOLIO}</section>'
def xday_page():
    qr=mw.qr_uri("https://rainingcad.com/CY2027/365")
    img=b64(f"{IMG}/extraday.jpg")
    body=["A year has 52 weeks and one day left over. Most calendars hide it. This one gives it to a cat that did not exist until 1981, the Burmilla, a Burmese crossed with a Chinchilla Persian.","It was an accident. At a cattery in England, a lilac Burmese named Bambino Lilac Faberg&eacute; and a Chinchilla Persian named Jamari Sanquist were kept in separate rooms. One night a door was left open. Four silver shaded kittens arrived, and the breed was named for both parents. The Burmese came in week 4. The Persian came in week 14. Today they meet. Write down one thing you want to remember about this year."]
    return f'''<section class="page fm xd"><div class="pad"><div class="kicker">Sunday, December 19, 2027 &nbsp;&middot;&nbsp; Day 365</div><h1>Burmilla</h1><p class="pos">One more day, and one more breed.</p>
      <div class="xi"><img src="{img}" alt=""></div>{"".join(f'<p class="xb">{t}</p>' for t in body)}
      <div class="xr"><a class="qr" href="https://rainingcad.com/CY2027/365"><img src="{qr}" alt=""></a><div class="write">{"<span></span>"*5}</div></div></div>{FOLIO}</section>'''
def close_page():
    qr=mw.qr_uri("https://rainingcad.com/CY2027")
    return f'''<section class="page fm endp"><div class="epad"><div class="kicker">The Last Walk</div><h1>That is the year.</h1><p class="pos">The cats thank you for the company.</p><div class="trule"></div>
      <p class="ebody">Every day in this book has a page online, with a bigger photograph and more of the story. Scan the code to see the whole year again, any time you like.</p>
      <a class="qr bigqr" href="https://rainingcad.com/CY2027"><img src="{qr}" alt=""></a><p class="eurl">rainingcad.com/CY2027</p></div>{FOLIO}</section>'''

def part_pages(part):
    """return {pageno: html} for the part"""
    d={}
    if part=="A":
        d[1]=title_page(); d[2]=copy_page(); d[3]=intro_page(); d[4]=toc_page(["winter","spring"],True); d[5]=toc_page(["summer","fall"],False)
        seasons=["winter"]
        import holiday_seq
        for i,h in enumerate(holiday_seq.pages()): d[6+i]=h
    elif part=="B": seasons=["spring"]
    elif part=="C": seasons=["summer"]
    else: seasons=["fall"]
    for s in seasons:
        prep(s); o=STRUCT[s]["open"]; pages=opener_pages(s)+week_pages(s)
        for i,h in enumerate(pages): d[o+i]=h
    if part=="D":
        d[INDEX_PAGE]=index_page(); d[XDAY]=xday_page()
        for i,pg in enumerate(NOTES): d[pg]=notes_page(i==0)
        d[CLOSE]=close_page()
    return d

def render(part):
    d=part_pages(part); nums=sorted(d)
    sheets=[]
    for i in nums:
        sec=d[i].replace("[ # ]",str(i)); side="recto" if i%2==1 else "verso"
        sheets.append(f'<div class="sheet {side}" data-n="{i}">{sec}</div>')
    css=mw.font_faces()+"\n"+mw.CSS+"\n"+EXTRA_CSS
    html=f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="deck">{"".join(sheets)}</div></body></html>'
    tmp=f"{ROOT}/year_{part}.html"; open(tmp,"w",encoding="utf-8").write(html)
    raw=f"{ROOT}/year_{part}_raw.pdf"
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(); pg.goto("file://"+tmp); pg.wait_for_timeout(2000)
        pg.evaluate('''()=>{document.querySelectorAll(".intro").forEach(pgEl=>{
          const side=pgEl.querySelector(".side"), story=pgEl.querySelector(".story"), qr=pgEl.querySelector(".profqr"); if(!side||!story) return;
          const ps=[...side.querySelectorAll(".fblock p")];
          let f=11.5; const setSide=()=>{ps.forEach(p=>p.style.fontSize=f+"px"); side.querySelectorAll(".fblock").forEach(b=>{b.style.marginTop=(f>10?14:9)+"px";b.style.paddingTop=(f>10?10:7)+"px"})};
          setSide(); const sideBox=()=>{const last=side.lastElementChild.getBoundingClientRect(); const pg=pgEl.getBoundingClientRect(); return last.bottom-(pg.bottom-0.95*96)};
          while(sideBox()>0 && f>8.4){f-=.1; setSide()}
          let s2=13; const sb=()=>story.getBoundingClientRect().bottom-qr.getBoundingClientRect().top+10;
          while(sb()>0 && s2>9.6){s2-=.1; story.style.fontSize=s2+"px"}
          pgEl.dataset.fit=f.toFixed(1)+"/"+s2.toFixed(1);
        })}''')
        pg.evaluate('''()=>{document.querySelectorAll(".dtext").forEach(e=>{let s=14;while(e.scrollWidth>e.clientWidth&&s>12){s-=.25;e.style.fontSize=s+"px"} if(e.scrollWidth>e.clientWidth){e.style.whiteSpace="normal";e.style.fontSize="12.5px";e.style.lineHeight="1.35"}})}''')
        print('fit',sorted(set(pg.evaluate('()=>[...document.querySelectorAll(".intro")].map(e=>e.dataset.fit)'))))
        rep=pg.evaluate('''()=>{const out=[];document.querySelectorAll(".sheet").forEach(sh=>{const n=sh.dataset.n;
          sh.querySelectorAll(".story,.body,.side,.dtext,.lwbody,.cpad,.ebody,.cols,.toc .pad").forEach(e=>{
            const r=e.getBoundingClientRect(), pr=sh.querySelector(".page").getBoundingClientRect();
            if(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1||r.bottom>pr.bottom-0.45*96||r.right>pr.right+1) out.push([n,e.className,Math.round(e.scrollHeight-e.clientHeight),Math.round(r.bottom-pr.bottom)]);});});return out;}''')
        small=pg.evaluate('''()=>{const o=[];document.querySelectorAll(".dtext").forEach(e=>{const s=parseFloat(e.style.fontSize||14);if(s<12)o.push([e.closest(".sheet").dataset.n,s])});return o}''')
        print(part,"pages",nums[0],"-",nums[-1],"overflow:",rep,"small:",small)
        pg.pdf(path=raw,width="8.125in",height="10.25in",print_background=True); b.close()
    r=PdfReader(raw); w=PdfWriter()
    for n,pgx in zip(nums,r.pages):
        W,H=585.0,738.0
        pgx.mediabox=RectangleObject([0,0,W,H]);pgx.cropbox=RectangleObject([0,0,W,H]);pgx.bleedbox=RectangleObject([0,0,W,H])
        x0=0 if n%2==1 else 9
        pgx.trimbox=RectangleObject([x0,9,x0+576,729]); w.add_page(pgx)
    out=f"{OUTDIR}/CatYear2027_Interior_part{part}_p{nums[0]:03d}-{nums[-1]:03d}.pdf"; w.write(out); print("->",out,os.path.getsize(out)//1024,"KB")
    return out
if __name__=="__main__":
    for part in (sys.argv[2:] or ["A","B","C","D"]): render(part)
