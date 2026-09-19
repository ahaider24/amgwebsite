"""Independent outline-based avatar typesetting. No font lookup or fallback.
Run with the bundled Python (Pillow + NumPy), and Node + Sharp.
"""
from pathlib import Path
import argparse, hashlib, io, json, math, subprocess
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'brand/avatars'
PROOF = ROOT / 'brand/proofs'
SOURCE = ROOT / 'brand/source/geist-700-outlines.json'
FONT = json.loads(SOURCE.read_text())
assert FONT['family'] == 'Geist' and FONT['upem'] == 1000
SHARP = '/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'
NODE = '/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
PAPER, ACCENT = '#FBF8F2', '#FF4D1C'
# Explicit pair corrections in em, in addition to tracking. No automatic kerning
# is present in the supplied outline JSON.
PAIRS = {'Am': -.009, 'mi': -.003, 'ir': -.004, 'rG': -.017,
         'Ge': -.012, 'et': -.009, 'ts': -.013,
         'Le': -.023, 'ea': -.009, 'ad': -.007, 'ds': -.007}
CAP, XHEIGHT = 710, 536
OPTIONS = [
    dict(key='a', name='Equal optical widths', top=804, ratio=1.00, logic='axis', gap=.24),
    dict(key='b', name='Measured step', top=832, ratio=.84, logic='axis', gap=.28),
    dict(key='c', name='Shared type size', top=832, ratio=None, logic='axis', gap=.34),
    dict(key='d', name='Shared left edge', top=806, ratio=.83, logic='left', gap=.28),
]

def word(text, tracking, italic=False, small=False):
    commands = []; cursor = 0
    shear = math.tan(math.radians(12 if small else 14)) if italic else 0
    for i, ch in enumerate(text):
        glyph = FONT['glyphs'][str(ord(ch))]
        for c in glyph['commands']:
            row = [c[0]]
            for j in range(1,len(c),2):
                x,y=c[j:j+2]; row += [cursor+x+shear*y, -y]
            commands.append(row)
        if i+1 < len(text):
            cursor += glyph['advance'] + tracking*1000 + PAIRS.get(text[i:i+2],0)*1000*(.35 if small else 1)
    return commands

def transform(commands, scale=1, dx=0, dy=0):
    return [[c[0]] + [v*scale+(dx if j%2 == 1 else dy) for j,v in enumerate(c[1:],1)] for c in commands]

def path(commands, fill):
    return '<path fill="'+fill+'" d="'+' '.join(c[0]+' '.join(f'{v:.4f}' for v in c[1:]) for c in commands)+'"/>'

def render(svg, size):
    js = "const s=require(process.argv[1]);let b=[];process.stdin.on('data',x=>b.push(x));process.stdin.on('end',async()=>{let r=await s(Buffer.concat(b)).resize(+process.argv[2],+process.argv[2]).png().toBuffer();process.stdout.write(r)});"
    # SVG is rasterized at 4x the target then reduced once. No 1024px PNG master.
    svg = svg.replace('width="1024" height="1024"', f'width="{size*4}" height="{size*4}"')
    p = subprocess.run([NODE,'-e',js,SHARP,str(size)],input=svg.encode(),stdout=subprocess.PIPE,check=True)
    return Image.open(io.BytesIO(p.stdout)).convert('RGBA')

def svg(body, title='Geist 700 avatar', circle=True):
    bg = '<circle cx="512" cy="512" r="512" fill="url(#cta)"/>' if circle else '<rect width="1024" height="1024" fill="url(#cta)"/>'
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024" role="img">'
        '<title>'+title+'</title><defs><linearGradient id="cta" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#3CB8DE"/><stop offset=".46" stop-color="#2596BE"/>'
        '<stop offset="1" stop-color="#1A5E92"/></linearGradient></defs>'+bg+body+'</svg>')

