# Final insights

**Project:** Beyond the Price Tag — Beauty Value Intelligence Engine
**Status:** Living document. Finding 1 is from Stage 1.1 (C-track,
2026-08-26; category cut added 2026-08-27). Phase 2 adds the remaining
findings, each traceable to a calculation in this repository.

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
`python src/ingest/feasibility_pdp_analyse.py`. Category cut:
`data/raw/feasibility/_category_breakdown.json` and, per product,
`_category_assignments.csv`, from
`python src/ingest/feasibility_category_breakdown.py`.

### For a shopper, in one paragraph

Standing in a shop with a drugstore blush in one hand and a prestige one
in the other, the number that would settle which is the better buy is how
much product each one holds — and neither brand's website will give it to
you. On the five drugstore brands' own storefronts it is missing from all
1,098 products; on most prestige brands' storefronts it is missing almost
as often, and only MAC and Tom Ford Beauty publish it as a matter of
course. So the price-per-gram comparison cannot be made from the brands'
own listings, for any category, and the cheaper sticker may or may not be
the cheaper product. The packaging is the only place left to look, which
is why the rest of this project goes there.

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

### By category — the zero does not depend on what the product is

Measured 2026-08-27, `_category_breakdown.json`. The expectation going in
was that liquids would be disclosed more often than powders, because a
volume is printed on liquids for regulatory reasons more often than a
weight is on powders. The category cut tests that.

How a product gets a category: the same ordered keyword rules on
`product_type` and title that pre-registered the capture list
(`src/ingest/preregister_capture_list.py`), applied to every product in
every tier, with the rule that fired recorded per product in
`_category_assignments.csv`. It is a keyword guess, not a verified label;
its precision is unmeasured until the §34 audit. Every product lands in
exactly one bucket. Three are not categories: `out_of_scope` (a rule says
it is not a §7 product — eyeliner), `unclassified` (no rule matched:
products named without a category word, such as a MAC shade name under
`product_type` "Lips"), and `excluded` (the capture list's word list for
sets, kits, tools and non-makeup). That word list also catches makeup —
`lash`, `cream`, `oil` and `duo` between them exclude 87 drugstore
products that are mascaras, cream blushes and lip oils — and is reused
unchanged here for comparability with the registered list, so the
`excluded` bucket is large (1,454 of 3,333) and is reported, not hidden.
Unit basis is from `config/categories.yaml`: weight (g), volume (mL), or
form-dependent where the category splits on form (highlighter, brow).

| Category | Basis | Drugstore | Other non-drugstore | MAC + Tom Ford |
| --- | --- | ---: | ---: | ---: |
| Foundation | volume | 0 / 3 | 0 / 22 | 6 / 7 |
| Concealer | volume | 0 / 48 | 0 / 72 | 2 / 2 |
| Powder blush | weight | 0 / 9 | 0 / 21 | 7 / 7 |
| Liquid blush | volume | 0 / 5 | 0 / 6 | — |
| Bronzer | weight | 0 / 88 | 0 / 22 | 16 / 17 |
| Setting powder | weight | 0 / 14 | 2 / 23 | — |
| Pressed powder | weight | 0 / 17 | 1 / 9 | — |
| Lip liner | weight | 0 / 23 | 0 / 19 | 1 / 1 |
| Lipstick | weight | 0 / 81 | 0 / 38 | 57 / 65 |
| Lip gloss | volume | 0 / 87 | 0 / 51 | 20 / 22 |
| Mascara | volume | 0 / 26 | 0 / 24 | 2 / 2 |
| Primer | volume | 0 / 19 | 1 / 23 | 2 / 2 |
| Setting spray | volume | 0 / 17 | 1 / 11 | — |
| Eyeshadow singles | weight | 0 / 53 | 0 / 34 | 27 / 29 |
| Eyeshadow palettes | weight | 0 / 23 | 0 / 40 | 1 / 1 |
| Highlighter | form-dependent | 0 / 41 | 0 / 32 | 1 / 1 |
| Cream blush | weight | 0 / 15 | 0 / 5 | 1 / 1 |
| Liquid lipstick | volume | 0 / 20 | 0 / 9 | 12 / 14 |
| Brow | form-dependent | 0 / 42 | 0 / 42 | 18 / 20 |
| *out of scope* | — | 0 / 40 | 0 / 31 | 14 / 15 |
| *unclassified* | — | 0 / 96 | 14 / 231 | 131 / 141 |
| *excluded* | — | 0 / 331 | 5 / 1,049 | 38 / 74 |
| **Total** | | **0 / 1,098** | **24 / 1,814** | **356 / 421** |

Collapsed to the unit basis of the category:

| Basis | Drugstore | Other non-drugstore | MAC + Tom Ford |
| --- | ---: | ---: | ---: |
| Weight (g) | 0 / 323 (0.0%) | 3 / 211 (1.4%) | 110 / 121 (90.9%) |
| Volume (mL) | 0 / 225 (0.0%) | 2 / 218 (0.9%) | 44 / 49 (89.8%) |
| Form-dependent | 0 / 83 (0.0%) | 0 / 74 (0.0%) | 19 / 21 (90.5%) |

**The pattern, in one line: disclosure does not vary by category or by
whether the category is sold by weight or by volume — drugstore is zero in
all 19 categories, MAC and Tom Ford Beauty disclose on 85–100% of every
category they sell, and every other brand sits at 1.4% for weight-basis
categories against 0.9% for volume-basis — so the powders-versus-liquids
expectation is not supported, and disclosure is a brand practice, not a
category one.** The category differences that appear when all tiers are
pooled (lipstick 31.0%, concealer 1.6%) are the mix of what MAC and Tom
Ford Beauty sell, not a property of the categories.

The 24 disclosures outside MAC and Tom Ford Beauty, read product by
product (`prestige_ex_disclosures` in the JSON): **5 are §7 makeup
products** — two Huda Beauty loose-powder blisters listed as a 6 × 0.15 g
sample, a Makeup by Mario setting spray, a Pixi primer and a Pixi powder.
The other 19 are perfume (Huda Beauty 3, Rare Beauty 4), skincare and
face mists (Pixi 10, a Fenty cleanser, a Huda scrub). Restricted to the
makeup those brands sell, the comparator is **5 of 503 categorised
products (1.0%)**, and half of that is one sample-size item. The 1.3%
figure above is therefore, if anything, generous to the prestige side.

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
form, and that this holds in every one of the 19 categories measured. For
prestige brands other than MAC and Tom Ford Beauty, the same is true
98.7% of the time — 99.0% of the time on their makeup.

It does **not** say:

- anything about **packaging** — net contents printed on the physical
  product were not measured here (that is the B-track's job);
- anything about **product form** as a mechanism — the category cut
  rules out "powders are labelled by weight less often than liquids by
  volume" as the explanation, because the zero holds for weight-basis
  and volume-basis categories alike; it does not supply another
  explanation;
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
