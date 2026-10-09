from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np
T="/usr/share/texmf/fonts/opentype/public/tex-gyre/"
def font(s): return ImageFont.truetype(T+"texgyrepagella-bold.otf",s)
picks=[(1,"NorwegianForestCat","BUILT FOR WINTER"),(4,"Burmese","HEAVY HEART. VELVET COAT.")]
MW,MH=2700,1000
for n,fn,txt in picks:
    S=f"/home/claude/rainingcad/site/CY2027/{n}/"
    t=[Image.open(S+f).convert('RGB') for f in ["hero.webp"]+[f"{i}.webp" for i in range(1,9)]]
    # slogan once, centered = opposite the handle. Handle zones = outer 8% each end.
    edge=int(MW*.08); sw=260; g=16
    colw=(MW//2-edge-sw//2-g*2)//2; th=(MH-3*g)//2
    left=[t[1],t[2],t[3],t[4]]; right=[t[5],t[6],t[7],t[8]]
    # right block faces right: use hero and strongest in the outer positions
    mug=Image.new('RGB',(MW,MH),'white')
    def put(im,x,y):
        sc=max(colw/im.width,th/im.height); i2=im.resize((int(im.width*sc)+1,int(im.height*sc)+1),Image.LANCZOS)
        x0=(i2.width-colw)//2;y0=(i2.height-th)//2; mug.paste(i2.crop((x0,y0,x0+colw,y0+th)),(x,y))
    for k,im in enumerate(left):
        r,c=divmod(k,2); put(im,edge+c*(colw+g),g+r*(th+g))
    x2=MW-edge-2*colw-g
    for k,im in enumerate(right):
        r,c=divmod(k,2); put(im,x2+c*(colw+g),g+r*(th+g))
    sz=200; f=font(sz); lay=Image.new('RGBA',(MH,300),(255,255,255,0)); ld=ImageDraw.Draw(lay)
    while ld.textlength(txt,font=f)>MH-80: sz-=5; f=font(sz)
    ld.text(((MH-ld.textlength(txt,font=f))/2,(300-sz*1.2)/2),txt,font=f,fill='#2a2a2d')
    rot=lay.rotate(90,expand=True); mug.paste(rot,((MW-rot.width)//2,0),rot)
    mug.save(f"merch/{fn}-mug_print.png")
    # mockup: front view = middle 52% of wrap on a cylinder, handle at right
    PW,PH=640,300; front=mug.crop((int(MW*.24),0,int(MW*.76),MH)).resize((PW,int(PW*MH/(MW*.52))),Image.LANCZOS)
    H=front.height; arr=np.array(front).astype(float)
    x=np.linspace(-1,1,PW); sh=0.55+0.45*np.sqrt(1-x**2*.92); 
    # squeeze edges to fake curvature
    cols=(np.arcsin(x*.93)/np.arcsin(.93)+1)/2*(PW-1)
    arr=arr[:,cols.astype(int),:]*sh[None,:,None]
    arr=np.clip(arr+ (np.exp(-((x+.35)/.12)**2)*40)[None,:,None],0,255)
    body=Image.fromarray(arr.astype('uint8'))
    cv=Image.new('RGB',(900,H+120),'#e9e6df'); d=ImageDraw.Draw(cv)
    bx=130;by=50
    # handle
    d.arc((bx+PW-30,by+H*.18,bx+PW+130,by+H*.78),270,90,fill='#f4f4f4',width=26)
    d.arc((bx+PW-30,by+H*.18,bx+PW+130,by+H*.78),270,90,fill='#cfcfcf',width=4)
    cv.paste(body,(bx,by)); d.rectangle((bx,by-10,bx+PW,by),fill='#f8f8f8')
    d.ellipse((bx+40,by+H-6,bx+PW-40,by+H+30),fill='#bdbab2')
    # wrap strip below
    cv=cv.convert('RGB'); out=Image.new('RGB',(900,cv.height+330),'#e9e6df'); out.paste(cv,(0,0))
    strip=mug.resize((860,318),Image.LANCZOS); out.paste(strip,(20,cv.height+6))
    ImageDraw.Draw(out).rectangle((20,cv.height+6,20+int(860*.08),cv.height+324),fill=None,outline='#c00',width=2)
    ImageDraw.Draw(out).rectangle((20+860-int(860*.08),cv.height+6,880,cv.height+324),outline='#c00',width=2)
    out.save(f"merch/{fn}-mug_preview.jpg",quality=90)
