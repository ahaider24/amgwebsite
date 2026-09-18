"""Deterministic brand build. Run with Pillow, ReportLab and pypdf available."""
from pathlib import Path
import base64, io, json, math, subprocess, hashlib
from PIL import Image, ImageDraw, ImageCms
from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject, ArrayObject, TextStringObject, NumberObject

ROOT=Path(__file__).resolve().parents[2]
B=ROOT/'brand'
PAPER='#FBF8F2'; INK='#14110A'; ORANGE='#FF4D1C'; SOFT='#574F40'
FONTS={k:json.loads((B/'source'/v).read_text()) for k,v in {
    'geist':'geist-700-outlines.json','body':'archivo-400-outlines.json','bodybold':'archivo-600-outlines.json'}.items()}
SHARP='/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'
ICC=Path('/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc')
srgb=ImageCms.createProfile('sRGB'); cmyk=ImageCms.getOpenProfile(str(ICC))
TO_CMYK=ImageCms.buildTransformFromOpenProfiles(srgb,cmyk,'RGB','CMYK',renderingIntent=1,flags=0x2000)

def colour(hexvalue):
    pixel=Image.new('RGB',(1,1),hexvalue)
    return tuple(v/255 for v in ImageCms.applyTransform(pixel,TO_CMYK).getpixel((0,0)))

def glyphs(text,size,x=0,y=0,font='geist',italic=False,tracking=None):
    f=FONTS[font]; scale=size/f['upem']; commands=[]
    if tracking is None: tracking=-.02 if font=='geist' else 0
    skew=math.tan(math.radians(14)) if italic else 0
    for ch in text:
        g=f['glyphs'][str(ord(ch))]
        for cmd in g['commands']:
            c=[cmd[0]]
            for i in range(1,len(cmd),2):
                px,py=cmd[i:i+2]; c.extend([x+(px+skew*py)*scale,y-py*scale])
            commands.append(c)
        x+=g['advance']*scale+size*tracking
    return commands

def bounds(commands):
    p=[(c[i],c[i+1]) for c in commands for i in range(1,len(c),2)]
    return min(x for x,y in p),min(y for x,y in p),max(x for x,y in p),max(y for x,y in p)

def centred(text,size,cx,baseline,**kw):
    c=glyphs(text,size,**kw); x0,y0,x1,y1=bounds(c)
    return glyphs(text,size,cx-(x0+x1)/2,baseline,**kw)

def svgpath(commands,fill):
    d=' '.join(c[0]+' '.join(f'{v:.4f}' for v in c[1:]) for c in commands)
    return f'<path fill="{fill}" d="{d}"/>'

def svgfile(path,body,title,width=1024,height=1024):
    path.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{title}</title>{body}</svg>')

def render(svg,png,size):
    subprocess.run(['node','-e',f"require({json.dumps(SHARP)})(process.argv[1],{{density:144}}).resize(Number(process.argv[3]),Number(process.argv[3])).png().toFile(process.argv[2])",str(svg),str(png),str(size)],check=True)

