"""Pull the opening of each chapter from the book text into excerpts.json (verbatim)."""
import re, json, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/eb/eb.txt'
SMALL = {'a','an','the','of','to','and','in','on','with','for','up','at','by','or','is','it','not'}
def is_head(line):
    w = line.split()
    if not w or len(w) > 8 or re.search(r'[.,!?;:—]$', line): return False
    if re.search(r'[.!?;:—]', line): return False
    return w[0][0].isupper() and all(x[0].isupper() or x.lower() in SMALL for x in w)
L = open(SRC, encoding='utf-8').read().split('\n')
starts = [i for i, l in enumerate(L) if i > 70 and re.match(r'^\s*(INTRODUCTION|CHAPTER [A-Z]+|CONCLUSION)\s*$', l)]
res = []
for k, s in enumerate(starts):
    e = starts[k+1] if k+1 < len(starts) else len(L)
    chunk = L[s+1:e]
    j = next(i for i, l in enumerate(chunk) if re.match(r'^\s*\d+\s*$', l))
    blocks = []; cur = []
    for l in chunk[j+1:]:
        if re.match(r'^\s*\d+\s*$', l): continue
        if not l.strip():
            if cur: blocks.append(cur); cur = []
        else: cur.append(l.strip())
    if cur: blocks.append(cur)
    items = []
    for b in blocks:
        if len(b) > 1 and is_head(b[0]):
            items.append(['h', b[0]]); b = b[1:]
        t = ' '.join(b)
        if t.startswith('Small Dog. Big Opinions. '):
            items.append(['h', 'Small Dog. Big Opinions.']); t = t[len('Small Dog. Big Opinions. '):]
        items.append(['p', t])
    pick = []; n = 0; w = 0
    for t, x in items:
        if t == 'h' and n >= 4 and w >= 60: break
        pick.append([t, x])
        if t == 'p': n += 1; w += len(x.split())
        if n >= 8: break
    while pick[-1][0] == 'h': pick.pop()
    res.append(pick)
json.dump(res, open('tools/excerpts.json', 'w'), ensure_ascii=False, indent=1)
for k, p in enumerate(res):
    for t, x in p:
        if t == 'p' and re.match(r'^([A-Z][a-z\']+ ){2,6}[A-Z][a-z]+ [A-Z]', x) and not re.search(r'^[A-Z][a-z]+ [a-z]', x): print('CHECK', k, x[:70])
    print(k, [x for t, x in p if t == 'h'])
