import os, json, html
from meter_data import HOME, WORK, TIERS, TIER_TEXT, MEANS

E = html.escape
HERE = os.path.dirname(__file__)
QSRC = os.path.join(HERE, '..', 'qimg')

METER_CSS = """
.mt{max-width:1040px;margin:0 auto;padding:26px 20px 70px}
.hud{position:sticky;top:var(--nh,56px);z-index:20;background:var(--black);color:#fff;padding:10px 20px;display:none;border-bottom:3px solid var(--pink)}
.hud.on{display:block}
.hud .row{max-width:1000px;margin:0 auto;display:flex;gap:18px;align-items:center;font:800 11px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase}
.hud .pg{flex:1;height:8px;background:#2a2a30;position:relative}
.hud .pg i{position:absolute;left:0;top:0;bottom:0;width:0;background:var(--pink);transition:width .5s}
.hud .rd{white-space:nowrap;color:var(--pink)}
.hud .rd b{font:800 18px Spectral,serif;letter-spacing:0;color:#fff;margin-left:6px}
.intro h1{font:800 clamp(38px,7vw,68px)/1 Spectral,serif;margin:6px 0 14px}
.intro .p{color:var(--pink)}
.start{margin-top:18px}
.stage{scroll-margin-top:calc(var(--nh,56px) + 56px);display:none;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:34px;margin-top:26px;align-items:start}
.stage.on{display:grid;animation:rise .45s both}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@media(max-width:760px){.stage{grid-template-columns:1fr;gap:18px}}
.pic{position:relative;aspect-ratio:4/5;background:var(--black);box-shadow:10px 10px 0 var(--pink);overflow:hidden}
@media(max-width:760px){.pic{aspect-ratio:16/11;box-shadow:6px 6px 0 var(--pink)}}
.pic img{width:100%;height:100%;object-fit:cover;display:block}
.pic .tag{position:absolute;left:0;bottom:0;background:var(--pink);color:var(--black);font:800 11px Hanken,sans-serif;letter-spacing:.16em;text-transform:uppercase;padding:6px 12px}
.ph{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;background:repeating-linear-gradient(135deg,#FF1493 0 22px,#F0138B 22px 44px);color:var(--black);text-align:center;padding:20px}
.ph b{font:800 clamp(64px,12vw,120px)/1 Spectral,serif;color:#fff}
.ph span{font:800 12px Hanken,sans-serif;letter-spacing:.18em;text-transform:uppercase;background:var(--black);color:#fff;padding:4px 10px}
.qn{font:800 12px Hanken,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--pink-deep);margin:0 0 6px}
.qt{font:800 clamp(24px,3.4vw,34px)/1.15 Spectral,serif;margin:0 0 18px}
.ans{display:grid;gap:10px}
.ans button{all:unset;box-sizing:border-box;display:flex;gap:12px;align-items:flex-start;width:100%;cursor:pointer;background:#fff;border:2px solid var(--black);padding:12px 14px;font:19px/1.35 Spectral,serif;transition:transform .12s,box-shadow .12s,background .12s}
.ans button:hover:not([disabled]){transform:translate(-2px,-2px);box-shadow:5px 5px 0 var(--pink)}
.ans button:focus-visible{outline:3px solid var(--pink);outline-offset:2px}
.ans .k{flex:none;width:26px;height:26px;background:var(--black);color:#fff;font:800 13px/26px Hanken,sans-serif;text-align:center}
.ans button[disabled]{cursor:default;opacity:.45}
.ans button.me{opacity:1;background:var(--black);color:#fff}
.ans button.me .k{background:var(--pink);color:var(--black)}
.ans button.best{opacity:1;border-color:var(--pink);box-shadow:5px 5px 0 var(--pink)}
.rev{margin-top:18px;border:2px solid var(--black);background:#fff;padding:16px 18px;display:none}
.rev.on{display:block;animation:rise .35s both}
.bdg{display:inline-block;font:800 11px Hanken,sans-serif;letter-spacing:.16em;text-transform:uppercase;padding:4px 10px;background:var(--black);color:#fff;margin-bottom:8px}
.bdg.s3{background:var(--pink);color:var(--black)}
.roast{font:800 22px/1.25 Spectral,serif;margin:0 0 10px}
.move{margin:0 0 8px;color:var(--pink-deep)}
.why{font-style:italic;border-left:4px solid var(--pink);padding-left:12px;margin:0 0 14px;color:#444}
.next{cursor:pointer}
.fin{scroll-margin-top:calc(var(--nh,56px) + 10px);display:none;margin-top:30px}
.fin.on{display:block;animation:rise .5s both}
.fin .pct{font:800 clamp(80px,18vw,170px)/1 Spectral,serif;color:var(--pink-deep);margin:0}
.dist{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:20px 0}
.dist div{border:2px solid var(--black);background:#fff;padding:10px;text-align:center}
.dist b{display:block;font:800 34px/1 Spectral,serif;color:var(--pink-deep)}
.dist span{font:800 10px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase}
.moments{display:grid;gap:12px;margin:14px 0 26px}
.mm{border:2px solid var(--black);background:#fff;padding:12px 16px}
.mm .h{font:800 11px Hanken,sans-serif;letter-spacing:.16em;text-transform:uppercase;color:var(--pink-deep);margin:0 0 4px}
.mm p{margin:0 0 4px}
.scoring{margin:26px 0 8px}
.scoring h2{font:800 12px Hanken,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:var(--pink-deep);margin:0 0 10px}
.ladder{display:grid;grid-template-columns:repeat(4,1fr);gap:0;border:2px solid var(--black);background:#fff}
@media(max-width:640px){.ladder{grid-template-columns:1fr 1fr}}
.ladder div{padding:12px 14px;border-right:2px solid var(--black)}
.ladder div:last-child{border-right:0;background:var(--pink)}
@media(max-width:640px){.ladder div:nth-child(2){border-right:0}.ladder div:nth-child(-n+2){border-bottom:2px solid var(--black)}}
.ladder b{display:block;font:800 30px/1 Spectral,serif}
.ladder span{display:block;font:800 11px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase;margin:4px 0 6px}
.ladder i{display:block;font:italic 600 16px/1.3 Spectral,serif}
.scoring p{margin:10px 0 0;font:italic 600 18px/1.35 Spectral,serif}
.vol{display:flex;align-items:center;gap:10px;margin-top:10px;font:800 10px Hanken,sans-serif;letter-spacing:.14em;text-transform:uppercase}
.vol i{flex:1;height:6px;background:linear-gradient(90deg,var(--black),var(--pink));display:block}
.hubgrid{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin:30px 0}
@media(max-width:760px){.hubgrid{grid-template-columns:1fr}}
.hubc{display:block;text-decoration:none;background:var(--black);color:#fff;box-shadow:10px 10px 0 var(--pink);transition:transform .15s}
.hubc:hover{transform:translate(-3px,-3px)}
.hubc img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;display:block}
.hubc div{padding:20px 22px 24px}
.hubc h2{font:800 34px/1.05 Spectral,serif;margin:0 0 8px;color:var(--pink)}
.hubc p{margin:0 0 14px;color:#ddd}
.hubc .btn{pointer-events:none}
"""

