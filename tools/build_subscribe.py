"""Builds /subscribe/ (site/subscribe/index.html), the page that explains and takes the free Dog Year and Cat Year subscription.
Usage (repo root): python3 tools/build_subscribe.py   The form itself is drawn by site/sub.js; the date and the API live in worker.js (FREE_UNTIL)."""
import os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); SITE = os.path.join(ROOT, 'site'); T = os.path.join(ROOT, 'tools')
tp = open(os.path.join(SITE, 'books', 'the-cats-pajamas', 'look-inside', 'index.html'), encoding='utf-8').read()
css = re.search(r'<style>(.*?)\.book\{', tp, re.S).group(1)
nav = tp[tp.index('<body>') + 6:tp.index('<p class="kick">')]
extra = open(os.path.join(T, 'rcd.css'), encoding='utf-8').read() + '''
.sb-hero{max-width:760px}.sb-why{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;margin:18px 0 6px}
.sb-why div{border-top:3px solid var(--gold);padding:12px 0 0}.sb-why h3{font:800 21px/1.15 Spectral,serif;margin:0 0 6px}.sb-why p{margin:0;font-size:17px;line-height:1.5}
.sb-steps{counter-reset:s;list-style:none;padding:0;margin:10px 0}.sb-steps li{counter-increment:s;padding:10px 0 10px 46px;position:relative;border-bottom:1px solid var(--line)}
.sb-steps li:before{content:counter(s);position:absolute;left:0;top:8px;width:32px;height:32px;border-radius:50%;background:var(--gold-deep);color:#fff;font:800 16px/32px Hanken,sans-serif;text-align:center}
.sb-faq details{border-bottom:1px solid var(--line);padding:12px 0}.sb-faq summary{cursor:pointer;font:700 19px Spectral,serif}.sb-faq p{margin:8px 0 0}
.sb-two{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:18px 0}@media(max-width:600px){.sb-two{grid-template-columns:1fr}}
.sb-two a{display:block;text-decoration:none;border:1px solid var(--line);background:#FBFAF6;padding:16px}.sb-two b{display:block;font:800 22px Spectral,serif}.sb-two span{color:var(--soft)}
'''
title = 'Subscribe free to Dog Year and Cat Year | Raining Cats & Dogs'
desc = 'Free until December 31, 2026. Subscribe to Dog Year 2027 and Cat Year 2027 with one email and keep your notes on every device.'
body = '''<div class="sb-hero"><p class="kick">Free until December 31, 2026</p><h1>Keep every note. Subscribe free.</h1>
<p class="sub">One email. No card. No password.</p>
<p>Dog Year and Cat Year give you a new breed every week and a place to write about your own dog or cat. A free subscription keeps those notes safe and puts them on every device you use.</p></div>
<div data-rc-form="pick" id="subscribe"></div>
<h2>Why subscribe</h2>
<div class="sb-why">
<div><h3>Your notes follow you</h3><p>Write on your phone at the park. Read and add to them on your laptop that night. My Dog-Eared Notes and My Cat-Eared Notes stay in step.</p></div>
<div><h3>Nothing gets lost</h3><p>Without a subscription, notes live in one browser, and clearing it erases them. Subscribers&rsquo; notes are kept in their account.</p></div>
<div><h3>Easy from the first tap</h3><p>Type your email once. That is the whole signup. A short sync key lets you add a second device in seconds.</p></div>
<div><h3>Free right now</h3><p>The subscription is free until December 31, 2026. There is no card to enter and nothing renews on its own.</p></div>
</div>
<h2>How it works</h2>
<ol class="sb-steps"><li>Enter your email above and tap Subscribe free.</li><li>Write notes in Dog Year or Cat Year as you always do. They save to your account as you type.</li><li>On another phone or computer, subscribe again with the same email and your sync key. Your notes appear.</li></ol>
<div class="sb-two"><a href="/DY2027/"><b>Dog Year 2027</b><span>Every Day Has Its Dog</span></a><a href="/CY2027/"><b>Cat Year 2027</b><span>Every Day Has Its Cat</span></a></div>
<h2>Questions</h2><div class="sb-faq">
<details><summary>Do I need the book?</summary><p>No. The subscription is free for everyone. The paperback and Kindle edition are a lovely way to follow the year, and every date in them has a QR code that opens that day here.</p></details>
<details><summary>What happens after December 31, 2026?</summary><p>Your notes stay on your devices, and the Download all my notes button saves them as a text file at any time. We will tell you by email before anything changes.</p></details>
<details><summary>What do you do with my email?</summary><p>It is used for this subscription and for occasional news from Raining Cats &amp; Dogs. It is never sold.</p></details>
<details><summary>I lost my sync key.</summary><p>Your notes stay safe on the device where you subscribed. Write to us from the email you used and we will help you.</p></details>
</div>'''
foot = '<div class="foot">&copy; Richard J. Koret. Raining Cats &amp; Dogs. <a href="/">rainingcad.com</a></div>\n</div><script src="/menu.js" defer></script></body></html>'
d = os.path.join(SITE, 'subscribe'); os.makedirs(d, exist_ok=True)
E_ = lambda s: html.escape(s, quote=True)
open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(
    f'<!doctype html><html lang="en"><head><meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>{E_(title)}</title><meta name="description" content="{E_(desc)}">'
    f'<link rel="canonical" href="https://rainingcad.com/subscribe/"><meta property="og:title" content="{E_(title)}"><meta property="og:description" content="{E_(desc)}"><meta property="og:image" content="https://rainingcad.com/img/rcd-logo-960.webp">'
    f'<link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/menu.css">\n<style>{css}{extra}</style></head><body>{nav}{body}{foot}')
print('built /subscribe/')
