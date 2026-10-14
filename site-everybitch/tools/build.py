import os, sys, html, json
sys.path.insert(0, os.path.dirname(__file__))
from data import CH

ROOT = os.path.join(os.path.dirname(__file__), '..', 'public')
SITE = 'https://everybitch.com'
E = html.escape

CSS = """
@font-face{font-family:Spectral;font-weight:400;src:url(/fonts/spectral-400.woff2) format('woff2');font-display:swap}
@font-face{font-family:Spectral;font-weight:400;font-style:italic;src:url(/fonts/spectral-400i.woff2) format('woff2');font-display:swap}
@font-face{font-family:Spectral;font-weight:600;font-style:italic;src:url(/fonts/spectral-600i.woff2) format('woff2');font-display:swap}
@font-face{font-family:Spectral;font-weight:800;src:url(/fonts/spectral-800.woff2) format('woff2');font-display:swap}
@font-face{font-family:Hanken;font-weight:100 900;src:url(/fonts/hanken.woff2) format('woff2');font-display:swap}
:root{--pink:#FF1493;--pink-deep:#C8006A;--black:#0E0E10;--ink:#1B1B1E;--soft:#66606A;--cream:#FBF5F0;--rose:#F7DCE8;--line:rgba(14,14,16,.16)}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:64px}
body{margin:0;background:var(--cream);color:var(--ink);font:19px/1.6 Spectral,Georgia,serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{max-width:100%}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
.nav{position:sticky;top:0;z-index:50;background:var(--black);border-bottom:3px solid var(--pink)}
.nav .wrap{display:flex;align-items:center;gap:22px;flex-wrap:wrap;padding-top:12px;padding-bottom:12px}
.nav .brand{font:800 17px Spectral,serif;color:#fff;text-decoration:none;margin-right:auto;letter-spacing:.01em}
.nav .brand b{color:var(--pink)}
.nav a.l{font:500 11px Hanken,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:#fff;text-decoration:none;padding:4px 0}
.nav a.l.b{font-weight:800}
.nav a.l:hover,.nav a.l.on{color:var(--pink)}
.nav a.l.on{font-weight:800}
.nav a.get{font-weight:800}
.nav a.get{background:var(--pink);color:var(--black);padding:9px 14px}
.nav a.get:hover{background:#fff;color:var(--black)}
@media(max-width:640px){.nav .brand{flex-basis:100%}.nav .wrap{gap:14px}}
.hero{background:var(--black);color:#fff;padding:54px 0 60px}
.hero .wrap{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;align-items:center}
@media(max-width:760px){.hero .wrap{grid-template-columns:1fr;gap:28px}}
.cov{display:block;width:100%;height:auto;box-shadow:14px 14px 0 var(--pink),0 20px 50px rgba(0,0,0,.5);background:#222}
.kick{font:700 11px Hanken,sans-serif;letter-spacing:.26em;text-transform:uppercase;color:var(--pink);margin:0 0 14px}
h1{font:800 clamp(44px,8vw,82px)/.96 Spectral,serif;margin:0 0 16px;letter-spacing:-.015em}
h1 .p{color:var(--pink);display:block}
.hero h1{color:#fff}
.tag{font:italic 600 clamp(20px,3vw,28px)/1.3 Spectral,serif;color:#fff;margin:0 0 20px}
.hero p.s{color:#d9d4dc;max-width:34em}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 0}
.btn{font:800 12px Hanken,sans-serif;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;padding:15px 22px;border:2px solid var(--pink);color:var(--pink);display:inline-block}
.btn.main{background:var(--pink);color:var(--black)}
.btn.main:hover{background:#fff;border-color:#fff}
.btn.off{border-color:rgba(255,255,255,.28);color:#aaa;pointer-events:none}
.light .btn.off,.sec .btn.off,.getbox .btn.off{border-color:rgba(14,14,16,.4);color:#4a444e}
.band{background:var(--pink);color:var(--black);padding:46px 0;text-align:center}
.band p{font:italic 600 clamp(22px,3.6vw,34px)/1.3 Spectral,serif;margin:0 auto;max-width:21em}
.band p b{font-style:normal;font-weight:800}
h2{font:800 clamp(30px,5vw,46px)/1.05 Spectral,serif;margin:0 0 14px;letter-spacing:-.01em}
h2 .p{color:var(--pink-deep)}
.sec{padding:60px 0}
.lede{font-size:clamp(20px,2.6vw,24px);max-width:36em}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:26px 22px;margin:30px 0 0}
.card{text-decoration:none;display:block}
.card img{display:block;width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;background:#ddd;box-shadow:6px 6px 0 var(--black);transition:transform .15s,box-shadow .15s}
.card:hover img{transform:translate(-3px,-3px);box-shadow:9px 9px 0 var(--pink)}
.card .n{font:700 11px Hanken,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--pink-deep);margin:16px 0 2px}
.card b{display:block;font:800 22px/1.1 Spectral,serif}
.card .t{font-size:16px;line-height:1.45;color:var(--soft);margin:6px 0 0}
.rules{background:var(--black);color:#fff;padding:64px 0}
.rules h2{color:#fff}
.rules h2 .p{color:var(--pink)}
.rl{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:0 44px;margin-top:26px}
.rl blockquote{margin:0;padding:22px 0;border-top:2px solid var(--pink);font:italic 600 clamp(21px,2.6vw,26px)/1.3 Spectral,serif}
.rl blockquote span{display:block;font:700 11px Hanken,sans-serif;font-style:normal;letter-spacing:.2em;text-transform:uppercase;color:var(--pink);margin-top:10px}
.quizband{background:var(--rose);border-top:3px solid var(--black);border-bottom:3px solid var(--black);padding:54px 0;text-align:center}
.quizband p{max-width:30em;margin:0 auto 22px}
.btn.dark{background:var(--black);border-color:var(--black);color:#fff}
.btn.dark:hover{background:var(--pink);border-color:var(--pink);color:var(--black)}
.look{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:16px;margin-top:26px}
.look img{display:block;width:100%;height:auto;border:1px solid var(--line);box-shadow:5px 5px 0 var(--black);background:#fff}
.gifts{columns:2 320px;column-gap:44px;margin:26px 0 0;padding:0;list-style:none}
.gifts li{break-inside:avoid;padding:14px 0 14px 28px;border-top:1px solid var(--line);position:relative}
.gifts li:before{content:"";position:absolute;left:0;top:25px;width:12px;height:12px;background:var(--pink);border-radius:50%}
.foot{background:var(--black);color:#bdb6c0;padding:36px 0 46px;font:13px/1.7 Hanken,sans-serif}
.foot a{color:var(--pink);text-decoration:none}
.foot b{color:#fff}
/* chapter page */
.ch{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;align-items:start;padding:50px 0 20px}
@media(max-width:760px){.ch{grid-template-columns:1fr;gap:24px}}
.ch img.pt{display:block;width:100%;height:auto;box-shadow:10px 10px 0 var(--pink);background:#ddd}
.ch h1{font-size:clamp(36px,6vw,60px);color:var(--black)}
.cap{font:italic 400 clamp(19px,2.4vw,23px)/1.35 Spectral,serif;color:var(--pink-deep);margin:0 0 24px}
.ex{margin:30px 0 0;padding:0;list-style:none}
.ex li{border-left:5px solid var(--pink);padding:4px 0 4px 18px;margin:0 0 16px;font:italic 600 21px/1.35 Spectral,serif}
.pn{display:flex;justify-content:space-between;gap:16px;border-top:3px solid var(--black);margin-top:34px;padding:22px 0}
.pn a{text-decoration:none;font:800 20px/1.2 Spectral,serif;max-width:46%}
.pn a span{display:block;font:700 11px Hanken,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:var(--pink-deep);margin-bottom:4px}
.pn a:last-child{text-align:right;margin-left:auto}
.pn a:hover{color:var(--pink-deep)}
.getbox{background:var(--rose);border:3px solid var(--black);padding:26px;margin:26px 0 50px;text-align:center}
.getbox b{font:800 26px Spectral,serif;display:block;margin-bottom:6px}
.getbox .btns{justify-content:center}
/* quiz */
.q{margin:0 0 34px;padding:0;border:0}
.q legend{font:800 24px/1.2 Spectral,serif;padding:0;margin-bottom:12px}
.q label{display:block;border:2px solid var(--black);padding:12px 16px;margin:0 0 10px;cursor:pointer;background:#fff;font-size:18px;line-height:1.35}
.q label:hover{background:var(--rose)}
.q input{accent-color:var(--pink);margin-right:10px}
.q input:checked+span{font-weight:700}
.res{display:none;background:var(--black);color:#fff;padding:30px;margin-top:20px;box-shadow:10px 10px 0 var(--pink)}
.res.on{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:26px;align-items:center}
@media(max-width:640px){.res.on{grid-template-columns:1fr}}
.res img{width:100%;height:auto;display:block}
.res h3{font:800 34px/1.05 Spectral,serif;margin:0 0 10px;color:var(--pink)}
.res p{margin:0 0 12px}
.res a{color:var(--pink)}
.mres{display:none;margin-top:26px}
.mres.on{display:block}
.pct{font:800 clamp(72px,16vw,150px)/1 Spectral,serif;color:var(--pink-deep);margin:0}
.bar{height:22px;background:var(--black);border:3px solid var(--black);margin:6px 0 22px;box-shadow:8px 8px 0 var(--pink)}
.bar i{display:block;height:100%;width:0;background:var(--pink);transition:width 1.1s cubic-bezier(.2,.8,.2,1)}
.tier{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,2fr);gap:26px;align-items:center;background:var(--black);color:#fff;padding:28px;margin-top:8px}
@media(max-width:640px){.tier{grid-template-columns:1fr}}
.tier img{width:100%;height:auto;display:block}
.tier h3{font:800 34px/1.05 Spectral,serif;margin:0 0 10px;color:var(--pink)}
.tier p{margin:0 0 12px}
.tier a{color:var(--pink)}
.twist{border-left:5px solid var(--pink);padding:6px 0 6px 18px;margin:26px 0;font:italic 600 21px/1.35 Spectral,serif}
details.rv{margin:18px 0;border:2px solid var(--black);background:#fff;padding:12px 16px}
details.rv summary{cursor:pointer;font:800 12px Hanken,sans-serif;letter-spacing:.16em;text-transform:uppercase}
details.rv ol{margin:12px 0 0;padding-left:20px}
details.rv li{margin:0 0 10px;font-size:17px}
.sharebtn{margin-top:6px;cursor:pointer;background:var(--pink);border-color:var(--pink);color:var(--black)}
"""