RULES = ('<div class="scoring"><h2>How she scores you</h2><div class="ladder">'
         '<div><b>+0</b><span>Doormat</span><i>Apologizes to the furniture.</i></div>'
         '<div><b>+1</b><span>Loud</span><i>Wins the argument. Loses the room.</i></div>'
         '<div><b>+2</b><span>Petty</span><i>Clever. Visible. A little smug.</i></div>'
         '<div><b>+3</b><span>Perfect</span><i>Does less. Gets more.</i></div></div>'
         '<div class="vol"><span>Loud</span><i></i><span>Quiet</span></div>'
         '<p>Higher is bitchier. The coolest head wins and the loudest answer never does. Twenty questions, sixty points, one percentage.</p></div>')

def _img_url(key):
    if key.startswith('ch'):
        return f'/img/{key}.webp'
    p = f'/img/q/{key}.webp'
    return p if os.path.exists(os.path.join(HERE, '..', 'public', 'img', 'q', f'{key}.webp')) else None

def convert_new_images():
    """Turn any supplied originals in qimg/ into public/img/q/<key>.webp (900 wide)."""
    from PIL import Image
    out = os.path.join(HERE, '..', 'public', 'img', 'q')
    os.makedirs(out, exist_ok=True)
    got = []
    if os.path.isdir(QSRC):
        for f in sorted(os.listdir(QSRC)):
            stem, ext = os.path.splitext(f)
            if ext.lower() in ('.png', '.jpg', '.jpeg', '.webp'):
                im = Image.open(os.path.join(QSRC, f)).convert('RGB')
                if im.width > 900:
                    im = im.resize((900, round(im.height * 900 / im.width)))
                im.save(os.path.join(out, stem + '.webp'), quality=82)
                got.append(stem)
    return got

