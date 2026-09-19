"""Build held Axiom chat studies. All outputs stay beside this file.

Use the cached Python runtime with ReportLab, Pillow, pypdf and Poppler.
Generic chat UI only. No QR, product marks, website edits or deployment.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('axiom_primitives', HERE.parent/'build.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.FONTS['body'] = json.loads((HERE/'source/geist-400-outlines.json').read_text())
base.FONTS['medium'] = json.loads((HERE/'source/geist-500-outlines.json').read_text())
PAPER, INK, SOFT, ORANGE = '#FBF8F2', '#14110A', '#574F40', '#FF4D1C'
TAKES = ['01-minimal', '02-app', '03-full-interface']
TITLES = ['MINIMAL FRAME', 'CHAT APP', 'FULL INTERFACE']
STROKES = []
RECORDS = base.RECORDS
QR = {'status': 'Omitted by brief', 'encoded_url': None}


def text(c, value, size, x, y, h=252, w=144, **kw):
    assert chr(0x2014) not in value
    base.text(c, value, size, x, y, h, tw=w, **kw)


def stroke(c, width=.8, color=SOFT):
    assert width > .5
    STROKES.append(width)
    c.setStrokeColor(HexColor(color))
    c.setLineWidth(width)
    c.setLineCap(1)
    c.setLineJoin(1)


def line(c, x1, y1, x2, y2, width=.8, color=SOFT):
    stroke(c, width, color)
    c.line(x1, 252-y1, x2, 252-y2)


def box(c, x, y, w, h, radius=8, color=SOFT, width=.8):
    stroke(c, width, color)
    c.roundRect(x, 252-y-h, w, h, radius, stroke=1, fill=0)


def plus(c, x, y):
    line(c,x-3,y,x+3,y)
    line(c,x,y-3,x,y+3)


def send(c, x, y):
    # Real, optical-size send affordance. No low-contrast orange text.
    stroke(c,.85,SOFT)
    c.circle(x,252-y,7.3,fill=0,stroke=1)
    line(c,x,y+3,x,y-3,1.2,ORANGE)
    line(c,x-2.7,y-.3,x,y-3,1.2,ORANGE)
    line(c,x,y-3,x+2.7,y-.3,1.2,ORANGE)


def composer(c, full=False):
    if full:
        box(c,18,194,108,40,10)
        text(c,'Message...',8.5,27,209,font='body',color=SOFT)
        plus(c,28,223)
        send(c,114,223)
    else:
        box(c,12,211,120,29,12)
        text(c,'Message...',9,23,229,font='body',color=SOFT)
        send(c,119,225.5)


def prompt(c, x, y, w, size=9.5):
    box(c,x,y,w,59,10)
    for value,dy in zip(["I need marketing", "but I don't know", "who to pick."],[19,32,45]):
        text(c,value,size,x+10,y+dy,font='body')


def reply(c, x, y, size=11):
    text(c,'AmirGetsLeads.',size,x,y,font='medium')
    text(c,'Turn the card over.',9,x,y+17,font='body')


def vertical(c, take):
    base.ACTIVE = take+'/vertical'
    if take == TAKES[0]:
        # The composer and asymmetrical turn alignment carry the recognition.
        text(c,'AI chat',9,14,29,font='medium',color=SOFT)
        prompt(c,30,57,102)
        reply(c,14,148,11.5)
        composer(c)
    elif take == TAKES[1]:
        # A normal app bar, transcript and anchored composer without a device bezel.
        line(c,14,23,24,23)
        line(c,14,27,21,27)
        text(c,'AI chat',10,34,29,font='medium')
        plus(c,125,25)
        line(c,12,42,132,42)
        prompt(c,30,60,102)
        text(c,'Assistant',7.5,14,140,font='medium',color=SOFT)
        reply(c,14,157,11.5)
        composer(c)
    else:
        # A complete generic app viewport. Controls are drawn at print-safe weights.
        box(c,10,12,124,228,11)
        line(c,19,26,28,26)
        line(c,19,30,25,30)
        text(c,'AI chat',9.5,39,32,font='medium')
        plus(c,121,28)
        line(c,10,46,134,46)
        prompt(c,32,60,94,9)
        # Neutral square, no interlaced or product-derived avatar.
        box(c,19,132,7,7,1.3)
        text(c,'Assistant',7.5,32,138,font='medium',color=SOFT)
        reply(c,19,156,10.8)
        # Familiar copy and retry controls, without invented feedback or ratings.
        box(c,20,180,5.5,6.5,.7)
        line(c,22,178,28,178)
        line(c,28,178,28,184)
        stroke(c,.8)
        c.arc(36,252-186,44,252-178,startAng=35,extent=280)
        line(c,44,180,44,177)
        line(c,44,180,41,180)
        composer(c,full=True)


def horizontal(c):
    base.ACTIVE = 'shared/horizontal'
    def t(value,size,x,y,**kw): text(c,value,size,x,y,h=144,w=252,**kw)
    t('AmirGetsLeads',23,18,38)
    t('Marketing and AI agency',10,18,56,font='body',color=SOFT)
    # Block tightened to fit four lines inside the 9pt safe margin: the build's
    # own safe-area assertion rejected the website at y=142, which is exactly
    # what that check is for.
    t('Amir Haider',12,18,84,font='medium')
    t('559-550-5474',11.5,18,101,font='body')
    t('amir@amirgetsleads.com',10.5,18,117,font='body')
    # Amir 2026-09-18: "on the other side i just want the website listed".
    # It was absent from the information face entirely.
    t('amirgetsleads.com',11,18,132,font='medium')


def face(c,take,side,material=False,bleed=True,upright=False):
    """Each file page is landscape. Rotate portrait composition in the page."""
    c.saveState()
    if bleed: c.translate(9,9)
    if side == 'vertical' and not upright:
        c.translate(252,0); c.rotate(90)
    w,h = (144,252) if side == 'vertical' else (252,144)
    if material:
        margin = 9 if bleed else 0
        base.rect(c,-margin,-margin,w+2*margin,h+2*margin,PAPER)
        c.saveState(); c.translate(-margin,-margin)
        base.linen(c,w+2*margin,h+2*margin); c.restoreState()
    if side == 'vertical': vertical(c,take)
    else: horizontal(c)
    c.restoreState()


def render(pdf):
    stem=pdf.stem
    prefix=HERE/'proofs'/stem
    subprocess.run(['pdftoppm','-r','300','-png',str(pdf),str(prefix)],check=True,stderr=subprocess.PIPE)
    for n,side in [(1,'vertical'),(2,'horizontal')]:
        path=Path(str(prefix)+f'-{n}.png')
        im=Image.open(path)
        assert im.size == (1125,675)
        im.save(HERE/'proofs'/f'{stem}-{side}-landscape-300dpi.png',dpi=(300,300))
        if side == 'vertical':
            im.transpose(Image.Transpose.ROTATE_270).save(HERE/'proofs'/f'{stem}-{side}-upright-300dpi.png',dpi=(300,300))
        path.unlink()


def comparison():
    path=HERE/'comparison-HOLD.pdf'
    c=canvas.Canvas(str(path),pagesize=(612,648))
    base.rect(c,0,0,612,648,'#E7E2D9')
    def label(s,x,y,size=10):
        c.setFillColor(HexColor(INK)); c.setFont('Helvetica',size); c.drawString(x,y,s)
    label('THE CARD THAT ANSWERS ITS OWN QUESTION',36,611,16)
    label('AXIOM NATURAL WHITE LINEN / 100# / DESIGN REVIEW',36,590,8)
    label('Three generic chat interfaces. Proposed choice: 02. Print specifications await Axiom.',36,568,9)
    for i,take in enumerate(TAKES):
        x=36+i*180
        label(f'{i+1:02d} / {TITLES[i]}',x,538,10)
        c.saveState(); c.translate(x,270)
        face(c,take,'vertical',material=True,bleed=False,upright=True)
        c.restoreState()
        label(['Minimal frame','Recognisably an app / ship','Fully rendered viewport'][i],x,253,8)
    label('SHARED INFORMATION FACE',36,223,10)
    c.saveState(); c.translate(36,62)
    face(c,TAKES[1],'horizontal',material=True,bleed=False); c.restoreState()
    for line,y in [
        ('All cards shown at actual trim size.',187),
        ('Print this sheet at 100% to judge scale.',172),
        ('Linen texture is a digital simulation.',145),
        ('No QR. Website on information face.',130),
        ('The exchange is authored card copy.',103),
        ('No captured AI response is presented.',88)]: label(line,318,y,9)
    label('REVIEW ONLY / 3.5 x 2 in trim / 0.125 in bleed and safety assumed / 18 Sep 2026',36,31,8)
    c.showPage(); c.save()
    subprocess.run(['pdftoppm','-r','300','-png','-singlefile',str(path),str(HERE/'proofs/comparison-HOLD-300dpi')],check=True,stderr=subprocess.PIPE)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('-o',type=Path,default=HERE/'report.md')
    args=parser.parse_args()
    if not args.o.resolve().is_relative_to(HERE):
        raise ValueError('Report output must stay inside brand/axiom/chat for this asset-only task.')
    (HERE/'proofs').mkdir(exist_ok=True)
    outputs=[]
    RECORDS.clear(); STROKES.clear()
    for take in TAKES:
        for material in [False,True]:
            suffix='linen' if material else 'artwork'
            out=HERE/f'{take}-{suffix}-HOLD.pdf'
            raw=HERE/f'.{take}-{suffix}-raw.pdf'
            c=canvas.Canvas(str(raw),pagesize=(270,162),pageCompression=1)
            for side in ['vertical','horizontal']:
                face(c,take,side,material=material)
                c.showPage()
            c.save(); base.finish(raw,out,252,144); render(out)
            outputs.append(out)
    comparison()
    records=list({json.dumps(r,sort_keys=True):r for r in RECORDS}.values())
    files={}
    for path in outputs+[HERE/'comparison-HOLD.pdf']:
        pages=PdfReader(path).pages
        if 'comparison' not in path.name:
            assert len(pages)==2
            for p in pages:
                assert list(p.mediabox)==[0,0,270,162]
                assert list(p.trimbox)==[9,9,261,153]
                assert list(p.bleedbox)==[0,0,270,162]
                assert not p.get('/Rotate',0)
                assert not p.get('/Annots')
                assert not p['/Resources'].get('/XObject')
                if '-artwork-' in path.name:
                    for operands,operator in p.get_contents().operations:
                        if operator == b'w': assert float(operands[0]) > .5
            files_horizontal = Image.open(HERE/'proofs'/f'{path.stem}-horizontal-landscape-300dpi.png').tobytes()
            if path.name.startswith(TAKES[0]):
                if '-artwork-' in path.name: shared_art = files_horizontal
                else: shared_linen = files_horizontal
            else:
                assert files_horizontal == (shared_art if '-artwork-' in path.name else shared_linen)
        files[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':len(pages)}
    inputs=[HERE.parent/'build.py',ROOT/'brand/source/font-outlines.c',ROOT/'brand/source/geist-700-outlines.json',
            ROOT/'brand/fonts/Geist-googlefonts-latin.woff2',HERE/'source/geist-400-outlines.json',
            HERE/'source/geist-500-outlines.json']
    report=(HERE/'report-source.md').read_text()
    for path in [HERE/'build.py',HERE/'report-source.md']:
        assert chr(0x2014) not in path.read_text(),path
    assert chr(0x2014) not in report
    args.o.parent.mkdir(parents=True,exist_ok=True)
    args.o.write_text(report)
    (HERE/'qr-verification.json').write_text(json.dumps(QR,indent=2)+'\n')
    result={'status':'HOLD, not press-ready','report_path':str(args.o.resolve()),
            'qr':QR,'files':files,'glyph_bounds':records,
            'font_inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
            'card_page_points':[270,162],'trim_points':[9,9,261,153],
            'safe_points':[18,18,252,144], 'all_card_pages_landscape':True,
            'all_card_text_outlined':True,'em_dash_check':'pass',
            'minimum_artwork_stroke_pt':min(STROKES),
            'shared_information_face_pixel_identical':True,
            'recommended_take':'02-app',
            'reviewed_dpi':300,
            'colour':'Exploratory DeviceRGB. No approved output intent.',
            'texture':'Procedural illustration only; absent from artwork PDFs.'}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'pdfs':len(files),'glyph_records':len(records),'report':str(args.o),'qr':QR['status']},indent=2))


if __name__=='__main__': main()
