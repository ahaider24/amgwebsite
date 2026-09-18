# AmirGetsLeads assets

Use **direction B, the AL monogram**, for social profiles. It stays legible at 48px. Direction A preserves the original fingertip moment, but its engraving is faint at timeline size. Both are supplied for Amir to choose.

| Files | Use |
| --- | --- |
| `avatars/avatar-a-spark-{1024,512,400,180}.png` | Hero fingertip crop on warm paper, square social alternative. |
| `avatars/avatar-b-monogram-{1024,512,400,180}.png` | Recommended social avatar: paper A and orange italic L on ink. |
| `avatars/avatar-*-48.png` | Native timeline-size tests. |
| `avatars/avatar-a-spark.svg` | Self-contained SVG source with embedded original raster crop. |
| `avatars/avatar-b-monogram.svg` | Fully outlined, scalable Geist 700 source. |
| `gbp-wordmark-1024.png`, `gbp-wordmark.svg` | Google Business Profile: stacked AmirGets / orange italic Leads on paper; circle-safe. SVG lettering is outlined. |
| `business-cards.pdf` | Two pages, front then back. US 3.5 x 2 inch trim, 3mm bleed, outside crop marks, CMYK, vector lettering, 300dpi art. |
| `business-cards-moo-luxe.pdf`, `business-cards-moo-luxe-ink.pdf` | Recommended ink landscape front and portrait spark back, both in the MOO landscape bleed box; unprinted note band. |
| `business-cards-moo-luxe-paper.pdf` | Same layout with a paper front and identical portrait spark back. |
| `proofs/moo-luxe-directions-side-by-side-300dpi.png` | Compare both complete directions in one image, backs shown upright. |
| `proofs/business-card-*-300dpi.png` | Both PDF pages rendered at 300dpi, with bleed and crop marks visible. |
| `proofs/moo-luxe-*-300dpi.png` | Both MOO pages at 300dpi, full bleed size of 1098 x 648px. |
| `proofs/avatar-export-review.png` | Both directions at native export sizes, including 48px. |
| `proofs/avatar-*-circle-180.png`, `proofs/gbp-circle-1024.png` | Circle-mask proofs on paper-3. |
| `proofs/existing-favicon*.png` | Visual audit of existing site icons. They use an orange serif A on ink, with no old name, and remain unchanged. |
| `fonts/` | Real cached Google Fonts Geist and Archivo files, source CSS, SIL OFL license. |
| `source/` | Deterministic builder, outline extraction source, font outline data, and measured verification results. |
| `REPORT.md` | Current second-pass card report, colour caveats and verification. Earlier work is documented in `REPORT-first-pass.md`. |

The wordmark uses Geist 700, -0.02em tracking. The site's Google Fonts request loads upright Geist only, so the orange payoff uses a deterministic 14-degree synthetic italic, matching that relationship. Archivo 400/600 is used for card contact information. The back repeats the approved positioning in Geist 700 as a compact brand statement.

`#FF4D1C` is a bright RGB orange and **will shift in CMYK**. The PDF converts it with the embedded Generic CMYK profile to approximately C0 M73.33 Y85.49 K0. Dark contact text on the paper front is single K for clean registration; the ink front uses paper lettering. Obtain a printer proof for the actual stock and press profile; the PDF is not certified PDF/X.

For MOO Luxe, choose the paper or ink PDF and Standard size. Both contain a landscape front and a portrait back rotated inside the landscape upload artboard. The reverse uses the supplied composited spark, exact positioning and a 2.0 x 0.719 inch unprinted note band. Tiger Orange is the confirmed seam choice in the supplied direction note. Orange Leads and the spark are still printed orange, subject to CMYK shift. The original 3mm PDF remains the generic printer edition.

Orange on paper is **3.13:1**, failing WCAG AA for normal text but passing its 3:1 large-text threshold. Orange on ink is **5.68:1**, passing normal-text AA. Small orange body text on paper should instead use accent-deep, which measures **4.92:1**. Logos themselves are exempt from the text contrast requirement.

No HTML, site configuration, deployment, or existing site icon was changed. Existing photographs in this directory are unrelated and untouched.