def embedded(im):
    stream=io.BytesIO(); im.save(stream,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode()

def circle(im):
    mask=Image.new('L',im.size); ImageDraw.Draw(mask).ellipse((0,0,im.width-1,im.height-1),fill=255)
    result=Image.new('RGB',im.size,'#E7DDC8'); result.paste(im.convert('RGB'),(0,0),mask); return result

def avatars():
    hero=Image.open(ROOT/'hero-hands.webp')
    bg=Image.new('RGBA',(hero.width,hero.height+100),PAPER); bg.alpha_composite(hero,(0,100))
    crop=bg.crop((1149,50,1909,810)).convert('RGB')
    # The original engraving and gap are retained, with no invented glow or art.
    svgfile(B/'avatars/avatar-a-spark.svg',f'<image width="1024" height="1024" xlink:href="{embedded(crop)}"/>','AmirGetsLeads fingertip spark, cropped from hero-hands.webp')
    a=glyphs('A',600); amax=bounds(a)[2]
    l=glyphs('L',600,x=amax+24,italic=True)
    x0,y0,x1,y1=bounds(a+l); shiftx=512-(x0+x1)/2; shifty=512-(y0+y1)/2
    def shift(cmds):
        return [[c[0]]+[v+(shiftx if i%2 else shifty) for i,v in enumerate(c[1:],1)] for c in cmds]
    svgfile(B/'avatars/avatar-b-monogram.svg','<rect width="1024" height="1024" fill="'+INK+'"/>'+svgpath(shift(a),PAPER)+svgpath(shift(l),ORANGE),'AmirGetsLeads AL monogram, Geist 700 with italic orange L')
    for key in ('a-spark','b-monogram'):
        for n in (1024,512,400,180,48):
            render(B/f'avatars/avatar-{key}.svg',B/f'avatars/avatar-{key}-{n}.png',n)
        circle(Image.open(B/f'avatars/avatar-{key}-180.png')).save(B/f'proofs/avatar-{key}-circle-180.png')
    body='<rect width="1024" height="1024" fill="'+PAPER+'"/>'
    paths=[centred('AmirGets',144,512,472),centred('Leads',194,512,676,italic=True)]
    for p,c in zip(paths,[INK,ORANGE]):body+=svgpath(p,c)
    svgfile(B/'gbp-wordmark.svg',body,'AmirGetsLeads stacked wordmark')
    render(B/'gbp-wordmark.svg',B/'gbp-wordmark-1024.png',1024)
    im=Image.open(B/'gbp-wordmark-1024.png');circle(im).save(B/'proofs/gbp-circle-1024.png')
    # Prove every non-paper pixel lies within an inner radius of 440 px.
    maxradius=0
    for y in range(1024):
        for x in range(1024):
            if im.getpixel((x,y))[:3]!=(251,248,242): maxradius=max(maxradius,math.hypot(x-512,y-512))
    assert maxradius<440,maxradius
    return maxradius

def drawpath(c,commands,fill,pageheight):
    c.setFillColor(CMYKColor(*fill)); p=c.beginPath(); current=(0,0)
    for cmd in commands:
        op=cmd[0]; pts=[(cmd[i],pageheight-cmd[i+1]) for i in range(1,len(cmd),2)]
        if op=='M':p.moveTo(*pts[0]);current=pts[0]
        elif op=='L':p.lineTo(*pts[0]);current=pts[0]
        elif op=='Q':
            q,end=pts
            p.curveTo(current[0]+2*(q[0]-current[0])/3,current[1]+2*(q[1]-current[1])/3,end[0]+2*(q[0]-end[0])/3,end[1]+2*(q[1]-end[1])/3,*end);current=end
        elif op=='C':p.curveTo(*[v for pt in pts for v in pt]);current=pts[-1]
        elif op=='Z':p.close()
    c.drawPath(p,fill=1,stroke=0,fillMode=1)

def cards():
    bleed=3*72/25.4; margin=18; w=252+2*margin; h=144+2*margin
    out=B/'business-cards.pdf'; temp=Path('/tmp/agl-cards-raw.pdf')
    c=canvas.Canvas(str(temp),pagesize=(w,h),pageCompression=1)
    c.setTitle('AmirGetsLeads business cards');c.setAuthor('AmirGetsLeads')
    colours={v:colour(v) for v in [PAPER,INK,ORANGE,SOFT]}
    black=(0,0,0,1)
    def text(t,size,x,y,font='geist',fill=INK,italic=False):
        # Registration-safe single K for fine dark lettering on the contact side.
        ink=black if fill==INK else colours[fill]
        drawpath(c,glyphs(t,size,x+margin,y+margin,font,italic),ink,h)
    def ground(hexvalue):
        c.setFillColor(CMYKColor(*colours[hexvalue]));c.rect(margin-bleed,margin-bleed,252+2*bleed,144+2*bleed,fill=1,stroke=0)
    def marks():
        c.setStrokeColor(CMYKColor(0,0,0,1));c.setLineWidth(.25)
        for x in [margin,margin+252]:
            for y,sgn in [(margin,-1),(margin+144,1)]:c.line(x,y+sgn*(bleed+2),x,y+sgn*(bleed+7))
        for y in [margin,margin+144]:
            for x,sgn in [(margin,-1),(margin+252,1)]:c.line(x+sgn*(bleed+2),y,x+sgn*(bleed+7),y)
    ground(PAPER)
    text('AmirGets',23,14,31);text('Leads',28,14,59,fill=ORANGE,italic=True)
    text('Amir Haider',12.5,135,29,font='bodybold')
    text('Fresno and Los Angeles',7.6,135,43,font='body')
    text('(559) 550-5474',10.2,14,91,font='body')
    text('outreach@amirgetsleads.com',10.2,14,108,font='body')
    text('amirgetsleads.com',10.2,14,125,font='bodybold')
    marks();c.showPage()
    ground(INK)
    # Use the original alpha engraving, recoloured paper/orange for the dark side.
    hero=Image.open(ROOT/'hero-hands.webp').convert('RGBA')
    import numpy as np
    a=np.array(hero);rgb=a[:,:,:3].astype(float)
    strength=np.clip((rgb[:,:,0]-20)/235,0,1)[:,:,None]
    paper=np.array([251,248,242]);accent=np.array([255,77,28])
    recolour=paper[None,None,:]*(1-strength)+accent[None,None,:]*strength
    a[:,:,:3]=recolour.astype('uint8');hero=Image.fromarray(a)
    # 269pt wide at 300dpi, art placed through both side bleeds.
    pixels=(round((252+2*bleed)*300/72),round(64*300/72))
    cropheight=round(hero.width*pixels[1]/pixels[0])
    art=hero.crop((0,130,hero.width,130+cropheight)).resize(pixels,Image.Resampling.LANCZOS)
    bg=Image.new('RGBA',pixels,INK);bg.alpha_composite(art)
    artc=ImageCms.applyTransform(bg.convert('RGB'),TO_CMYK)
    c.drawImage(ImageReader(artc),margin-bleed,h-(margin-bleed)-64,width=252+2*bleed,height=64)
    text('Get found.',19,14,78,fill=PAPER)
    text('Get clients.',19,14,101,fill=PAPER)
    text('Get back to life.',19,14,124,fill=ORANGE)
    marks();c.showPage();c.save()
    reader=PdfReader(temp);writer=PdfWriter()
    for page in reader.pages:
        writer.add_page(page); p=writer.pages[-1]
        p.trimbox.lower_left=(margin,margin);p.trimbox.upper_right=(margin+252,margin+144)
        p.bleedbox.lower_left=(margin-bleed,margin-bleed);p.bleedbox.upper_right=(margin+252+bleed,margin+144+bleed)
    profile=DecodedStreamObject();profile.set_data(ICC.read_bytes());profile[NameObject('/N')]=NumberObject(4)
    intent=DictionaryObject({NameObject('/Type'):NameObject('/OutputIntent'),NameObject('/S'):NameObject('/GTS_PDFX'),NameObject('/OutputConditionIdentifier'):TextStringObject('Generic CMYK Profile'),NameObject('/Info'):TextStringObject('Generic CMYK fallback. Printer-specific proof required.'),NameObject('/DestOutputProfile'):writer._add_object(profile)})
    writer._root_object[NameObject('/OutputIntents')]=ArrayObject([writer._add_object(intent)])
    writer.add_metadata({'/Title':'AmirGetsLeads business cards','/Author':'AmirGetsLeads','/Subject':'Two sides, US 3.5 x 2 in trim, 3 mm bleed, CMYK, outlined type. Not certified PDF/X.'})
    with out.open('wb') as f:writer.write(f)
    subprocess.run(['pdftoppm','-r','300','-png',str(out),str(B/'proofs/business-card')],check=True)
    for n,label in [(1,'front'),(2,'back')]:
        p=B/f'proofs/business-card-{n}.png';im=Image.open(p);im.save(B/f'proofs/business-card-{label}-300dpi.png',dpi=(300,300));p.unlink()
    return {k:[round(v*100,2) for v in vals] for k,vals in colours.items()}

def contrast(a,b):
    def lum(h):
        rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
        rgb=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
        return sum(v*w for v,w in zip(rgb,[.2126,.7152,.0722]))
    x,y=sorted([lum(a),lum(b)]);return (y+.05)/(x+.05)

if __name__=='__main__':
    for p in ['avatars','proofs']: (B/p).mkdir(exist_ok=True)
    radius=avatars();cm=cards()
    metrics={'gbp_max_radius_px':radius,'gbp_circle_radius_px':512,'contrast_orange_paper':contrast(ORANGE,PAPER),'contrast_orange_ink':contrast(ORANGE,INK),'contrast_deep_paper':contrast('#C8380E',PAPER),'cmyk_percent':cm,'icc_profile':str(ICC),'icc_sha256':hashlib.sha256(ICC.read_bytes()).hexdigest()}
    (B/'source/verification.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics,indent=2))
