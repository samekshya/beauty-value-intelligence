# EXECUTION PLAN — Beyond the Price Tag

This file is the single source of progress truth. The conversation
transcript is not. If the transcript and this file disagree, this file
wins.

Authority: docs/PROJECT_SPEC.md (§ references) · docs/ROADMAP.md (gates)
· docs/DEVELOPMENT.md (rules, git workflow).

---

## PROTOCOL — how to work this file

1. On session start: read docs/DEVELOPMENT.md, then this file. Find the FIRST
   unchecked `[ ]` task. Announce it in one line. Begin.
2. A task is complete only when its **Done when** condition is true and
   you have VERIFIED it by running something — a query, a test, a
   script. Assertion is not verification.
3. On completion: commit and push per docs/DEVELOPMENT.md, change `[ ]` to `[x]`
   with the date, commit this file's change too, and proceed to the
   next task WITHOUT asking.
4. ⛔ markers are hard stops. `⛔ HUMAN` = state exactly what you need
   from the human, then end your turn. `⛔ GATE` = produce the gate
   report specified, then end your turn. NEVER work past a ⛔, even if
   you are confident what the human will decide.
5. If a task fails or reveals necessary new work: add indented
   sub-tasks directly beneath it. Never delete, reorder, or reword
   existing tasks. Never add tasks that expand scope beyond the spec —
   propose those in the Deviation Log instead and keep moving.
6. Every figure you write into a report must come from output produced
   in this repo. No recalled numbers, no estimates presented as
   measurements. (§80, §95)
7. If context is running long: finish the current task, commit, then
   tell the human to /clear. State survives in this file.
8. Log every surprise, correction, or judgement call in the Deviation
   Log at the bottom, one line each, dated.

---

## PHASE 1 · STAGE 1.0 — FEASIBILITY (close-out)

- [x] 2026-08-22 **1.0-R Recovery sweep.** Check git log and working tree for
      anything half-finished from the dropped session. Grep the
      feasibility report for the stale 12.3% figure and the ~410
      ceiling; correct every dependent number to the strict 11.4% /
      ~380 measurement.
      Done when: no stale figures remain anywhere in reports/ and the
      tree is clean.

- [x] 2026-08-22 **1.0-T2a Walmart.** Locate the real terms of use — not an
      interstitial (apply the Ulta lesson). Quote verbatim the clauses
      governing automated access and data extraction. Check robots.txt
      separately; record that robots ≠ permission. Verdict: permitted /
      prohibited / ambiguous, with evidence.
      Done when: the report contains quoted clauses and a verdict.

- [x] 2026-08-22 SKIPPED — not permitted (see T2a). **1.0-T2b Walmart test (only if permitted).** 20 drugstore
      products from the §11 brand list. Measure quantity coverage on
      spec tables. Store raw responses under data/raw/feasibility/
      with provenance.
      Done when: measured coverage % is in the report.

- [x] 2026-08-22 Both steps: terms prohibit; test not run. **1.0-T2c Target.** Same discipline as Walmart, both steps.
      Done when: same standard.

- [x] 2026-08-22 **1.0-T3a OBF preparation.** Decide export flavour (JSONL /
      Parquet / CSV) with reasons. Specify fields to measure — raw
      text quantity AND any pre-parsed numeric quantity. Define how
      US makeup is identified inside a global cosmetics database
      (countries tags, categories taxonomy — state the method and its
      weaknesses). Write the DuckDB queries NOW, including a
      dual-flavour row-count integrity check: if two flavours disagree
      materially, the export is broken and no fill-rate conclusion is
      valid. (Known risk: OBF dumps have shipped incomplete before.)
      Done when: queries exist in sql/ or notebooks/01, untested but
      complete, and the report states what the human must download.

- [x] 2026-08-26 Delivered as beauty.parquet + en.openbeautyfacts.org.products.csv (moved into data/raw/obf/, names kept); site total not supplied — the publisher's advertised row count for the same Parquet was used instead. **HUMAN — download OBF exports.** Two flavours as specified by
      1.0-T3a, placed in data/raw/obf/. Also read the advertised
      product total from world.openbeautyfacts.org (a browser is not
      blocked; automated fetching is) and provide it as corroboration.

- [x] 2026-08-26 **1.0-T3b OBF measurement.** Run the integrity check first. If it
      passes, measure US-makeup fill rate for quantity, price
      (expected absent), brand, category, barcode. Report honestly —
      OBF has no price data, so its role is quantity + barcode joins,
      and the report must say so.
      Done when: measured fill rates are in the report with the
      integrity check result stated first.
      - [x] 2026-08-26 Integrity did not PASS: WARN. CSV flavour is a
            2026-05-07 snapshot; Parquet current and byte-identical to
            the publisher's advertised file. Diagnosed, gate extended,
            stated first in the report.
      - [x] 2026-08-26 Makeup filter corrected after the first run
            (taxonomy uses family tags and capitalised free-text tags).
      - [x] 2026-08-26 Result: rate usable (62.5% drugstore, parsed with
            unit), volume not — 57 US makeup rows, 16 drugstore, 10 with
            quantity. Outcome 3.