def esc(s): return E(s, quote=True)

NAV_ITEMS = [('/', 'Book', 1), ('/merch/', 'Merch', 1), ('/#secrets', 'The Secrets', 0), ('/which-bitch/', 'Which Bitch?', 0), ('/bitch-o-meter/', 'Bitch-O-Meter', 0), ('/#inside', 'Look Inside', 0)]

def nav(cur=''):
    links = ''.join(f'<a class="l{" b" if b else ""}{" on" if h==cur else ""}" href="{h}">{t}</a>' for h, t, b in NAV_ITEMS)
    return (f'<nav class="nav"><div class="wrap"><a class="brand" href="/">Every <b>Bitch</b> Has Her Way</a>'
            f'{links}<a class="l get" href="/#get">Buy</a></div></nav>')

FOOT = ('<div class="foot"><div class="wrap"><b>Every Bitch Has Her Way</b>, Secrets of the Well-Bred Bitch. By Richard J. Koret.<br>'
        '&copy; 2026 Richard J. Koret. Published by <a href="https://rainingcad.com/">Raining Cats &amp; Dogs Press</a>.<br>'
        'This book is about female dogs. Any resemblance to people you know is a compliment.</div></div>')

def head(title, desc, path, og='/img/og.jpg', extra=''):
    url = SITE + path
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">'
            f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
            f'<meta property="og:image" content="{SITE}{og}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0E0E10">'
            f'<link rel="icon" href="/favicon.svg" type="image/svg+xml"><style>{CSS}</style>{extra}</head><body>')

