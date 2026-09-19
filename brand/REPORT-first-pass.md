# AmirGetsLeads brand asset report

Built on `feat/brand-assets`. All authored outputs are in `brand/`. No HTML, live site asset, deploy configuration, push, or deployment was changed or performed. The existing five photographs are untouched. `MOO_LUXE_SPEC.md` appeared during the build and was treated as a supplied production note, not authored by this build.

## Completion status

All asset creation and visual checks are complete. The requested commit was attempted and failed because the sandbox denied creation of `.git/index.lock` with Operation not permitted. Git metadata is read-only and escalation is disabled. No commit was created. All deliverables remain in the working tree on `feat/brand-assets`.

The command-line `-o` destination was not exposed to this process. This report is saved at `brand/REPORT.md`; the final response also provides the handoff for capture by the caller.

## Recommendation and visual review

Recommend **B, the AL monogram**, for social use. At native 48px the paper A and orange italic L remain readable, with strong separation from the ink ground. A stands for Amir and L for Leads; the second letter carries the payoff colour and italic treatment. Its circle crop retains both letters.

Direction A is an exact crop of the hero engraving around the fingertip gap. The hero's alpha channel is essential: its uncomposited RGB layer looks like a glow. I composited it on warm paper, then cropped the original region x1149..1909, y-50..710, padding above the original with paper. No generated letterforms, replacement hand art, or invented spark was added. At 48px it reads as two pale fingertips, but the mechanical detail and focal gap are weaker than the monogram. At 180px and 1024px it is distinctive and attractive. The SVG contains its raster crop, not traced vector art; the 1024px export upscales the 760px crop.

Both directions were rendered from their SVG sources and personally inspected at 48, 180 and 1024px. All 400px and 512px exports were inspected in a native-size contact sheet. The 180px circular crops were also viewed.

GBP retains the stacked camel-case relationship: AmirGets above orange italic Leads, on #FBF8F2. Both the full 1024px PNG and a circular-mask proof were viewed. The farthest non-paper pixel is 337.54px from centre, inside the 512px circle radius, leaving about 174.46px of radial clearance. Nothing meaningful is clipped.

The generic card front and back were rendered from the final PDF at 300dpi and inspected with bleed and crop marks visible. The front contains only verified details. The back uses the existing hero art and the site's exact positioning: Get found. Get clients. Get back to life. A contour-fill issue found during review was corrected, and the final lettering was re-rendered and inspected.

## Type and source provenance

Geist 700 is real Google Fonts Geist, with -0.02em tracking. Fresh shell downloads failed because DNS/network access was restricted, and no connected browser was available. I recovered the exact WOFF2 already downloaded by the browser for amirgetsleads.com, identified its Google Fonts URL, matched its cached source CSS, and verified its Geist family and 100..900 weight axis. Archivo was recovered the same way for 400/600 contact typography. These are not substitute fonts.

The wordmark's orange italic is a deterministic 14-degree synthetic italic applied to Geist 700 outlines. This reflects the site's CSS relationship: upright Geist is loaded and italic is requested in styling. All type in the SVG wordmark, monogram and PDFs is outlined. The back statement uses Geist 700; no substitute Bricolage face was introduced.

