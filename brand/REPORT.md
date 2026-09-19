# MOO Luxe card, second pass

Ship the **ink-front direction with the portrait spark back and Tiger Orange seam**. The larger stacked wordmark, right-aligned name and ruled contact band give the front a deliberate structure. The ink ground connects both faces; the spark supplies an identifiable image when the card turns in the hand. The paper alternative is equally complete and easier to annotate on its front, but ink is the stronger visual pairing.

The single comparison image is `proofs/moo-luxe-directions-side-by-side-300dpi.png`. It shows both fronts above their portrait backs, at trim, using native 300-DPI pixels. Its full size is 2356 x 2160 px. Screen display size depends on the viewer.

## Deliverables

All paths below are relative to `brand/`.

| File | Purpose |
| --- | --- |
| `business-cards-moo-luxe-ink.pdf` | Recommended direction, front then back |
| `business-cards-moo-luxe-paper.pdf` | Paper-front alternative, front then identical back |
| `business-cards-moo-luxe.pdf` | Byte-identical copy of the recommended ink PDF at the existing handoff path |
| `proofs/moo-luxe-paper-front-300dpi.png` | Paper front with bleed |
| `proofs/moo-luxe-paper-back-300dpi.png` | Paper direction's rotated portrait back, landscape upload artboard |
| `proofs/moo-luxe-ink-front-300dpi.png` | Ink front with bleed |
| `proofs/moo-luxe-ink-back-300dpi.png` | Ink direction's rotated portrait back, landscape upload artboard |
| `proofs/moo-luxe-{paper,ink}-back-upright-300dpi.png` | Upright portrait viewing copies, not differently sized PDF uploads |
| `proofs/moo-luxe-directions-side-by-side-300dpi.png` | One comparison sheet containing all four faces |
| `proofs/moo-luxe-{front,back}-300dpi.png` | Existing proof paths updated to the recommended direction |
| `source/build-moo.py` | Card-only builder with `-o` report output support |
| `source/moo-luxe-verification.json` | Geometry, glyph bounds, contrast, CMYK values and source checksums |
| `REPORT-first-pass.md` | Preserved first-pass report; historical, not the current card specification |

## Design and content

Real Geist 700 outlines and Archivo 400/600 are retained from the verified cached fonts. `AmirGets` sits above orange italic `Leads`, retaining camel case, -0.02em Geist tracking and the existing 14-degree synthetic italic treatment. All printed typography remains vector outlines, without fallback fonts. Dark type on the paper front uses single K for registration; its paper ground is the CMYK conversion of #FBF8F2. The ink front uses the conversion of #14110A, with paper lettering and orange Leads.

Both front layouts use a larger 28pt / 36pt wordmark, a name anchor at right, a 0.45pt rule and two aligned contact rows. The bottom-right quadrant now contains the email and service locations. Only the verified name, phone, email, website and Fresno and Los Angeles appear. There is no street address or invented positioning.

The supplied `avatars/spark-ink-1024.png` is placed intact and converted to CMYK. Its original file is untouched. This is the corrected asset with the composited CSS glow, not the first-pass glowless crop. Its SHA-256 is recorded in verification. The earlier avatar assessment is not carried over to this card-scale artwork, and the AL avatar recommendation remains unchanged.

`CARD_DIRECTION.md` appeared during this pass and supplied the mixed-orientation decision. The front reads landscape; the back reads portrait. The portrait composition is rotated 90 degrees inside the same landscape PDF page. No portrait-shaped PDF page is delivered. Turning the landscape back clockwise makes the statement upright. The paper statement reads exactly: "Get found. Get clients. Get back to life." It sits above the hands and luminous gap.

The ink/image field reaches the bleed edges; an intentional unprinted band interrupts it at the portrait bottom to satisfy the writing-space requirement. This band is 2.0 x 0.719 inches within trim. It knocks out all four plates, leaving actual substrate rather than pale printed ink. The image is not a small inset or a bordered thumbnail. In the upright portrait composition the hands reach horizontally across the card; in the landscape upload artboard their reach is vertical.

## Production verification

| Check | Result |
| --- | --- |
| Branch | `feat/brand-assets` |
| Pages per PDF | 2, front then back |
| MediaBox / BleedBox | 263.52 x 155.52 pt, 3.66 x 2.16 in |
| TrimBox | [5.76, 5.76, 257.76, 149.76] pt, 3.5 x 2.0 in |
| Safe area | 3.34 x 1.84 in; all glyph bounds checked inside it |
| Bleed per edge | 0.08 in, 2.032 mm |
| Page rotation metadata | 0; back content itself is rotated |
| Individual page PNGs | 1098 x 648 px, 300 DPI |
| Upright back viewing PNGs | 648 x 1098 px, 300 DPI |
| Spark effective resolution | 474.07 DPI from the supplied 1024px image at 2.16 in |
| Crop marks | None |
| Type | Outlined, no embedded or substituted text fonts |
| Colour | CMYK image and vector paints, four-channel ICC OutputIntent |

I rendered and visually inspected both fronts and both backs, including the rotated upload view and upright reading view, and inspected the single comparison sheet. The type is unclipped, counters are intact, the front's paired footer rows are separated, and the back statement does not cross the spark. Both back renders are pixel-identical. The note band is white in the rendered proof and zero-ink CMYK in the PDF. The render is a digital check, not a physical stock sample.

## Colour honesty

| Pair | sRGB contrast | Normal-text AA |
| --- | --- | --- |
| Orange #FF4D1C on paper #FBF8F2 | 3.13:1 | Fail |
| Orange #FF4D1C on ink #14110A | 5.68:1 | Pass |

Orange remains confined to the large front wordmark and supplied spark art. Small contact type is dark on paper or paper on ink. These digital ratios do not predict press contrast.

The Generic CMYK ICC conversion gives orange approximately C0 M73.33 Y85.49 K0, paper C1.96 M2.35 Y3.92 K0, and ink C70.20 M69.02 Y70.59 K71.37 (about 281% total ink). The profile is the existing fallback, not a MOO-specific uncoated profile. The PDFs are not certified PDF/X. Paper is a faint printed tint on the paper front; the writing band is unprinted stock. Warm paper type and black can look different in different PDF viewers.

Tiger Orange is a physical seam choice. The requested orange Leads and orange spark mean the seam is **not the only orange in the object**. These two versions therefore do not eliminate orange's CMYK gamut limitation. The explicit request to retain those elements takes precedence over the seam-only colour rationale in the direction note. No fluorescent ink, exact seam match or physical press proof is claimed. MOO upload acceptance and the physical mixed-orientation flip have not been checked in its ordering interface.

## Scope and report destination

Only assets and documentation under `brand/` were authored. No HTML page or deploy configuration was changed. The supplied spark, fonts, avatar exports, GBP assets, generic printer PDF, MOO spec and card direction note were preserved. No commit, push, deployment or print order was made.

No caller-provided `-o` path was visible in the conversation. After requesting it and receiving no replacement, I used the announced fallback and ran:

```sh
/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 brand/source/build-moo.py -o /Users/amir/amgwebsite/brand/REPORT.md
```

The builder writes this report to its `-o` argument. The current destination is `/Users/amir/amgwebsite/brand/REPORT.md`. New textual card sources and documentation were checked for the forbidden em dash.
