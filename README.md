# Beyond the Price Tag

A retail analytics project that normalises US makeup products into
comparable unit prices — price per gram or per millilitre — so that a
product cheaper at the till can be told apart from one that is merely
smaller, and a tool on top of it that finds alternatives cheaper per unit
rather than only cheaper at checkout. Neither the unit prices nor the tool
exists yet. What exists is the measured reason they are hard to build.

Python 3.13 · DuckDB · pandas · RapidOCR today. SQL views, scikit-learn,
Sentence Transformers and Streamlit are planned for later phases and are
not in `requirements.txt`.

## Why this project

Beauty products are compared by sticker price. A $12 drugstore concealer
looks cheaper than a $35 prestige one. Whether it is cheaper depends on
how much product is in the tube, and the label rarely makes that
comparable.

Answering that needs the net contents of every product. That number is
where the project becomes difficult. Everything below is measured and
recorded in
[`reports/source_feasibility_report.md`](reports/source_feasibility_report.md),
with the clauses quoted.

**Every US multi-brand retailer that sells mass-market makeup is closed to
this project on its own terms.** Checked 2026-08-22. Sephora serves
`robots.txt` itself with HTTP 403; the site refuses automated requests at
the edge, and no circumvention was attempted. Ulta's terms exclude from
the licence "any collection and use of any product listings, descriptions,
or prices" and prohibit "any use of data mining, robots, or similar data
gathering and extraction tools". Target's terms prohibit any "use of data
extraction, scraping, mining or other data gathering tools, or create a
database by systematically downloading or storing Site content" — a
description of this project's `data/raw/` layer. Walmart's terms could not
be read: three URLs on two domains served a CAPTCHA, and the project stops
there; the prohibition is corroborated by its corporate-site terms and not
verified on the retail site. Ulta's and Target's `robots.txt` leave product
pages open to every crawler. A permissive `robots.txt` is not permission;
where it and the terms disagree, the terms govern.

**Brand-owned storefronts publish price and name reliably, size almost
never.** 19 of 20 brand storefronts whose robots policies permit product
paths returned public catalogue JSON: 3,333 products, collected
2026-08-21. Product name, brand, list price and URL are present on 100%.
A net quantity in a structured slot — variant title, option value or
product title — is present on 380 of 3,333 (11.4%). 356 of those 380 are
two brands, MAC and Tom Ford Beauty. Outside those two, 24 of 1,814
non-drugstore products (1.3%) carry one.

**Drugstore specifically: 0 of 1,098.** Five drugstore brands — ColourPop,
essence, Milani, Physicians Formula, Wet n Wild — each measured separately,
each at zero. A second method, reading the visible text of 21 saved
product pages with scripts and styles removed, found a size on 2 pages,
neither a single drugstore product; all 14 single-product drugstore pages
showed none. The zero is a measurement of what these brands publish on
one channel, their own storefronts, on one date. It says nothing about
what is printed on the packaging and nothing about intent.

**The field that looks like the answer is shipping weight.** Shopify's
variant `grams` field — `weight` in the storefront API — is populated on
55.7% of the 3,333 products, 1,857 of them, over four times the real size
coverage. It is shipping weight including packaging: the bottle, pump and
carton, not the product. It arrives without a documented unit. Used as net
quantity it would have produced price-per-gram figures for 1,857 products
that look reasonable and are all wrong, and no validation rule in the
specification — price above zero, quantity above zero, quantity within a
sane range — would have flagged one of them, because the values are
plausible. The field is forbidden as a quantity source in
`config/unit_rules.yaml`; the test that enforces the rule is not written
yet.

**Regex on raw HTML fabricates coverage.** A first pass over the 21 saved
pages reported a size on 18. Strict measurement — scripts dropped, visible
text only, a plausible magnitude required — gave 2. The extra 16 were
identifier fragments inside minified scripts (`029g`, `0MG`, `7G`). The
strict figures are the ones cited anywhere in this repository.

