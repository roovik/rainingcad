#!/usr/bin/env python3
"""
A Dog Year - weekly spread generator (project copy, font loader switched to woff2).
Usage:  python3 make_week.py <week.json> <images_dir> <out.pdf>
"""
import sys, os, io, json, base64, datetime
import qrcode
from qrcode.constants import ERROR_CORRECT_M

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "npm", "node_modules")
SP = os.path.join(FONTS, "@fontsource", "spectral", "files")
HG = os.path.join(FONTS, "@fontsource-variable", "hanken-grotesk", "files")
DAY_KEYS  = ["sun","mon","tue","wed","thu","fri","sat"]
DAY_NAMES = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
WEEK1_SUNDAY = datetime.date(2027,1,3)

def b64_img(path):
    ext = path.rsplit(".",1)[-1].lower()
    mime = {"png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg","webp":"image/webp"}[ext]
    return f"data:{mime};base64," + base64.b64encode(open(path,"rb").read()).decode()

def find_img(d, stem):
    for ext in ("png","jpg","jpeg","webp","PNG","JPG","JPEG","WEBP"):
        p = os.path.join(d, f"{stem}.{ext}")
        if os.path.exists(p): return b64_img(p)
    raise SystemExit(f"Missing image '{stem}.(png|jpg|jpeg|webp)' in {d}")

