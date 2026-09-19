"""Axiom exploration. No production exports. All writes stay in brand/axiom.

Run with the cached Python runtime and -o report.md. Layouts, type and material
shading are code-native PDF drawing, with untouched supplied art in test panels.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import random
import subprocess
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'brand/source'
PROOFS = HERE / 'proofs'
PAPER, INK, ORANGE = '#FBF8F2', '#14110A', '#FF4D1C'
FONTS = {k: json.loads((SOURCE / v).read_text()) for k, v in {
    'geist': 'geist-700-outlines.json', 'body': 'archivo-400-outlines.json',
    'medium': 'archivo-600-outlines.json'}.items()}
BLEED = 9
RECORDS = []
ACTIVE = ''
DIRECTIONS = ['01-natural-linen', '02-painted-edge', '03-personal-linen']


def glyphs(text, size, font='geist', italic=False):
    face = FONTS[font]
    scale = size / face['upem']
    x, commands = 0, []
    for ch in text:
        glyph = face['glyphs'][str(ord(ch))]
        for cmd in glyph['commands']:
            values = [cmd[0]]
            for i in range(1, len(cmd), 2):
                px, py = cmd[i:i+2]
                values += [x + (px + (math.tan(math.radians(14))*py if italic else 0))*scale, -py*scale]
            commands.append(values)
        x += glyph['advance']*scale + (-.02*size if font == 'geist' else 0)
    return commands


def text(c, value, size, x, baseline, h, font='geist', color=INK, italic=False, align='left', check=True, tw=252):
    commands = glyphs(value, size, font, italic)
    points = [(cmd[i], cmd[i+1]) for cmd in commands for i in range(1, len(cmd), 2)]
    x0, x1 = min(p[0] for p in points), max(p[0] for p in points)
    y0, y1 = min(p[1] for p in points), max(p[1] for p in points)
    dx = x - (x0 if align == 'left' else x1 if align == 'right' else (x0+x1)/2)
    bb = [x0+dx, y0+baseline, x1+dx, y1+baseline]
    if check:
        assert bb[0] >= 9 and bb[1] >= 9 and bb[2] <= tw-9 and bb[3] <= h-9, (value, bb, tw, h)
        RECORDS.append({'direction_side': ACTIVE, 'text': value, 'font': font, 'size_pt': size, 'bounds_trim_top_left_pt': bb})
    c.setFillColor(HexColor(color))
    p = c.beginPath()
    current = (0, 0)
    for cmd in commands:
        pts = [(cmd[i]+dx, h-(cmd[i+1]+baseline)) for i in range(1, len(cmd), 2)]
        if cmd[0] == 'M':
            p.moveTo(*pts[0]); current = pts[0]
        elif cmd[0] == 'L':
            p.lineTo(*pts[0]); current = pts[0]
        elif cmd[0] == 'Q':
            q, end = pts
            p.curveTo(current[0]+2*(q[0]-current[0])/3, current[1]+2*(q[1]-current[1])/3,
                      end[0]+2*(q[0]-end[0])/3, end[1]+2*(q[1]-end[1])/3, *end)
            current = end
        elif cmd[0] == 'C':
            p.curveTo(*[v for pt in pts for v in pt]); current = pts[-1]
        elif cmd[0] == 'Z':
            p.close()
    c.drawPath(p, fill=1, stroke=0, fillMode=1)


def rect(c, x, y, w, h, color):
    c.setFillColor(HexColor(color)); c.rect(x, y, w, h, stroke=0, fill=1)


def linen(c, w, h, overlay=False):
    """Illustrative crosshatch relief, not a measured Axiom stock or ink model."""
    rng = random.Random(764)
    c.saveState()
    p = c.beginPath(); p.rect(0, 0, w, h); c.clipPath(p, stroke=0, fill=0)
    # Broken, softly irregular relief avoids implying a printed graph grid.
    # Thread width and contrast remain illustrative, not measured stock data.
    c.setLineCap(1)
    for axis in (0, 1):
        limit = h if axis == 0 else w
        length = w if axis == 0 else h
        pos = -2.0
        while pos < limit + 2:
            pos += rng.uniform(1.0, 1.9)
            a = -2.0
            while a < length:
                run = rng.uniform(1.3, 5.0)
                drift = rng.uniform(-.22, .22)
                width = rng.uniform(.13, .37)
                shade = rng.uniform(.06, .14)
                for offset, color, alpha in [(0, '#8E8067', shade), (.24, '#FFFFFF', .16 if overlay else .65)]:
                    c.setStrokeColor(HexColor(color)); c.setStrokeAlpha(alpha)
                    c.setLineWidth(width)
                    b = pos+offset+.15*math.sin(a*.3+pos)
                    if axis == 0: c.line(a,b,a+run,b+drift)
                    else: c.line(b,a,b+drift,a+run)
                a += run+rng.uniform(.04,.30)
    c.restoreState()


def card(c, direction, side, material=False, bleed=True):
    """Draw at trim origin with upright reading orientation."""
    global ACTIVE
    ACTIVE = direction + '/' + side
    portrait = direction == DIRECTIONS[2]
    tw, th = (144, 252) if portrait else (252, 144)
    margin = 9 if bleed else 0
    c.saveState(); c.translate(margin, margin)
    # Bare artwork has no tint, texture or pretend paper ink.
    if material:
        rect(c, -margin, -margin, tw+2*margin, th+2*margin, PAPER if direction != DIRECTIONS[1] else '#FAF9F6')
        if direction != DIRECTIONS[1]:
            c.saveState(); c.translate(-margin, -margin)
            linen(c, tw+2*margin, th+2*margin); c.restoreState()
    def t(value, size, x, y, **kw):
        text(c, value, size, x, y, th, tw=tw, **kw)
    if direction == DIRECTIONS[0]:
        if side == 'front':
            t('AmirGets', 24, 18, 35)
            t('Leads', 28, 18, 64, italic=True)
            rect(c, 233, th-24, 3, 3, ORANGE)
            t('Amir Haider', 12, 236, 63, font='medium', align='right')
            t('(559) 550-5474', 11.5, 18, 92, font='medium')
            t('outreach@amirgetsleads.com', 10, 18, 111, font='body')
            t('amirgetsleads.com', 10, 18, 128, font='body')
        else:
            t('Get found. Get clients.', 13, 18, 30)
            t('Get back to life.', 13, 18, 48)
            t('Fresno and Los Angeles', 9, 18, 128, font='body')
    elif direction == DIRECTIONS[1]:
        if side == 'front':
            t('AmirGets', 33, 126, 58, align='center')
            t('Leads', 39, 126, 96, italic=True, align='center')
            t('Fresno and Los Angeles', 8.5, 126, 127, font='body', align='center')
        else:
            t('Amir Haider', 21, 22, 39)
            t('(559) 550-5474', 12, 22, 74, font='medium')
            t('outreach@amirgetsleads.com', 10.5, 22, 96, font='body')
            t('amirgetsleads.com', 10.5, 22, 118, font='body')
    else:
        if side == 'front':
            t('Amir', 25, 16, 43)
            t('Haider', 25, 16, 71)
            t('AmirGetsLeads', 10.5, 16, 94)
            t('(559) 550-5474', 10.5, 16, 177, font='medium')
            t('outreach@amirgetsleads.com', 8.5, 16, 196, font='body')
            t('amirgetsleads.com', 9, 16, 214, font='body')
            t('Fresno and Los Angeles', 8, 16, 236, font='body')
        else:
            t('AmirGets', 16, 16, 36)
            t('Leads', 19, 16, 57, italic=True)
    c.restoreState()


def finish(raw, out, tw, th):
    writer = PdfWriter()
    for page in PdfReader(raw).pages:
        writer.add_page(page)
        p = writer.pages[-1]
        p.trimbox.lower_left = (9, 9); p.trimbox.upper_right = (tw+9, th+9)
        p.bleedbox.lower_left = (0, 0); p.bleedbox.upper_right = (tw+18, th+18)
    writer.add_metadata({'/Title': out.stem, '/Author': 'AmirGetsLeads',
        '/Subject': 'EXPLORATION ONLY. RGB. 0.125 in bleed and safe are working conventions, not confirmed Axiom specs. Material PDFs simulate stock; never send to press.'})
    with out.open('wb') as stream: writer.write(stream)
    raw.unlink()


def render(pdf, prefix):
    cmd = ['pdftoppm', '-r', '300', '-png']
    subprocess.run(cmd+[str(pdf), str(prefix)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def label(c, value, x, y, size=10, color=INK):
    c.setFont('Helvetica', size); c.setFillColor(HexColor(color)); c.drawString(x, y, value)


def comparison():
    # PDF page is exactly 300-DPI compatible, card views remain 1:1 physical size.
    c = canvas.Canvas(str(HERE/'comparison.pdf'), pagesize=(630, 936))
    rect(c, 0, 0, 630, 936, '#E8E3DA')
    c.translate(0,36)
    label(c, 'AXIOM / THREE DIRECTIONS', 36, 856, 22)
    label(c, 'AmirGetsLeads   /   Material studies   /   18 September 2026', 36, 832, 10)
    label(c, '300 DPI at actual trim dimensions. Simulated materials. Exploration only.', 36, 810, 9)
    for i, title, sub, y in [
        (0, '01 / NATURAL LINEN', 'Warm, writable, owner-operator voice.', 772),
        (1, '02 / PAINTED EDGE', 'Smooth faces. Custom orange lives on the edge.', 531),
        (2, '03 / PERSONAL LINEN', 'A quieter introduction on the same linen stock as 01.', 290)]:
        label(c, title, 36, y, 13)
        label(c, sub, 36, y-18, 9)
        if i < 2:
            for j, side in enumerate(('front', 'back')):
                x = 36 + j*306
                label(c, side.upper(), x, y-36, 7.5)
                if i == 1:
                    # Edge is outside the face, never an orange face border.
                    rect(c, x, y-194, 252, 2.304, ORANGE)
                c.saveState(); c.translate(x, y-191); card(c, DIRECTIONS[i], side, material=True, bleed=False); c.restoreState()
            if i == 1: label(c, 'Edge strip is a schematic 32PT option, not a matched paint sample.', 36, y-215, 8)
        else:
            # Portrait panels at 1:1, with room for a caption alongside.
            for j, side in enumerate(('front','back')):
                x = 36+j*180
                c.saveState(); c.translate(x, 11); card(c, DIRECTIONS[i], side, material=True, bleed=False); c.restoreState()
            label(c, 'FRONT', 380, 242, 8)
            label(c, 'Name and contact details.', 380, 226, 9)
            label(c, 'BACK', 380, 191, 8)
            label(c, 'Quiet wordmark.', 380, 175, 9)
            label(c, 'Open paper for a note.', 380, 159, 9)
            label(c, 'No slogan. No orange.', 380, 124, 9)
    c.showPage(); c.save()
    render(HERE/'comparison.pdf', PROOFS/'comparison-300dpi')


def stress_panel(c, x, y, kind, simulated):
    c.saveState(); c.translate(x, y)
    p=c.beginPath(); p.rect(0,0,252,144); c.clipPath(p,stroke=0,fill=0)
    rect(c,0,0,252,144,PAPER)
    if kind == 0:
        card(c, DIRECTIONS[0], 'front', False, False)
    elif kind == 1:
        rect(c,0,0,252,144,INK)
        text(c,'Amir Haider',21,18,39,144,color=PAPER)
        text(c,'outreach@amirgetsleads.com',10,18,110,144,color=PAPER,font='body')
    else:
        # Intact supplied spark image, geometrically clipped to card trim.
        # 1024 pixels across 3.5 inches gives 292.57 effective source DPI.
        c.drawImage(str(ROOT/'brand/avatars/spark-ink-1024.png'),0,-54,width=252,height=252)
    if simulated:
        linen(c,252,144,True)
        # An intentionally assumed defect field, not measured ink behaviour.
        rng=random.Random(425+kind)
        c.setFillColor(HexColor(PAPER)); c.setFillAlpha(.14)
        for _ in range(1600):
            x0,y0=rng.uniform(0,252),rng.uniform(0,144)
            c.rect(x0,y0,rng.uniform(.08,.28),rng.uniform(.08,.32),fill=1,stroke=0)
    c.restoreState()


def stress():
    c = canvas.Canvas(str(HERE/'linen-stress-test.pdf'),pagesize=(612,792))
    rect(c,0,0,612,792,'#E8E3DA')
    label(c,'LINEN / COVERAGE AND LINEWORK',36,751,20)
    label(c,'Digital sensitivity study. Deliberately assumed relief and ink loss. Not a press prediction.',36,730,8)
    label(c,'FLAT CONTROL',36,700,10)
    label(c,'SIMULATED LINEN + ASSUMED INK LOSS',324,700,9)
    for kind,title,y in [(0,'01 / Sparse dark type on bare paper',526),(1,'02 / Full dark coverage with reversed type',310),(2,'03 / Supplied engraved spark, cropped at card scale',94)]:
        label(c,title,36,y+158,10)
        stress_panel(c,36,y,kind,False); stress_panel(c,324,y,kind,True)
    label(c,'Each panel is 3.5 x 2 in. Source spark: 1024 px at 3.5 in = 292.6 effective DPI.',36,64,8)
    label(c,'Texture visibility and defects are illustrative. A physical printed sample is required.',36,48,8)
    c.showPage(); c.save(); render(HERE/'linen-stress-test.pdf',PROOFS/'linen-stress-test-300dpi')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-o','--report',type=Path,required=True)
    args=parser.parse_args()
    PROOFS.mkdir(parents=True,exist_ok=True)
    for direction in DIRECTIONS:
        tw,th=(144,252) if direction == DIRECTIONS[2] else (252,144)
        for material in (False, True):
            suffix='material-study' if material else 'artwork-study'
            out=HERE/f'{direction}-{suffix}.pdf'
            raw=HERE/'_raw.pdf'
            c=canvas.Canvas(str(raw),pagesize=(tw+18,th+18))
            for side in ('front','back'):
                card(c,direction,side,material); c.showPage()
            c.save(); finish(raw,out,tw,th)
            prefix=PROOFS/f'{direction}-{suffix}'
            render(out,prefix)
            for n,side in enumerate(('front','back'),1):
                path=PROOFS/f'{prefix.name}-{n}.png'
                final=PROOFS/f'{direction}-{side}-{suffix}-300dpi.png'
                # Rename Poppler outputs only, no material edits to bitmap artwork.
                path.rename(final)
                # Poppler rounds half-pixel page bounds upward.
                expected=(math.ceil((tw+18)*300/72),math.ceil((th+18)*300/72))
                assert Image.open(final).size == expected, (final,Image.open(final).size,expected)
    comparison(); stress()
    inputs=[SOURCE/f for f in ('geist-700-outlines.json','archivo-400-outlines.json','archivo-600-outlines.json')]+[ROOT/'brand/avatars/spark-ink-1024.png']
    verification={
        'purpose':'Exploration only. Not press ready.',
        'branch':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),
        'working_convention':{'trim_in':[3.5,2],'bleed_in':.125,'safe_in':.125,'axiom_confirmed':False},
        'portrait_direction':'03-personal-linen uses the same physical trim, rotated to 2 x 3.5 in',
        'dpi':300,'landscape_bleed_png_px':[1125,675],'portrait_bleed_png_px':[675,1125],
        'color':'DeviceRGB exploration. No assigned press profile or PDF/X certification.',
        'material_simulation':'Procedural vector crosshatch. Paper shade is a placeholder. Not measured Axiom stock.',
        'orange':'01 front has one 3pt square. 02 faces and all 03 faces have no orange.',
        'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},
        'bounds':RECORDS,'report_destination':str(args.report.resolve()),
        'pdf_checks':[]}
    for path in sorted(HERE.glob('*.pdf')):
        r=PdfReader(path)
        verification['pdf_checks'].append({'file':path.name,'pages':len(r.pages),'media_boxes':[list(p.mediabox) for p in r.pages],'trim_boxes':[list(p.trimbox) for p in r.pages]})
    (HERE/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    template=HERE/'report-source.md'
    assert template.exists(), 'Write the report-source.md before running.'
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(template.read_text())
    print(json.dumps({'report':str(args.report),'pdfs':len(verification['pdf_checks']),'text_instances_checked':len(RECORDS)},indent=2))


if __name__=='__main__': main()