def buttons(light=False):
    return ('<div class="btns"><span class="btn off">Paperback coming soon</span><span class="btn off">Kindle coming soon</span></div>')

def write(path, content):
    full = os.path.join(ROOT, path.strip('/'), 'index.html') if not path.endswith('.html') else os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(content)

def idx(i): return f'{i:02d}'

# ---------------- chapter pages ----------------
def chapter_page(i):
    c = CH[i]
    prev_ = CH[i-1] if i > 0 else None
    next_ = CH[i+1] if i < len(CH)-1 else None
    label = c['n'] if c['n'] in ('Introduction', 'Conclusion') else f'Chapter {c["n"]}'
    pn = '<div class="pn">'
    pn += (f'<a href="/secrets/{prev_["slug"]}/"><span>Previous</span>{E(prev_["title"])}</a>' if prev_ else '<span></span>')
    pn += (f'<a href="/secrets/{next_["slug"]}/"><span>Next</span>{E(next_["title"])}</a>' if next_ else '<a href="/#get"><span>That is all of them</span>Get the book</a>')
    pn += '</div>'
    ex = ''.join(f'<li>{E(x)}</li>' for x in c['ex'])
    cap = ' '.join(c['cap'])
    body = (head(f'{c["title"]}, Every Bitch Has Her Way', c['teaser'], f'/secrets/{c["slug"]}/', og=f'/img/ch{idx(i)}.webp')
            + nav('/#secrets')
            + f'<div class="wrap"><div class="ch"><img class="pt" src="/img/ch{idx(i)}.webp" width="900" alt="Illustrated portrait for {esc(c["title"])}">'
            + f'<div><p class="kick">{label}</p><h1>{E(c["title"])}</h1><p class="cap">{E(cap)}</p>'
            + f'<p class="lede">{E(c["teaser"])}</p><ul class="ex">{ex}</ul></div></div>'
            + pn
            + '<div class="getbox"><b>Read the rest of her secrets.</b>Seventeen portraits. Sixteen breeds. One uncomfortable mirror.'
            + buttons() + '</div></div>' + FOOT + '</body></html>')
    write(f'/secrets/{c["slug"]}/', body)

