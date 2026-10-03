import base64,io,sys,os
from playwright.sync_api import sync_playwright
F='npm/node_modules/@fontsource/spectral/files/'
H='npm/node_modules/@fontsource-variable/hanken-grotesk/files/hanken-grotesk-latin-wght-normal.woff2'
b=lambda p:base64.b64encode(open(p,'rb').read()).decode()
grid=sys.argv[1] if len(sys.argv)>1 else 'grid.png'
gimg='data:image/png;base64,'+b(grid) if grid else ''
bg=f'background:url({gimg}) center/cover' if grid else 'background:repeating-linear-gradient(45deg,#2a2723,#2a2723 14px,#302c28 14px,#302c28 28px)'
ph='' if grid else '<div class="ph">PLACEHOLDER<br>7 x 7 DOG PHOTO MATRIX</div>'
html=f'''<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:Spectral;font-weight:800;src:url(data:font/woff2;base64,{b(F+'spectral-latin-800-normal.woff2')})}}
@font-face{{font-family:Spectral;font-weight:400;font-style:italic;src:url(data:font/woff2;base64,{b(F+'spectral-latin-400-italic.woff2')})}}
@font-face{{font-family:Hanken;font-weight:100 900;src:url(data:font/woff2;base64,{b(H)})}}
@page{{size:8in 10in;margin:0}}
*{{margin:0;box-sizing:border-box}}
body{{width:8in;height:10in;position:relative;overflow:hidden;{bg};color:#fff}}
.scrim{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 27% at 50% 46%,rgba(18,15,12,.80) 0,rgba(18,15,12,.62) 60%,rgba(18,15,12,0) 100%),linear-gradient(180deg,rgba(18,15,12,0) 82%,rgba(18,15,12,.7) 100%)}}
.t{{position:absolute;left:0;right:0;top:3.42in;text-align:center}}
.k{{font:700 15pt Hanken;letter-spacing:.42em;color:#f2c14e;text-transform:uppercase;margin:.0in 0 0}}
h1{{font:800 84pt/0.95 Spectral;letter-spacing:.01em;color:#fff;paint-order:stroke fill;-webkit-text-stroke:2px #000;text-shadow:0 6px 28px #000,0 0 40px rgba(0,0,0,.9)}}
h1 span{{color:#f2c14e}}
.tag,.k,.au{{paint-order:stroke fill;-webkit-text-stroke:1px #000;text-shadow:0 0 6px #000,0 2px 12px #000,0 0 22px #000}}
.rule{{width:1.6in;height:2px;background:#f2c14e;margin:.2in auto .18in}}
.tag{{margin-top:.22in;font:italic 400 36pt Spectral;color:#fff}}
.au{{color:#fff;position:absolute;left:0;right:0;bottom:.5in;text-align:center;font:600 12pt Hanken;letter-spacing:.38em;text-transform:uppercase}}
.ph{{position:absolute;left:.75in;right:.75in;top:.75in;height:2.2in;border:2px dashed #c9a24a;color:#c9a24a;font:600 13pt Hanken;letter-spacing:.2em;text-align:center;padding-top:.8in}}
</style><body>{ph}
<div class=t><h1>DOG YEAR<br><span>2027</span></h1><div class=tag>Every Day a Dog</div><div class=k>Calendar &amp; Journal</div></div>
<div class=au>Richard J. Koret</div></body>'''
open('cover.html','w').write(html)
with sync_playwright() as p:
    br=p.chromium.launch();pg=br.new_page();pg.goto('file://'+os.path.abspath('cover.html')+'');pg.wait_for_timeout(500)
    pg.pdf(path=sys.argv[2] if len(sys.argv)>2 else 'DogYear2027_Cover.pdf',width='8in',height='10in',print_background=True);br.close()
