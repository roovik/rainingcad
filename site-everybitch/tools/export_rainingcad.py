"""Copy the Bitch-O-Meter pages from site-everybitch/public into ../site/bitch-o-meter/ for rainingcad.com.
Standalone: no site menu, noindex, assets under /bitch-o-meter/img/, book links point to everybitch.com."""
import os, re, shutil, glob
H = os.path.dirname(__file__)
PUB = os.path.join(H, '..', 'public')
DST = os.path.join(H, '..', '..', 'site', 'bitch-o-meter')
if os.path.isdir(DST): shutil.rmtree(DST)
os.makedirs(os.path.join(DST, 'img', 'q'), exist_ok=True)
for f in glob.glob(os.path.join(PUB, 'img', 'ch*.webp')) + [os.path.join(PUB, 'img', 'og.jpg'), os.path.join(PUB, 'img', 'og-certificate.jpg')]:
    shutil.copy(f, os.path.join(DST, 'img'))
for f in glob.glob(os.path.join(PUB, 'img', 'q', '*.webp')):
    shutil.copy(f, os.path.join(DST, 'img', 'q'))
NAV = '<nav class="nav"><div class="wrap"><a class="brand" href="https://everybitch.com/">Every <b>Bitch</b> Has Her Way</a></div></nav>'
def fix(t):
    t = re.sub(r'<nav class="nav">.*?</nav>', NAV, t, flags=re.S)
    t = t.replace('https://everybitch.com/bitch-o-meter', 'https://rainingcad.com/bitch-o-meter')
    t = t.replace("'https://everybitch.com'+D.path", "'https://rainingcad.com'+D.path")
    t = t.replace('src="/img/', 'src="/bitch-o-meter/img/').replace('"img": "/img/', '"img": "/bitch-o-meter/img/')
    t = t.replace('content="https://everybitch.com/img/', 'content="https://rainingcad.com/bitch-o-meter/img/')
    t = t.replace("href=\"/secrets/'", "href=\"https://everybitch.com/secrets/'")
    t = t.replace('href="/which-bitch/"', 'href="https://everybitch.com/which-bitch/"')
    t = t.replace('<meta charset="utf-8">', '<meta charset="utf-8"><meta name="robots" content="noindex,nofollow">', 1)
    t = t.replace('<link rel="icon" href="/favicon.svg" type="image/svg+xml">', '')
    return t
for f in ['index.html', 'home/index.html', 'work/index.html', 'certificate/index.html']:
    t = open(os.path.join(PUB, 'bitch-o-meter', f), encoding='utf-8').read()
    out = os.path.join(DST, f); os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(fix(t))
print('exported to', DST)