# ---------------- home ----------------
def home():
    cards = ''
    for i, c in enumerate(CH):
        label = c['n'] if c['n'] in ('Introduction', 'Conclusion') else f'Chapter {c["n"]}'
        cards += (f'<a class="card" href="/secrets/{c["slug"]}/"><img loading="lazy" src="/img/t{idx(i)}.webp" width="420" height="560" alt="{esc(c["title"])} portrait">'
                  f'<div class="n">{label}</div><b>{E(c["title"])}</b><p class="t">{E(c["teaser"])}</p></a>')
    rules = [("A bitch knows what she wants. Not always.", "Meet the Bitch"),
             ("Size is information. Not destiny.", "The Underbitch"),
             ("Control is power with a leash.", "The Bitch on the Line"),
             ("She doesn't audition. She occupies the present.", "Big Bitch Energy"),
             ("Luck, in a bitch, is suspicious. Luck, in a bastard, is talent.", "Lucky Bitch"),
             ("Not every tree is worth barking at.", "Bitching Up the Wrong Tree")]
    rl = ''.join(f'<blockquote>{E(q)}<span>{E(s)}</span></blockquote>' for q, s in rules)
    gifts = ["The Border Collie who cannot stop organizing your calendar.",
             "The Chihuahua who runs the boardroom and cannot be seen above the table.",
             "The Afghan Hound who left town with the top down and never said goodbye.",
             "The friend who left the group chat and is thriving.",
             "Your sister. Obviously.",
             "Whoever is quietly becoming a better bitch."]
    gl = ''.join(f'<li>{E(g)}</li>' for g in gifts)
    look = ''.join(f'<a href="/img/in{k}.webp"><img loading="lazy" src="/img/in{k}.webp" width="660" height="990" alt="Sample page {k} of Every Bitch Has Her Way"></a>' for k in range(1, 6))
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "Book", "name": "Every Bitch Has Her Way",
                         "alternativeHeadline": "Secrets of the Well-Bred Bitch", "author": {"@type": "Person", "name": "Richard J. Koret"},
                         "publisher": {"@type": "Organization", "name": "Raining Cats & Dogs Press"}, "inLanguage": "en", "url": SITE + "/"})
    h = (head('Every Bitch Has Her Way by Richard J. Koret',
              'Secrets of the Well-Bred Bitch. Seventeen portraits of the she-dogs who run the world. Deadpan, warm and inspiring. A gift book for the bitch in your life.',
              '/', extra=f'<script type="application/ld+json">{jsonld}</script>')
         + nav('/')
         + '<header class="hero"><div class="wrap"><img class="cov" src="/img/cover.webp" width="900" height="1350" alt="Every Bitch Has Her Way cover">'
         + '<div><p class="kick">A gift book for the bitch in your life</p><h1>Every Bitch<span class="p">Has Her Way</span></h1>'
         + '<p class="tag">What she-dogs know that humans forget.</p>'
         + '<p class="s">Secrets of the Well-Bred Bitch. Seventeen original portraits. Deadpan. Warm. Inspiring. By Richard J. Koret.</p>'
         + buttons() + '<div class="btns"><a class="btn main" href="#secrets">Meet the bitches</a><a class="btn" href="/which-bitch/">Which bitch are you?</a></div></div></div></header>'
         + '<section class="band"><div class="wrap"><p>This book is about a certain type of woman.<br>This book is about female dogs.<br><b>If you have a problem with that, this book is for you.</b></p></div></section>'
         + '<section class="sec"><div class="wrap"><h2>The Border Collie who cannot stop <span class="p">organizing.</span></h2>'
         + '<p class="lede">The Chihuahua who runs the boardroom but cannot be seen above the table. The Afghan Hound who left town with the top down and never said goodbye.</p>'
         + '<p class="lede">Every she-dog carries wisdom most humans spend a lifetime trying to acquire. We tell their secrets, so you can become a better bitch.</p></div></section>'
         + f'<section class="sec" id="secrets" style="padding-top:0"><div class="wrap"><h2>Sixteen breeds. <span class="p">One uncomfortable mirror.</span></h2>'
         + f'<p class="lede">Every chapter is a she-dog, a lesson and a portrait. Pick one and see how long you last.</p><div class="grid">{cards}</div></div></section>'
         + f'<section class="rules"><div class="wrap"><h2>The house rules of the <span class="p">well-bred bitch.</span></h2><div class="rl">{rl}</div></div></section>'
         + '<section class="quizband"><div class="wrap"><h2>Which bitch <span class="p">are you?</span></h2><p class="lede">Five questions. No wrong answers. Several uncomfortable ones. Then find out how much of a bitch you really are.</p><div class="btns" style="justify-content:center"><a class="btn dark" href="/which-bitch/">Which breed?</a><a class="btn dark" href="/bitch-o-meter/">Bitch-O-Meter</a></div></div></section>'
         + f'<section class="sec" id="inside"><div class="wrap"><h2>Look <span class="p">inside.</span></h2><p class="lede">Short sentences. Long pauses. Every chapter opens with a full page portrait.</p><div class="look">{look}</div></div></section>'
         + f'<section class="sec" style="padding-top:0"><div class="wrap"><h2>Buy it for <span class="p">her.</span></h2><ul class="gifts">{gl}</ul></div></section>'
         + '<section class="sec" id="get" style="padding-top:0"><div class="wrap"><div class="getbox"><b>Get Every Bitch Has Her Way</b>Paperback, 6 x 9 in, full color, 114 pages. Also on Kindle.'
         + buttons() + '</div></div></section>'
         + FOOT + '</body></html>')
    write('/', h)

