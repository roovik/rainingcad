#!/usr/bin/env python3
"""Add the one-page Twelve Dogs of Christmas landing page to site/DY2027 and link it. Idempotent. Usage: build_dy_twelve.py SITEDIR"""
import re,sys,os,datetime
import qrcode,qrcode.image.svg
SITE=sys.argv[1]; DY=f"{SITE}/DY2027"; BASE="https://rainingcad.com"; URL=f"{BASE}/DY2027/twelve-dogs/"
def qr(url):
    q=qrcode.QRCode(border=1,error_correction=qrcode.constants.ERROR_CORRECT_M);q.add_data(url);q.make(fit=True)
    s=q.make_image(image_factory=qrcode.image.svg.SvgPathImage).to_string().decode()
    return re.search(r'<path[^>]*\bd="([^"]+)"',s).group(1)
DOGS=["Poodle","Dachshunds","Huskies","Corgis","Golden Pups","Greyhounds","Beagles","Bernese","Frenchies","Collies","Pointers","Chihuahuas"]
t=open(f"{DY}/holiday2/index.html",encoding='utf-8').read()
TITLE="The Twelve Dogs of Christmas · Holiday Season · Dog Year 2027"; DESC="Twelve days. Twelve breeds. Seventy-eight dogs. One pear tree."
t=re.sub(r'<title>.*?</title>',f'<title>{TITLE}</title>',t)
t=re.sub(r'(<meta name="description" content=")[^"]*"',r'\g<1>'+DESC+'"',t)
t=re.sub(r'(<meta property="og:description" content=")[^"]*"',r'\g<1>'+DESC+'"',t)
t=re.sub(r'(<meta property="og:title" content=")[^"]*"',r'\g<1>'+TITLE+'"',t)
t=re.sub(r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{URL}">',t)
t=re.sub(r'<meta property="og:image" content="[^"]*">',f'<meta property="og:image" content="{URL}hero.webp">',t)
i=t.index('<div class="wrap">'); j=t.index('<div class="qr">')
top=t[i:t.index('</div>',i)+7]
d0=datetime.date(2026,12,20); cards=''; tot=0
for n,name in enumerate(DOGS,1):
    tot+=n; dd=d0+datetime.timedelta(days=n-1)
    part,k=('holiday1',n) if n<=7 else ('holiday2',n-7)
    lab=dd.strftime('%b ')+str(dd.day)
    cards+=f'<a href="/DY2027/{part}/{k}/"><img loading=lazy src="/DY2027/{part}/t{k}.webp" alt="Day {n}, {name}"><b>Day {n}, {name}</b><small>{lab} &middot; {tot} in all</small></a>'
after=''.join(f'<a href="/DY2027/holiday2/{k}/"><img loading=lazy src="/DY2027/holiday2/t{k}.webp" alt="{a}"><b>{a}</b><small>{b}</small></a>' for k,a,b in ((6,"New Year&rsquo;s Day","Fri Jan 1"),(7,"The dog not on the list","Sat Jan 2"),(8,"Last Walk","Week close")))
body=top+f'''
<div class=kick>Holiday Season &middot; Dec 20 &ndash; Jan 2</div>
<h1>The Twelve Dogs of Christmas</h1><p class=pos>Twelve days. Twelve breeds. Seventy-eight dogs. One pear tree.</p>
<img class=big src="/DY2027/twelve-dogs/hero.webp" alt="The Twelve Dogs of Christmas">
<div class=story style="margin-top:28px"><p>Every carol has a list. This one has dogs. The old song counts twelve days of gifts. Ours counts twelve days of dogs in one snowy courtyard, starting on Sunday, December 20. A Poodle sits in the pear tree. Every day after that, a bigger group of a new breed joins her, until the courtyard holds all seventy-eight on New Year&rsquo;s Eve.</p><p>The days run in order below. Tap a day to see the courtyard and keep your notes.</p></div>
<div class=kick>The twelve days</div><div class=days>{cards}</div>
<div class=kick>After the twelfth day</div><div class=days>{after}</div>
<div class=nav><a href="/DY2027/">&larr; All weeks</a><a href="/DY2027/holiday1/">Dec 20 to 26</a><a href="/DY2027/holiday2/">Dec 27 to Jan 2</a></div>
'''
t=t[:i]+body+t[j:]
t=re.sub(r'(<path d=")[^"]+(" id="qr-path")',lambda m:m.group(1)+qr(URL)+m.group(2),t,count=1)
out=f"{DY}/twelve-dogs"; os.makedirs(out,exist_ok=True)
import shutil; shutil.copy(f"{DY}/holiday2/hero.webp",f"{out}/hero.webp")
open(f"{out}/index.html","w",encoding='utf-8').write(t)
# index: one card in place of two
p=f"{DY}/index.html"; x=open(p,encoding='utf-8').read()
if 'twelve-dogs' not in x:
    a=x.index('<a href="/DY2027/holiday1/">'); b=x.index('</b></a>',x.index('/DY2027/holiday2/'))+8
    x=x[:a]+'<a href="/DY2027/twelve-dogs/"><img loading=lazy src="/DY2027/twelve-dogs/hero.webp" alt="The Twelve Dogs of Christmas"><small>Holiday season, days 1 to 12</small><b>The Twelve Dogs of Christmas</b></a>'+x[b:]
    open(p,'w',encoding='utf-8').write(x)
# link up from both weekly pages
for h in ('holiday1','holiday2'):
    p=f"{DY}/{h}/index.html"; x=open(p,encoding='utf-8').read()
    if 'twelve-dogs' not in x:
        tag=f'<img class=big src="/DY2027/{h}/hero.webp"'
        x=x.replace(tag,'<p><a href="/DY2027/twelve-dogs/" style="font:700 12px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase">See all twelve days in one place &rarr;</a></p>\n'+tag,1)
        open(p,'w',encoding='utf-8').write(x)
print("ok")