JS = r"""
const D=__DATA__;
function setNh(){const n=document.querySelector('.nav');if(n)document.documentElement.style.setProperty('--nh',n.offsetHeight+'px')}setNh();window.addEventListener('resize',setNh);
const $=function(i){return document.getElementById(i)};
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;')}
const N=D.q.length,LAB=['Doormat','Loud','Petty','Perfect'];
let cur=0,tot=0,locked=false;const res=[];
function shuf(a){a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));const x=a[i];a[i]=a[j];a[j]=x}return a}
function pic(q,i){return q.img?'<img src="'+q.img+'" alt="" width="900" height="1125" loading="eager">':'<div class="ph"><b>'+(i+1)+'</b><span>Portrait coming</span></div>'}
function show(i){
  const q=D.q[i];locked=false;
  const opts=shuf(q.a.map(function(t,s){return {t:t,s:s}}));
  $('stage').innerHTML='<div class="pic">'+pic(q,i)+'<span class="tag">'+esc(D.name)+' '+(i+1)+'</span></div><div><p class="qn">Question '+(i+1)+' of '+N+'</p><h2 class="qt">'+esc(q.q)+'</h2><div class="ans" role="group" aria-label="Answers">'
   +opts.map(function(o,k){return '<button type="button" data-s="'+o.s+'"><span class="k">'+'ABCD'[k]+'</span><span>'+esc(o.t)+'</span></button>'}).join('')+'</div><div class="rev" id="rev" aria-live="polite"></div></div>';
  $('stage').classList.remove('on');void $('stage').offsetWidth;$('stage').classList.add('on');
  $('stage').querySelectorAll('.ans button').forEach(function(b){b.addEventListener('click',function(){pick(b)})});
  $('pgb').style.width=(i/N*100)+'%';$('cnt').textContent=(i+1)+' / '+N;
  if(i>0)$('stage').scrollIntoView({behavior:'smooth',block:'start'});
}
function pick(b){
  if(locked)return;locked=true;
  const s=+b.dataset.s,q=D.q[cur];tot+=s;res.push(s);
  $('stage').querySelectorAll('.ans button').forEach(function(x){x.disabled=true;if(x===b)x.classList.add('me');if(+x.dataset.s===3&&s<3)x.classList.add('best')});
  const last=cur===N-1;
  const r=$('rev');
  r.innerHTML='<span class="bdg s'+s+'">+'+s+' '+LAB[s]+'</span><p class="roast">'+esc(q.r[s])+'</p>'
   +(s<3?'<p class="move"><b>Her move:</b> '+esc(q.a[3])+'</p>':'')+'<p class="why">'+esc(q.x)+'</p>'
   +'<button class="btn dark next" id="nx" type="button">'+(last?'Read my meter':'Next question')+'</button>';
  r.classList.add('on');
  $('nx').addEventListener('click',next);$('nx').focus({preventScroll:true});
  const pct=Math.round(tot/(res.length*3)*100);$('rdn').textContent=pct+'%';$('pgb').style.width=(res.length/N*100)+'%';
  r.scrollIntoView({behavior:'smooth',block:'nearest'});
}
function next(){if(cur<N-1){cur++;show(cur)}else finish()}
function finish(){
  $('stage').classList.remove('on');$('hud').classList.remove('on');
  const pct=Math.round(tot/(N*3)*100);let t=D.tiers[0],zi=0;D.tiers.forEach(function(x,k){if(pct>=x.min){t=x;zi=k}});
  const cnt=[0,0,0,0];res.forEach(function(s){cnt[s]++});
  const idx=res.map(function(s,i){return i});
  const worst=idx.slice().sort(function(a,b){return res[a]-res[b]||a-b}).slice(0,3).filter(function(i){return res[i]<3});
  const bestI=idx.filter(function(i){return res[i]===3}).slice(0,3);
  const mm=function(h,i){return '<div class="mm"><p class="h">'+h+'</p><p><b>'+esc(D.q[i].q)+'</b></p><p>'+esc(D.q[i].r[res[i]])+'</p></div>'};
  const zones=D.tiers.map(function(x,k){return '<span class="z'+(k===zi?' here':'')+'">'+esc(x.name)+'</span>'}).join('');
  const out=$('fin');
  out.innerHTML='<p class="kick" style="color:var(--pink-deep)">Your Bitch-O-Meter reading, '+esc(D.name)+' edition</p><p class="pct" id="pc">0%</p><div class="bar"><i id="bi"></i></div>'
   +'<div class="tier"><img src="'+t.img+'" alt=""><div><p class="kick">You are</p><h3>'+esc(t.name)+'</h3><p>'+esc(t.text)+'</p><p><a href="/secrets/'+t.slug+'/">Read her chapter</a></p></div></div>'
   +'<h2 class="keyh">What the number really means</h2><div class="scale"><div class="track"><i style="left:'+pct+'%"><em>You</em></i></div><div class="zones">'+zones+'</div></div>'
   +'<p class="means"><b>'+esc(D.means[zi].h)+'.</b> '+esc(D.means[zi].t)+' You scored '+tot+' of '+(N*3)+'. '+(tot===N*3?'Nothing left to fix. Please stop reading.':'The missing '+(N*3-tot)+' points are what the loud, meek and petty answers cost you.')+'</p>'
   +'<div class="dist"><div><b>'+cnt[3]+'</b><span>Perfect</span></div><div><b>'+cnt[2]+'</b><span>Petty</span></div><div><b>'+cnt[1]+'</b><span>Loud</span></div><div><b>'+cnt[0]+'</b><span>Doormat</span></div></div>'
   +'<div class="moments">'+bestI.map(function(i){return mm('Your finest hour',i)}).join('')+worst.map(function(i){return mm('Your lowest moment',i)}).join('')+'</div>'
   +'<p class="twist">Plot twist: the loudest answers scored lower than the calm ones. In this book, being a bitch is about timing, not volume.</p>'
   +'<button class="btn sharebtn" id="sh" type="button">Share my score</button> <a class="btn dark" href="'+D.other+'">Take the '+esc(D.otherName)+' test</a> <button class="btn dark" id="again" type="button">Try again</button> <a class="btn dark" href="/which-bitch/">Find your breed</a>';
  out.classList.add('on');out.scrollIntoView({behavior:'smooth',block:'start'});
  requestAnimationFrame(function(){$('bi').style.width=pct+'%'});
  let c=0;const el=$('pc');const iv=setInterval(function(){c+=Math.max(1,Math.round(pct/30));if(c>=pct){c=pct;clearInterval(iv)}el.textContent=c+'%'},30);
  $('again').addEventListener('click',function(){location.reload()});
  $('sh').addEventListener('click',function(){const text='I scored '+pct+'% on the '+D.name+' Bitch-O-Meter: '+t.name+'. How much of a bitch are you?';const url='https://everybitch.com'+D.path;
   if(navigator.share){navigator.share({title:'Bitch-O-Meter',text:text,url:url}).catch(function(){})}
   else if(navigator.clipboard){navigator.clipboard.writeText(text+' '+url).then(function(){$('sh').textContent='Copied'})}});
}
$('go').addEventListener('click',function(){$('intro').style.display='none';$('hud').classList.add('on');cur=0;show(0)});
document.addEventListener('keydown',function(e){
  if(!$('hud').classList.contains('on'))return;
  const n='1234'.indexOf(e.key);
  if(n>-1&&!locked){const b=$('stage').querySelectorAll('.ans button')[n];if(b)pick(b)}
  else if(e.key==='Enter'&&locked&&document.activeElement!==$('nx')){e.preventDefault();next()}
});
"""