# ---------------- quiz ----------------
QUIZ = {
 'qs': [
  ("Your calendar is", ["Color coded. I also did yours.", "Mine, yours and the boardroom's.", "A suggestion.", "By invitation only.", "Whatever time I arrive.", "Lunch, with gaps for more lunch."]),
  ("Someone cuts the line. You", ["Reorganize the line.", "Look up. Way up. Then speak.", "Leave. Better line elsewhere.", "Stare. Calmly. Until they notice.", "Let them. I am in no hurry.", "Check if they have snacks."]),
  ("Friday night is", ["Planning Saturday.", "Closing a deal and a bottle.", "A convertible. No destination.", "Whoever is on the list.", "A table in the sun. Mine.", "Dinner. Then dessert. Then a second dinner."]),
  ("Your secret weapon is", ["A spreadsheet.", "Confidence taller than I am.", "Leaving without a goodbye.", "One look.", "Impeccable timing.", "Genuine enthusiasm."]),
  ("At the end of the party you", ["Stack the plates.", "Have already taken over the playlist.", "Are gone. No one saw you go.", "Decide who gets a ride home.", "Leave on your own schedule.", "Take leftovers. Apologize to no one."]),
 ],
 'res': [
  ("The Border Collie", "02", "You cannot stop organizing. You herd people, deadlines and sometimes the entire neighborhood. The sheep are not consulted. They are better off.", "every-bitch-needs-a-job"),
  ("The Chihuahua", "04", "You run the boardroom and nobody can see you above the table. They will notice eventually. It will be too late.", "the-underbitch"),
  ("The Afghan Hound", "03", "Top down. No destination. You leave town without announcement, explanation or farewell and somehow everyone is fine with it.", "bitches-off-the-leash"),
  ("The Doberman", "09", "You decide who gets past the velvet rope. There is no appeals process. The sign on the gate is a courtesy.", "beware-of-the-bitch"),
  ("The Poodle", "00", "You arrive ten minutes late, pick the table in the sun and the block rearranges itself. Not because it was empty. Because it was yours.", "meet-the-bitch"),
  ("The Labrador", "11", "You eat. You love. You apologize to no one. Everyone wants to sit near you and nobody can explain why.", "bitching-up-the-wrong-tree"),
 ]
}

