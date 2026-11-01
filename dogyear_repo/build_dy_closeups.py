#!/usr/bin/env python3
"""Use dog close-ups on the holiday pages. Usage: build_dy_closeups.py IMGDIR SITEDIR   (IMGDIR holds dclose01.png .. dclose12.png)"""
import os,re,sys
from PIL import Image
IMG,SITE=sys.argv[1],sys.argv[2]; DY=f"{SITE}/DY2027"
def save(im,path,size,q=80): im.resize(size,Image.LANCZOS).convert('RGB').save(path,'WEBP',quality=q,method=6)
done=[]
for h,off,mx in (('holiday1',0,7),('holiday2',7,5)):
    for k in range(1,mx+1):
        n=k+off; f=f"{IMG}/dclose{n:02d}.png"
        if not os.path.exists(f): print("missing close-up",n); continue
        im=Image.open(f); d=f"{DY}/{h}"
        save(im,f"{d}/c{k}.webp",(1086,1448)); save(im,f"{d}/ct{k}.webp",(480,640),75)
        p=f"{d}/{k}/index.html"; t=open(p,encoding='utf-8').read()
        t=re.sub(rf'(<img class=big src="/DY2027/{h}/)(?:{k}|c{k})(\.webp")',rf'\g<1>c{k}\2',t,count=1)
        open(p,'w',encoding='utf-8').write(t); done.append(n)
    p=f"{DY}/{h}/index.html"; t=open(p,encoding='utf-8').read()
    for k in range(1,mx+1):
        if os.path.exists(f"{DY}/{h}/ct{k}.webp"): t=t.replace(f'src="/DY2027/{h}/t{k}.webp"',f'src="/DY2027/{h}/ct{k}.webp"')
    hero=f"{IMG}/dclose{7 if h=='holiday1' else 12:02d}.png"
    if os.path.exists(hero): save(Image.open(hero),f"{DY}/{h}/hero.webp",(1086,1448))
    open(p,'w',encoding='utf-8').write(t)
print("close-ups placed for days",done)