Two more routes were measured on 2026-08-26 and neither closes the gap.
Open Beauty Facts carries a parsed quantity field, but its export holds 57
US-tagged makeup rows, 10 of them drugstore products with a quantity.
Google Shopping listing titles, through a paid API on its free tier,
offered a candidate size for 12 of 20 drugstore products probed, on 5% of
listings and with conflicting figures for the same product — a hint to
verify, not a source.

The project therefore has to build the quantity layer itself: the
storefront catalogues as the product spine; net quantity captured
separately, from packaging in the storefronts' own product images by OCR
or by hand, against a product list fixed before any size is read; each
capture joined back to its US listing by barcode or flagged; and one rule
that price always comes from the US snapshot and never from where the
package was read.

## Status

**Phase 1 · Stage 1.1 — acquisition. 2026-08-27.** The Stage 1.0
feasibility gate closed on 2026-08-26 with the decision to write up the
disclosure asymmetry first, then capture drugstore quantities. Finding 1
is written, with its tier, brand and category cuts. The capture list is
registered. The OCR probe on storefront product images read a net quantity
for 8 of the 30 pre-registered drugstore products (26.7%), every one of
the 8 correct against the image; 19 of the 22 misses have no size on the
item the storefront photographs, so better OCR would not move them
([`reports/ocr_feasibility_report.md`](reports/ocr_feasibility_report.md)).
Against the plan's threshold of about 40%, OCR was judged not viable on
2026-08-27; net quantity will be read from packaging in hand, on a
capture sheet and protocol fixed before any pack is read
(`docs/shelf_capture_protocol.md`). No pack has been read yet. No unit
price has been computed for any product.

Finding 1, from [`reports/final_insights.md`](reports/final_insights.md):
on their own storefronts, drugstore brands disclose net quantity on 0 of
1,098 products, against 24 of 1,814 (1.3%) for non-drugstore brands
outside MAC and Tom Ford Beauty. The asymmetry is between 0.0% and 1.3%,
not between 0% and 17%; seven prestige brands, 942 products, are also at
exactly zero. Cut by category on 2026-08-27, the drugstore zero holds in
all 19 categories and on both unit bases — 0 of 323 weight-basis products
and 0 of 225 volume-basis — while the other non-drugstore brands sit at 3
of 211 (1.4%) and 2 of 218 (0.9%), so product form does not explain the
gap. The category is a keyword guess whose precision is unmeasured, and
1,454 of 3,333 products fall into that rule's excluded bucket. Restricted
to makeup, the non-drugstore comparator is 5 of 503 (1.0%). One channel,
one date, no claim about intent.

Task-level progress: [`docs/EXECUTION_PLAN.md`](docs/EXECUTION_PLAN.md).

## What exists now

Everything below is committed and re-runs from saved files. No step needs
the network except the original probes.

- `reports/source_feasibility_report.md` — every source checked, clauses
  quoted, verdicts, measured coverage, and the Stage 1.0 decision memo.
- `reports/final_insights.md` — finding 1 with its tier, brand and
  category cuts and a one-paragraph statement for a shopper, each figure
  named to the file it comes from.
- `data/raw/feasibility/` — the 19 storefront catalogue responses with
  provenance (`shopify_*.json`), the strict tier and brand breakdown
  (`_tier_breakdown.json`), the category cut (`_category_breakdown.json`,
  per-product `_category_assignments.csv`), the visible-text page analysis
  (`_pdp_strict_analysis.json`), the Open Beauty Facts measurement and the
  Google Shopping probe summary. Saved product pages and the Open Beauty
  Facts exports are gitignored and re-downloadable;
  `data/raw/obf/PROVENANCE.md` records what was downloaded and how it was
  verified.
- `data/raw/capture/` — the pre-registered capture list: 250 drugstore
  products, 50 per brand across 19 categories, and the 30-product OCR
  sample. Identity and provenance fields only; no quantity, no price. The
  rule is in `docs/capture_list.md`. Beside it, the OCR probe's output:
  per-product recognised text with every image's URL (`ocr/`), the run
  summary, the analysis, and a by-eye audit of all 30 products
  (`_ocr_probe_visual_audit.csv`). The images are gitignored and
  re-downloadable. And the shelf-capture sheet
  (`shelf_capture_template.csv`): the 250 registered products in a fixed
  capture order with identity columns pre-filled and the capture columns
  blank; built by `src/ingest/build_capture_template.py`, no price field.
