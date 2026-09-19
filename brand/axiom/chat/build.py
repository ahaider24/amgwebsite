"""Build held Axiom chat studies. All outputs stay beside this file.

Use the cached Python runtime with ReportLab, Pillow, pypdf and Poppler.
No QR is generated until a prompt URL has been verified in a live browser.
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
TAKES = ['01-understated', '02-exchange', '03-dialogue']
RECORDS = base.RECORDS
QR = {'encoded_url': None, 'status': 'PLACEHOLDER: prefill not verified',
      'candidate_url': 'https://chatgpt.com/?q=Why%20should%20I%20hire%20AmirGetsLeads%3F',
      'prompt': 'Why should I hire AmirGetsLeads?',
      'attempt_date': '2026-09-18',
      'browser_result': 'No browser is available',
      'web_result': 'Failed to fetch, Cache miss; normalized spaces to +',
      'reserved_square_pt': 64.8, 'reserved_square_inches': 0.9,
      'quiet_zone': 'Must be included inside the reserved square when a code is approved.'}


def text(c, value, size, x, y, h=252, w=144, **kw):
    assert chr(0x2014) not in value
    base.text(c, value, size, x, y, h, tw=w, **kw)


def qr_placeholder(c):
    """Removed 2026-09-18. Amir: "no qr code, our brand will adapt in the next
    months, we just need to complete the move." The right call: the engine's own
    measurement shows AmirGetsLeads at zero mentions across AI surfaces while
    AmirGetsJobs still has 27, so a scan would have asked about a brand the
    models do not know yet. The website on the information face carries it
    instead, and the vertical face is stronger without a third of it given to a
    placeholder."""
    return


def vertical(c, take):
    base.ACTIVE = take+'/vertical'
    if take == TAKES[0]:
        for line,y in zip(['I need marketing','but I don\'t know','who to pick.'],[74,95,116]):
            text(c,line,14.5,16,y,font='body',color=SOFT)
        text(c,'AmirGetsLeads.',13.5,16,160)
        text(c,'Turn the card over.',10,16,178,font='body')
    elif take == TAKES[1]:
        for line,y in zip(['I need marketing','but I don\'t know','who to pick.'],[74,95,116]):
            text(c,line,14.5,16,y,font='body',color=SOFT)
        # One non-semantic orange mark. Weight and indent carry the exchange.
        base.rect(c,16,252-149,3,3,ORANGE)
        text(c,'AmirGetsLeads.',12.5,28,153)
        text(c,'Turn the card over.',9.5,28,172,font='body')
    else:
        text(c,'QUESTION',7,16,62,font='medium',color=SOFT)
        for line,y in zip(['I need marketing','but I don\'t know','who to pick.'],[83,101,119]):
            text(c,line,13.5,16,y,font='body',color=SOFT)
        text(c,'ANSWER',7,16,146,font='medium',color=SOFT)
        text(c,'AmirGetsLeads.',13.5,16,166)
        text(c,'Turn the card over.',10,16,183,font='body')
    qr_placeholder(c)


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
    label('HOLD: brand findability, email alias, QR prefill and Axiom specification approval.',36,568,9)
    for i,take in enumerate(TAKES):
        x=36+i*180
        label(['01 / UNDERSTATED','02 / EXCHANGE','03 / DIALOGUE'][i],x,538,10)
        c.saveState(); c.translate(x,270)
        face(c,take,'vertical',material=True,bleed=False,upright=True)
        c.restoreState()
        label(['Nearly invisible','Moderate / proposed choice','More explicit'][i],x,253,8)
    label('SHARED INFORMATION FACE',36,223,10)
    c.saveState(); c.translate(36,62)
    face(c,TAKES[1],'horizontal',material=True,bleed=False); c.restoreState()
    for line,y in [
        ('All cards shown at actual trim size.',187),
        ('Print this sheet at 100% to judge scale.',172),
        ('Linen texture is a digital simulation.',145),
        ('No QR: the website carries it on the information face.',130),
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
    comparison()
    records=list({json.dumps(r,sort_keys=True):r for r in RECORDS}.values())
    files={}
    for path in sorted(HERE.glob('*.pdf')):
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
        files[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':len(pages)}
    inputs=[HERE.parent/'build.py',ROOT/'brand/source/font-outlines.c',ROOT/'brand/source/geist-700-outlines.json',
            ROOT/'brand/fonts/Geist-googlefonts-latin.woff2',HERE/'source/geist-400-outlines.json',
            HERE/'source/geist-500-outlines.json']
    report=(HERE/'report-source.md').read_text()
    for path in [HERE/'build.py',HERE/'report-source.md']:
        assert chr(0x2014) not in path.read_text(),path
    args.o.write_text(report)
    (HERE/'qr-verification.json').write_text(json.dumps(QR,indent=2)+'\n')
    result={'status':'HOLD, not press-ready','report_path':str(args.o.resolve()),
            'qr':QR,'files':files,'glyph_bounds':records,
            'font_inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
            'card_page_points':[270,162],'trim_points':[9,9,261,153],
            'safe_points':[18,18,252,144], 'all_card_pages_landscape':True,
            'all_text_outlined':True,'em_dash_check':'pass',
            'colour':'Exploratory DeviceRGB. No approved output intent.',
            'texture':'Procedural illustration only; absent from artwork PDFs.'}
    (HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'pdfs':len(files),'glyph_records':len(records),'report':str(args.o),'qr':QR['status']},indent=2))


if __name__=='__main__': main()
