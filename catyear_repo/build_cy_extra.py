#!/usr/bin/env python3
"""Build site/CY2027/365 (Burmilla). Usage: build_cy_extra.py EXTRA_PNG SITEDIR"""
import re,sys,os,html
from PIL import Image
import qrcode,qrcode.image.svg
PNG=sys.argv[1]; SITE=sys.argv[2]
DY=f"{SITE}/DY2027"; OUT=f"{SITE}/CY2027/365"; BASE="https://rainingcad.com"
URL=f"{BASE}/CY2027/365/"
def qr(url):
    q=qrcode.QRCode(border=1,error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url);q.make(fit=True)
    s=q.make_image(image_factory=qrcode.image.svg.SvgPathImage).to_string().decode()
    return re.search(r'<path[^>]*\bd="([^"]+)"',s).group(1)
t=open(f"{DY}/365/index.html",encoding='utf-8').read()
TITLE="Burmilla · Day 365 · Cat Year 2027"
DESC="A year has 52 weeks and one day left over. This one goes to the Burmilla."
t=re.sub(r'<title>.*?</title>',f'<title>{TITLE}</title>',t)
t=re.sub(r'(<meta name="description" content=")[^"]*"',r'\g<1>'+DESC+'"',t)
t=re.sub(r'(<meta property="og:description" content=")[^"]*"',r'\g<1>'+DESC+'"',t)
t=re.sub(r'(<meta property="og:title" content=")[^"]*"',r'\g<1>'+TITLE+'"',t)
t=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{URL}">',t)
t=re.sub(r'<meta property="og:image" content="[^"]*">',f'<meta property="og:image" content="{URL}hero.webp">',t)
t=t.replace('<span class="q"><a href="/DY2027/" class="on">Dog Year</a><a href="/CY2027/">Cat Year</a></span>','<span class="q"><a href="/DY2027/">Dog Year</a><a href="/CY2027/" class="on">Cat Year</a></span>').replace('<a href="/DY2027/" class="on">Dog Year 2027</a><a href="/CY2027/">Cat Year 2027</a>','<a href="/DY2027/">Dog Year 2027</a><a href="/CY2027/" class="on">Cat Year 2027</a>')
i=t.index('<div class="wrap">'); j=t.index('<div class="qr">')
TOP='<div class="wrap"><div class="top"><a class="mk" href="/" aria-label="Raining Cats &amp; Dogs home"><img src="/img/rcd-mark-96.webp" srcset="/img/rcd-mark-96.webp 1x,/img/rcd-mark-192.webp 2x" width="48" height="31" alt="Raining Cats &amp; Dogs"></a><a href="/CY2027/">Cat Year 2027 &middot; Every Day Has Its Cat</a></div>\n'
body=TOP+'''<div class=kick>Day 365 &middot; Sunday, Dec 19, 2027</div>
<h1>Burmilla</h1><p class=pos>One more day, and one more breed.</p>
<img class=big src="/CY2027/365/hero.webp" alt="Burmilla">
<div class=story style="margin-top:28px"><p>A year has 52 weeks and one day left over. Most calendars hide it. This one gives it to a cat that did not exist until 1981, the Burmilla, a Burmese crossed with a Chinchilla Persian.</p><p>It was an accident. At a cattery in England, a lilac Burmese named Bambino Lilac Fabergé and a Chinchilla Persian named Jamari Sanquist were kept in separate rooms. One night a door was left open. Four silver shaded kittens arrived, and the breed was named for both parents.</p><p>The Burmese came in week 4. The Persian came in week 14. Today they meet.</p><p>Write down one thing you want to remember about this year.</p></div>
<div class="notes" id="notes" data-key="365" data-title="Day 365 · Burmilla"><h2>My Cat-Eared Notes</h2><textarea rows="7" placeholder="What did your cat do today?" aria-label="My Cat-Eared Notes"></textarea><p class="saved">Notes are saved on this device only.</p><button type="button" class="dl">Download all my notes</button></div>
<div class=nav><a href="/CY2027/">&larr; All weeks</a><a href="/CY2027/50/">Week 50</a><span></span></div>
'''
t=t[:i]+body+t[j:]
t=re.sub(r'(<path d=")[^"]+(" id="qr-path")',lambda m:m.group(1)+qr(URL)+m.group(2),t,count=1)
t=t.replace("dy27:","cy27:").replace("MY DOG YEAR 2027 NOTES","MY CAT YEAR 2027 NOTES").replace("my-dog-year-notes","my-cat-year-notes")
t=t.replace("Dog Year 2027 &middot; Every Day Has Its Dog","Cat Year 2027 &middot; Every Day Has Its Cat")
os.makedirs(OUT,exist_ok=True)
Image.open(PNG).convert('RGB').resize((1086,1448),Image.LANCZOS).save(f"{OUT}/hero.webp",'WEBP',quality=80,method=6)
open(f"{OUT}/index.html","w",encoding='utf-8').write(t)
print("built",OUT)
