# Found, chosen, booked.

Research and proposed hero typography, 19 September 2026.

**Status: incomplete.** Research and six specifications are supplied below. No PNG renders were produced. The session sandbox prevents both installed Chrome renderers from starting, and the local runtime cannot download Google Fonts. Consequently, typography, wrapping, font payloads and dark appearance have not been visually verified. No site file was modified. This report uses `brand/hero-type/REPORT.md` because the request did not include an actual `-o` filename.

## Research, before design

The most relevant three-beat hospitality reference is Soho House's invitation to “eat, drink, and connect”: ordinary verbs, commas that preserve conversation, and an invitation to participate. Aman similarly describes “privacy, peace and local immersion”; Auberge du Soleil places two short, punctuated thoughts together, while deVOL leads with “Simple Furniture, Beautifully Made.” These are useful verbal references for an agency serving expensive, considered purchases: the promise sounds settled and human, with no need for an exclamation mark or urgency. They support keeping both commas and the final period in Amir's line, preserving sentence case, and giving each complete word room to register. These observations come from the brands' published content, not from a measured browser audit of their type. Sources: [Soho House](https://qr.sohohouse.com/food-and-drink), [Aman Tokyo](https://www.aman.com/hotels/aman-tokyo), [Auberge du Soleil](https://auberge.com/auberge-du-soleil/), [deVOL](https://www.devolkitchens.co.uk/).

