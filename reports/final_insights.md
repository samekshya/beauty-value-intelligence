# Final insights

**Project:** Beyond the Price Tag — Beauty Value Intelligence Engine
**Status:** Living document. Finding 1 is from Stage 1.1 (C-track,
2026-08-26). Phase 2 adds the remaining findings, each traceable to a
calculation in this repository.

Every figure below names the file it comes from. Nothing is recalled or
estimated.

---

## Finding 1 — On their own storefronts, mass-market makeup brands do not disclose net quantity

**Measured:** catalogues collected 2026-08-21; strict re-measurement
2026-08-22; re-run unchanged 2026-08-26.
**Source of every figure:** `data/raw/feasibility/_tier_breakdown.json`
(`by_tier`, `by_brand`, `non_drugstore_excluding_mac_and_tom_ford`),
produced by `python src/ingest/feasibility_tier_breakdown.py` from the
saved catalogue responses in `data/raw/feasibility/shopify_*.json` — no
network needed to reproduce. Second method:
`data/raw/feasibility/_pdp_strict_analysis.json`, from
`python src/ingest/feasibility_pdp_analyse.py`.

### The claim, stated at its measured size

Across **1,098 products from five drugstore brands' own storefronts, a
net quantity appears in a structured slot on 0.** Across 2,235 products
from fourteen non-drugstore brands it appears on 380 (17.0%) — but 356
of those 380 are two brands, MAC and Tom Ford Beauty. **Outside those two,
non-drugstore disclosure is 24 of 1,814 (1.3%).**

The asymmetry is therefore between **0.0% and 1.3%**, not between 0% and
17%. Stated at that size it is still a finding: a categorical zero across
1,098 products and five brands, each measured separately, is not noise.

### What "disclosed" means here

A size counts when a plausible size token — a number with `g`, `mg`,
`mL`/`ml`, `oz` or `fl oz`, within the magnitude bounds of
`config/unit_rules.yaml` — appears in a **structured slot**: a variant
title, an option value, or the product title. Sizes that appear only in
description prose are counted separately as `body_only` and **not**
credited, because prose can describe a bundle component or a recommended
product rather than the item itself. Shopify's shipping-weight field
(`variants[].grams`) is never read; it is packaging weight, not net
content.

### By tier

| Tier | Products | With quantity | Coverage | Body-only mentions |
| --- | ---: | ---: | ---: | ---: |
| **Drugstore** | **1,098** | **0** | **0.0%** | 22 |
| Mid-range | 593 | 12 | 2.0% | 20 |
| High-end | 1,471 | 225 | 15.3% | 135 |
| Luxury | 171 | 143 | 83.6% | 6 |
| All | 3,333 | 380 | 11.4% | 183 |

### By brand within drugstore — the zero is uniform, not an average

| Brand | Products | With quantity | Coverage | Body-only |
| --- | ---: | ---: | ---: | ---: |
| ColourPop | 250 | 0 | 0.0% | 22 |
| essence | 233 | 0 | 0.0% | 0 |
| Milani | 161 | 0 | 0.0% | 0 |
| Physicians Formula | 204 | 0 | 0.0% | 0 |
| Wet n Wild | 250 | 0 | 0.0% | 0 |

No brand is dragging down an otherwise non-zero average. Each of the five
is at zero on its own, including the two largest catalogues (250 products
each). ColourPop's 22 body-only mentions are bundle listings naming the
sizes of their components, which is exactly why prose is not credited.

### The prestige side, brand by brand

| Brand | Tier | Products | With quantity | Coverage |
| --- | --- | ---: | ---: | ---: |
| MAC | high-end | 250 | 213 | 85.2% |
| Tom Ford Beauty | luxury | 171 | 143 | 83.6% |
| Pixi | mid-range | 250 | 12 | 4.8% |
| Huda Beauty | high-end | 175 | 6 | 3.4% |
| Rare Beauty | high-end | 137 | 4 | 2.9% |
| Makeup by Mario | high-end | 60 | 1 | 1.7% |
| Fenty Beauty | high-end | 250 | 1 | 0.4% |
| Anastasia Beverly Hills | high-end | 179 | 0 | 0.0% |
| Tarte | high-end | 249 | 0 | 0.0% |
| Juvia's Place | mid-range | 184 | 0 | 0.0% |
| Morphe | mid-range | 159 | 0 | 0.0% |
| Saie | high-end | 61 | 0 | 0.0% |
| Tower 28 | high-end | 62 | 0 | 0.0% |
| Haus Labs | high-end | 48 | 0 | 0.0% |

Seven prestige brands — 942 products — are at exactly 0.0%, indistinguishable
from drugstore. So the defensible statement is not "prestige discloses,
drugstore doesn't." It is: **drugstore disclosure is categorically zero;
prestige disclosure is near-zero with two exceptions.**

### Second method — visible page text

The catalogue endpoint could, in principle, omit something the product
page shows. Twenty-one product pages were saved (three each from seven
brands, five of them drugstore) and read as visible text with scripts,
styles and hidden blocks removed, under the same size rule. **Two of 21**
showed a size: an Anastasia Beverly Hills lip balm, and a ColourPop
*bundle* listing the sizes of its components. **All fourteen single-product
drugstore pages showed none.** The zero is not an artefact of which
endpoint was read.

### What this finding says — and what it does not

It says: on the storefronts that drugstore brands themselves operate, a
shopper cannot compute price per gram or per millilitre without leaving
the site, because the net content is not on the page in any structured
form. For prestige brands other than MAC and Tom Ford Beauty, the same is
true 98.7% of the time.

It does **not** say:

- anything about **packaging** — net contents printed on the physical
  product were not measured here (that is the B-track's job);
- anything about **retailer listings** — a separate probe of Google
  Shopping titles found a candidate size for 12 of 20 drugstore products,
  on 5% of listings, with conflicting figures (see the feasibility
  report);
- anything about **intent**. The data show a disclosure gap on one
  channel — brand-owned Shopify storefronts — measured on one date, by
  one mechanism (whether the structured product slots that Shopify
  provides, and that MAC and Tom Ford Beauty populate, are populated).
  Why they are empty is not observable in this data, and this report does
  not guess.

### Scope and limits

- One channel: brand-owned storefronts reachable through the Shopify
  catalogue endpoint. Brands whose storefronts refused automated access
  (e.l.f. among drugstore brands; five luxury houses) are absent, so the
  drugstore figure covers five of the eleven §11 brands.
- One snapshot: 2026-08-21, capped at 250 products per brand by the
  endpoint. Coverage could change if brands change their listings.
- The size rule is strict by design; it under-counts rather than
  over-counts. A looser rule on raw page HTML reported 18 of 21 pages
  with a size — every extra hit was an identifier fragment inside a
  script, not a size. The strict figures are the ones to cite.

**Reproduce:** `python src/ingest/feasibility_tier_breakdown.py` and
`python src/ingest/feasibility_pdp_analyse.py` (both read saved files
only).