- `reports/ocr_feasibility_report.md` — the OCR test: hit rate under the
  pre-registered rule and under a labelled post-hoc one, every hit checked
  against its image, the misses classified, and the ceiling.
- `src/ingest/` — the probes and measurements behind the above: storefront
  catalogue probe, coverage, tier and category breakdowns, saved-page
  strict analysis, Open Beauty Facts query with an export-integrity gate,
  Google Shopping title probe with a free-tier hard stop, capture-list
  pre-registration, and the OCR size probe on storefront product images
  — bounded, resumable from disk — with its read-only analysis script.
  `sql/obf_feasibility.sql` holds the Open Beauty Facts query.
- `config/` — categories with their unit basis (`categories.yaml`),
  conversions and forbidden conversions (`unit_rules.yaml`), the
  provisional brand-tier list (`tier_mapping.yaml`), the source registry
  with measured coverage (`data_sources.yaml`), usage assumptions.
- `docs/` — `PROJECT_SPEC.md` (authoritative), `ROADMAP.md` (phase gates),
  `EXECUTION_PLAN.md` (progress), `DEVELOPMENT.md` (conventions, hazards),
  `methodology.md` (the rules that shape every number), `capture_list.md`,
  `shelf_capture_protocol.md` (how packaging is read and photographed, and
  how a stranger re-audits it), `README_TEMPLATE.md` (the skeleton of the
  final README).
- `requirements.txt` — Phase 1 dependencies only. Setup is in
  `docs/DEVELOPMENT.md`.

`app/`, `database/`, `notebooks/`, `tests/` and every `src/` package other
than `src/ingest/` are placeholders. No database exists. No test exists.

## Planned — not built

None of the following exists. Each is a phase gate in `docs/ROADMAP.md`.

- **Quantity capture and verification** (Stage 1.1). OCR on storefront
  product images for the registered list, or manual capture with
  photographs and barcodes if OCR fails; every captured quantity matched
  to its US listing by barcode or flagged `identity_unverified`. Physical
  capture supplies quantity only; price always comes from the US
  storefront snapshot (`docs/methodology.md`).
- **Cleaning, units, entity resolution** (Stage 1.2). A quantity parser
  that keeps weight ounces and fluid ounces apart, resolves multipacks to
  a pack count and a total, prefers the printed metric value on dual-unit
  labels and never converts grams to millilitres; entity resolution
  barcode first, with a confidence band on every pair; a data-quality flag
  on every row, nothing dropped; a DuckDB model with products separate
  from retailer offers.
- **Unit economics** (Stage 1.3). Price per standard unit, category
  unit-price index, price premium, quantity index, Bayesian-weighted
  rating; one SQL view behind each figure; hypotheses committed before any
  metric runs.
- **Analysis** (Phase 2). Tier comparisons with effect sizes and
  confidence intervals, a regression controlling for category, the
  Drugstore Illusion Index and value classifications, the Mini Tax on
  matched variants only, price against rating.
- **Dupe intelligence** (Phase 3). Candidate filtering, text and attribute
  similarity with price structurally excluded and a test that asserts it,
  a hand-labelled benchmark, documented failures, a true-value layer with
  separable components.
- **Dashboard and delivery** (Phase 4). An eight-page Streamlit
  application reading precomputed views, diagrams, a verification suite
  that re-checks every README figure by script, methodology, data
  dictionary and limitations documents, a clean-clone rebuild.

Pipeline shape when built: sources → `data/raw` (immutable) → staging →
processed → analytics → DuckDB → app. Not built.

The full README ships at Phase 4 from `docs/README_TEMPLATE.md`, with
every figure re-checked by script before it is pushed.