def qr_uri(url):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=10, border=2)
    q.add_data(url); q.make(fit=True)
    im = q.make_image(fill_color="#2A2A2D", back_color="white").convert("RGB")
    b = io.BytesIO(); im.save(b,"PNG",optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

def font_faces():
    def face(fam,style,weight,path):
        b = base64.b64encode(open(path,"rb").read()).decode()
        return (f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{weight};"
                f"src:url(data:font/woff2;base64,{b}) format('woff2');font-display:block;}}")
    out = []
    for w in (400,600,700,800):
        out.append(face('Spectral','normal',w,os.path.join(SP,f'spectral-latin-{w}-normal.woff2')))
    for w in (400,600):
        out.append(face('Spectral','italic',w,os.path.join(SP,f'spectral-latin-{w}-italic.woff2')))
    out.append(face('Hanken Grotesk','normal','100 900',os.path.join(HG,'hanken-grotesk-latin-wght-normal.woff2')))
    return "\n".join(out)

CSS = r""":root{ --paper:#F3F2EC; --ink:#2A2A2D; --ink-soft:#6F6F74; --gold:#B0822B; --gold-deep:#876217; --line:rgba(42,42,45,.16); }
*{box-sizing:border-box}
html{background:#fff}
body{margin:0;font-family:"Spectral",Georgia,serif;color:var(--ink);-webkit-font-smoothing:antialiased}
.deck{display:flex;flex-direction:column;align-items:center}
.page{position:relative;width:8in;height:10in;background:var(--paper);overflow:hidden}
.pad{position:absolute;inset:0;padding:.75in}
.kicker{font-family:"Hanken Grotesk",sans-serif;font-weight:600;text-transform:uppercase;letter-spacing:.24em;font-size:10.5px;color:var(--gold-deep)}
.folio{position:absolute;left:.75in;right:.75in;bottom:.42in;display:flex;justify-content:space-between;align-items:baseline;font-family:"Hanken Grotesk",sans-serif;font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-soft)}
.folio .pageno{letter-spacing:.12em;opacity:.7}
.hero .holder{position:absolute;inset:.75in;overflow:hidden;border-radius:2px;border:1px solid rgba(42,42,45,.14)}
.hero .holder img{width:100%;height:100%;object-fit:cover}
.intro .p2{display:flex;gap:32px;height:100%}
.intro .main{flex:1;min-width:0}
.intro .side{flex:0 0 210px}
.intro .kicker{margin-bottom:14px}
.intro h1{font-family:"Spectral",serif;font-weight:800;font-size:46px;line-height:.94;margin:0;letter-spacing:-.01em}
.intro .pos{font-family:"Spectral",serif;font-style:italic;font-weight:600;font-size:19px;color:var(--gold-deep);margin:13px 0 17px;max-width:24ch;line-height:1.28}
.intro .story{font-size:13px;line-height:1.52;text-align:justify}
.intro .story p{margin:0 0 9px}
.intro .story p:first-child:first-letter{font-family:"Spectral",serif;font-weight:800;float:left;font-size:56pt;line-height:.66;padding:8px 11px 0 0;color:var(--gold)}
.side .stats{border-top:3px solid var(--gold);padding-top:13px}
.side .sl{font-family:"Hanken Grotesk",sans-serif;font-size:9.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:11px}
.side .rank{display:flex;align-items:flex-start;gap:10px}
.side .rank .num{font-family:"Spectral",serif;font-weight:800;font-size:34px;line-height:.82;color:var(--ink);white-space:nowrap}
.side .season{font-family:"Hanken Grotesk",sans-serif;font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-deep);margin-top:9px}
.intro .main{position:relative}
.profqr{position:absolute;left:0;bottom:.15in;display:flex;align-items:center;gap:14px}
.profqr .qr{height:96px;width:96px}
.profqr .pl{font-family:"Hanken Grotesk",sans-serif;font-size:9.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep)}
.profqr .ps{font-size:12.5px;margin-top:5px;max-width:20ch;line-height:1.35}
.side .rank .cap{font-family:"Hanken Grotesk",sans-serif;font-size:10px;line-height:1.32;color:var(--ink-soft);flex:1;margin-top:2px}
.side .stats dl{margin:13px 0 0;border-top:1px solid var(--line)}
.grow{display:flex;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px solid var(--line)}
.grow:last-of-type{border-bottom:none}
.grow dt{font-family:"Hanken Grotesk",sans-serif;font-weight:600;font-size:10px;letter-spacing:.04em;text-transform:uppercase;color:var(--ink-soft)}
.grow dd{margin:0;font-size:12px;text-align:right;font-weight:500}
.fblock{margin-top:14px;border-top:1px solid var(--line);padding-top:10px}
.fblock .fl{font-family:"Hanken Grotesk",sans-serif;font-size:9.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--gold-deep);margin-bottom:6px}
.fblock p{font-size:11.5px;line-height:1.5;margin:0;color:var(--ink)}
.wk .pad{display:flex;flex-direction:column}
.weekhead{display:flex;align-items:flex-end;border-bottom:2px solid var(--ink);padding-bottom:9px}
.weekhead h2{font-family:"Spectral",serif;font-weight:800;font-size:24px;margin:0;line-height:1.02}
.days{flex:1;display:flex;flex-direction:column;min-height:0}
.day{flex:1;min-height:0;display:flex;gap:16px;align-items:stretch;padding:15px 0;border-bottom:1px solid var(--line)}
.thumb{position:relative;flex:0 0 128px;width:128px;align-self:stretch;min-height:104px;display:block;border-radius:2px;overflow:hidden;text-decoration:none;border:1px solid rgba(42,42,45,.14)}
.thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.dbody{flex:1;min-height:0;display:flex;flex-direction:column;min-width:0}
.dhead{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:5px}
.dhead .dow{font-family:"Spectral",serif;font-weight:700;font-size:19px}
.dhead .date{font-family:"Hanken Grotesk",sans-serif;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-deep)}
.dtext{font-size:14px;line-height:1.5;margin:0;color:var(--ink);white-space:nowrap;overflow:hidden}
.lower{flex:1;min-height:0;display:flex;gap:14px;padding-top:9px}
.qr{flex:0 0 auto;height:100%;aspect-ratio:1/1;background:#fff;border:1px solid var(--line);border-radius:2px;padding:4px;overflow:hidden;display:block}
.qr img{width:100%;height:100%;object-fit:contain;image-rendering:pixelated;display:block}
.write{flex:1;min-width:0;display:flex;flex-direction:column;justify-content:space-between}
.write span{display:block;border-bottom:1px solid rgba(42,42,45,.22)}
.lastrow .dhead{margin-bottom:6px}
.lwarea{flex:1;min-height:0;display:flow-root}
.lwarea::before{content:"";display:block;float:left;width:0;height:calc(100% - 88px)}
.lwqr{float:left;clear:left;width:88px;height:88px;aspect-ratio:auto;margin:0 14px 0 0}
.lwbody{flex:1;min-width:0;margin:0;font-size:13px;line-height:1.5;color:var(--ink);overflow:hidden}
.lwtext .lw1{display:block;margin-bottom:4px}
@page{size:8in 10in;margin:0}
.page{page-break-after:always;break-after:page}
.page:last-child{page-break-after:auto}
"""

def slugify(s):
    return "".join(c.lower() if c.isalnum() else "-" for c in s).strip("-").replace("--","-")

def build(data, images_dir):
    num   = data["num"]
    breed = data["breed"]
    base  = f'{data.get("base_url","https://rainingcad.com/DY2027")}/{num}'
    name_html = data.get("name_lines")
    name_html = "<br>".join(name_html) if name_html else breed
    sunday = WEEK1_SUNDAY + datetime.timedelta(days=7*(num-1))
    dates = [(sunday+datetime.timedelta(days=i)).strftime("%b %-d") for i in range(7)]
    imgs = {k: find_img(images_dir,k) for k in (["hero"]+DAY_KEYS+["lastwalk"])}

    LINES = "".join("<span></span>" for _ in range(5))
    def strip(i):
        dow, date, key = DAY_NAMES[i], dates[i], DAY_KEYS[i]
        text = data["days"][i][2]
        url = f"{base}/{i+1}"
        qr = qr_uri(url)
        return f'''<article class="day"><a class="thumb" href="{url}"><img src="{imgs[key]}" alt=""></a>
          <div class="dbody"><div class="dhead"><span class="dow">{dow}</span><span class="date">{date}</span></div>
          <p class="dtext">{text}</p><div class="lower"><a class="qr" href="{url}"><img src="{qr}" alt=""></a>
          <div class="write">{LINES}</div></div></div></article>'''
    def last_row():
        url = f"{base}/8"
        qr = qr_uri(url)
        lead, _, body = data["last_walk"].partition("\n")
        return f'''<article class="day lastrow"><a class="thumb" href="{url}"><img src="{imgs['lastwalk']}" alt=""></a>
          <div class="dbody"><div class="dhead"><span class="dow">Last Walk of the Week</span></div>
          <p class="dtext">{lead}</p><div class="lower"><a class="qr" href="{url}"><img src="{qr}" alt=""></a>
          <p class="lwbody">{body}</p></div></div></article>'''

    p3 = "".join(strip(i) for i in range(4))
    p4 = "".join(strip(i) for i in range(4,7)) + last_row()
    story = "".join(f"<p>{p}</p>" for p in data["story"])
    glance = "".join(f'<div class="grow"><dt>{k}</dt><dd>{v}</dd></div>' for k,v in data["glance"])
    fblocks = "".join(f'<div class="fblock"><div class="fl">{t}</div><p>{x}</p></div>' for t,x in data["fblocks"])
    folio = '<div class="folio"><span>A Dog Year &middot; Every Day Has Its Dog</span><span class="pageno">[ # ]</span></div>'

    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<style>{font_faces()}
{CSS}</style></head><body><div class="deck">
<section class="page hero"><div class="holder"><img src="{imgs['hero']}" alt="{breed}"></div></section>
<section class="page intro"><div class="pad"><div class="p2">
  <div class="main"><div class="kicker">Week {num} &nbsp;&middot;&nbsp; A Dog Year</div>
    <h1>{name_html}</h1><p class="pos">{data["positioning"]}</p><div class="story">{story}</div>
    <div class="profqr"><a class="qr" href="{base}"><img src="{qr_uri(base)}" alt=""></a><div><div class="pl">Meet the breed online</div><div class="ps">Scan for this week&rsquo;s page, photos, and more.</div></div></div></div>
  <aside class="side"><div class="stats"><div class="sl">At a Wag of the Tail</div>
    <div class="rank"><span class="num">{data["rank_num"]}</span><span class="cap">{data["rank_cap"]}</span></div><div class="season">{data.get("season_line","")}</div>
    <dl>{glance}</dl></div>{fblocks}</aside></div></div>{folio}</section>
<section class="page wk"><div class="pad"><div class="weekhead"><h2>Week of the {breed}</h2></div>
  <div class="days">{p3}</div></div>{folio}</section>
<section class="page wk"><div class="pad">
  <div class="days">{p4}</div></div>{folio}</section>
</div></body></html>'''

def main():
    data_path, images_dir, out_pdf = sys.argv[1], sys.argv[2], sys.argv[3]
    data = json.load(open(data_path, encoding="utf-8"))
    html = build(data, images_dir)
    tmp = out_pdf + ".html"; open(tmp,"w",encoding="utf-8").write(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto("file://"+os.path.abspath(tmp)); pg.wait_for_timeout(1000)
        pg.evaluate('''()=>{document.querySelectorAll(".dtext").forEach(e=>{let s=14;while(e.scrollWidth>e.clientWidth&&s>12){s-=.25;e.style.fontSize=s+"px"}})}''')
        pg.pdf(path=out_pdf, prefer_css_page_size=True, print_background=True)
        b.close()
    print("wrote", out_pdf)

if __name__ == "__main__":
    main()
