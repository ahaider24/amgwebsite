# AMG results rebuild: source and review report

> Status update, September 7, 2026: Amir authorized final narrative editing in the subsequent site-strategy mission. The narrative sections in all three results pages are now finalized, all DRAFT markers are removed, and the primary body CTA points to the $499 diagnostic. The draft-status sections below describe the earlier handoff only. Source definitions, metric tables, exclusions and fingerprints remain unchanged. See [ASTRA_SITE_STRATEGY_REPORT.md](ASTRA_SITE_STRATEGY_REPORT.md) for the final editorial state, complete site audit, applied fixes and current verification limits.

Prepared 2026-09-07. Public comparison cutoff: 2026-09-05, the latest supplied GSC capture. Website working tree only. No commits or deployments. The engine repository was read only.

## Deliverables

- `results.html`: outcome cards, before/after tables, full dated Google history, and links to supporting case studies.
- `ai-seo-quality-beverage-results.html`: the organic visit story, including the decline in the previous weekly comparison and Google clicks still below the Aug 22 capture.
- `ai-seo-patriot-crane-results.html`: first recorded Google clicks, explicitly framed as an early traffic result.
- `sitemap.xml`: the two new case-study URLs.
- This report: every published client figure, exclusions, copy handoff, and verification limits.

## Scope, naming, and cornerstone links

The public pages retain only the three client names already present on results.html: Quality Beverage & Paper Distribution, Patriot Crane & Rigging, and Fresno Distributing. No additional client is introduced, including under an invented anonymous persona. Proof headings and explanations are location-neutral. Existing site navigation and footer geography are retained.

The existing dark hero, paper backgrounds, accent colors, Fraunces/Archivo hierarchy, and Geist wordmark are retained. New large result figures use Geist. This follows the actual site typography rather than replacing it.

Applied `/Users/amir/amg-seo-engine/skills/topical_authority_cornerstone.md`, especially its requirements for literal topic overlap, supporting pages, and upward links. Both new URLs, titles, and bodies include “AI SEO”; both link to `/ai-seo` in the breadcrumb, contextual copy area, and CTA. `/results` links to both cases and `/ai-seo`; the existing `/ai-seo` page already links to `/results`. No bulk cluster or additional case study for thin visibility-only data was created. These are draft supporting pages for review; the later click-gated publishing cadence remains Amir’s decision.

## Metric definitions and date rules

All source paths below are relative to `/Users/amir/amg-seo-engine/`. Public HTML comments use those same paths, plus capture dates, field names, and computations. Repeated headline/card/table occurrences cite their sources locally.

- GSC `clicks`: clicks from Google search results, described as visits from Google search. Not unique visitors, calls, or jobs.
- GSC `impressions`: appearances in search results. Not people or purchases.
- GSC `pages_with_impressions`: website pages that appeared in search. Not an index count, nor necessarily catalog/product pages.
- Analytics `organic_sessions_28d`: organic sessions, described as organic search visits. Not the same counter as GSC clicks; may include other search engines.
- All changes are absolute subtraction. No calculated growth percentages, rounded increases, summed overlapping windows, or inferred monetary value are published.
- Aug 20 to Aug 22 is a two-day capture step. Aug 22 to Aug 29 and Aug 29 to Sep 5 are weekly capture steps. Each GSC window itself spans 28 inclusive days and overlaps the next. The pages state this beside the comparisons.
- The broader organic case comparison uses Jul 6 and Sep 5 captures of 28-day totals. It does not claim that the difference is the total incremental traffic over that elapsed period.

### All GSC windows used

| Source file / capture | Inclusive search window |
|---|---|
| `outputs/gsc_snapshot_2026-08-20.json` | 2026-07-24 to 2026-08-20 |
| `outputs/gsc_snapshot_2026-08-22.json` | 2026-07-26 to 2026-08-22 |
| `outputs/gsc_snapshot_2026-08-29.json` | 2026-08-02 to 2026-08-29 |
| `outputs/gsc_snapshot_2026-09-05.json` | 2026-08-09 to 2026-09-05 |

