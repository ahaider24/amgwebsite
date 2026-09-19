# Social avatar, ready to upload

The filename says where it goes. Upload as is.

## What shipped

The **stacked wordmark** on the site's own CTA gradient: `AmirGets` in paper
above `Leads` in orange italic, over `#3CB8DE` to `#2596BE` to `#1A5E92`. Real
Geist 700 with the italic second word, which is the same relationship the site's
logo uses.

Stacking is the mechanism that makes a wordmark work as an avatar. Two lines
roughly double the height available per character versus one long line, which is
why the old amirgetsjobs avatar survived at small size. At 48px nobody reads the
letters anyway; they recognise the shape and the colour split, and the stack
keeps both.

| File | Where it goes |
|---|---|
| `x-twitter-400.png` | X |
| `linkedin-400.png` | LinkedIn personal and company |
| `instagram-320.png` | Instagram |
| `facebook-360.png` | Facebook page |
| `slack-512.png` | Slack workspace |
| `youtube-800.png` | YouTube channel |
| `master-1024.png` | source for anything else |

For Google Business Profile use `../gbp-wordmark-1024.png`. GBP displays larger
and on warm paper rather than blue, and it was verified under a circular mask
with nothing cut.

## Typesetting

Set by Astra, 2026-09-18, after Amir called my first attempt short of best work.
He was right: I had centred two bounding boxes with a chosen gap, which is
arithmetic rather than typesetting. Four decisions were wrong and are fixed:

- Centring an italic by its bounding box leaves it optically left, because the
  box is skewed. `Leads` now sits on a shared optical axis.
- No tracking was applied. The site sets its logo at -.02em and Geist wants
  tightening at display size.
- The vertical gap was a number I picked rather than derived from cap height.
- The size relationship between an eight character word and a five character one
  was undecided rather than designed.

Shipped option B, a measured step: `Leads` at 84 percent of the upper line's
width, optically shifted right, with deliberate clearance inside the circle.
Three alternates were rendered and are in `../proofs/avatar-typesetting-comparison.png`:
equal optical widths, one shared type size, and a shared left reading edge.

**Separate display and small cuts.** A mark drawn at 1024 and downsampled is not
the same as one drawn for 32px, where counters fill and the italic lean muddies.
The 48 and 32 exports come from their own cut, not from the display master.

## Rejected, and why it is worth knowing

An AL monogram was built first and rejected. Amir: "AL is not gonna stick." He is
right that two generic letters say nothing, and the wordmark carries the actual
name. The monogram survives 32px slightly better, which was the argument for it,
but legibility of individual letters is not what recognition depends on at that
size.

An earlier set shipped on ink, white and orange. That was an error: blue is a
core brand colour appearing across 28 files sitewide, not just the CTA button.
See the memory note reference-amg-brand-palette.
