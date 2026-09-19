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

## Alternates

Swapping is a rename, not a rebuild. All three are rendered at every size in
`../avatars/`.

- `alt-wordmark-even-400.png`, both words the same size, calmest
- `alt-wordmark-tight-400.png`, largest overall, most legible at 32px
- shipped: `wordmark-leads`, the payoff word larger, matching the site's own
  emphasis and the strongest at profile size where people actually judge a brand

Compare them at real sizes in `../proofs/avatar-wordmark.png`.

## Rejected, and why it is worth knowing

An AL monogram was built first and rejected. Amir: "AL is not gonna stick." He is
right that two generic letters say nothing, and the wordmark carries the actual
name. The monogram survives 32px slightly better, which was the argument for it,
but legibility of individual letters is not what recognition depends on at that
size.

An earlier set shipped on ink, white and orange. That was an error: blue is a
core brand colour appearing across 28 files sitewide, not just the CTA button.
See the memory note reference-amg-brand-palette.