## Every published GSC figure and calculation

For each table below, field order is **clicks / impressions / pages_with_impressions**. The row’s source is `outputs/gsc_snapshot_DATE.json`, `properties["sc-domain:DOMAIN"]`. All before-numbers appear within a comparison or a dated history, never alone as a win.

### Quality Beverage & Paper Distribution

Property: `sc-domain:qualitybevco.com`.

| Capture | Clicks | Appearances | Pages | Exact change since preceding capture |
|---|---:|---:|---:|---|
| 2026-08-20 | 34 | 2319 | 12 | Before row; no win claimed. |
| 2026-08-22 | 40 | 2440 | 12 | 40 - 34 = +6; 2440 - 2319 = +121; 12 - 12 = +0 |
| 2026-08-29 | 33 | 2207 | 12 | 33 - 40 = -7; 2207 - 2440 = -233; 12 - 12 = +0 |
| 2026-09-05 | 35 | 2427 | 13 | 35 - 33 = +2; 2427 - 2207 = +220; 13 - 12 = +1 |

### Patriot Crane & Rigging

Property: `sc-domain:thepatriotcrane.com`.

| Capture | Clicks | Appearances | Pages | Exact change since preceding capture |
|---|---:|---:|---:|---|
| 2026-08-20 | 0 | 99 | 4 | Before row; no win claimed. |
| 2026-08-22 | 1 | 244 | 4 | 1 - 0 = +1; 244 - 99 = +145; 4 - 4 = +0 |
| 2026-08-29 | 5 | 528 | 9 | 5 - 1 = +4; 528 - 244 = +284; 9 - 4 = +5 |
| 2026-09-05 | 8 | 1483 | 11 | 8 - 5 = +3; 1483 - 528 = +955; 11 - 9 = +2 |

### Fresno Distributing

Property: `sc-domain:fresnod.com`.

| Capture | Clicks | Appearances | Pages | Exact change since preceding capture |
|---|---:|---:|---:|---|
| 2026-08-20 | 315 | 11696 | 230 | Before row; no win claimed. |
| 2026-08-22 | 325 | 12645 | 250 | 325 - 315 = +10; 12645 - 11696 = +949; 250 - 230 = +20 |
| 2026-08-29 | 320 | 13708 | 326 | 320 - 325 = -5; 13708 - 12645 = +1063; 326 - 250 = +76 |
| 2026-09-05 | 321 | 15540 | 348 | 321 - 320 = +1; 15540 - 13708 = +1832; 348 - 326 = +22 |

### Additional repeated comparisons and headline placement

- Quality Beverage Google context: Sep 5 vs Aug 22, `clicks`: 35 - 40 = -5. Public copy prints 35 versus 40 to disclose that the latest Google total has not recovered to the earlier level. Sources: `outputs/gsc_snapshot_2026-09-05.json` and `outputs/gsc_snapshot_2026-08-22.json`.
- Patriot headline on the hub and case page: Aug 20 to Sep 5, `clicks`: 8 - 0 = +8. This uses the GSC frozen before-number, not a different metric from the separate Patriot baseline JSON. Sources: `outputs/gsc_snapshot_2026-08-20.json` and `outputs/gsc_snapshot_2026-09-05.json`.
- Patriot hub card: Aug 29 to Sep 5, `clicks`: 8 - 5 = +3, with both counts beside the card. Same subtraction appears in its latest table.
- Fresno Distributing hub card and headline: Aug 29 to Sep 5, `impressions`: 15540 - 13708 = +1832. The adjacent latest table also discloses `clicks`: 321 - 320 = +1 and `pages_with_impressions`: 348 - 326 = +22.
- Fresno Distributing longer traffic context: Sep 5 vs Aug 22, `clicks`: 321 - 325 = -4. Public copy prints 321 versus 325. Sources: `outputs/gsc_snapshot_2026-09-05.json` and `outputs/gsc_snapshot_2026-08-22.json`.

## Every published analytics figure and calculation