- [x] 2026-08-26 Key present in .env (validated against the account endpoint: free plan, 250 searches unused). **HUMAN — SerpApi key.** Add SERPAPI_KEY to .env, or say
      "skip SerpApi" explicitly.

- [x] 2026-08-26 **1.0-T4 SerpApi test (only if key present).** 20 drugstore
      products; measure whether Google Shopping titles carry inline
      size. Free tier only. Hard stop at the limit.
      Done when: measured coverage is in the report, or the skip is
      recorded.
      - [x] 2026-08-26 First run crashed: one call hung ~54 min past
            its socket timeout. Probe rebuilt with a wall-clock cap per
            call, a run cap, no retries, resume from saved responses;
            resumed run completed. 20 searches spent in total.
      - [x] 2026-08-26 Result: 12/20 products with at least one sized
            listing title; 27/530 titles (5.1%); figures conflict
            across listings. A hint source, not a quantity source.

- [x] 2026-08-26 **1.0-T5 Decision memo.** Revised ceiling: products with verified
      quantity, and how many are drugstore. The three paths — (a)
      narrow to prestige-only, (b) hybrid with manual capture filling
      the drugstore gap, (c) reframe around the disclosure asymmetry —
      each with tradeoffs against §9, §10, §98. Do NOT choose.
      Done when: the memo is the final section of the feasibility
      report and Stage 1.0's gate checklist in ROADMAP.md is satisfied.

- [ ] ⛔ **GATE 1.0 — human chooses the branch.** Present the memo in
      ≤ 30 lines. Wait.

- [ ] **1.0-G Post-gate rewrite.** Rewrite the Stage 1.1 section below
      to match the chosen branch: concrete sources, concrete targets,
      concrete ingestion tasks. Update docs/DEVELOPMENT.md if conventions change.
      Done when: Stage 1.1 below contains no BRANCH-DEPENDENT markers.

---

## PHASE 1 · STAGE 1.1 — ACQUISITION
*(BRANCH-DEPENDENT — rewritten at task 1.0-G. Invariants below stand
regardless of branch.)*

- [ ] **1.1-a Tier mapping.** brand_tier_mapping.csv per §12 for every
      brand that survived feasibility: brand, market_tier,
      classification_basis, source_or_reason, reviewed_date. Ambiguous
      cases documented. Tier never derived from price.
- [ ] **1.1-b Ingestion pipeline** for the chosen sources →
      data/raw/, immutable, 100% provenance (§24-25).
- [ ] **1.1-c BRANCH-DEPENDENT: drugstore quantity route** (retailer
      spec tables / OBF barcode joins / manual capture template with
      photo provenance — per gate decision).
- [ ] **1.1-d Collection audit** (notebook 02): counts by tier, brand,
      category; missing fields; duplicates. Honest coverage vs §88.
- [ ] ⛔ **GATE 1.1** — targets per the branch (default §9: 600+
      products, 10+ categories, 30+ brands) or the gate report states
      exactly why not and what that costs.

---

## PHASE 1 · STAGE 1.2 — CLEANING · UNITS · ENTITY RESOLUTION

- [ ] **1.2-a Quantity parser** (§27-31): every format in §87,
      weight-oz ≠ fluid-oz, multipacks, dual-unit labels preferring
      the explicit metric value, never g↔mL. Shopify variant `grams`
      remains a forbidden source (unit_rules.yaml).
- [ ] **1.2-b tests/test_units.py** — every §87 format plus the traps
      discovered in 1.0 (hash-fragment false positives, shipping
      weight). Done when: pytest green.
- [ ] **1.2-c Entity resolution** (§22-23) with match_confidence and
      thresholds; uncertain matches stored, not merged.
- [ ] **1.2-d Data quality flags** (§32) — nothing silently dropped.
- [ ] **1.2-e DuckDB schema + load** (§21).
- [ ] ⛔ **HUMAN — manual audit (§34).** 50 random products verified
      by the human against source pages. A script prepares the
      sample sheet; the human fills it.
- [ ] **1.2-f Audit reconciliation.** Done when: ~95% critical-field
      accuracy or the gap is diagnosed and fixed.
- [ ] ⛔ **GATE 1.2** — tests green from clean environment, audit
      passed.

---

## PHASE 1 · STAGE 1.3 — CORE UNIT ECONOMICS

- [ ] **1.3-a Pre-register hypotheses.** docs/hypotheses.md: expected
      direction for each §6 question the branch can answer. Committed
      BEFORE any metric is computed — the git timestamp is the point.
- [ ] **1.3-b Metrics** (§35-40): price_per_standard_unit, category
      unit index, premium %, quantity index, Bayesian weighted rating.
- [ ] **1.3-c SQL views** (§67) behind each headline figure.
- [ ] **1.3-d Drugstore vs prestige comparison** — or the branch's
      version of it.
- [ ] ⛔ **GATE 1.3 / PHASE 1 COMPLETE** — the central question (§98)
      has a defensible number, or the reframed question does.

---

