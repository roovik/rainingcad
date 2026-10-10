import json,glob,base64,io,html,qrcode,os,sys
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
sys.path.insert(0,'.')
import build_mugs_all as BM
SITE="/home/claude/rainingcad/site"; OUT="merch/printify_cats"; os.makedirs(OUT+"/Mugs_15oz_2475x1275",exist_ok=True)
T="/usr/share/texmf/fonts/opentype/public/tex-gyre/"
INK='#2A2A2D'; GOLD='#876217'
PICK=[(1,"norwegian-forest-cat","NorwegianForestCat","VIKING QUEEN")]
def tf(b,s): return ImageFont.truetype(T+("texgyrepagella-bold.otf" if b else "texgyrepagella-italic.otf"),s)
def tee_front(n,breed,txt,out):
    S=f"{SITE}/CY2027/{n}/"; tiles=[Image.open(S+f).convert('RGB') for f in ["hero.webp"]+[f"{i}.webp" for i in range(1,9)]]
    W,H=3852,4398; m=110; top=480; bot=300; g=36
    cw=(W-2*m-2*g)//3; ch=(H-top-bot-2*g)//3
    im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    for k,t in enumerate(tiles):
        r,c=divmod(k,3); sc=max(cw/t.width,ch/t.height); t2=t.resize((int(t.width*sc)+1,int(t.height*sc)+1),Image.LANCZOS)
        x0=(t2.width-cw)//2;y0=(t2.height-ch)//2; im.paste(t2.crop((x0,y0,x0+cw,y0+ch)),(m+c*(cw+g),top+r*(ch+g)))
    sz=270;ft=tf(1,sz)
    while d.textlength(txt,font=ft)>W-2*m: sz-=5;ft=tf(1,sz)
    d.text(((W-d.textlength(txt,font=ft))/2,90),txt,font=ft,fill=INK)
    cap=f"{breed}  ·  Cat Year 2027"; fb=tf(0,160)
    d.text(((W-d.textlength(cap,font=fb))/2,H-250),cap,font=fb,fill=INK); im.save(out)
def fu(p,m): return 'data:%s;base64,%s'%(m,base64.b64encode(open(p,'rb').read()).decode())
def tee_back(w,out):
    n=w['num']; q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=30,border=2); q.add_data(f"https://rainingcad.com/CY2027/{n}/"); q.make(fit=True)
    buf=io.BytesIO(); q.make_image(fill_color=INK,back_color='white').convert('RGB').save(buf,'PNG'); qr='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
    css=f"@font-face{{font-family:Spectral;font-weight:400;src:url({fu(SITE+'/fonts/spectral-400.woff2','font/woff2')})}}@font-face{{font-family:Spectral;font-weight:400;font-style:italic;src:url({fu(SITE+'/fonts/spectral-400i.woff2','font/woff2')})}}@font-face{{font-family:Spectral;font-weight:800;src:url({fu(SITE+'/fonts/spectral-800.woff2','font/woff2')})}}@font-face{{font-family:Hanken;font-weight:100 900;src:url({fu(SITE+'/fonts/hanken.woff2','font/woff2')})}}"
    paras=w['story'][:4]
    facts=''.join(f"<div class=fr><span>{html.escape(a)}</span><b>{html.escape(b)}</b></div>" for a,b in w['glance'])
    blks=''.join(f"<div class=bl><h4>{html.escape(a)}</h4><p>{html.escape(b)}</p></div>" for a,b in w['fblocks'][:5])
    first=html.escape(paras[0]); rest=''.join(f"<p>{html.escape(p)}</p>" for p in paras[1:])
    h=f"""<style>{css}*{{box-sizing:border-box;margin:0;padding:0}}body{{width:3852px;height:4398px;background:#fff;position:relative;padding:240px 240px}}
.k{{font:600 62px Hanken;letter-spacing:.2em;text-transform:uppercase;color:{GOLD}}}h1{{font:800 250px/1 Spectral;color:{INK};margin:50px 0 40px;max-width:2300px}}
.pos{{font:italic 400 100px/1.2 Spectral;color:{GOLD};max-width:2300px;margin-bottom:100px}}
.main{{position:absolute;left:240px;top:1250px;width:2300px;font:400 72px/1.42 Spectral;color:{INK}}}.main p{{margin-bottom:46px}}.dc::first-letter{{float:left;font:800 330px/.8 Spectral;color:{GOLD};padding:14px 24px 0 0}}
.side{{position:absolute;left:2680px;top:240px;width:932px;border-top:20px solid {GOLD};padding-top:50px}}
.rk{{display:flex;align-items:baseline;gap:30px}}.rk b{{font:800 230px/1 Spectral;color:{INK}}}.rk span{{font:600 52px Hanken;letter-spacing:.1em;text-transform:uppercase;color:{GOLD}}}
.cap{{font:400 56px/1.3 Hanken;color:#666;margin:20px 0 50px}}.fr{{display:flex;justify-content:space-between;border-top:3px solid #ddd;padding:26px 0;font:400 54px Hanken}}.fr span{{text-transform:uppercase;letter-spacing:.08em;color:#777;font-size:46px}}
.bl{{margin-top:56px}}.bl h4{{font:600 46px Hanken;letter-spacing:.16em;text-transform:uppercase;color:{GOLD};margin-bottom:12px}}.bl p{{font:400 56px/1.35 Spectral;color:{INK}}}
.qr{{position:absolute;left:240px;bottom:240px;display:flex;gap:70px;align-items:center}}.qr img{{width:560px;height:560px;border:8px solid #ddd}}.qr h5{{font:600 50px Hanken;letter-spacing:.14em;text-transform:uppercase;color:{GOLD};margin-bottom:14px}}.qr p{{font:400 64px/1.3 Spectral;color:{INK};width:1300px}}</style>
<div class=k>Week {n} &nbsp;·&nbsp; Cat Year 2027</div><h1>{html.escape(w['breed'])}</h1><div class=pos>{html.escape(w['positioning'])}</div>
<div class=main><p class=dc>{first}</p>{rest}</div>
<div class=side><div class=rk><b>{w['rank_num']}</b><span>{html.escape(w['rank_cap'])}</span></div><div class=cap>{html.escape(w['cap'])}</div>{facts}{blks}</div>
<div class=qr><img src="{qr}"><div><h5>Meet the breed online</h5><p>Scan for this week’s page, photos, and more.</p></div></div>"""
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={'width':3852,'height':4398}); pg.set_content(h); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(1200)
        over=pg.evaluate("(()=>{const m=document.querySelector('.main').getBoundingClientRect(),q=document.querySelector('.qr').getBoundingClientRect(),s=document.querySelector('.side').getBoundingClientRect();return [m.bottom,q.top,s.bottom]})()")
        print(w['breed'],'main bottom/qr top/side bottom',over)
        pg.screenshot(path=out,clip={'x':0,'y':0,'width':3852,'height':4398}); b.close()
if __name__=="__main__":
    for n,slug,name,txt in PICK:
        w=json.load(open(glob.glob(f"weeks/week{n:02d}_*.json")[0],encoding='utf-8'))
        tee_front(n,w['breed'],txt,f"{OUT}/{slug}_TEE_FRONT.png"); tee_back(w,f"{OUT}/{slug}_TEE_BACK.png")
        for H,path in ((1155,f"{OUT}/{slug}_MUG.png"),(1275,f"{OUT}/Mugs_15oz_2475x1275/{slug}_MUG15.png")):
            BM.MW,BM.MH=2475,H; BM.wrap(f"CY2027/{n}",txt).save(path)
        print('ok',slug)
