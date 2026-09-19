# Social avatar, ready to upload

Decided 2026-09-18 by rendering every candidate circular, on white, at the sizes
platforms actually display. Sheet: `../proofs/avatar-circle-decision.png`.

The AL monogram on ink holds at 400, 180, 48 and 32px. Both spark versions lose
legibility below 180px; on paper the spark nearly disappears against a white
timeline. Every platform masks avatars to a circle, so a square proof would have
flattered a design that fails in practice.

| File | Where it goes |
|---|---|
| `x-twitter-400.png` | X, displays at 48px in timeline |
| `linkedin-400.png` | LinkedIn personal and company |
| `instagram-320.png` | Instagram |
| `facebook-360.png` | Facebook page |
| `slack-512.png` | Slack workspace |
| `youtube-800.png` | YouTube channel |
| `master-1024.png` | source for anything else |

For Google Business Profile use `../gbp-wordmark-1024.png` instead. GBP shows
the image larger, so the full wordmark reads there and carries more brand than a
two-letter mark. It was verified under a circular mask with nothing cut.

Ground is the site's own CTA gradient, `#3CB8DE` to `#2596BE` to `#1A5E92`,
with the A in paper `#FBF8F2` and the italic L in accent `#FF4D1C`.

Corrected 2026-09-18. The first export was ink, white and orange, because I had
wrongly concluded blue was only a button colour. It is not: `#2596BE` appears 12
times in index.html and across 28 files sitewide as the section eyebrow colour.
Amir: "the whole point was like a sky blue orange and white." Black, white and
orange is a common palette; sky blue with orange on warm white is not.

Alternatives rendered in `../avatars/`: `al-blue-ground` flat blue,
`al-paper-ground` for light surfaces, `al-ink-ground` if a dark mark is ever
needed. All four are real Geist 700 with the italic L.

Open question, Amir's call: AL is a two letter mark and two letters is roughly
all that survives 32px. If it reads as too generic, the alternative is accepting
a mark that is beautiful on a profile page and illegible in a timeline.