## PHASE 2 — ANALYSIS & FINDINGS
*(Coarse by design. First task on arrival: expand into atomic tasks
with done-conditions, as above.)*

- [ ] Expand this phase into atomic tasks.
- [ ] Distributions first; tests with effect sizes + CIs (§48);
      regression (§49); Illusion Index + classifications (§43-44);
      Mini Tax on matched variants only (§45); price vs rating (§50);
      brand analysis with minimum-n (§51); showdowns (§47).
- [ ] Score results against docs/hypotheses.md — hits AND misses.
- [ ] ⛔ **GATE 2** — 5-8 findings in reports/final_insights.md, each
      traceable to a run calculation.

## PHASE 3 — DUPE INTELLIGENCE

- [ ] Expand this phase into atomic tasks.
- [ ] Candidate filtering → embeddings → benchmark (30-50 anchors,
      P@3/P@5, failure cases) → True-Value layer (§53-63).
- [ ] tests/test_dupe_logic.py: similarity unchanged under price
      perturbation (§54).
- [ ] ⛔ **GATE 3** — benchmark numbers + documented failures.

## PHASE 4 — PRODUCT & DELIVERY

- [ ] Expand this phase into atomic tasks.
- [ ] Streamlit (8 pages, no placeholders) · README from
      docs/README_TEMPLATE.md — `Select-String README.md -Pattern
      "\{\{"` must return nothing · verification suite: every README
      figure re-checked by script; app and notebooks import identical
      metric functions from src/, asserted by identity · methodology,
      data dictionary, limitations.
- [ ] ⛔ **HUMAN — deploy.** Streamlit Community Cloud account; deploy;
      link in README.
- [ ] ⛔ **GATE 4 / FINISH LINE** — see below.

---

## FINISH LINE

The project is done when (1) §93 works: a stranger names a product and
gets a quantified, classified, evidence-based answer; (2) §92's
acceptance checklist passes line by line; (3) a clean clone rebuilds
everything with the documented commands; and (4) the human can answer
§98 aloud in two sentences using figures from this repo.

## DEVIATION LOG
*(one line each, dated, newest first)*

- 2026-08-26 · SerpApi probe: the first run's 7th call was charged but
  hung ~54 min before its nominal 60 s read timeout fired and the script
  crashed uncaught; the owner asked for it to be stopped. Rebuilt with a
  90 s wall-clock bound per call (thread join, independent of the
  socket), an 8-minute run cap, zero retries, transport errors skipped,
  and resume from saved responses. Re-run once, deliberately, as the
  owner allowed; it completed with no abandoned calls. 20 searches
  spent, 230 of 250 remain.
- 2026-08-26 · SerpApi probe selection rule tightened twice before the
  first request (product_type appended only when the title names no
  type; exclusions applied to product_type; duplicate queries skipped)
  — all before any search was spent, so the rule stands as pre-registered.

- 2026-08-26 · OBF makeup filter corrected after the first real run:
  the taxonomy uses `en:makeup` and family tags plus capitalised
  free-text tags, which a case-sensitive prefix filter missed (15 → 24
  strict US rows, 57 broad). Changed before any conclusion was written.
- 2026-08-26 · Runner halts only on FAIL now; WARN prints and continues.
- 2026-08-26 · Site product total not supplied and no browser route was
  available; the Hugging Face datasets-server row count for the same
  Parquet file (73,747, byte size matching) was used as the external
  total. Stronger than a site figure, but not the corroboration the
  task named. Recorded in data/raw/obf/PROVENANCE.md.
- 2026-08-26 · Dual-flavour integrity check FAILed on row count (12.9%)
  as designed. Cause diagnosed as snapshot age — the published CSV
  export is a 2026-05-07 snapshot, both files downloaded the same day —
  not truncation. Gate extended with a WARN path that requires a ≥ 30-day
  staleness gap AND external corroboration of the Parquet; anything
  else still halts.
- 2026-08-26 · Exports arrived in data/raw/ under their published names;
  moved to data/raw/obf/ unchanged, names kept for provenance.

- 2026-08-22 · Repo hygiene pass at owner's request: conventions
  consolidated into docs/DEVELOPMENT.md, local editor state untracked,
  tooling-specific wording removed from this plan, the report and config.
  PROTOCOL 5 (never reword tasks) overridden by direct instruction for
  those phrases only.

- 2026-08-22 · T3a exceeded its "untested but complete" bar: the OBF
  query was self-tested on a synthetic Parquet+CSV pair and the
  integrity gate proven to halt on a truncated file (exit 3).
- 2026-08-22 · T2b/T2c tests not run: Walmart and Target both
  prohibited on terms, so the "only if permitted" condition failed.
- 2026-08-22 · Plan tasks 1.0-R through T3a were already done before
  the plan existed; each was re-verified by running its Done-when
  check before being ticked, per PROTOCOL 2.

- 2026-08-22 · Stale figure corrected: 12.3% → 11.4% strict
  quantity coverage; ceiling ~410 → ~380.
- 2026-08-22 · Ulta terms found at /company/terms-and-conditions;
  first URL served an interstitial that was wrongly accepted.