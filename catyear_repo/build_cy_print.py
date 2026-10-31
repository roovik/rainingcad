"""Cat Year print builder: derives site/CY2027/print from the Dog Year print page and the Cat Year week JSON."""
import json,glob,os,re,shutil,datetime
SITE='/home/claude/rainingcad/site'
src=open(f'{SITE}/DY2027/print/index.html',encoding='utf-8').read()
P='@@RCD@@'
s=src.replace('Raining Cats &amp; Dogs',P)
R=[('Dog Year 2027 &middot; Every Day Has Its Dog','Cat Year 2027 &middot; Every Day Has Its Cat'),('Dog Year 2027','Cat Year 2027'),('Dog Year','Cat Year'),
('Every Day<br>a Dog','Every Day<br>Has Its Cat'),('Every Day a Dog','Every Day Has Its Cat'),('<em>dog journal.</em>','<em>cat journal.</em>'),
("Your dog's name","Your cat's name"),("your dog's name","your cat's name"),('placeholder="Biscuit"','placeholder="Mochi"'),('your dog do today','your cat do today'),
('add your dog','add your cat'),('Add your own dog','Add your own cat'),('your own dog','your own cat'),('every dog online','every cat online'),('My dog year','My cat year'),
('my-dog-year','my-cat-year'),('dy27','cy27'),('/DY2027/','/CY2027/'),('Dogs of ','Cats of '),
('Fifty dogs. Fifty weeks. One for every day.','A new cat every week. One for every day.'),
('/CY2027/26/hero.webp','/CY2027/1/hero.webp'),('/CY2027/11/hero.webp','/CY2027/2/hero.webp'),('/CY2027/29/hero.webp','/CY2027/4/hero.webp'),
('<b>1</b>Make it yours','<b>1</b>Make it yours'),("'All 50'","'All '+D.length"),('>All 50<','>All<'),
("'+seas.map(function(s){return '<button class=\"chip\" data-s=\"'+s+'\">'+s+'</button>'}).join('')+'","'+seas.map(function(s){return '<button class=\"chip\" data-s=\"'+s+'\">'+s+'</button>'}).join('')+'"),
("var seas=['Winter','Spring','Summer','Fall'];","var seas=['Winter','Spring','Summer','Fall'].filter(function(x){return D.some(function(w){return w.se===x})});"),
('Pick at least one week to see your journal.','Pick at least one week to see your journal.'),
('Fifty','Four'),("var KIND='dog'","var KIND='cat'")]
for a,b in R: s=s.replace(a,b)
s=s.replace(P,'Raining Cats &amp; Dogs')
s=s.replace('Print Your Own Journal · Cat Year 2027','Print Your Own Journal · Cat Year 2027')
s=s.replace('Make your own Every Day a Dog journal.','Make your own Every Day Has Its Cat journal.').replace("add your dog's name","add your cat's name").replace("dog's name and your own photos","cat's name and your own photos")
s=s.replace('The page was','The page was')
s=s.replace("fetch('/CY2027/print/data.json')","fetch('/CY2027/print/data.json')")
os.makedirs(f'{SITE}/CY2027/print',exist_ok=True)
open(f'{SITE}/CY2027/print/index.html','w',encoding='utf-8').write(s)
shutil.copy(f'{SITE}/DY2027/print/qr.js',f'{SITE}/CY2027/print/qr.js')
out=[];st=datetime.date(2027,1,3)
for f in sorted(glob.glob('catyear_repo/weeks/week*.json')):
    w=json.load(open(f,encoding='utf-8'));n=w['num'];d0=st+datetime.timedelta(days=7*(n-1))
    lw=w['last_walk'].split('\n',1)
    out.append(dict(n=n,b=w['breed'],nl=[w['breed']],p=w['positioning'],s=w['story'],rn=w['rank_num'],rc=w['cap'],se='Winter',g=w['glance'],f=w['fblocks'],d=[[x[0],x[1],x[2]] for x in w['days']],lw=[lw[0],lw[1] if len(lw)>1 else ''],start=d0.isoformat()))
json.dump(out,open(f'{SITE}/CY2027/print/data.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
left=sorted(set(re.findall(r'[^ <>"\']*\b[Dd]ogs?\b[^ <>"\']*',s)))
print('built',len(out),'weeks; remaining dog mentions:',left)