Primary source: `outputs/droplet-mirror/quality-beverage-fresno/perf_history.jsonl`, keyed by `date`, field `organic_sessions_28d`. Corresponding dated `perf_score.json` files were also inspected to confirm these are organic session fields with successful analytics access; synthetic call estimates in the same snapshots are not used.

| Placement / comparison | Before | After | Exact computation |
|---|---|---|---|
| Hub headline, case hero, first analytics row | 39 on 2026-07-06 | 77 on 2026-09-05 | 77 - 39 = +38 organic sessions |
| Previous weekly comparison row | 61 on 2026-08-22 | 57 on 2026-08-29 | 57 - 61 = -4 organic sessions |
| Hub card and latest weekly comparison row | 57 on 2026-08-29 | 77 on 2026-09-05 | 77 - 57 = +20 organic sessions |

The former Jul 6 to Aug 5 story (39 to 59) is supported in the history but superseded with the common Sep 5 cutoff. Sep 7 records 79 organic sessions, but that later daily reading is not mixed into the public Sep 5 comparisons. These are scope/date decisions, not claims of missing data.

## Stories and claims excluded

### Revenue, calls, jobs, and ad savings

- **Quality Beverage roughly $1,000 revenue, Sep 3:** present in the old website copy, but no corroborating owner report or revenue receipt was located in the supplied mirrored client records or allowed ledgers. The old HTML is not an approved source. Removed, including from metadata. Do not infer that no revenue occurred; this source set does not verify it.
- **Quality Beverage call totals and “qualified” calls:** the Sep 5 `outputs/droplet-mirror/quality-beverage-fresno/2026-09-05/call_attribution.json` records 100 events, 8 qualified, but only 50 unique `call_id` values, each repeated across channel entries. Sep 3 records 102 events / 51 unique IDs; Sep 7 records 102 / 51. Qualification is also based on answered-call duration, not a confirmed sale or booked job. No public call delta or custom deduplicated result was manufactured. Source files: the corresponding `2026-09-03`, `2026-09-05`, and `2026-09-07/call_attribution.json` artifacts.
- **Patriot and the unnamed construction property’s calls:** `call_attribution.json` and `perf_history.jsonl` mark call mode `synthetic_estimate`, with actual call counts null. Estimates including zero are not client measurements. No calls, leads, or jobs are claimed.
- **Patriot ad “savings” / 20% budget cut:** `docs/patriot_crane_results_ledger.md`, Aug 31, records a configured daily budget change from $75 to $60: (75 - 60) / 75 = 20%. This is an input, not proof of lower actual spend at preserved lead quality. Removed from the results page. Its historical spend/conversion figures are an unverified before-number, not a result. The ledger explicitly leaves conversion meaning to be verified.
- **Booked jobs, order value, store visits, revenue attribution:** no sufficiently verified before/after artifacts in this source set. No synthetic examples or projections substituted.

### AI naming and share of model

- **No AI-naming statistic is published.** The approved client tracker outputs were inspected; no new AI-surface score or delta was derived.
- The old July 84% ChatGPT / 80% Claude wording can be traced to `outputs/droplet-mirror/quality-beverage-fresno/2026-07-30/som_baseline.json`, but it is a single dated surface reading, not proof of improvement. It does not establish that visitors arrived ready to buy.
- `2026-08-27/som_baseline.json` records `claude_search` 88.0; `2026-09-03/som_baseline.json` records 84.0 and the tracker’s own -4.0 delta, `signal: false`. However, the two 25-question sets have zero exact questions in common. The aggregates do not establish a comparable client improvement.
- `outputs/droplet-mirror/quality-beverage-fresno/som_core_panel.json` was pinned on 2026-09-03 at 18:30 UTC from the pre-patch run and explicitly says the first core-versus-core delta lands next run. It contains questions, not a measured performance gain. No later core-versus-core result is supplied.
- Recent ChatGPT surface readings are null due to errors in the tracker artifacts. Null is not zero, and an old reading is not current performance. No AIO/AI Mode percentages, mixed-surface averages, or reconstructed counts are used. Sonnet/Opus measurement implementation stays out of public copy.
- No Patriot measured AI-naming before/after was found in its mirror. Frozen narrative percentages and targets in `docs/patriot_crane_results_ledger.md` are not a sanctioned new delta.

