"""Mug wraps: slogan once, opposite the handle, 4 photos each side. Output merch/mugs/<Name>-mug_print.png (2700x1000) and -preview.jpg"""
from PIL import Image,ImageDraw,ImageFont
import numpy as np,os
T="/usr/share/texmf/fonts/opentype/public/tex-gyre/"
def font(s): return ImageFont.truetype(T+"texgyrepagella-bold.otf",s)
SITE="/home/claude/rainingcad/site"
J=[("Bulldog","DY2027/10","STUBBORN BY DESIGN"),("GoldenRetriever","DY2027/11","EVERYTHING’S GOLDEN"),("Beagle","DY2027/14","FOLLOW YOUR NOSE"),
("Dachshund","DY2027/15","LONG STORY SHORT"),("Poodle","DY2027/21","FANCY WITHOUT TRYING"),("GermanShepherd","DY2027/22","SHEP HAPPENS"),
("Labrador","DY2027/24","LABSOLUTELY!"),("Corgi","DY2027/26","BORN TO LOAF"),("Pug","DY2027/29","COFFEE PUG"),
("GermanShorthairedPointer","DY2027/39","WHAT’S YOUR POINT?"),("FrenchBulldog","DY2027/44","OUI, OUI, OUI"),("Rottweiler","DY2027/45","TOUGH OUTSIDE, TEDDY INSIDE"),
("NorwegianForestCat","CY2027/1","BUILT FOR WINTER"),("Burmese","CY2027/4","HEAVY HEART. VELVET COAT.")]
MW,MH=2700,1000; os.makedirs("merch/mugs",exist_ok=True)
def lines(txt):
    if len(txt)<=17: return [txt]
    w=txt.split(' '); best=None
    for i in range(1,len(w)):
        a,b=' '.join(w[:i]),' '.join(w[i:]); sc=abs(len(a)-len(b))
        if best is None or sc<best[0]: best=(sc,[a,b])
    return best[1]
def wrap(src,txt):
    t=[Image.open(f"{SITE}/{src}/{f}.webp").convert('RGB') for f in ["hero","1","2","3","4","5","6","7","8"]]
    L=lines(txt); sw=260 if len(L)==1 else 420; edge=int(MW*.08); g=16
    colw=(MW//2-edge-sw//2-g*2)//2; th=(MH-3*g)//2
    left=[t[0],t[1],t[2],t[3]]; right=[t[4],t[5],t[6],t[8]]
    mug=Image.new('RGB',(MW,MH),'white')
    def put(im,x,y):
        sc=max(colw/im.width,th/im.height); i2=im.resize((int(im.width*sc)+1,int(im.height*sc)+1),Image.LANCZOS)
        x0=(i2.width-colw)//2;y0=(i2.height-th)//2; mug.paste(i2.crop((x0,y0,x0+colw,y0+th)),(x,y))
    for k,im in enumerate(left): r,c=divmod(k,2); put(im,edge+c*(colw+g),g+r*(th+g))
    x2=MW-edge-2*colw-g
    for k,im in enumerate(right): r,c=divmod(k,2); put(im,x2+c*(colw+g),g+r*(th+g))
    sz=200; 
    while True:
        f=font(sz); lay=Image.new('RGBA',(MH,sw),(255,255,255,0)); ld=ImageDraw.Draw(lay)
        if max(ld.textlength(l,font=f) for l in L)<=MH-80 and sz*1.15*len(L)<=sw-30: break
        sz-=5
    y=(sw-sz*1.15*len(L))/2
    for l in L:
        ld.text(((MH-ld.textlength(l,font=f))/2,y),l,font=f,fill='#2a2a2d'); y+=sz*1.15
    rot=lay.rotate(90,expand=True); mug.paste(rot,((MW-rot.width)//2,0),rot); return mug
def preview(mug):
    PW=640; front=mug.crop((int(MW*.24),0,int(MW*.76),MH)); front=front.resize((PW,int(PW*MH/(MW*.52))),Image.LANCZOS)
    H=front.height; arr=np.array(front).astype(float); x=np.linspace(-1,1,PW); sh=0.55+0.45*np.sqrt(1-x**2*.92)
    cols=(np.arcsin(x*.93)/np.arcsin(.93)+1)/2*(PW-1); arr=arr[:,cols.astype(int),:]*sh[None,:,None]
    arr=np.clip(arr+(np.exp(-((x+.35)/.12)**2)*40)[None,:,None],0,255)
    body=Image.fromarray(arr.astype('uint8')); cv=Image.new('RGB',(900,H+60),'#e9e6df'); d=ImageDraw.Draw(cv); bx,by=130,25
    d.arc((bx+PW-30,by+H*.18,bx+PW+130,by+H*.78),270,90,fill='#f4f4f4',width=26)
    d.arc((bx+PW-30,by+H*.18,bx+PW+130,by+H*.78),270,90,fill='#cfcfcf',width=4)
    cv.paste(body,(bx,by)); d.ellipse((bx+40,by+H-6,bx+PW-40,by+H+24),fill='#bdbab2')
    out=Image.new('RGB',(900,cv.height+330),'#e9e6df'); out.paste(cv,(0,0)); out.paste(mug.resize((860,318),Image.LANCZOS),(20,cv.height+6))
    o=ImageDraw.Draw(out); w=int(860*.08)
    o.rectangle((20,cv.height+6,20+w,cv.height+324),outline='#c00',width=2); o.rectangle((880-w,cv.height+6,880,cv.height+324),outline='#c00',width=2)
    return out
if __name__=="__main__":
    ps=[]
    for name,src,txt in J:
        m=wrap(src,txt); m.save(f"merch/mugs/{name}-mug_print.png"); p=preview(m); p.save(f"merch/mugs/{name}-mug_preview.jpg",quality=88); ps.append(p); print(name)
    for k in range(0,len(ps),4):
        grp=ps[k:k+4]; s=Image.new('RGB',(1800,sum(1 for _ in range(0,len(grp),2))*0+ (len(grp)+1)//2*ps[0].height),'#e9e6df')
        for i,p in enumerate(grp): s.paste(p,((i%2)*900,(i//2)*ps[0].height))
        s.save(f"/tmp/mugsheet_{k//4}.jpg",quality=85)