def quiz():
    qs = ''
    for qi, (q, opts) in enumerate(QUIZ['qs']):
        o = ''.join(f'<label><input type="radio" name="q{qi}" value="{k}"><span>{E(t)}</span></label>' for k, t in enumerate(opts))
        qs += f'<fieldset class="q"><legend>{qi+1}. {E(q)}</legend>{o}</fieldset>'
    res = json.dumps([{"name": n, "img": f"/img/ch{im}.webp", "text": t, "slug": s} for n, im, t, s in QUIZ['res']])
    js = ("const R=" + res + ";"
          "const f=document.getElementById('qz'),out=document.getElementById('res'),msg=document.getElementById('msg');"
          "f.addEventListener('submit',function(e){e.preventDefault();const c=[0,0,0,0,0,0];let n=0;"
          "for(let i=0;i<5;i++){const v=f.querySelector('input[name=q'+i+']:checked');if(v){c[+v.value]++;n++}}"
          "if(n<5){msg.textContent='Answer all five. She does not leave things unfinished.';return}msg.textContent='';"
          "let b=0;for(let i=1;i<6;i++){if(c[i]>c[b])b=i}const r=R[b];"
          "out.innerHTML='<img src=\"'+r.img+'\" alt=\"\"><div><p class=\"kick\">You are</p><h3>'+r.name+'</h3><p>'+r.text+'</p><p><a href=\"/secrets/'+r.slug+'/\">Read her chapter</a> &middot; <a href=\"/bitch-o-meter/\">How much of a bitch are you?</a></p></div>';"
          "out.classList.add('on');out.scrollIntoView({behavior:'smooth',block:'center'})});")
    h = (head('Which Bitch Are You? Every Bitch Has Her Way', 'Five questions. Six she-dogs. Find out which bitch you are.', '/which-bitch/')
         + nav('/which-bitch/')
         + '<div class="wrap" style="max-width:760px;padding-top:50px"><p class="kick" style="color:var(--pink-deep)">The quiz</p><h1 style="color:var(--black)">Which bitch <span class="p">are you?</span></h1>'
         + '<p class="lede">Five questions. Six breeds. Answer fast. She would.</p>'
         + f'<form id="qz" novalidate>{qs}<button class="btn dark" type="submit">Reveal me</button> <span id="msg" style="font:700 14px Hanken,sans-serif;color:var(--pink-deep);margin-left:10px"></span></form>'
         + '<div id="res" class="res" aria-live="polite"></div>'
         + '<div class="getbox" style="margin-top:50px"><b>Want the full pack?</b>Sixteen breeds, seventeen portraits, one uncomfortable mirror.' + buttons() + '</div></div>'
         + FOOT + f'<script>{js}</script></body></html>')
    write('/which-bitch/', h)

METER = [
 ("Someone cuts in line at the coffee shop. You", [
   ("Tap their shoulder and announce it to the whole cafe.",1),
   ("Say \"no worries!\" and replay it in your head for six hours.",0),
   ("Smile, let them go, and quietly note which barista likes you better.",2),
   ("Order second, tip better, and let them wonder why they feel small.",3)]),
 ("Your friend is forty minutes late and texts \"omw!!\" You", [
   ("Send a screenshot of the clock and three knife emojis.",1),
   ("Apologize for being early.",0),
   ("Reply \"no rush!!\" and start a group chat without her.",2),
   ("Order the appetizer, eat it slowly, and greet her like it's seven o'clock.",3)]),
 ("A coworker presents your idea as their own. You", [
   ("Slam the door so hard it echoes in HR.",1),
   ("Tell your cat all about it later.",0),
   ("Compliment them warmly, then forward the original email to the whole team \"for context.\"",2),
   ("Say \"Glad you like it. Here are the next three steps,\" and hand out the steps.",3)]),
 ("At a dinner party someone says, \"You should really be nicer.\" You", [
   ("Deliver a seven minute speech with slides.",1),
   ("Cry in the bathroom for forty minutes, then apologize to the hostess.",0),
   ("Agree loudly, then be nicer to everyone except them for the rest of the night.",2),
   ("Say \"Noted,\" and keep eating.",3)]),
 ("Your ex texts \"hey stranger\" at one in the morning. You", [
   ("Write four paragraphs, delete them, write them again.",1),
   ("Reply \"Missed you too!\"",0),
   ("Reply in four seconds: \"Who is this?\" You saved the number as DO NOT.",2),
   ("Leave it unread until Thursday, then send \"Just saw this. Hope you're well.\"",3)]),
 ("The waiter brings the wrong dish. You", [
   ("Send it back with a note about your disappointment and his tip.",1),
   ("Eat it. It's fine. It's probably fine.",0),
   ("Photograph it for a review before he leaves the table.",2),
   ("Say \"I ordered the other one,\" pleasantly, once, and wait.",3)]),
 ("Someone invites you to a \"quick call\" that could have been an email. You", [
   ("Reply all with a six paragraph critique of calendars.",1),
   ("Say yes, join early, and bring snacks.",0),
   ("Accept, mute yourself, and fold laundry.",2),
   ("Say \"Happy to, send an agenda.\" No agenda arrives. You never join.",3)]),
 ("Your sister asks to borrow your favorite jacket. You", [
   ("Say \"Absolutely not,\" and count the buttons.",1),
   ("Say \"Of course! Keep it forever!\"",0),
   ("Say yes, then wear it to her birthday dinner.",2),
   ("Say \"Sure,\" and attach the dry cleaning receipt.",3)]),
 ("A stranger on the train tells you to smile. You", [
   ("Shout \"Make me!\" and turn the whole car's head.",1),
   ("Smile. Hate yourself.",0),
   ("Smile at him until he gets nervous and changes seats.",2),
   ("Say \"Wow,\" return to your book, and turn the page. Slowly.",3)]),
 ("It's your birthday and nobody planned anything. You", [
   ("Wait by the phone, eat cake alone, and post a sad story.",1),
   ("Say \"it's fine!\" fourteen times.",0),
   ("Cancel everyone else's plans out of principle.",2),
   ("Plan your own party, invite the right six, and hand out hats.",3)]),
]
TIERS = [
 (0, "The Puppy", 4, "You apologize to furniture and say sorry when someone bumps into you. The world adores you and takes advantage of that. Start with Chapter Four, The Underbitch.", "the-underbitch"),
 (20, "The Desperate Bitch", 14, "Big feelings, big volume, and one eye on the scoreboard. You care and everybody knows it. The neighbor's boat is still on your mind. Try Chapter Fourteen.", "desperate-bitches"),
 (40, "The Bitch on the Line", 5, "You hold the line most days. Sometimes you explain it. Nobody needed the explanation. Chapter Five will tighten things up.", "the-bitch-on-the-line"),
 (60, "Beware of the Bitch", 9, "Calm, clear and slightly terrifying. The velvet rope is yours, and you know exactly who is on the list. Chapter Nine is your mirror.", "beware-of-the-bitch"),
 (80, "The Alpha Bitch", 15, "You didn't raise your voice. You didn't need to. Nobody voted and nobody objected. Chapter Fifteen was written about you.", "the-alpha-bitch"),
]

