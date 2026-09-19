# Axiom chat card: interface studies

Ship **02 / Chat app**, subject to Axiom confirming the print setup and approving a physical proof. It reads as an AI chat before the words resolve: a compact app bar, a right-aligned rounded prompt, an unboxed assistant reply and an anchored message composer with a send button. The UI uses Geist at interface sizes, warm dark outlines and open paper. The information face remains unchanged.

The response is authored card copy, not a captured answer or an endorsement by a named assistant. No company-specific assistant name, logo or near-copy is used. The generic label is `AI chat`. No QR and no street address.

## Three takes

| Take | Construction and judgment | Upright linen proof, 300 DPI | Two-face assets |
| --- | --- | --- | --- |
| 01 / Minimal frame | A small title, right-aligned prompt bubble, flowing reply and bottom composer. Immediately more chat-like than the previous typography studies. Quietest, but without an app bar the composition still has some advertising-layout ambiguity. | [01 proof](proofs/01-minimal-linen-HOLD-vertical-upright-300dpi.png) | [Artwork](01-minimal-artwork-HOLD.pdf), [linen simulation](01-minimal-linen-HOLD.pdf) |
| 02 / Chat app | Menu, generic title and new-chat affordance establish an app bar. A speaker label makes the unboxed reply explicit. The composer has comfortable inset text and a circular upward send affordance. Best balance of recognition and restraint. **Ship this design.** | [02 proof](proofs/02-app-linen-HOLD-vertical-upright-300dpi.png) | [Artwork](02-app-artwork-HOLD.pdf), [linen simulation](02-app-linen-HOLD.pdf) |
| 03 / Full interface | An enclosing rounded viewport, header divider, neutral square avatar, copy/retry toolbar and a multiline composer with add and send controls. Most literal app rendering. Its extra chrome competes with the business identity at card scale. | [03 proof](proofs/03-full-interface-linen-HOLD-vertical-upright-300dpi.png) | [Artwork](03-full-interface-artwork-HOLD.pdf), [linen simulation](03-full-interface-linen-HOLD.pdf) |

[Actual-size comparison](comparison-HOLD.pdf) places all three portrait faces and the shared information face at 100% trim size. [Comparison PNG](proofs/comparison-HOLD-300dpi.png). Print the PDF at actual size with scaling disabled. A screen zoom cannot establish arm's-length physical legibility.

My conservative-room read: 02 looks intentional as a marketing and AI agency's card. Familiar controls make the premise readable without a logo, and the restrained ink on open linen keeps it from looking like a miniature screenshot. The prompt and self-answer remain a sales device. Some recipients will still call that gimmicky, and the stock does not remove that risk. I would hand it over with the information face up. 01 is quieter but less convincing as an app; 03 reads most instantly as software but feels more like a novelty card. I would not ship 03 into that room.

## Copy and unchanged information face

Prompt: `I need marketing but I don't know who to pick.`

Reply: `AmirGetsLeads.` followed by `Turn the card over.`

The shared horizontal face retains exactly:

- AmirGetsLeads
- Marketing and AI agency
- Amir Haider
- 559-550-5474
- amir@amirgetsleads.com
- amirgetsleads.com

[Shared information-face linen proof](proofs/02-app-linen-HOLD-horizontal-landscape-300dpi.png). It is page 2 of every two-face PDF. No claims, performance figures or named-assistant recommendations have been added.

## Print decisions

- Stock specified by the brief: Axiom Natural White linen, 100#, uncoated. The digital texture is illustrative, not a measured simulation of this stock or ink transfer.
- Palette: paper `#FBF8F2`, ink `#14110A`, ink-soft `#574F40`, accent `#FF4D1C`. The artwork PDFs contain no printed paper tint and no simulated texture. Those appear only in the linen review PDFs and proofs.
- All intentional UI borders and rules are at least 0.8pt. Send-arrow strokes are 1.2pt. The thin procedural texture lines represent the paper in review files only; they are absent from print artwork. No large dark panel fills.
- Orange is confined to the send arrow. No text uses orange. Labels and placeholders use ink-soft; message and response copy use ink.
- Main UI type: prompt 9.5pt in 01 and 02, 9pt in 03, at 13pt line spacing. Response brand 11.5pt in 01 and 02, 10.8pt in 03. Turn instruction 9pt. Supporting speaker labels are 7.5pt. The narrower full interface pays for its extra controls with smaller type.
- Trim 3.5 x 2 in, or 252 x 144pt. Portrait reading orientation is 2 x 3.5 in. Bleed and safety are each assumed at 0.125 in, pending Axiom confirmation.
- Every card PDF uses two landscape pages, MediaBox and BleedBox `[0, 0, 270, 162]`, TrimBox `[9, 9, 261, 153]`, zero page rotation. Portrait art is rotated inside page 1. Confirm duplex orientation with Axiom using a physical dummy.
- Full-bleed renders are 1125 x 675 pixels at 300 DPI, or 675 x 1125 upright. The trim itself is 1050 x 600 pixels. The comparison places the cards at actual trim size.
- Vector card text uses the existing Geist outlines. DeviceRGB review assets, no approved press profile or PDF/X claim. `HOLD` means print setup remains unresolved. Send bare artwork only after Axiom specifies its colour workflow; never print the simulated linen background.

## Verification and practical limits

The builder checks every text placement against the assumed safe area, all card page boxes, absence of page rotation and link annotations, vector-only card artwork, minimum artwork rule weight, identical information-face pixels across takes, source hashes and absence of the forbidden punctuation. Results are in [verification.json](verification.json).

Visual review covers each latest 300 DPI upright linen proof, the information face and the actual-size comparison. All three show separate user and assistant turns, an unmistakable composer and a readable send affordance. No clipping or overlap is visible. The 7.5pt speaker label and small toolbar controls in 03 remain the weakest elements on textured stock. Digital review cannot certify viewing distance, ink gain, line dropout or the feel of linen. A physical proof is still necessary.

Confirm with Axiom: trim/bleed/safe-area template, exact Natural White 100# stock, duplex orientation, minimum positive type and rule sizes on the actual process, small-text black and colour conversion/output profile. Approve the physical proof before ordering. No brand-findability or QR gate is carried over from the superseded report.

## Rebuild and scope

The earlier `understated`, `exchange` and `dialogue` files are superseded historical studies. This report and `verification.json` cover only the three new interface takes and the updated comparison.

No explicit report filename was supplied, so the build uses `-o brand/axiom/chat/report.md`:

```sh
/Users/amir/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 brand/axiom/chat/build.py -o brand/axiom/chat/report.md
```

All deliverables stay inside `brand/axiom/chat`. Assets only. No push, deployment, site edits or print order.
