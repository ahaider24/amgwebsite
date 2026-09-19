# Avatar typesetting / Astra

Ship **B, Measured step**. The larger italic has enough presence to answer the upright line, while its deliberately shorter width makes a coherent two-line silhouette inside the circle. It reads as a compact wordmark rather than two independently centred words.

No `-o` destination was supplied in the request. The report destination is `brand/proofs/avatar-typesetting-report.md`; the builder accepts another destination through `-o`.

## Four distinct decisions

All measurements below use a 1024-unit circle. The comparison contains every option at native 400, 180, 48 and 32px, circular on white. The 400 and 180px rows use display cuts. The 48 and 32px rows use separate small cuts with output-specific baseline fitting.

| Option | Typographic decision | Assessment |
| --- | --- | --- |
| A / Equal optical widths | Both lines occupy about 804 units. Leads is 1.56 times the upper type size. The italic is moved right after ink-centre alignment, rather than forcing identical box edges. | A strong, near-rectangular block. The larger orange line dominates, and the lower corners approach the circle more closely. |
| B / Measured step | Upper width 832 units. Leads width 699 units, 84% of the upper line, at 1.31 times its type size. Each line has an independently reviewed optical axis. | Selected. The step is explicit, the top line remains large, and the lower line has both emphasis and breathing room. |
| C / Shared type size | Both words use the same 192-unit em in the display cut. Leads naturally occupies about 64% of the upper width. | The quietest hierarchy, but the shorter orange word loses too much presence at 32px. |
| D / Shared left edge | Align the italic L at half x-height with the upright A's visible left edge. Leads occupies 83% of the upper width. | Deliberately editorial. The left alignment works as a lockup, but the empty lower-right quadrant pulls it away from the circle's axis. |

Comparison: [avatar-typesetting-comparison.png](avatar-typesetting-comparison.png)

Small-size audit: [avatar-typesetting-small-audit.png](avatar-typesetting-small-audit.png)

Optical-axis study: [avatar-axis-study.png](avatar-axis-study.png). The middle treatment was selected. Its labels record the rightward correction after ink-centre alignment, in 1024-unit coordinates.

## What changed in the chosen setting

The supplied `brand/source/geist-700-outlines.json` was read successfully. All lettering, including proof labels, is made from its actual glyph paths. No system face, font lookup, or fallback was used. Source SHA-256: `eab57193376ad8273ef7121e260bf74123a9dbdc8b06cde181e745422288d687`.

The source contains upright Geist 700. Its documented italic treatment is a 14-degree shear, consistent with the site's upright-only Geist loading and italic CSS. This build uses that real outline source with the same shear for display. It does not claim to contain a separately drawn Geist Italic font. The small cut reduces the shear to 12 degrees.

Display tracking is -0.034em on AmirGets and -0.036em on Leads, with additional pair adjustments. The rG transition, Ge, ts and Le receive particular attention. The supplied outline data has advances but no kerning table, so these are explicit wordmark adjustments, not a claim to recover the font's kerning. Exact values are in the builder.

The type measures 710 units in cap height and 536 in x-height. B's visible interline gap is 1.28 times that difference at the upper line's size: 42.77 units. This is about 0.314 of its cap height. It keeps a visible band of blue between the words without disconnecting them. The overall vertical position blends the silhouette and ink centres, then raises the lockup slightly within the circle.

Horizontal placement begins with the signed ink-area centroid, including counters. That is a starting point, not the final optical decision. I reviewed +6, +16 and +26 units of additional rightward correction on Leads and selected +16. Its visible box consequently sits about 5.2 units right of the circle's axis. The upright's visible box sits about 8.1 units left of the axis. Those unequal box positions produce the better visual relationship. The small cut uses a reduced +10-unit correction.

The upper line occupies 81.25% of the circle diameter. The closest display outline control point remains about 83 units inside the circle, a conservative radial clearance of about 8% of the diameter. This checks the curve around the actual outlines, not merely the square's edges. The broad upper line and inset lower line leave the rounded sides room to work.

The background uses the site's CTA stops exactly: #3CB8DE at 0%, #2596BE at 46%, #1A5E92 at 100%, along its 135-degree direction. Paper is #FBF8F2 and the italic is #FF4D1C. The avatar is a static, full-field rendering of that gradient.

## Small cut and the 32px limit

A separate small cut is included. Tracking opens to -0.004em and -0.008em, pair corrections are reduced to 35% of the display corrections, and the upper width grows to 842 units. The italic lean reduces to 12 degrees. The original 700 weight is retained to protect the already small counters.

Opening tracking alone was insufficient. A baseline-phase comparison exposed the softer top line, so each line's baseline is fitted to the target output grid. At 32px the baselines are 14px and 21px; at 48px they are 21px and 31px. This creates about 1.60px clear interline space at 32px. The small SVG masters for 32 and 48 therefore differ in baseline placement, as well as differing from the display cut in fit and slant.

Every PNG is rasterized from vector outlines at four times its own target dimensions and filtered once. The 32px PNG is not a reduction of the 1024px PNG. I inspected the complete comparison and the native-size plus enlarged pixel audit. The small cut improves separation and the upper line's pixel pattern, particularly at 48px.

At 32 actual pixels, AmirGets has approximately 4.1px cap height and 3.1px x-height. The wordmark is recognizable, but effortless reading of the entire name is not a defensible promise at that resolution. This is the remaining limit of the settled eight-letter top line, not a reason to return to the rejected monogram.

## Delivered files

Chosen circular PNGs, transparent outside the circle:

`brand/avatars/astra-avatar-{size}.png`

Sizes: **1024, 800, 512, 400, 360, 320, 180, 48, 32**. The first seven use the display cut; 48 and 32 use their respective small cuts. The comparison presents them on white.

Vector masters:

- `brand/avatars/astra-avatar-display.svg`
- `brand/avatars/astra-avatar-small.svg`, fitted for 32px
- `brand/avatars/astra-avatar-small48.svg`, fitted for 48px

For a profile platform that accepts one square upload and generates every thumbnail, use **`brand/avatars/astra-avatar-upload-small-1024.png`**. It contains the small-cut geometry at upload resolution with the gradient extending into the square's corners, ready for the platform's circular mask. This preserves the small-cut fit when the service generates thumbnails; its resizing filter can still alter the pixel result.

`brand/avatars/astra-avatar-upload-display-1024.png` is the corresponding display-cut upload for contexts where the avatar stays large. Each option's individual proof PNGs and vector cuts are in `brand/avatars/astra-options/`.

Metrics: [avatar-typesetting-metrics.json](avatar-typesetting-metrics.json). Export checks: [avatar-typesetting-verification.json](avatar-typesetting-verification.json).

Independent rebuild:

```sh
/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 brand/avatars/typeset-avatar.py -o brand/proofs/avatar-typesetting-report.md
```

This pipeline reads the supplied outlines directly and does not import or patch the previous builder. All new files are confined to `brand/avatars/` and `brand/proofs/`. Existing attempts are preserved. Nothing was pushed or deployed; no HTML or deployment configuration was created or changed.

## What the proof cannot settle

An on-platform test must settle the service's resampling, compression, crop scaling, and whether it serves enough physical pixels for high-density displays. Test the small-cut upload at 32 and 48 CSS pixels on both a standard-density screen and a phone, at normal viewing distance. Native 32px artwork and a 32 CSS-pixel avatar backed by 64 or 96 physical pixels are different conditions.

A real-device viewing test should also settle unfamiliar readers' recognition of AmirGets and the orange word's visibility at ordinary screen brightness. The supplied native-pixel proof makes the constraints visible, but it does not replace those tests. No account upload was performed.