### Rankings, reviews, baseline-only figures, and launches

- **Quality Beverage page-one claims:** both `serp_receipt_co2_refill_fresno_2026-07-19.json` and `serp_receipt_co2_tank_refill_fresno_2026-07-19.json`, under its mirror root, show the same CO2 delivery URL at organic position 5 on that date. They do not supply a comparable before/after by themselves. `outputs/fleet_stocktake_2026-08-21.md` reports #7 on Aug 19 to #4 on Aug 21 but explicitly requires a confirming re-pull before using it as a receipt. No confirmed same-query series was located here. No ranking-growth claim was published.
- **Patriot pack rank / reviews:** `outputs/patriot_baseline_2026-08-20.json` and `docs/patriot-baseline-2026-08-20.md` are frozen before-numbers. The later ledger records held pack position and a review loss (47 to 37, Aug 28–30); it does not support a positive review-growth story. Knowledge Graph failure is missing measurement, not zero.
- **Patriot “five pages indexed” headline:** replaced with actual GSC click gains. Published-page counts are work outputs; `pages_with_impressions` is not a total index count. The Sep 1 ledger also corrects an earlier mistaken claim that service pages did not exist, so that earlier diagnosis is not repeated.
- **Fresno Distributing 250 catalog pages:** replaced with dated GSC comparisons. GSC supports website pages with impressions, without classifying every row as a catalog page. The old claim that this work caused every surfaced page is not established by these files.
- **Fresno Distributing 5,305 Shopping submissions:** a launch in progress in the old copy, without approved dated customer outcome evidence. Removed. No store traffic or sales inferred from submission.
- **Fresno Distributing standalone case study:** omitted because the supplied series supports broader visibility but nearly flat clicks, with no verified order/store-visit payoff. It remains a clearly bounded receipt on the hub.
- **Plausible baseline:** `outputs/plausible_fleet_baseline_2026-08-21.txt` contains 30-day visitor and source totals, without a comparable follow-up. These cannot be treated as gains or paired with GA4 sessions or GSC clicks. AI referrals do not establish AI-naming share.
- **Unnamed construction property and AMG:** weekly GSC data were inspected and computed below for completeness, but neither is newly introduced as client proof. The construction client is not named on the existing results page; AMG is the agency itself.
- **Fixtures / dry runs / composite health scores / estimates:** excluded. Mirrored early dry-run reports, modelled call totals, inherited `som_pct`, health/composite scores, and task-launch status are not client outcome measurements.

## Complete GSC weekly audit for properties not published

Internal source audit only. These names do not appear in new public content. Field order: clicks / impressions / pages_with_impressions.

| Property | Capture comparison | Exact changes |
|---|---|---|
| `amassiiconstruction.com` | 2026-08-20 to 2026-08-22 | 11 - 10 = +1; 180 - 174 = +6; 6 - 6 = +0 |
| `amassiiconstruction.com` | 2026-08-22 to 2026-08-29 | 12 - 11 = +1; 200 - 180 = +20; 6 - 6 = +0 |
| `amassiiconstruction.com` | 2026-08-29 to 2026-09-05 | 12 - 12 = +0; 245 - 200 = +45; 6 - 6 = +0 |
| `amirgetsjobs.com` | 2026-08-20 to 2026-08-22 | 16 - 12 = +4; 637 - 531 = +106; 17 - 17 = +0 |
| `amirgetsjobs.com` | 2026-08-22 to 2026-08-29 | 16 - 16 = +0; 756 - 637 = +119; 22 - 17 = +5 |
| `amirgetsjobs.com` | 2026-08-29 to 2026-09-05 | 18 - 16 = +2; 1651 - 756 = +895; 30 - 22 = +8 |

