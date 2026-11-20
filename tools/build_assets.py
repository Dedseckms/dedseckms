"""Build original code-drawn profile artwork. Requires Pillow; no remote services."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
BG, FG, MUTED, GREEN, CYAN = '#090e14', '#e6edf3', '#91a4b5', '#b5f76b', '#58dfd0'
MONO = "Consolas, 'Liberation Mono', monospace"
SANS = "'Segoe UI', Arial, sans-serif"

def svg(name, w, h, body):
    content = '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 %s %s">%s</svg>\n' % (w,h,w,h,body)
    with (OUT / name).open('w', encoding='utf-8', newline='\n') as handle:
        handle.write(content)

def text(x,y,value,size=20,color=FG,font=MONO,extra=''):
    return '<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" %s>%s</text>' % (x,y,font,size,color,extra,value)

body = '''<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#1c2b35" stroke-width="1"/></pattern>
<linearGradient id="fade"><stop stop-color="#090e14"/><stop offset="1" stop-color="#10242b"/></linearGradient>
</defs>
<rect width="1280" height="470" rx="22" fill="url(#fade)"/>
<rect x="720" y="0" width="560" height="470" fill="url(#grid)" opacity=".5"/>
<path d="M0 444H1280" stroke="#b5f76b" stroke-width="2"/>
<path d="M43 48h12m-6-6v12" stroke="#b5f76b" stroke-width="2"/>
<rect x="44" y="83" width="4" height="253" fill="#b5f76b"/>
'''
body += text(70,55,'DEDSEC / INDEPENDENT SOFTWARE',18,GREEN,extra='letter-spacing="3"')
body += text(1230,55,'PROFILE_01',16,MUTED,extra='text-anchor="end"')
body += text(72,124,'BUILD TO MAKE IT YOURS.',16,MUTED,extra='letter-spacing="3"')
body += text(65,238,'Dedseckms',115,FG,SANS,extra='font-weight="700" letter-spacing="-5"')
body += text(73,295,'Играть. Слушать. Наблюдать. Создавать.',25,'#bdcdd7',SANS)
body += text(73,378,'OPEN SOURCE',16,GREEN,extra='letter-spacing="2"')
body += text(255,378,'/',18,'#3a515d')
body += text(288,378,'WINDOWS · LINUX · ANDROID',16,MUTED,extra='letter-spacing="1"')
body += '''<g fill="none" stroke="#58dfd0" stroke-width="2">
<path d="M1005 106l110 64v128l-110 64-110-64V170z" opacity=".2"/>
<path d="M1005 133l87 50v102l-87 50-87-50V183z" opacity=".6"/>
<path d="M964 205l-34 29 34 29m82-58l34 29-34 29m-30-74l-23 90" stroke-width="5"/>
<path d="M1115 234h75v100h44M895 234h-40v-89h-32" opacity=".5"/>
<circle cx="1190" cy="234" r="5" fill="#58dfd0"/>
<circle cx="855" cy="145" r="4" fill="#b5f76b" stroke="#b5f76b"/>
</g>'''
body += text(73,462,'D / K',12,'#526875',extra='letter-spacing="3"')
body += text(1228,462,'CODE → TOOLS → EVERYDAY',12,'#526875',extra='text-anchor="end" letter-spacing="2"')
svg('hero-dedseckms.svg',1280,470,body)

for key,n,category,title,color,subtitle in [
    ('mineded','01','PLAY','MineDed',GREEN,'MINECRAFT / TOGETHER'),
    ('music','02','LISTEN','Dedsec Music',CYAN,'YOUR LIBRARY / YOUR RHYTHM'),
    ('monitor','03','OBSERVE','Dedsec Monitor','#e5cf82','EVERY FRAME / UNDER CONTROL'),
    ('studio','04','CREATE','DedsecAI Studio','#bda8ff','LOCAL MODELS / OPEN IDEAS'),
]:
    b = '<rect width="600" height="148" rx="12" fill="%s"/><rect x="0" y="20" width="3" height="108" fill="%s"/>' % (BG,color)
    b += text(25,36,n+' / '+category,14,color,extra='letter-spacing="2"')
    b += text(25,84,title,35,FG,SANS,extra='font-weight="600"')
    b += text(25,122,subtitle,12,MUTED,extra='letter-spacing="1.5"')
    b += text(568,40,'↗',25,color,extra='text-anchor="end"')
    svg(key+'.svg',600,148,b)

svg('footer.svg',1280,104,'<rect width="1280" height="104" rx="14" fill="%s"/><path d="M32 30h42" stroke="%s" stroke-width="3"/>' % (BG,GREEN) + text(95,37,'DEDSEC /',18,GREEN) + text(95,73,'От идеи до работающего инструмента.',22,FG,SANS) + text(1236,67,'[ EOF ]',16,MUTED,extra='text-anchor="end"'))

font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
small = ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
frames = []
for i in range(40):
    im = Image.new('RGB',(1280,82),BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((1,1,1278,80),radius=12,outline='#20303b',width=1)
    d.text((26,31),'DEDSEC / OPEN SOURCE',font=font,fill=GREEN)
    d.line((294,42,460,42),fill='#2e444d',width=2)
    # Calm moving packet; no flashing or sudden full-frame changes.
    x = 312 + int((i/39)*130)
    d.ellipse((x-4,38,x+4,46),fill=CYAN)
    d.text((500,32),'PLAY   /   LISTEN   /   OBSERVE   /   CREATE',font=small,fill='#bdcdd7')
    d.text((1168,31),'</>',font=font,fill=GREEN)
    frames.append(im)
frames[0].save(OUT/'signal.png',optimize=True)
frames[0].save(OUT/'signal.gif',save_all=True,append_images=frames[1:],duration=150,loop=0,optimize=True,disposal=1)

for path in sorted(OUT.rglob('*')):
    if path.suffix.lower() in ('.gif','.png','.webp'):
        with Image.open(path) as im:
            print('%s: %sx%s, %s bytes, %s frames' % (path.relative_to(ROOT),im.width,im.height,path.stat().st_size,getattr(im,'n_frames',1)))
