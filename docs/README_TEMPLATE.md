<!--
═══════════════════════════════════════════════════════════════════════
TEMPLATE — NOT A FINISHED README. DELETE THIS BLOCK BEFORE SHIPPING.

Every {{PLACEHOLDER}} is a figure that does not exist yet. Fill each
one from output produced in this repository. Nothing from memory.

Before any push where this file is README.md:

    Select-String -Path README.md -Pattern "\{\{"

Returns nothing = finished. Returns anything = not finished.

Sections you cannot fill yet: delete them. A short honest README beats
a long one with holes.

Structure and voice follow sworaj42/f1-data-warehouse. Key techniques
to preserve:
  · explain the DATA PROBLEM before the solution
  · state a finding, then caveat it in the same paragraph
  · justify why the obvious alternative design was rejected
  · report work you removed on evidence, not just work you kept
  · no adjectives, no marketing, short declarative sentences
═══════════════════════════════════════════════════════════════════════
-->

# Beyond the Price Tag

{{ONE_SENTENCE: what this is. Shape: "A retail analytics project that
normalises N makeup products from M brands into comparable unit prices,
and a tool that identifies genuinely cheaper alternatives rather than
merely cheaper-looking ones."}}

Python · DuckDB · SQL · scikit-learn · Sentence Transformers · Streamlit

## Why this project

Beauty products are compared by sticker price. A $12 drugstore
concealer looks cheaper than a $35 prestige one. Whether it *is*
cheaper depends on how much product is in the tube, and package sizes
across this market vary by an order of magnitude.

Answering that requires the net contents of each product. That number
is where the project becomes difficult.

{{THE_DATA_PROBLEM — the strongest paragraph in this README. Write it
from measured facts in reports/source_feasibility_report.md:

 · every US multi-brand retailer is excluded on terms — name them and
   note that permissive robots.txt is not permission
 · brand storefronts publish price and name reliably, size almost
   never: {{N}} of {{N}} products carried a net quantity
 · drugstore specifically: {{N}} of {{N}}
 · the Shopify variant `weight` field looks exactly like net contents
   and is shipping weight including packaging, populated on {{PCT}}
   of products — roughly {{N}}× the real size coverage. Using it would
   have corrupted every unit-price figure in the project without
   tripping a single validation rule, because the values look
   reasonable.

Close with what the project therefore had to build.}}

This project builds that layer:

- {{A permitted-source acquisition pipeline with provenance on every
  row.}}
- {{A quantity parser that standardises N size formats and refuses to
  guess.}}
- {{A DuckDB model separating products from retailer offers.}}
- {{N SQL views defining every published metric.}}
- {{A similarity engine in which price is structurally excluded.}}
- {{An N-page Streamlit application reading those views and nothing
  else.}}

## Project at a glance

| Products | Brands | Categories | With verified quantity | Retailers | Views | Dashboard pages |
| -------- | ------ | ---------- | ---------------------- | --------- | ----- | --------------- |
| {{N}}    | {{N}}  | {{N}}      | {{N}}                  | {{N}}     | {{N}} | {{N}}           |

{{Scope line: "US list-price snapshot, DATE. Prices are list, not sale.
Quantity verified for N of M products; coverage by tier in Scope and
limitations."}}

## Architecture

{{Diagram: diagrams/pipeline_architecture.png — sources → data/raw →
staging → processed → analytics → DuckDB → app. Draw it once the
pipeline is real.}}

- `data/raw/` is immutable and is the network boundary. Only ingestion
  reaches the network; every stage after it reads from disk, so a
  rerun costs nothing and runs offline.
- {{The validated handoff between stages, and what fails the run.}}
- {{Quantity provenance: how a captured or extracted size is traced
  back to the image, page or photograph it came from.}}
- {{Price and quantity may come from different sources. State the rule
  that keeps them compatible.}}

## Data model

{{Diagram: diagrams/data-model.svg}}

Products and offers are separate tables. Three retailers listing the
same product produce three offer rows sharing one product id, not one
row overwritten twice. {{Why the obvious alternative was rejected: a
single table with a price column cannot represent disagreement between
retailers, and the disagreement is data — §20.}}

{{Same treatment for variants and sizes: a mini and a full size are
variants of one product, and collapsing them would destroy the Mini
Tax measurement entirely.}}

[Data dictionary](docs/data_dictionary.md) ·
[Methodology](docs/methodology.md) ·
[Limitations](docs/limitations.md)

## Engineering highlights

### Permitted-source acquisition

{{Sources checked before collection, not after. {{N}} rejected on
quoted terms. No CAPTCHA handling, no proxy rotation, no rate-limit
evasion — where a source prohibited automated access the project used
a different source. The rejections and their governing clauses are in
reports/source_feasibility_report.md.}}

### Quantity parsing

{{The technical centre of the project. Cover: formats handled; weight
ounces and fluid ounces never treated as equivalent; multipacks
resolved to pack count and total; dual-unit labels preferring the
manufacturer's explicit metric value; grams never converted to
millilitres, because density is unknown and inventing it would corrupt
every downstream figure.

Include the false-positive traps the parser rejects — hash fragments
in minified JavaScript reading as `029g`, `0MG`, `7G`. A naive regex
scored {{N}}/21 on a sample where strict measurement scored {{N}}/21.}}

### Entity resolution

{{Barcode first where available, then normalised brand, then fuzzy
name with category and size compatibility. Every pair carries a
match_confidence. Three bands: auto-merge, human review, reject.
Uncertain matches are stored, never merged. {{N}} merged, {{N}} held,
{{N}} rejected.}}

### Price excluded from similarity

{{Similarity and value are computed separately and stored separately.
If price entered the similarity model it would learn that cheap means
similar, which is the opposite of the question. A test asserts the
similarity score is unchanged when a candidate's price is perturbed.}}

### Quality flags over deletion

{{Nothing is silently dropped. Every row carries a data_quality_flag;
rows unfit for unit analysis are excluded from that analysis by flag
and remain visible in the catalogue. Counts per flag: {{TABLE}}.}}

## Selected analytical findings

{{Follow the F1 pattern exactly: bold claim sentence, the number, then
the caveats in the same paragraph. Write these only when the
calculations have run.}}

**{{FINDING_1_CLAIM}}** {{The disclosure asymmetry is likely to be
finding #1: N of M drugstore products publish net contents against
PCT of prestige. Caveat in the same breath — one channel, brand
storefronts rather than retailer listings; prestige disclosure is also
poor, so the comparator is non-zero rather than good; and this is a
measurement of what is published, not a claim about intent.}}

**{{FINDING_2_CLAIM}}** {{Sticker gap versus unit gap — the project's
central contrast. State both numbers and the categories where the
direction reverses.}}

**{{FINDING_3_CLAIM}}** {{Mini Tax. Matched variants of the same
product only. State n pairs — if n is small, say so in the same
sentence rather than in a footnote.}}

**{{FINDING_4_CLAIM}}** {{Price versus rating. State precisely what
the correlation does and does not license a reader to conclude.}}

{{Include at least one finding that went against the pre-registered
hypothesis. docs/hypotheses.md was committed before any metric was
computed; the git timestamp is the evidence that the predictions came
first.}}

**The {{N}} analytical views**

All in `sql/analytics/`.

| View                     | Question it answers                              |
| ------------------------ | ------------------------------------------------ |
| `v_category_economics`   | Where is the prestige premium real?              |
| `v_unit_price_index`     | How does this product compare to its category?   |
| `v_drugstore_illusion`   | Which savings survive quantity adjustment?       |
| `v_mini_tax`             | What does a smaller size actually cost per gram? |
| `v_brand_value`          | Which brands give the most product per pound?    |
| `v_hero_products`        | {{...}}                                          |
| {{...}}                  | {{...}}                                          |

## Dashboard

{{Every metric is defined in SQL views. Streamlit reads, caches and
renders them without redefining aggregations in pandas. A test asserts
the app and the notebooks import the same metric functions by
identity, so a reimplementation inside the app fails the build rather
than silently diverging.}}

### True-Value Dupe Finder

{{The flagship. Screenshot. One paragraph: the user names a product;
the tool returns alternatives ranked by similarity, each showing
checkout saving and unit saving side by side. The two frequently
disagree, and that disagreement is the product.}}

### {{PAGE_2}}
{{Screenshot and one paragraph.}}

### {{PAGE_3}}
{{Screenshot and one paragraph.}}

## Validation

Each item below was exercised against the built dataset.

- {{Quantity parser: every format in the specification, plus the
  false-positive traps, asserted against known conversions.}}
- {{Manual audit: {{N}} randomly sampled products verified by hand
  against source pages. {{PCT}} correct on critical fields. Errors
  found: {{WHAT}}.}}
- {{Entity resolution verified on known same-product examples across
  sources.}}
- {{Price-independence verified: similarity output unchanged under
  price perturbation.}}
- {{Dupe benchmark: {{N}} anchors labelled by hand. Precision@3
  {{VALUE}}, Precision@5 {{VALUE}}. Failure cases documented in
  reports/dupe_failures.md.}}
- {{Reproducibility verified: a clean clone rebuilds every artefact
  from raw with the documented commands.}}

{{If measurement errors were found during development, state how many
and which direction they ran. If they consistently flattered the
result, that is worth saying — it is why verification is a script here
and not a habit.}}

{{If any component was built and then removed on evidence, say so and
give the evidence. Work discarded for a reason is a stronger signal
than work kept by default.}}

```
python scripts/run_verifications.py
  scripts/verify_readme_figures.py    {{N}} of {{N}} figures
  src/validation/quality_checks.py    {{N}} of {{N}} checks
  reproduce_all_results.py            {{N}} of {{N}} stages
  pytest                              {{N}} tests, {{N}} files
```

## Quick start

Prerequisites: Python 3.13, Git.

```
# 1. clone and set up
git clone {{REPO_URL}} beauty-value && cd beauty-value
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate           # macOS / Linux
pip install -r requirements.txt
cp .env.example .env                # fill in keys if your sources need them

# 2. rebuild processed data from raw
{{COMMAND}}

# 3. build the database
{{COMMAND}}

# 4. dashboard on http://localhost:8501
streamlit run app/app.py

# 5. verify every figure in this README
python scripts/run_verifications.py
pytest
```

{{Note anything slow, anything requiring a key, and anything that
cannot be reproduced without manual capture — and how a stranger can
audit that capture even if they cannot repeat it.}}

## Repository structure

```
.
├── app/                Streamlit application
├── config/             Categories, unit rules, tier mapping, usage
│                       assumptions. Every threshold lives here, not
│                       in a notebook.
├── data/
│   ├── raw/            Immutable source data (gitignored)
│   ├── staging/        Parsed, source-specific
│   ├── processed/      Normalised products, brands, sizes, offers
│   └── analytics/      Feature-engineered analytical dataset
├── database/           DuckDB schema and build
├── diagrams/           Architecture, data model, dashboard screenshots
├── docs/               Methodology, data dictionary, limitations,
│                       pre-registered hypotheses
├── notebooks/          01 to 12, in execution order
├── reports/            Source feasibility study, findings, failures
├── scripts/            Build, verification suite
├── sql/                Analytical views
├── src/
│   ├── ingest/         Permitted-source acquisition
│   ├── units/          Quantity parser
│   ├── matching/       Entity resolution
│   ├── validation/     Quality checks
│   ├── features/       Metric computation
│   └── modelling/      Similarity and true-value scoring
└── tests/
```

## Scope and limitations

- **Prices are a snapshot.** Collected {{DATE}}, list price rather
  than sale price so temporary promotions do not distort cross-product
  comparison. Nothing here states what a product costs today.
- **{{Quantity coverage}}.** {{Which tiers and categories have
  verified quantity, which do not, and which conclusions therefore do
  not extend to them.}}
- **Market tier is a judgement, not a measurement.** Assigned from
  distribution and brand positioning, never from price — deriving it
  from price would make the central question circular. The mapping is
  in `config/tier_mapping.yaml` and is arguable.
- **{{Sample composition}}.** {{The brands here are the brands with
  permitted, structured, accessible data. Name which tiers are thin
  and why. If luxury was cut because those houses run no accessible
  storefront, say exactly that.}}
- **Value is not quality.** The rating-adjusted score combines unit
  economics with a Bayesian-weighted rating. It measures how much
  product you get and how it was received, not whether it performs or
  suits you.
- **{{Shade}}.** {{If shade data was insufficient, state that the
  engine returns product-level alternatives rather than exact shade
  matches — and ensure the phrase "exact dupe" appears nowhere in this
  repository.}}
- **Ingredient overlap is not formulation equivalence.** Two products
  can share most of a list and behave differently.
- **{{Manual capture}}.** {{If quantities were captured by hand: a
  stranger can re-audit the photographs but cannot re-run the capture.
  State it plainly.}}
- **{{Cost per use}}.** {{If shipped: usage amounts are assumptions in
  config/usage_assumptions.yaml and apply to nobody in particular.}}
  ...
  lllll