## DRAFT sections awaiting Amir’s voice

Every narrative paragraph is bracketed with an exact `<!-- DRAFT FOR AMIR -->` marker and `<!-- END DRAFT FOR AMIR -->`, plus a `DRAFT ID` comment. Factual captions, labels, metric definitions, tables, and stat cards are structured editorial material. Headlines and CTA labels remain editable but are not presented as Amir-authored prose.

| Page | Draft IDs |
|---|---|
| `results.html` | `RESULTS-HERO`, `RESULTS-QB`, `RESULTS-QB-CONTEXT`, `RESULTS-PATRIOT`, `RESULTS-FD`, `RESULTS-FD-CONTEXT`, `CTA` |
| `ai-seo-quality-beverage-results.html` | `QB-HERO`, `QB-RESULT`, `QB-GOOGLE`, `QB-SCOPE`, `CTA` |
| `ai-seo-patriot-crane-results.html` | `PATRIOT-HERO`, `PATRIOT-RESULT`, `PATRIOT-CONTEXT`, `PATRIOT-SCOPE`, `CTA` |

The CTA paragraph is repeated on all three pages and should be rewritten consistently. Rewriting should retain metric scope and evidence limits, especially “visits” versus calls/orders and the overlapping-window qualification.

## Verification and remaining limitation

- Passed HTML parsing and structure checks: one H1, one main, unique IDs, correct per-page canonical and valid JSON-LD.
- All local page links and same-page anchor links resolve; both cases have contextual `/ai-seo` links. Sitemap XML parses and includes both new URLs.
- Every client table row has a adjacent source comment or one inside the row. All referenced source paths exist. Source comments include dates and fields/computation context. Numeric before/after values were checked against the supplied JSON and JSONL records.
- All inline JavaScript parses successfully. Mobile menu expanded states were corrected on these pages.
- No em dash characters or em dash HTML entities occur in the three edited/new public pages. All narrative paragraphs pass the DRAFT-marker check.
- Mobile structural checks: each of the 12 tables across the three pages is inside its own keyboard-focusable, named `overflow-x:auto` region with contained overscroll. Tables retain readable minimum widths rather than compressing data columns. Cards stack at 780px; navigation collapses at 900px; the narrow 380px rule reduces gutters. Menu/CTA controls have 44px minimum height, and story links/table disclosure controls have 48px minimum height. Focus outlines and reduced-motion support are present.
- **Rendered mobile/desktop verification could not run.** Browser discovery returned no available browsers. The filesystem execution sandbox rejected a local HTTP listener (`Operation not permitted`); an isolated headless Chrome launch exited 134. No permission bypass was attempted. Consequently actual visual appearance, measured overflow, horizontal swipe behavior, font loading, and interactive tapping remain unverified in a browser. Inspect at 320px, 375px, 768px, and desktop width before publishing.
- No build step exists for this static HTML site. No packages installed. No engine writes, commits, or deployments.

## Published-source fingerprints

SHA-256 of the exact input files used for public statistics, for later comparison with updated source data.

| Source | SHA-256 |
|---|---|
| `outputs/droplet-mirror/quality-beverage-fresno/perf_history.jsonl` | `f08c1b7734e0517ba01f6da350b1942ad2d97111de346e68b0dc50197001057d` |
| `outputs/gsc_snapshot_2026-08-20.json` | `3a3e4f90e6fd1bcf9ebf845460b8c9752d671792561c2a30e5f643ccfa0b2ada` |
| `outputs/gsc_snapshot_2026-08-22.json` | `72d37edc5110b33371b5cf8d19e83f3f21b0f4f750761025d840e128ec0ee87d` |
| `outputs/gsc_snapshot_2026-08-29.json` | `a5f9f584cff797c9f91dd79612cb1897bb889e326068728f26020ea03a9cbee7` |
| `outputs/gsc_snapshot_2026-09-05.json` | `ba48546724effceb04c3452ec26a7b99406f6e03a3c15ba23cb55b4bc9420031` |
