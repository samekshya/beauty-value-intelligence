# Beyond the Price Tag — Master Roadmap

Spec: `docs/PROJECT_SPEC.md` (99 sections, authoritative)
This file: phase structure, gates, and what "done" means at each step.

A phase is not complete until its gate is met. Do not start the next
phase early. Update `## Current phase` in CLAUDE.md when a gate passes.

---

## PHASE 1 — DATA FOUNDATION

The unglamorous phase that decides whether the project is credible.
Four stages, each with its own gate.

### Stage 1.0 — Feasibility
- Build repo structure (spec §65)
- Populate config/*.yaml with real starting values
- Identify 4-6 candidate sources for current US makeup data
- Verify legal/access status of each (spec §14) — cite the actual ToS
- Test ~20 representative products per source
- Write `reports/source_feasibility_report.md` (spec §16)

GATE: Primary + fallback source named. Real quantity-field coverage
      measured, not assumed. Legal status documented per source.

### Stage 1.1 — Acquisition
- Build ingestion for chosen sources into `data/raw/` (immutable)
- Every row carries: source_name, source_url, collected_at, method
- Build `config/tier_mapping.yaml` + `brand_tier_mapping.csv` (spec §12)
  — tier assigned from brand positioning, NEVER from price
- Run collection audit (spec §66, notebook 02)

GATE: 600+ products, 10+ categories, 30+ brands, 100% provenance.
      Tier coverage 100%. Coverage gaps reported honestly (spec §88).

### Stage 1.2 — Cleaning, units, entity resolution
- Quantity parser (spec §27-31) — the hardest technical piece
- Weight oz vs fluid oz kept distinct. Never g↔mL.
- Multipack parsing ("2 x 4 g" → pack_count 2, total 8 g)
- Dual-unit labels: prefer manufacturer's explicit metric value
- Entity resolution across sources with match_confidence (spec §22)
- data_quality_flag on every row (spec §32) — never silently drop
- DuckDB schema + load (spec §21)
- Tests: test_units.py, test_matching.py, test_data_quality.py

GATE: All formats in spec §87 parse correctly. 50-product manual audit
      at ~95% on critical fields. Tests pass from a clean environment.

### Stage 1.3 — Core unit economics
- price_per_standard_unit
- category unit price index (spec §37)
- price premium pct (spec §38)
- quantity index (spec §39)
- Bayesian weighted rating (spec §40)
- Drugstore vs prestige comparison by category
- SQL views (spec §67)

GATE: The central research question has a defensible number behind it.
      You can explain every metric's formula without looking it up.

At the end of Phase 1 the project is CREDIBLE. Everything after this
makes it impressive — but only because this part is solid.

---

## PHASE 2 — ANALYSIS & FINDINGS

- Distribution inspection before any test
- Mann-Whitney U / Welch's / Kruskal-Wallis as appropriate
- Effect sizes and CIs alongside every p-value (spec §48)
- Regression: log(price_per_unit) ~ tier + category + log(quantity) + ...
- Drugstore Illusion Index + value classifications (spec §43-44)
- Mini Tax on matched mini/full variants only (spec §45)
- Price vs rating (Spearman, spec §50)
- Brand value analysis with minimum sample thresholds (spec §51)
- Cult product showdowns (spec §47)

GATE: 5-8 real findings written into `reports/final_insights.md`,
      each traceable to a calculation you actually ran.
      Zero fabricated numbers. Zero pre-decided conclusions.

---

## PHASE 3 — DUPE INTELLIGENCE

- Candidate filtering FIRST (category/form/finish compatibility, §55)
- Sentence Transformer embeddings on product text
- Ingredient Jaccard where available
- Shade similarity only where data is trustworthy (§60)
- Category-specific weights, documented (§57)
- PRICE IS NEVER A SIMILARITY FEATURE (§54) — test enforces this
- Benchmark: 30-50 anchors, Precision@3 and @5 (§59)
- Document failure cases
- THEN layer True-Value scoring on top (§61-62)

GATE: Benchmark numbers exist. Failure cases documented. A test proves
      similarity output is unchanged when price is perturbed.

---

## PHASE 4 — PRODUCT & DELIVERY

- Streamlit app, 8 pages (spec §70-77)
- No placeholder values, no broken filters
- README with the story (spec §81)
- docs/methodology.md, docs/data_dictionary.md, docs/limitations.md
- Screenshots / demo
- Full reproducibility check from clean clone (spec §89)
- Acceptance checklist (spec §92) walked line by line

GATE: A stranger can clone, install, rebuild, and run. Every claim in
      the README can be defended in an interview.

---

## PHASE 5 — EXTENSIONS (optional, only if Phase 4 is excellent)

Nepal import premium · historical price comparison · review NLP ·
shade intelligence · promotion analysis · price tracking

---

## Anti-goals (from spec §83)

Do not: fabricate data · convert g↔mL · use price for tier or
similarity · scrape prohibited sources · report p-values without
effect sizes · over-engineer · add tools that don't earn their place.