def meter():
    qs = ''
    for qi, (q, opts) in enumerate(METER):
        qs += f'<fieldset class="q" data-q="{qi}"><legend>{qi+1}. {E(q)}</legend><div class="opts"></div></fieldset>'
    data = json.dumps({"q": [{"q": q, "a": [{"t": t, "s": sc} for t, sc in opts]} for q, opts in METER],
                       "tiers": [{"min": m, "name": n, "img": f"/img/ch{i:02d}.webp", "text": t, "slug": sl} for m, n, i, t, sl in TIERS]}, ensure_ascii=False)
    js = ("const D=" + data + ";"
          "const f=document.getElementById('mz'),msg=document.getElementById('mmsg'),out=document.getElementById('mres');"
          "function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/\"/g,'&quot;')}"
          "const ans=[];"
          "f.querySelectorAll('fieldset').forEach(function(fs,qi){const o=D.q[qi].a.map(function(a,k){return {t:a.t,s:a.s}});"
          "for(let i=o.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const x=o[i];o[i]=o[j];o[j]=x}"
          "fs.querySelector('.opts').innerHTML=o.map(function(a,k){return '<label><input type=\"radio\" name=\"m'+qi+'\" value=\"'+a.s+'\"><span>'+esc(a.t)+'</span></label>'}).join('')});"
          "f.addEventListener('submit',function(e){e.preventDefault();let tot=0,n=0;"
          "for(let i=0;i<D.q.length;i++){const v=f.querySelector('input[name=m'+i+']:checked');if(v){tot+=+v.value;n++}}"
          "if(n<D.q.length){msg.textContent='Answer all ten. She finishes what she starts.';return}msg.textContent='';"
          "const pct=Math.round(tot/(D.q.length*3)*100);let t=D.tiers[0];D.tiers.forEach(function(x){if(pct>=x.min)t=x});"
          "const best=D.q.map(function(q,i){const b=q.a.reduce(function(m,a){return a.s>m.s?a:m},q.a[0]);return '<li>'+esc(b.t)+'</li>'}).join('');"
          "out.innerHTML='<p class=\"kick\" style=\"color:var(--pink-deep)\">Your Bitch-O-Meter reading</p><p class=\"pct\" id=\"pc\">0%</p><div class=\"bar\"><i id=\"bi\"></i></div>'"
          "+'<div class=\"tier\"><img src=\"'+t.img+'\" alt=\"\"><div><p class=\"kick\">You are</p><h3>'+esc(t.name)+'</h3><p>'+esc(t.text)+'</p><p><a href=\"/secrets/'+t.slug+'/\">Read her chapter</a></p></div></div>'"
          "+'<p class=\"twist\">Plot twist: the loudest answers scored lower than the calm ones. In this book, being a bitch is about timing, not volume.</p>'"
          "+'<details class=\"rv\"><summary>Show me the top answers</summary><ol>'+best+'</ol></details>'"
          "+'<button class=\"btn sharebtn\" id=\"sh\" type=\"button\">Share my score</button> <a class=\"btn dark\" href=\"/which-bitch/\">Now find your breed</a>';"
          "out.classList.add('on');out.scrollIntoView({behavior:'smooth',block:'start'});"
          "requestAnimationFrame(function(){document.getElementById('bi').style.width=pct+'%'});"
          "let c=0;const el=document.getElementById('pc');const iv=setInterval(function(){c+=Math.max(1,Math.round(pct/30));if(c>=pct){c=pct;clearInterval(iv)}el.textContent=c+'%'},30);"
          "document.getElementById('sh').addEventListener('click',function(){const text='I scored '+pct+'% on the Bitch-O-Meter: '+t.name+'. How much of a bitch are you?';const url='https://everybitch.com/bitch-o-meter/';"
          "if(navigator.share){navigator.share({title:'Bitch-O-Meter',text:text,url:url}).catch(function(){})}"
          "else if(navigator.clipboard){navigator.clipboard.writeText(text+' '+url).then(function(){document.getElementById('sh').textContent='Copied'})}});"
          "});")
    h = (head('How Much of a Bitch Are You, Really? Every Bitch Has Her Way', 'Ten questions. Funny answers. The right one is not the one you think. Find your reading on the Bitch-O-Meter.', '/bitch-o-meter/')
         + nav('/bitch-o-meter/')
         + '<div class="wrap" style="max-width:760px;padding-top:50px"><p class="kick" style="color:var(--pink-deep)">The Bitch-O-Meter</p>'
         + '<h1 style="color:var(--black)">How much of a bitch <span class="p">are you, really?</span></h1>'
         + '<p class="lede">Ten questions. Every answer is funny. Only one is right, and it is probably not the one you want to pick.</p>'
         + f'<form id="mz" novalidate>{qs}<button class="btn dark" type="submit">Read my meter</button> <span id="mmsg" style="font:700 14px Hanken,sans-serif;color:var(--pink-deep);margin-left:10px"></span></form>'
         + '<div id="mres" class="mres" aria-live="polite"></div>'
         + '<div class="getbox" style="margin-top:50px"><b>Meet the real thing.</b>Sixteen breeds, seventeen portraits, one uncomfortable mirror.' + buttons() + '</div></div>'
         + FOOT + f'<script>{js}</script></body></html>')
    write('/bitch-o-meter/', h)