METRICS = {}
def metrics(commands):
    # Integrate flattened Bezier contours for an ink-area centroid, with hole winding.
    contours=[]; pts=[]; current=None
    for c in commands:
        if c[0]=='M':
            if pts: contours.append(pts)
            current=np.array(c[1:]); pts=[current]
        elif c[0]=='L':
            current=np.array(c[1:]); pts.append(current)
        elif c[0] in ('Q','C'):
            start=current.copy(); cp=np.array(c[1:]).reshape(-1,2)
            for t in np.linspace(0,1,25)[1:]:
                if c[0]=='Q': p=(1-t)**2*start+2*(1-t)*t*cp[0]+t*t*cp[1]
                else: p=(1-t)**3*start+3*(1-t)**2*t*cp[0]+3*(1-t)*t*t*cp[1]+t**3*cp[2]
                pts.append(p)
            current=cp[-1]
        elif c[0]=='Z':
            if pts: contours.append(pts); pts=[]
    if pts: contours.append(pts)
    area=cx=cy=0
    for p in contours:
        p=np.array(p); q=np.roll(p,-1,axis=0)
        cross=p[:,0]*q[:,1]-q[:,0]*p[:,1]
        a=cross.sum()/2; area+=a
        cx+=((p[:,0]+q[:,0])*cross).sum()/6
        cy+=((p[:,1]+q[:,1])*cross).sum()/6
    p=np.concatenate(contours)
    return dict(bounds=[*p.min(axis=0),*p.max(axis=0)], cx=cx/area, cy=cy/area, area=abs(area))

def layout(option, small=False, target=32):
    tracking = (-.004,-.008) if small else (-.034,-.036)
    top=word('AmirGets',tracking[0],small=small)
    low=word('Leads',tracking[1],True,small)
    tm,lm=metrics(top),metrics(low)
    # The measured ink width is only the size constraint. Alignment uses the ink
    # centroid plus the separately reviewed italic adjustment below.
    tw=option['top']+(10 if small else 0)
    ts=tw/(tm['bounds'][2]-tm['bounds'][0])
    ls=ts if option['ratio'] is None else tw*option['ratio']/(lm['bounds'][2]-lm['bounds'][0])
    if small: ls*=.985
    # Gap comes from the top line's cap-to-x-height difference, not a fixed pixel gap.
    # Small cut reserves additional breathing room for the pixel filter.
    gap=(CAP-XHEIGHT)*ts*(1.0+option['gap'])
    if small: gap=max(gap, 1024/32*1.05)
    top=transform(top,ts); low=transform(low,ls)
    tm,lm=metrics(top),metrics(low)
    # Baseline separation: upper bottom to lower top equals derived clear gap.
    lowdy=tm['bounds'][3]+gap-lm['bounds'][1]
    if option['logic']=='axis':
        topdx=512-tm['cx']
        # Visual review of +6, +16 and +26 settled on +16 after ink centring.
        lowdx=512-lm['cx']+(10 if small else 16)
    else:
        # Match the lower L at half x-height to the upper A's visible left edge.
        topdx=-tm['bounds'][0]
        lowdx=-(math.tan(math.radians(12 if small else 14))*XHEIGHT*.5*ls+54*ls)
    top=transform(top,dx=topdx); low=transform(low,dx=lowdx,dy=lowdy)
    tm,lm=metrics(top),metrics(low)
    if option['logic']=='left':
        unionmid=(min(tm['bounds'][0],lm['bounds'][0])+max(tm['bounds'][2],lm['bounds'][2]))/2
        dx=512-unionmid
        top=transform(top,dx=dx);low=transform(low,dx=dx)
    # Optical vertical balance: blend silhouette midpoint with ink centre.
    tm,lm=metrics(top),metrics(low)
    silhouette=(tm['bounds'][1]+lm['bounds'][3])/2
    inkcy=(tm['cy']*tm['area']+lm['cy']*lm['area'])/(tm['area']+lm['area'])
    dy=502-(.70*silhouette+.30*inkcy)
    top=transform(top,dy=dy);low=transform(low,dy=dy)
    if small:
        # Fit each baseline to the actual output grid. G overshoots by 16 units;
        # the lowercase round forms in Leads overshoot by 12 units.
        tm,lm=metrics(top),metrics(low)
        unit=1024/target
        tb=tm['bounds'][3]-16*ts; lb=lm['bounds'][3]-12*ls
        top=transform(top,dy=round(tb/unit)*unit-tb)
        low=transform(low,dy=round(lb/unit)*unit-lb)
    tm,lm=metrics(top),metrics(low)
    gap=lm['bounds'][1]-tm['bounds'][3]
    body=path(top,PAPER)+path(low,ACCENT)
    # Record conservative radial safety, from all control points, not just square margins.
    coords=np.array([(c[j],c[j+1]) for commands in (top,low) for c in commands for j in range(1,len(c),2)])
    clearance=512-np.linalg.norm(coords-[512,512],axis=1).max()
    info=dict(top_em=ts*1000,leads_em=ls*1000,tracking_em=tracking,
              gap=gap,cap_height=CAP*ts,x_height=XHEIGHT*ts,
              top_bounds=tm['bounds'],leads_bounds=lm['bounds'],
              top_ink_axis=tm['cx'],leads_ink_axis=lm['cx'],
              circle_clearance=clearance,italic_degrees=12 if small else 14)
    return body,info

