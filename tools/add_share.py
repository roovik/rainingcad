# Adds "Share this day" (/share-day.js) to every Dog Year and Cat Year page that has My Dog-Eared / Cat-Eared Notes.
# Safe to run again; run it after rebuilding the DY2027 or CY2027 pages.
import os, re, sys
SITE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'site')
TAG = '<script src="/share-day.js?v={v}" defer></script>'
import hashlib
v = hashlib.md5(open(os.path.join(SITE, 'share-day.js'), 'rb').read()).hexdigest()[:8]
n = 0
for book in ('DY2027', 'CY2027'):
    for root, _, files in os.walk(os.path.join(SITE, book)):
        if 'index.html' not in files: continue
        p = os.path.join(root, 'index.html'); s = open(p, encoding='utf-8').read()
        if 'id="notes"' not in s: continue
        t = re.sub(r'<script src="/share-day\.js[^"]*" defer></script>', '', s).replace('</body>', TAG.format(v=v) + '</body>', 1)
        if t != s: open(p, 'w', encoding='utf-8').write(t); n += 1
print(n, 'pages')
