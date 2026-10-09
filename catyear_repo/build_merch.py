from PIL import Image,ImageDraw,ImageFont
T="/usr/share/texmf/fonts/opentype/public/tex-gyre/"
def font(b,s): return ImageFont.truetype(T+("texgyrepagella-bold.otf" if b else "texgyrepagella-italic.otf"),s)
picks=[(1,"Norwegian Forest Cat","BUILT FOR WINTER","NorwegianForestCat"),(4,"Burmese","HEAVY HEART. VELVET COAT.","Burmese")]
for n,breed,txt,fn in picks:
    S=f"/home/claude/rainingcad/site/CY2027/{n}/"
    tiles=[Image.open(S+f).convert('RGB') for f in ["hero.webp"]+[f"{i}.webp" for i in range(1,9)]]
    W,H=2400,2740; m=70; top=300; bot=190; g=24
    cw=(W-2*m-2*g)//3; ch=(H-top-bot-2*g)//3
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    for k,t in enumerate(tiles):
        r,c=divmod(k,3); sc=max(cw/t.width,ch/t.height); t2=t.resize((int(t.width*sc)+1,int(t.height*sc)+1),Image.LANCZOS)
        x0=(t2.width-cw)//2; y0=(t2.height-ch)//2
        im.paste(t2.crop((x0,y0,x0+cw,y0+ch)),(m+c*(cw+g),top+r*(ch+g)))
    sz=170; ft=font(1,sz)
    while d.textlength(txt,font=ft)>W-2*m: sz-=5; ft=font(1,sz)
    d.text(((W-d.textlength(txt,font=ft))/2,60),txt,font=ft,fill='#2a2a2d')
    cap=f"{breed}  ·  Cat Year 2027"; fb=font(0,100)
    d.text(((W-d.textlength(cap,font=fb))/2,H-155),cap,font=fb,fill='#2a2a2d')
    im.save(f"merch/{fn}-tee_print.png"); im.resize((640,731),Image.LANCZOS).save(f"merch/{fn}-tee_preview.jpg",quality=88)
    MW,MH=2700,1000; mug=Image.new('RGB',(MW,MH),'white')
    sz=150; fm=font(1,sz)
    lay=Image.new('RGBA',(MH,230),(255,255,255,0)); ld=ImageDraw.Draw(lay)
    while ld.textlength(txt,font=fm)>MH-60: sz-=5; fm=font(1,sz)
    ld.text(((MH-ld.textlength(txt,font=fm))/2,30),txt,font=fm,fill='#2a2a2d'); rot=lay.rotate(90,expand=True)
    tw2=(MW-2*240-5*16)//4; th=(MH-3*16)//2
    sel=[tiles[1],tiles[2],tiles[3],tiles[5],tiles[6],tiles[0],tiles[4],tiles[8]]
    for k,t in enumerate(sel):
        r,c=divmod(k,4); sc=max(tw2/t.width,th/t.height); t2=t.resize((int(t.width*sc)+1,int(t.height*sc)+1),Image.LANCZOS)
        x0=(t2.width-tw2)//2;y0=(t2.height-th)//2
        mug.paste(t2.crop((x0,y0,x0+tw2,y0+th)),(240+16+c*(tw2+16),16+r*(th+16)))
    mug.paste(rot,(5,0),rot); mug.paste(rot,(MW-235,0),rot)
    mug.save(f"merch/{fn}-mug_print.png"); mug.resize((1080,400),Image.LANCZOS).save(f"merch/{fn}-mug_preview.jpg",quality=88)
