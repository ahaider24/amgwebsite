"""MOO Luxe second pass. Rebuild only card assets, never the site or avatars."""
from build import *
import argparse
import shutil
from PIL import ImageFont

BLEED = 0.08 * 72
W, H = 3.66 * 72, 2.16 * 72
SAFE = (2 * BLEED, 2 * BLEED, W - 2 * BLEED, H - 2 * BLEED)
PROOFS = B / 'proofs'
SPARK = B / 'avatars/spark-ink-1024.png'
COLORS = {v: colour(v) for v in (INK, PAPER, ORANGE)}
K = (0, 0, 0, 1)
WHITE = (0, 0, 0, 0)
TEXT_BOUNDS = []


def rect(c, x, y, width, height, fill):
    c.setFillColor(CMYKColor(*fill))
    c.rect(x, H-y-height, width, height, fill=1, stroke=0)


def text(c, value, size, x, baseline, fill, font='geist', italic=False, right=False):
    commands = glyphs(value, size, font=font, italic=italic)
    b = bounds(commands)
    # Align visible outline edges, rather than variable side bearings.
    dx = x + BLEED - (b[2] if right else b[0])
    dy = baseline + BLEED
    commands = [[cmd[0]] + [v + (dx if i % 2 else dy)
                for i, v in enumerate(cmd[1:], 1)] for cmd in commands]
    b = bounds(commands)
    assert b[0] >= SAFE[0] and b[1] >= SAFE[1] and b[2] <= SAFE[2] and b[3] <= SAFE[3], (value, b)
    TEXT_BOUNDS.append({'text': value, 'bounds_pt_from_top_left': b})
    drawpath(c, commands, fill, H)


def front(c, direction):
    dark = direction == 'ink'
    rect(c, 0, 0, W, H, COLORS[INK if dark else PAPER])
    fg = COLORS[PAPER] if dark else K
    text(c, 'AmirGets', 28, 15, 36, fg)
    text(c, 'Leads', 36, 15, 75, COLORS[ORANGE], italic=True)
    text(c, 'Amir Haider', 11.5, 237, 74, fg, font='bodybold', right=True)
    # The rule and paired footer rows make every corner purposeful.
    rect(c, BLEED+15, BLEED+90, 222, 0.45, fg)
    text(c, '(559) 550-5474', 9.5, 15, 110, fg, font='body')
    text(c, 'outreach@amirgetsleads.com', 9.2, 237, 110, fg, font='body', right=True)
    text(c, 'amirgetsleads.com', 10, 15, 130, fg, font='bodybold')
    text(c, 'Fresno and Los Angeles', 7.6, 237, 130, fg, font='body', right=True)


def back(c):
    # Portrait composition rotated inside an unchanged landscape PDF page.
    pw, ph = H, W
    c.saveState()
    c.translate(W, 0)
    c.rotate(90)
    c.setFillColor(CMYKColor(*COLORS[INK]))
    c.rect(0, 0, pw, ph, fill=1, stroke=0)
    art = ImageCms.applyTransform(Image.open(SPARK).convert('RGB'), TO_CMYK)
    c.drawImage(ImageReader(art), 0, ph-58-pw, width=pw, height=pw)
    for value, baseline in [('Get found.',24), ('Get clients.',42), ('Get back to life.',60)]:
        commands=glyphs(value,14)
        bx=bounds(commands)[0]
        commands=[[cmd[0]]+[v+(BLEED+15-bx if i%2 else BLEED+baseline)
                  for i,v in enumerate(cmd[1:],1)] for cmd in commands]
        b=bounds(commands)
        assert b[0]>=2*BLEED and b[1]>=2*BLEED and b[2]<=pw-2*BLEED and b[3]<=ph-2*BLEED
        TEXT_BOUNDS.append({'text':value,'portrait_bounds_pt_from_top_left':b})
        drawpath(c,commands,COLORS[PAPER],ph)
    # Real unprinted stock for a short handwritten note.
    c.setFillColor(CMYKColor(*WHITE))
    c.rect(0,0,pw,ph-206,fill=1,stroke=0)
    c.restoreState()


def finish(raw, out, direction):
    writer = PdfWriter()
    for page in PdfReader(raw).pages:
        writer.add_page(page)
        p = writer.pages[-1]
        p.trimbox.lower_left = (BLEED, BLEED)
        p.trimbox.upper_right = (BLEED+252, BLEED+144)
        p.bleedbox.lower_left = (0, 0)
        p.bleedbox.upper_right = (W, H)
    profile = DecodedStreamObject()
    profile.set_data(ICC.read_bytes())
    profile[NameObject('/N')] = NumberObject(4)
    intent = DictionaryObject({
        NameObject('/Type'): NameObject('/OutputIntent'),
        NameObject('/S'): NameObject('/GTS_PDFX'),
        NameObject('/OutputConditionIdentifier'): TextStringObject('Generic CMYK Profile'),
        NameObject('/Info'): TextStringObject('Generic CMYK fallback; not a MOO press profile.'),
        NameObject('/DestOutputProfile'): writer._add_object(profile)})
    writer._root_object[NameObject('/OutputIntents')] = ArrayObject([writer._add_object(intent)])
    writer.add_metadata({'/Title': f'AmirGetsLeads MOO Luxe: {direction} front + spark back',
        '/Author': 'AmirGetsLeads',
        '/Subject': '3.66 x 2.16 in bleed; 3.5 x 2 in trim; 3.34 x 1.84 in safe; outlined type; CMYK; no crop marks; not certified PDF/X.'})
    with out.open('wb') as stream:
        writer.write(stream)


