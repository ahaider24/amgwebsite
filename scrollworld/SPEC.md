# Scroll-World build spec (PAUSED 2026-08-06 to onboard Patriot Crane)

**Subject:** "How AMG's AI unifies your workplace." Fly through a miniature clay-diorama business; each room = one of the five AI workflows; ends unified into one intelligence. Lives on AMG's own site (amirgetsjobs.com). First Fresno agency with an Apple-tier scroll cinematic.

**Camera:** Continuous walkthrough = Architecture A (one forward glide, no cuts, never reversing; each leg's start-image = previous leg's ACTUAL last frame; NO connectors, NO end-image). N legs = N videos (cheaper than B's 2N-1).

**Art direction:** warm clay diorama, isometric tilt-shift miniature, soft matte low-poly, warm light. AMG palette: paper #FBF8F2 / paper-2 #F1EAD9 / ink #14110A / accent #FF4D1C / accent-deep #C8380E / gold #F2B01E.

**Journey (7 scenes; each = a room + one AI; editable):**
1. Your shop from above (establishing) — descend toward a quiet miniature business.
2. Front desk -> Speed to Lead — every call/text/form answered under 60s.
3. Workbench -> Quote Automation — photo + voice note in, branded estimate out.
4. Back office -> Document Processing — invoices/POs/intake read + filed, no hands.
5. Customer wall -> Database Reactivation — past customers scored, best revived.
6. Owner's desk -> Unified Reporting — one plain-English dashboard, Mon 7am.
7. Rise to reveal -> One intelligence — whole business glowing + wired; evenings back. CTA.
   (Scene 7 = forward + crane-up reveal, NOT a pull-back — Arch A forbids reversing across a seam.)

**Pipeline status (2026-08-06):**
- ffmpeg present; codex logged in via ChatGPT -> STILLS ARE FREE.
- higgsfield + monid NOT installed. Higgsfield CLI = npm `@higgsfield/cli@1.1.20` (installable). Higgsfield needs interactive OAuth (Amir runs `higgsfield auth login`) + credits. Monid install method TBD.
- Work dir: /Users/amir/amgwebsite/scrollworld (stills/ subdir created).

**Resume checklist:**
1. Generate 7 stills via codex (free) -> review cohesion -> show Amir.
2. Interview leftovers: mobile (y/n), budget tier (480p previz ~$4 / 720p ~$12 / 1080p ~$27-31; mobile ~2x).
3. Video GATES: install @higgsfield/cli, Amir OAuth, fund credits/Monid.
4. Render legs (Arch A forward glides) -> encode (-g 8, blob-seek) -> wire references/scrub-engine.js -> QA seams (Step 8).

Related memory: project-amg-flywheel-intelligence-layer, reference-premium-immersive-design.