# Proof labels are also drawn from the supplied Geist paths, with no installed font.
def label(text,size=20,color='#263641'):
    cmds=word(text,0)
    m=metrics(cmds); x0,y0,x1,y1=m['bounds']
    width=math.ceil((x1-x0)*size/1000)+4; height=math.ceil((y1-y0)*size/1000)+4
    p=transform(cmds,size/1000,2-x0*size/1000,2-y0*size/1000)
    s='<svg xmlns="http://www.w3.org/2000/svg" width="'+str(width)+'" height="'+str(height)+'">'+path(p,color)+'</svg>'
    js="require(process.argv[1])(Buffer.from(process.argv[2])).png().toBuffer().then(b=>process.stdout.write(b))"
    b=subprocess.run([NODE,'-e',js,SHARP,s],stdout=subprocess.PIPE,check=True).stdout
    return Image.open(io.BytesIO(b)).convert('RGBA')

def putlabel(canvas,xy,text,size=20,color='#263641'):
    im=label(text,size,color);canvas.paste(im,xy,im)

def onwhite(im):
    bg=Image.new('RGB',im.size,'white');bg.paste(im,(0,0),im);return bg

def main():
    parser=argparse.ArgumentParser();parser.add_argument('-o',type=Path,default=PROOF/'avatar-typesetting-report.md')
    args=parser.parse_args(); OUT.mkdir(exist_ok=True);PROOF.mkdir(exist_ok=True)
    (OUT/'astra-options').mkdir(exist_ok=True)
    data={}; arts={}; cuts={}
    for option in OPTIONS:
        key=option['key'];data[key]={};arts[key]={}
        for small in (False,True):
            cut='small' if small else 'display';body,info=layout(option,small)
            data[key][cut]=info
            s=svg(body,option['name']+' | '+cut+' cut | real Geist 700 outlines')
            cuts[key,cut]=s
            (OUT/f'astra-options/{key}-{cut}.svg').write_text(s)
        body,info=layout(option,True,target=48)
        cuts[key,'small48']=svg(body,option['name']+' | 48px small cut | real Geist 700 outlines')
        data[key]['small48']=info
        (OUT/f'astra-options/{key}-small48.svg').write_text(cuts[key,'small48'])
        for size in (400,180,48,32):
            im=render(cuts[key,'small48' if size==48 else 'small' if size<=32 else 'display'],size)
            im.save(OUT/f'astra-options/{key}-{size}.png')
            arts[key][size]=im
    sheet=Image.new('RGB',(1824,1070),'white')
    putlabel(sheet,(36,27),'AMIRGETS / AVATAR TYPE STUDY',24)
    putlabel(sheet,(36,63),'Real Geist 700 outlines. CTA gradient. All circles shown at exact pixel dimensions.',16)
    descriptions=[('Same perceived line width','Leads becomes the second-line anchor'),
                  ('Leads at 84% of the upper width','A deliberate step, with a shared optical axis'),
                  ('One type size for both words','Quiet hierarchy, a much shorter second line'),
                  ('Align the left reading edge','An editorial lockup inside the circle')]
    for i,option in enumerate(OPTIONS):
        key=option['key'];x=32+i*448
        putlabel(sheet,(x,116),key.upper()+' / '+option['name']+(' (ship)' if key=='b' else ''),22)
        for j,line in enumerate(descriptions[i]):putlabel(sheet,(x,153+j*24),line,15)
        for size,y in [(400,240),(180,690),(48,918),(32,1004)]:
            xx=x+(400-size)//2
            sheet.paste(onwhite(arts[key][size]),(xx,y))
            putlabel(sheet,(x,y-25),f'{size}px'+(' / small cut' if size<=48 else ' / display cut'),14)
    sheet.save(PROOF/'avatar-typesetting-comparison.png')
    # Selected after visual review; B keeps the long top line large and the lower
    # word distinct without forcing a broad, bottom-heavy equal-width rectangle.
    chosen='b'
    for size in (1024,800,512,400,360,320,180,48,32):
        render(cuts[chosen,'small48' if size==48 else 'small' if size==32 else 'display'],size).save(OUT/f'astra-avatar-{size}.png')
    (OUT/'astra-avatar-display.svg').write_text(cuts[chosen,'display'])
    (OUT/'astra-avatar-small.svg').write_text(cuts[chosen,'small'])
    (OUT/'astra-avatar-small48.svg').write_text(cuts[chosen,'small48'])
    # Platforms accept one upload then make every derivative. Supply an upload
    # from the small cut as well, so the compensation survives that workflow.
    for small in (False,True):
        body,_=layout(OPTIONS[1],small)
        render(svg(body,circle=False),1024).save(OUT/f'astra-avatar-upload-{"small" if small else "display"}-1024.png')
    # A fair small-size check: display cut reduced vs separately drawn small cut.
    audit=Image.new('RGB',(1160,670),'white')
    putlabel(audit,(30,24),'B / SMALL-SIZE AUDIT',25)
    putlabel(audit,(30,61),'Native-size circles above. Nearest-neighbour enlargements below reveal the actual pixels.',16)
    for i,size in enumerate((48,32)):
        for j,cut in enumerate(('display','small')):
            x=30+(i*2+j)*282
            im=render(cuts['b','small48' if cut=='small' and size==48 else cut],size)
            putlabel(audit,(x,111),f'{size}px / {cut}',19)
            audit.paste(onwhite(im),(x,150))
            audit.paste(onwhite(im.resize((256,256),Image.Resampling.NEAREST)),(x,235))
    putlabel(audit,(30,545),'Small cut: looser fit, 12-degree lean, and baselines fitted to the output pixel grid.',17)
    putlabel(audit,(30,578),'Original 700 weight preserved to protect the small counters in the upper line.',17)
    putlabel(audit,(30,611),'32px is a recognition mark. Full-name reading remains constrained by the pixel budget.',17)
    audit.save(PROOF/'avatar-typesetting-small-audit.png')
    data['source_sha256']=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    data['selected']='b'
    (PROOF/'avatar-typesetting-metrics.json').write_text(json.dumps(data,indent=2)+'\n')
    report_source=PROOF/'avatar-typesetting-report-source.md'
    args.o.parent.mkdir(parents=True,exist_ok=True)
    args.o.write_text(report_source.read_text())
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