On the typographic side, Pentagram's Marina Bay Sands case study describes a distinctive serif family extending architectural letterforms into the wider identity; QUO's Steigenberger case study describes a serif balancing contemporary elegance with continuity. The transferable lesson is character with a reason, rather than an interchangeable luxury font. My design interpretation is to put contrast inside the letterforms and between a small, readable descriptor and a much larger statement: moderate weights, nearly natural tracking, and generous separation between the two roles. I could not inspect these live sites' computed weights, tracking or descriptor-to-heading ratios, and will not invent those measurements. Optical size is independently supported by the type designers: Undercase explains that Fraunces opens spacing, increases x-height and reduces contrast at small optical sizes, while Production Type describes Newsreader's screen-reading origins and expressive display cuts. Those findings justify explicit small-text and display settings below, but not claims that the reference brands use an optical-size axis. Sources: [Pentagram, Marina Bay Sands](https://www.pentagram.com/work/marina-bay-sands), [QUO, Steigenberger](https://www.quo-global.com/our-work/steigenberger/), [Undercase, Fraunces](https://fraunces.undercase.xyz/), [Production Type, Newsreader](https://productiontype.com/font/newsreader).

## Shared composition and exact content

Every specification is a proposal awaiting Chrome proofing. Sizes below are CSS pixels at a device scale factor of 1, for 1440px and 390px viewport widths respectively. Optical-size values are explicit axis coordinates, not a claim that the browser will infer the same setting from the CSS pixel size.

- Eyebrow text: `AmirGetsLeads · Marketing & AI agency · Fresno & Los Angeles`
- Heading text: `Found, chosen, booked.`
- Preserve all punctuation in real text, including the middle dots. Never generate punctuation only with CSS.
- Do not treat the plain-text agency name within the descriptor as a redesigned wordmark. The existing navigation wordmark remains untouched.
- Proposed proof canvases: desktop 1440 × 440px; mobile 390 × 520px. Only descriptor, slogan, background and grain appear. Contact-sheet labels sit outside the individual proofs.
- Desktop content width: 1280px with 80px side margins. Mobile content width: 342px with 24px side margins. Center the overall type group vertically in its proof canvas.
- Desktop eyebrow: one line. Mobile eyebrow: three centered lines, `AmirGetsLeads ·` / `Marketing & AI agency ·` / `Fresno & Los Angeles`. The wildcard aligns these left. Keep each phrase intact; allow natural wrapping under text zoom.
- All headings use normal case, kerning enabled, normal ligatures, no synthetic bold or italic, no strokes, no shadows and no type gradients. Set `font-synthesis: none`.
- Fraunces optical sizing is explicit: `font-optical-sizing: none` plus `font-variation-settings: "opsz" <value>`. The proposed custom-axis positions are SOFT 0 and WONK 1 throughout. These are the intended default positions, with no custom-axis animation or axis-range request. The current Google Fonts URL requests only ital, opsz and wght; it cannot be assumed to deliver adjustable SOFT and WONK axes. Inspect the actual downloaded font before implementation.
- Fraunces fallback: `"Fraunces", Georgia, "Times New Roman", serif`. Archivo fallback: `"Archivo", Arial, sans-serif`. Newsreader fallback: `"Newsreader", "Fraunces", Georgia, serif`.
- Use `font-display: swap`. An existing stylesheet declaration does not mean a font binary is already downloaded or cached. Regular and italic generally require separate font resources.

## The actual background and themes

The repo has a paper token of `#FBF8F2`, but its hero uses a more specific layered background. Preserve the existing hero recipe exactly for light proofs:

```css
background:
  radial-gradient(122% 78% at 50% 2%, #ffffff 0%, rgba(255,255,255,0) 56%),
  linear-gradient(180deg, #FCFAF4 0%, #F7F1E7 82%, #F1EBDF 100%);
```

Those colours are existing site background values, not proposed additions. Preserve `.hero-grain` from `index.html`: 140 × 140 SVG tile, fractal noise frequency 0.9, two octaves, stitchTiles stitch, opacity .045, multiply blend. Also preserve the existing body overlay: 150 × 150 SVG tile, frequency .85, three octaves, opacity .04, multiply blend. Do not add artificial wear to the glyphs themselves.

The current repo explicitly pauses dark mode with `(prefers-color-scheme: dark) and (max-width:1px)` and sets `color-scheme:light`. The requested dark proofs would therefore be proposed theme behaviour, not screenshots of current production behaviour. For those proofs use approved ink `#14110A` as the ground, approved paper `#FBF8F2` as the foreground, unchanged sky blue `#2596BE`, and the same grain geometry with screen blending. Retain the same typography in both themes; no opacity reduction on small text. This deliberately avoids introducing the site's dormant brown dark palette into a new proposal.

Sky blue belongs on the large statement in directions 2 and 6. The small descriptor stays ink in light mode and paper in dark mode. Its legibility must not depend on the blue passing small-text contrast requirements.

## 1. The house signature

**Argument and audience:** A medium-weight Fraunces statement makes the rounded serifs and irregular rhythm feel like lettering on a well-made hotel folio. It suits an owner-led service business that wants warmth and visible craft without losing authority.

| Element | Exact desktop setting | Exact mobile setting |
| --- | --- | --- |
| Eyebrow | Archivo, normal, 500; opsz not applicable; 14px; tracking .005em; line-height 1.5 | Archivo, normal, 500; opsz not applicable; 13px; tracking 0; line-height 1.55 |
| Slogan | Fraunces, normal, 520; opsz 96; SOFT 0; WONK 1; 104px; tracking -.035em; line-height 1.06 | Fraunces, normal, 520; opsz 48; SOFT 0; WONK 1; 64px; tracking -.025em; line-height 1.04 |
| Gap after eyebrow | 32px | 24px |
| Alignment and line structure | Centered; one line | Centered; `Found,` / `chosen,` / `booked.` |
| Colour | All type ink | All type ink |

**Cost:** No new family or style beyond the current font declarations. Fraunces regular may still be a cold-cache download; its actual payload was not measurable here. The main aesthetic risk is that weight 520 plus WONK reads friendly or nostalgic rather than reserved. Georgia preserves a warm serif voice on failure, but loses the distinctive outlines and variable weight; its width and the default fallback weight need browser testing. Keep the three mobile words on explicit lines with punctuation attached, rather than shrinking to force one line.

## 2. The concierge

**Argument and audience:** Archivo quietly answers who and where, while a lighter Fraunces statement delivers the promise and an italic blue final word gives the line a hospitable cadence. This is the best proposed balance for a contractor on a phone and a premium professional-services buyer opening the same page.

| Element | Exact desktop setting | Exact mobile setting |
| --- | --- | --- |
| Eyebrow | Archivo, normal, 500; opsz not applicable; 14px; tracking .005em; line-height 1.5 | Archivo, normal, 500; opsz not applicable; 13px; tracking 0; line-height 1.55 |
| Found, chosen, | Fraunces, normal, 430; opsz 96; SOFT 0; WONK 1; 100px; tracking -.03em; line-height 1.08 | Fraunces, normal, 430; opsz 40; SOFT 0; WONK 1; 46px; tracking -.025em; line-height 1.1 |
| booked. | Fraunces, true italic, 430; opsz 96; SOFT 0; WONK 1; 100px; tracking -.03em; line-height 1.08 | Fraunces, true italic, 430; opsz 40; SOFT 0; WONK 1; 46px; tracking -.025em; line-height 1.1 |
| Gap after eyebrow | 30px | 24px |
| Alignment and line structure | Centered; one line | Centered; `Found, chosen,` / `booked.` |
| Colour | Descriptor and first two words ink; entire `booked.` sky blue | Same |

**Cost:** No new family declaration. Both regular and italic Fraunces resources can be needed on first visit, so moving an italic above the fold can advance a download even though the site already declares it. The main rendering risk is the width of the first mobile line and the italic's right overhang; keep 24px side padding and check actual glyph bounds. If Fraunces fails, Georgia regular and true italic retain the two voices and the blue final beat, but the first line may need to wrap naturally. Do not clip it or impose `white-space:nowrap` on the whole heading. The period stays blue with its word, not a separate oversized decorative dot.

## 3. Three measured beats

**Argument and audience:** Three equal typographic units make the commas into pauses and the period into a quiet finish, with spacing doing the work that advertising often gives to boldness. It suits buyers who appreciate a process they can understand immediately, including trades clients scanning between jobs.

| Element | Exact desktop setting | Exact mobile setting |
| --- | --- | --- |
| Eyebrow | Archivo, normal, 500; opsz not applicable; 14px; tracking 0; line-height 1.5 | Archivo, normal, 500; opsz not applicable; 13px; tracking 0; line-height 1.55 |
| Each beat | Fraunces, normal, 460; opsz 72; SOFT 0; WONK 1; 86px; tracking -.02em; line-height 1.1 | Fraunces, normal, 460; opsz 48; SOFT 0; WONK 1; 60px; tracking -.02em; line-height 1.1 |
| Gap after eyebrow | 34px | 24px |
| Beat spacing | Flex row; 48px gap between complete word-and-punctuation spans | Flex column; 8px gap between complete spans |
| Alignment | Centered row | Centered column |
| Colour | All type ink | All type ink |

**Cost:** No additional family or style; regular Fraunces only for the heading. This treatment costs vertical space on mobile, and the 48px desktop gap must be tested for whether it feels like conversation or three navigation items. Keep actual inter-word spaces in the heading text for accessibility and copying, even when flex layout controls the visible gaps. Georgia retains the sequence on failure, though its punctuation has a different rhythm. Do not reduce, raise, detach or recolour the commas: the grid must not replace the sentence with three labels.

## 4. One family, two distances

**Argument and audience:** Fraunces at text optical size supplies a sturdy, intimate descriptor, while its display setting and a gradual increase in weight make the three-word promise feel composed within one coherent voice. It suits a consultancy seeking a more literary, quietly institutional identity without bringing in another family.

| Element | Exact desktop setting | Exact mobile setting |
| --- | --- | --- |
| Eyebrow | Fraunces, normal, 600; opsz 14; SOFT 0; WONK 1; 15px; tracking .005em; line-height 1.5 | Fraunces, normal, 600; opsz 13; SOFT 0; WONK 1; 14px; tracking 0; line-height 1.55 |
| Found, | Fraunces, normal, 360; opsz 120; SOFT 0; WONK 1; 100px; tracking -.025em; line-height 1.08 | Fraunces, normal, 360; opsz 40; SOFT 0; WONK 1; 60px; tracking -.02em; line-height 1.08 |
| chosen, | Same, weight 460 | Same, weight 460 |
| booked. | Same, weight 580 | Same, weight 580 |
| Gap after eyebrow | 34px | 26px |
| Alignment and line structure | Centered; one line; standard word spaces | Centered; `Found,` / `chosen,` / `booked.` |
| Colour | All type ink | All type ink |

**Cost:** One existing variable family and one regular style can serve all the roles. Optical-size contrast is the essential mechanism, so a static fallback loses more of this argument than it does in directions 1 or 2. Georgia can map the intended progression to only its available normal and bold faces; the subtle middle step may disappear. Watch the 360-weight display strokes in dark mode and the small serif descriptor on a real phone. The text setting is deliberately heavier and one pixel larger than the sans-serif descriptors. This is not a request for a thin luxury eyebrow.

## 5. The editorial reservation

**Argument and audience:** Newsreader offers an open, less eccentric serif voice with a display cut, making the slogan feel like a considered line from a respected publication. It is for finance, advisory and other clients who want warmth but may find Fraunces too expressive.

| Element | Exact desktop setting | Exact mobile setting |
| --- | --- | --- |
| Eyebrow | Archivo, normal, 500; opsz not applicable; 14px; tracking .005em; line-height 1.5 | Archivo, normal, 500; opsz not applicable; 13px; tracking 0; line-height 1.55 |
| Slogan | Newsreader, normal, 450; opsz 72; 108px; tracking -.025em; line-height 1.06 | Newsreader, normal, 450; opsz 36; 48px; tracking -.015em; line-height 1.12 |
| Gap after eyebrow | 32px | 24px |
| Alignment and line structure | Centered; one line | Centered; `Found, chosen,` / `booked.` |
| Colour | All type ink | All type ink |

**Cost and justification:** This is the only new-family proposal. It is on [Google Fonts](https://fonts.google.com/specimen/Newsreader), and its [official source repository](https://github.com/productiontype/Newsreader) documents a variable font and an open licence. Its reason to exist here is narrower than “another nice serif”: compared with Geist and Bricolage it adds genuine serif contrast; compared with Fraunces it offers a more restrained editorial personality rooted in screen reading. Fraunces remains the better choice if performance and family economy take priority.

Request only upright weight 450, retaining the 36 to 72 optical-size range, with `display=swap`; no italics and no unused weight range. For this fixed three-word use, a Google Fonts `text=Found%2C%20chosen%2C%20booked.` subset is a defensible payload reduction. That would introduce a dedicated stylesheet request and normally one subset font resource; exact response count, bytes and timing remain unmeasured. A text subset is unsuitable for arbitrary future headlines unless the request is updated. Fail first to existing Fraunces, then Georgia, so failure retains a serif statement. A slow connection still incurs the additional request and possible layout shift; I cannot certify “loads fast” without measuring it.

## 6. A note from the house

**Argument and audience:** A wholly italic, sky-blue Fraunces statement, aligned left, gives the promise the character of a personal note from a confident host. This is the wildcard for Amir as a visible founder: distinctly warm, memorable and less institutional than the other five.

| Element | Exact desktop setting | Exact mobile setting |
| --- | --- | --- |
| Eyebrow | Archivo, normal, 500; opsz not applicable; 14px; tracking 0; line-height 1.5 | Archivo, normal, 500; opsz not applicable; 13px; tracking 0; line-height 1.55 |
| Slogan | Fraunces, true italic, 440; opsz 96; SOFT 0; WONK 1; 102px; tracking -.02em; line-height 1.1 | Fraunces, true italic, 440; opsz 48; SOFT 0; WONK 1; 62px; tracking -.015em; line-height 1.06 |
| Gap after eyebrow | 32px | 24px |
| Alignment and line structure | Left; one line; centered 1120px type container | Left; `Found,` / `chosen,` / `booked.`; 342px type container |
| Colour | Eyebrow ink; entire slogan sky blue | Same |

**Cost:** No new family declaration, but the existing italic Fraunces resource must be loaded above the fold. The full line of italic may look more like a boutique creative practice than a hedge-fund-facing service firm; that is the real positioning cost. Check overhangs on the initial F and terminal period and avoid clipping the heading container. Georgia italic retains the personal-note idea on failure, with less characteristic detail. Keeping the entire slogan at large-text size makes blue a plausible functional choice, but the real paper gradient and rasterised strokes still require contrast and visual checks. Do not use reduced opacity to soften the blue.

## Recommendation

**My intended ship choice is direction 2, The concierge, subject to actual browser proofing.** The descriptor stays immediately readable; the regular and italic serif voices give the headline deliberate craft; sky blue becomes part of the promise. Its mobile target uses two lines instead of three, reserving more of the phone's first screen for the hero image and eventual action. The weight is substantial enough to avoid preciousness while leaving room for Fraunces' natural contrast. Of the proposed treatments, it best balances hospitality, character, mobile economy and a premium services audience.

**The safe second choice is direction 1, The house signature.** One upright serif heading, an all-ink treatment and three explicit mobile lines reduce dependence on italic fit and blue contrast. It trades extra vertical space and a friendlier personality for simpler behaviour.

I would not ship either specification without its 390px proof. The recommendations above are design judgments, not conclusions from nonexistent renders.

## Deliverables and missing renders

Produced:

- `REPORT.md`, this research and specification report.

Not produced:

- `hero-type-1-desktop.png` and `hero-type-1-mobile.png`
- `hero-type-2-desktop.png` and `hero-type-2-mobile.png`
- `hero-type-3-desktop.png` and `hero-type-3-mobile.png`
- `hero-type-4-desktop.png` and `hero-type-4-mobile.png`
- `hero-type-5-desktop.png` and `hero-type-5-mobile.png`
- `hero-type-6-desktop.png` and `hero-type-6-mobile.png`
- `hero-type-contact-sheet.png`, intended as six labelled desktop proofs stacked at equal scale.

Also pending are the twelve supplementary dark proofs, using the pattern `hero-type-<n>-<desktop|mobile>-dark.png`.

## Verification and blocker

Read `index.html` without altering it. Confirmed the existing font request, hero background, both grain layers, current eyebrow mobile treatment and paused dark-mode media query. Repository status was clean before this task.

Attempted the installed Google Chrome application through Playwright; it exited before creating a page. Attempted the installed Chrome headless shell; it failed with `bootstrap_check_in ... Permission denied (1100)` in the OS Mach-port setup. The local Google Fonts request failed DNS resolution. The available computer-use connector reported that no browser was available. This session does not permit approval escalation. No security controls were changed or bypassed.

The missing capability is a permitted headless Chrome session with access to Google Fonts, or an equivalent approved renderer with the exact font resources already available. Once available, the remaining work is to inspect the reference sites visually, render all six treatments, adjust actual glyph fit, verify loaded font faces and non-overflow at 390px, inspect light and dark proofs, and build the labelled contact sheet from the final desktop PNGs. None of those checks is marked complete here.

No commit, push or deployment was performed. No site source, asset, dependency or configuration file was changed. Only this report was added under the requested output directory.