def proofsheet():
    sheet = Image.new('RGB', (2356, 2160), '#E5E0D7')
    d = ImageDraw.Draw(sheet)
    # Proof annotations only. Printed typography remains genuine outlined Geist/Archivo.
    face = '/System/Library/Fonts/Helvetica.ttc'
    title = ImageFont.truetype(face, 38)
    label = ImageFont.truetype(face, 24)
    small = ImageFont.truetype(face, 20)
    d.text((80, 34), 'AmirGetsLeads / MOO Luxe', font=title, fill=INK)
    d.text((80, 90), 'Two front directions. Shared spark reverse. Tiger Orange seam.', font=label, fill=INK)
    for direction, x, name in [('paper',80,'01 / PAPER FRONT'),('ink',1226,'02 / INK FRONT')]:
        d.text((x,160), name, font=label, fill=INK)
        for side, y in [('front',208),('back',900)]:
            im = Image.open(PROOFS/f'moo-luxe-{direction}-{side}-300dpi.png').convert('RGB')
            # Show actual trim at native 300-DPI raster size. Bleed remains in individual proofs.
            trim = im.crop((24,24,1074,624))
            if side == 'back':
                trim = trim.transpose(Image.Transpose.ROTATE_270)
            px = x + (1050-trim.width)//2
            d.rectangle((px-1,y-1,px+trim.width,y+trim.height), fill='#BEB6A9')
            sheet.paste(trim,(px,y))
        d.text((x,852),'PORTRAIT SPARK BACK / shown upright',font=small,fill=INK)
    d.text((80,2040),'Trim shown at 300 DPI. Screen colour is a CMYK preview; seam is a physical stock choice.',font=small,fill=INK)
    sheet.save(PROOFS/'moo-luxe-directions-side-by-side-300dpi.png',dpi=(300,300))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--report', type=Path, default=B/'REPORT.md')
    args = parser.parse_args()
    PROOFS.mkdir(exist_ok=True)
    for direction in ('paper','ink'):
        raw = Path(f'/tmp/agl-moo-{direction}-raw.pdf')
        out = B/f'business-cards-moo-luxe-{direction}.pdf'
        c = canvas.Canvas(str(raw),pagesize=(W,H),pageCompression=1)
        front(c,direction)
        c.showPage()
        back(c)
        c.showPage()
        c.save()
        finish(raw,out,direction)
        prefix=PROOFS/f'moo-luxe-{direction}'
        subprocess.run(['pdftoppm','-r','300','-png',str(out),str(prefix)],check=True)
        for n,side in [(1,'front'),(2,'back')]:
            p=PROOFS/f'moo-luxe-{direction}-{n}.png'
            im=Image.open(p)
            assert im.size == (1098,648), im.size
            im.save(PROOFS/f'moo-luxe-{direction}-{side}-300dpi.png',dpi=(300,300))
            if side == 'back':
                im.transpose(Image.Transpose.ROTATE_270).save(PROOFS/f'moo-luxe-{direction}-back-upright-300dpi.png',dpi=(300,300))
            p.unlink()
        raw.unlink()
    # Stable handoff filename now points to the recommended ink direction.
    shutil.copyfile(B/'business-cards-moo-luxe-ink.pdf',B/'business-cards-moo-luxe.pdf')
    for side in ('front','back'):
        shutil.copyfile(PROOFS/f'moo-luxe-ink-{side}-300dpi.png',PROOFS/f'moo-luxe-{side}-300dpi.png')
    proofsheet()
    metrics = {
        'bleed_inches':[3.66,2.16], 'trim_inches':[3.5,2], 'safe_inches':[3.34,1.84],
        'bleed_per_edge_inches':0.08,'raster_pixels':[1098,648],'raster_dpi':300,
        'note_band_trim_inches':[2.0,round((BLEED+252-206)/72,6)],
        'spark_source_pixels':[1024,1024], 'spark_placed_effective_dpi':1024/2.16,
        'spark_sha256':hashlib.sha256(SPARK.read_bytes()).hexdigest(),
        'contrast_orange_paper':contrast(ORANGE,PAPER),'contrast_orange_ink':contrast(ORANGE,INK),
        'cmyk_percent':{k:[round(v*100,2) for v in c] for k,c in COLORS.items()},
        'icc_profile':str(ICC),'icc_sha256':hashlib.sha256(ICC.read_bytes()).hexdigest(),
        'text_safe_bounds_checked':True,'text_bounds':TEXT_BOUNDS,
        'report_path':str(args.report.resolve())}
    (B/'source/moo-luxe-verification.json').write_text(json.dumps(metrics,indent=2)+'\n')
    template=B/'source/moo-luxe-report.md'
    if template.exists():
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(template.read_text())
    print(json.dumps({k:v for k,v in metrics.items() if k!='text_bounds'},indent=2))

if __name__ == '__main__':
    main()