Official font sources: [Geist Google Fonts binary](https://fonts.gstatic.com/s/geist/v5/gyByhwUxId8gMEwcGFWNOITd.woff2), [Archivo Google Fonts binary](https://fonts.gstatic.com/s/archivo/v25/k3kPo8UDI-1M0wlSV9XAw6lQkqWY8Q82sLydOxKsv4Rn.woff2), [Geist metadata](https://raw.githubusercontent.com/google/fonts/main/ofl/geist/METADATA.pb). Source CSS and SIL OFL license are bundled.

## Print specifications and colour

`business-cards.pdf` is two pages, front then back. Trim is exactly 252 x 144pt, or 3.5 x 2 inches. It has 3mm bleed on all sides and crop marks outside the bleed. Media size is 288 x 180pt, or 4 x 2.5 inches. TrimBox and BleedBox are explicit. The 300dpi PNG proofs are 1200 x 750px. Lettering is vector; the back hero image is 1121 x 267px at approximately 300dpi. All PDF paint and image colour is CMYK, with an embedded four-channel Generic CMYK OutputIntent. Small dark lettering is single K to avoid registration fringing.

**#FF4D1C is a bright RGB orange and will shift when converted to CMYK.** I used an ICC conversion with relative colorimetric intent and black-point compensation. The approximate output is C0 M73.33 Y85.49 K0. The paper tint is C1.96 M2.35 Y3.92 K0. Large ink areas convert to C70.20 M69.02 Y70.59 K71.37, about 281% total ink. The digital assets retain the exact RGB tokens. No fluorescent or spot ink is implied.

A separate `business-cards-moo-luxe.pdf` responds to the production note added during this build. It uses MOO Standard dimensions: 3.66 x 2.16 inch bleed, 3.5 x 2 inch trim, with no crop marks. Its 300dpi proofs are 1098 x 648px. The front retains the orange payoff word; the reverse uses dark positioning text and leaves a large unprinted writing area. Natural stock supplies the paper ground. These dimensions and the writable uncoated stock were verified against [MOO's official Luxe guidelines](https://www.moo.com/us/business-cards/luxe). The supplied note recommends Tiger Orange for the seam. I did not order anything or verify a physical colour match.

Both PDFs use a generic CMYK fallback profile because a printer-specific profile was not supplied. They are not certified PDF/X. Press, substrate, physical orange shift, seam match, duplex orientation at a specific printer, and MOO's upload acceptance have not been physically or interactively verified. The MOO artboard follows the published numeric guidelines; template binaries could not be downloaded through the restricted shell. A stock-specific printer proof remains necessary, especially for uncoated paper.

## Contrast

| Pair | Ratio | WCAG AA for normal text | AA for large text |
| --- | ---: | --- | --- |
| #FF4D1C on #FBF8F2 | 3.13:1 | Fail | Pass |
| #FF4D1C on #14110A | 5.68:1 | Pass | Pass |
| #C8380E on #FBF8F2 | 4.92:1 | Pass | Pass |

Normal text needs 4.5:1; large text needs 3:1. The calculation uses standard sRGB relative luminance. Orange on paper is reserved for the large logo payoff; small contact information is dark. Logos are exempt from the text requirement, but the ratios are reported rather than hidden behind that exemption. RGB contrast calculations do not predict printed-stock contrast.

## Favicons

Inspected `favicon.svg`, `favicon-48.png`, `favicon-192.png`, and `apple-touch-icon.png`, including a PNG render of the SVG. All use an orange serif A on ink, with no old name or blue ground. They are fine with respect to the requested old-brand check and were left unchanged. Their existing Georgia-style serif is not Geist; this is explicitly documented, not presented as a newly harmonized icon set. `favicon.ico` was also left untouched. The review sheet captures all four requested files.

## File inventory

All paths below are relative to `brand/`. Byte counts refer to final files. The supplied MOO specification is listed for context and was excluded from the attempted staging command.

| File | Bytes | Dimensions or format | Purpose |
| --- | ---: | --- | --- |
| `MOO_LUXE_SPEC.md` | 3,294 | MD | Supplied production note, untouched |
| `README.md` | 3,716 | MD | Short usage guide |
| `REPORT.md` | 11,533 | MD | Complete report and inventory |
| `avatars/avatar-a-spark-1024.png` | 512,923 | 1024 x 1024px | Hero fingertip crop social alternative export |
| `avatars/avatar-a-spark-180.png` | 20,833 | 180 x 180px | Hero fingertip crop social alternative export |
| `avatars/avatar-a-spark-400.png` | 89,881 | 400 x 400px | Hero fingertip crop social alternative export |
| `avatars/avatar-a-spark-48.png` | 2,145 | 48 x 48px | Hero fingertip crop social alternative export |
| `avatars/avatar-a-spark-512.png` | 141,953 | 512 x 512px | Hero fingertip crop social alternative export |
| `avatars/avatar-a-spark.svg` | 255,252 | 1024 x 1024 SVG | Hero fingertip crop social alternative source |
| `avatars/avatar-b-monogram-1024.png` | 39,079 | 1024 x 1024px | Recommended Geist AL social avatar export |
| `avatars/avatar-b-monogram-180.png` | 3,209 | 180 x 180px | Recommended Geist AL social avatar export |
| `avatars/avatar-b-monogram-400.png` | 9,679 | 400 x 400px | Recommended Geist AL social avatar export |
| `avatars/avatar-b-monogram-48.png` | 822 | 48 x 48px | Recommended Geist AL social avatar export |
| `avatars/avatar-b-monogram-512.png` | 13,503 | 512 x 512px | Recommended Geist AL social avatar export |
| `avatars/avatar-b-monogram.svg` | 729 | 1024 x 1024 SVG | Recommended Geist AL social avatar source |
| `business-cards-moo-luxe.pdf` | 120,279 | 2-page CMYK PDF | MOO Standard companion, front/back, writable reverse |
| `business-cards.pdf` | 430,074 | 2-page CMYK PDF | Generic printer, 3mm bleed and marks, front/back |
| `fonts/Archivo-googlefonts-latin.woff2` | 34,940 | WOFF2 | Real variable Archivo, Latin subset |
| `fonts/Geist-googlefonts-latin.woff2` | 29,288 | WOFF2 | Real variable Geist, Latin subset |
| `fonts/Geist-googlefonts.css` | 4,960 | CSS | Cached Google Fonts source CSS for both families |
| `fonts/OFL.txt` | 4,367 | TXT | Font redistribution license |
| `gbp-wordmark-1024.png` | 47,091 | 1024 x 1024px | GBP square image |
| `gbp-wordmark.svg` | 9,920 | 1024 x 1024 SVG | Outlined stacked GBP wordmark source |
| `proofs/avatar-a-spark-circle-180.png` | 14,490 | 180 x 180px | Circular-crop proof |
| `proofs/avatar-b-monogram-circle-180.png` | 3,374 | 180 x 180px | Circular-crop proof |
| `proofs/avatar-export-review.png` | 271,622 | 1200 x 1305px | Native-size export comparison |
| `proofs/business-card-back-300dpi.png` | 213,425 | 1200 x 750px | Final PDF side rendered at 300dpi |
| `proofs/business-card-front-300dpi.png` | 46,467 | 1200 x 750px | Final PDF side rendered at 300dpi |
| `proofs/existing-favicon-review.png` | 21,555 | 900 x 320px | Audit of four existing favicons |
| `proofs/existing-favicon-svg-192.png` | 3,996 | 192 x 192px | Rendered existing SVG favicon |
| `proofs/gbp-circle-1024.png` | 39,001 | 1024 x 1024px | Circular-crop proof |
| `proofs/moo-luxe-back-300dpi.png` | 18,782 | 1098 x 648px | Final PDF side rendered at 300dpi |
| `proofs/moo-luxe-front-300dpi.png` | 44,655 | 1098 x 648px | Final PDF side rendered at 300dpi |
| `source/README.md` | 2,118 | MD | Rebuild instructions |
| `source/archivo-400-outlines.json` | 44,676 | JSON | Archivo 400 glyph geometry |
| `source/archivo-600-outlines.json` | 44,764 | JSON | Archivo 600 glyph geometry |
| `source/build-moo.py` | 2,268 | PY | MOO companion builder |
| `source/build.py` | 10,890 | PY | Deterministic core asset builder |
| `source/font-outlines.c` | 1,743 | C | FreeType outline extraction source |
| `source/geist-700-outlines.json` | 35,853 | JSON | Geist 700 glyph geometry |
| `source/verification.json` | 690 | JSON | Measured contrast, CMYK, circle clearance and ICC hash |

All new textual sources were checked for the forbidden em dash and none were found. No address, invented claim, or invented business number was used.
