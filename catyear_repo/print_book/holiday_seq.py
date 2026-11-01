import json,re,datetime,sys
sys.path.insert(0,'/tmp/we/tools/print_pipeline')
import make_week as mw
ROOT='/tmp/ce'; IMGD=f'{ROOT}/img/holidayseq'
ORD=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth","eleventh","twelfth"]
FOLIO='<div class="folio"><span>A Cat Year &middot; Every Day Has Its Cat</span><span class="pageno">[ # ]</span></div>'
def pages():
    a=json.load(open(f'{ROOT}/xmas/week_m1_twelve_cats_part1.json',encoding='utf-8'))
    b=json.load(open(f'{ROOT}/xmas/week_00_twelve_cats_part2.json',encoding='utf-8'))
    m=dict(a)
    m['kicker']='Holiday Season, Dec 20 to Jan 2'
    m['positioning']='Twelve days of Christmas. Seventy-eight cats. One courtyard.'
    m['story']=["Every carol has a list. This one has cats.",
     "The old song counts twelve days of gifts. Ours counts twelve days of cats, starting Sunday, December 20. A Maine Coon sits in the pear tree. Every day after that, a bigger group of a new breed joins her in the same snowy courtyard.",
     "Two Siamese talk. Three Manx mew. Four Folds creep. Five Sphynx sprint. Six Bengals bound. Seven Korats kick up the snow. Eight Ragdolls roll, nine Persians pounce, ten Munchkins march, eleven Devons dash. On New Year&rsquo;s Eve, twelve Abyssinians arch on the well.",
     "Add them up and the courtyard holds 78 cats, the exact sum of the song. The tune first appeared in print in England in 1780, in a children&rsquo;s book. The partridge, we decided, was a Maine Coon.",
     "Keep the cookies up high and the tinsel off the floor. A cat&rsquo;s idea of a present is the box.",
     "Turn the page. The Maine Coon is waiting, and she has no plan for getting down."]
    m['rank_num']='78'; m['rank_cap']='cats in all, by New Year&rsquo;s Eve'
    m['season_line']='12 days &middot; Holiday Season'
    m['glance']=[["Dates","Dec 20 to Jan 2"],["Days of the carol","1 to 12"],["Cats in all","78"],["Setting","A snowy courtyard"],["Song","The Twelve Days of Christmas"]]
    m['fblocks']=[a['fblocks'][0],["Notable Cats","Maine Coon, America&rsquo;s largest native breed. Siamese, the one with opinions. Sphynx, the one who wants the fire. Persian, the long-haired classic. Devon Rex, the pixie."],
      ["Good to Know","Lilies, tinsel and ribbon are dangerous for cats. Even a little lily pollen can harm the kidneys. Fireworks frighten many cats: give them a quiet room on New Year&rsquo;s Eve."],
      a['fblocks'][3],["By the Numbers","78 cats. 12 days. 1 pear tree."]]
    m['url_slug']='holiday1'; m['base_url']='https://rainingcad.com/CY2027'
    html=mw.build(m,IMGD)
    secs=re.findall(r'(<section class="page.*?</section>)',html,flags=re.S); hero,intro=secs[0],secs[1]
    LINES="".join("<span></span>" for _ in range(5))
    def row(i,dow,date,text,url,img,cap=None):
        qr=mw.qr_uri(url)
        capx=f'<span class="cap" style="font-family:Hanken Grotesk,sans-serif;font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:#8a6d2f;margin-left:10px">{cap}</span>' if cap else ''
        return f'''<article class="day"><a class="thumb" href="{url}"><img src="{mw.find_img(IMGD,img)}" alt=""></a>
          <div class="dbody"><div class="dhead"><span class="dow">{dow}{capx}</span><span class="date">{date}</span></div>
          <p class="dtext" style="white-space:normal;line-height:1.4">{text}</p><div class="lower"><a class="qr" href="{url}"><img src="{qr}" alt=""></a>
          <div class="write">{LINES}</div></div></div></article>'''
    start=datetime.date(2026,12,20)
    texts=[d[2] for d in a['days']]+[d[2] for d in b['days'][:5]]
    rows=[]
    for i in range(12):
        d=start+datetime.timedelta(days=i)
        url=f"https://rainingcad.com/CY2027/holiday1/{i+1}" if i<7 else f"https://rainingcad.com/CY2027/holiday2/{i-6}"
        rows.append(row(i,d.strftime('%A'),d.strftime('%b %-d'),texts[i],url,f'd{i+1:02d}',f'The {ORD[i]} day'))
    def wk(inner,head=None):
        h=f'<div class="weekhead"><h2>{head}</h2></div>' if head else ''
        return f'<section class="page wk"><div class="pad">{h}<div class="days">{inner}</div></div>{FOLIO}</section>'
    p8=wk("".join(rows[0:4]),"The Twelve Cats of Christmas")
    p9=wk("".join(rows[4:8]))
    p10=wk("".join(rows[8:12]))
    full=f'<section class="page hero"><div class="holder"><img src="{mw.find_img(IMGD,"full")}" alt="All seventy-eight cats"></div></section>'
    jan=[row(0,'Friday','Jan 1',b['days'][5][2],"https://rainingcad.com/CY2027/holiday2/6",'jan1'),
         row(0,'Saturday','Jan 2',b['days'][6][2],"https://rainingcad.com/CY2027/holiday2/7",'jan2')]
    lw_url="https://rainingcad.com/CY2027/holiday2/8"
    K='font-family:Hanken Grotesk,sans-serif;font-size:9.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#8a6d2f'
    lw=f'''<article class="day lastrow"><a class="thumb" href="{lw_url}"><img src="{mw.find_img(IMGD,'lastyear')}" alt=""></a>
          <div class="dbody"><div class="dhead"><span class="dow">Last Walk of the Week</span></div>
          <p class="dtext">The first cat of the year is already at the gate.</p><div class="lower"><a class="qr" href="{lw_url}"><img src="{mw.qr_uri(lw_url)}" alt=""></a>
          <p class="lwbody">A Norwegian Forest Cat walks out of the snow, tail high, in no hurry at all. Cats walk by themselves, and this one has somewhere to be. Follow him. The new year starts with his first step.</p></div></div></article>'''
    p12=f'''<section class="page wk"><div class="pad"><div class="weekhead"><h2>New Year Resolutions</h2></div>
      <div class="days" style="padding-top:18px"><div style="{K}">What I will do more of</div><div class="write" style="height:1.9in;margin:10px 0 26px">{"<span></span>"*6}</div>
      <div style="{K}">What I will do less of</div><div class="write" style="height:1.9in;margin:10px 0 26px">{"<span></span>"*6}</div>
      <div style="{K}">One thing I will finally do</div><div class="write" style="height:1.5in;margin-top:10px">{"<span></span>"*5}</div></div></div>{FOLIO}</section>'''
    p13=f'''<section class="page wk"><div class="pad"><div class="weekhead" style="align-items:baseline;gap:16px;border-bottom:2px solid #2A2A2D"><h2 style="font-size:64px;font-weight:900;color:#8a6d2f;letter-spacing:-.01em;line-height:1">2027</h2><h2 style="font-size:24px">The New Year Begins</h2></div>
      <div class="days">{jan[0]}{jan[1]}{lw}</div>{FOLIO}</section>'''
    return [hero,intro,p8,p9,p10,full,p12,p13]