def build(write, head, nav, FOOT, buttons, QTABS):
    convert_new_images()
    tests = {
        'home': dict(name='Home', title='The Home Test', data=HOME, path='/bitch-o-meter/home/', other='/bitch-o-meter/work/', otherName='Work', hero='ch06',
                     blurb='Twenty moments from your private life. Friends, family, exes, neighbors and one man in a convertible.'),
        'work': dict(name='Work', title='The Work Test', data=WORK, path='/bitch-o-meter/work/', other='/bitch-o-meter/home/', otherName='Home', hero='ch00',
                     blurb='Twenty moments from the office. Bosses, clients, rivals, interns and one sad flamingo.'),
    }
    for key, t in tests.items():
        data = {
            'name': t['name'], 'path': t['path'], 'other': t['other'], 'otherName': t['otherName'],
            'q': [{'q': x['q'], 'img': _img_url(x['img']), 'a': x['a'], 'r': x['r'], 'x': x['x']} for x in t['data']],
            'tiers': [{'min': m, 'name': n, 'img': f'/img/ch{i:02d}.webp', 'text': TIER_TEXT[key][k], 'slug': sl} for k, (m, n, i, sl) in enumerate(TIERS)],
            'means': [{'h': h, 'tx': tx, 't': tx} for h, tx in MEANS],
        }
        js = JS.replace('__DATA__', json.dumps(data, ensure_ascii=False))
        body = (head(f'The {t["name"]} Bitch-O-Meter, Every Bitch Has Her Way', t['blurb'] + ' Find your reading.', t['path'])
                + nav('/bitch-o-meter/')
                + '<div class="hud" id="hud"><div class="row"><span id="cnt">1 / 20</span><div class="pg"><i id="pgb"></i></div><span class="rd">Running reading<b id="rdn">0%</b></span></div></div>'
                + '<div class="mt">' + QTABS('meter')
                + f'<div class="intro" id="intro"><p class="kick" style="color:var(--pink-deep)">The Bitch-O-Meter, {t["name"]} edition</p>'
                + f'<h1>How much of a bitch <span class="p">are you at {t["name"].lower()}?</span></h1>'
                + f'<p class="lede">{E(t["blurb"])} Four answers each. All of them are funny. Only one is right, and it is probably not the one you want to pick. Every pick gets a verdict.</p>'
                + RULES + '<button class="btn dark start" id="go" type="button">Begin the test</button> '
                + f'<a class="btn" href="{t["other"]}" style="background:transparent;color:var(--black)">Or take the {t["otherName"]} test</a></div>'
                + '<div class="stage" id="stage"></div><div class="fin" id="fin" aria-live="polite"></div>'
                + '<div class="getbox" style="margin-top:60px"><b>Meet the real thing.</b>Sixteen breeds. Same bitch.' + buttons() + '</div></div>'
                + FOOT + f'<script>{js}</script></body></html>')
        write(t['path'], body)
    cards = ''
    for key, t in tests.items():
        cards += (f'<a class="hubc" href="{t["path"]}"><img src="/img/{t["hero"]}.webp" alt="" width="900" height="675" loading="lazy">'
                  f'<div><h2>The {t["name"]} Test</h2><p>{E(t["blurb"])}</p><span class="btn">Start, twenty questions</span></div></a>')
    hub = (head('The Bitch-O-Meter: How Much of a Bitch Are You, Really? Every Bitch Has Her Way',
                'Two tests of twenty questions each. Funny answers, a verdict for every pick, and a reading on the Bitch-O-Meter.', '/bitch-o-meter/')
           + nav('/bitch-o-meter/')
           + '<div class="mt">' + QTABS('meter') + '<div class="intro"><p class="kick" style="color:var(--pink-deep)">The Bitch-O-Meter</p>'
           + '<h1>How much of a bitch <span class="p">are you, really?</span></h1>'
           + '<p class="lede">Two tests. Twenty questions each. Every answer is funny and every pick gets a verdict. Only one answer per question is right, and it is probably not the one you want to pick. Take one or take both.</p></div>' + RULES.replace('Twenty questions, sixty points, one percentage.', 'Sixty points per test.')
           + f'<div class="hubgrid">{cards}</div>'
           + '<div class="getbox" style="margin-top:20px"><b>Meet the real thing.</b>Sixteen breeds. Same bitch.' + buttons() + '</div></div>'
           + FOOT + '</body></html>')
    write('/bitch-o-meter/', hub)