def merch():
    strip = ''.join(f'<a class="card" href="/secrets/{CH[i]["slug"]}/"><img loading="lazy" src="/img/t{idx(i)}.webp" width="420" height="560" alt="{esc(CH[i]["title"])} portrait"></a>' for i in (0, 3, 4, 9, 15))
    h = (head('Merch, Every Bitch Has Her Way', 'Mugs, tees and totes for the well-bred bitch. Coming soon to Etsy.', '/merch/')
         + nav('/merch/')
         + '<div class="wrap" style="padding-top:50px"><p class="kick" style="color:var(--pink-deep)">Merch</p><h1 style="color:var(--black)">For the well-bred <span class="p">bitch.</span></h1>'
         + '<p class="lede">Mugs, tees and totes, each with a she-dog from the book. Coming soon to Etsy.</p>'
         + f'<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">{strip}</div>'
         + '<div class="getbox" style="margin-top:44px"><b>Not sure which bitch you are?</b>Take the quiz first. The merch will match.<div class="btns"><a class="btn dark" href="/which-bitch/">Take the quiz</a></div></div></div>'
         + FOOT + '</body></html>')
    write('/merch/', h)

def misc():
    open(os.path.join(ROOT, 'favicon.svg'), 'w').write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#0E0E10"/>'
        '<g fill="#FF1493"><ellipse cx="32" cy="42" rx="13" ry="11"/><ellipse cx="15" cy="27" rx="6" ry="8"/><ellipse cx="26" cy="17" rx="6" ry="8"/>'
        '<ellipse cx="38" cy="17" rx="6" ry="8"/><ellipse cx="49" cy="27" rx="6" ry="8"/></g></svg>')
    open(os.path.join(ROOT, '_headers'), 'w').write('/img/*\n  Cache-Control: public, max-age=604800\n/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
    urls = ['/', '/which-bitch/', '/bitch-o-meter/', '/merch/'] + [f'/secrets/{c["slug"]}/' for c in CH]
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(f'<url><loc>{SITE}{u}</loc></url>' for u in urls) + '</urlset>')
    open(os.path.join(ROOT, '404.html'), 'w').write(head('Not found, Every Bitch Has Her Way', 'Page not found.', '/404.html')
        + nav() + '<div class="wrap" style="padding:80px 20px;text-align:center"><h1 style="color:var(--black)">She left.<span class="p">No explanation.</span></h1><p class="lede" style="margin:0 auto 24px">That page is gone. <a href="/" style="color:var(--pink-deep)">Back to the pack.</a></p></div>' + FOOT + '</body></html>')

if __name__ == '__main__':
    home(); quiz(); meter(); merch(); misc()
    for i in range(len(CH)): chapter_page(i)
    print('built', len(CH), 'chapters')
