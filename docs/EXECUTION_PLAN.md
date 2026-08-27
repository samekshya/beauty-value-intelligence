# EXECUTION PLAN — Beyond the Price Tag

Single source of progress truth. If the conversation and this file
disagree, this file wins.

Authority: docs/PROJECT_SPEC.md (§) · CLAUDE.md (rules, git,
attribution) · docs/ROADMAP.md (phase gates).

Branch chosen at Gate 1.0: **B + C** — reframe on the disclosure
asymmetry first (no new data), then hybrid manual quantity capture.
Path A rejected: 356 of 380 rows were two brands.

---

## HUMAN CHECKLIST — everything only you can do

```
[x] Download OBF exports
[x] SerpApi decision
[x] Gate 1.0 — branch choice (B+C)
[x] 1.1-B2  OCR go/no-go — after the measured hit rate lands
[ ] 1.1-B4  Shelf capture (ONLY if OCR fails) — 2 afternoons
[ ] 1.2-H   50-product manual audit (§34) — 2-3 hours, do not delegate
[ ] 3-H     Dupe benchmark labelling — 30-50 anchors, judged by you
[ ] 4-H     Streamlit Community Cloud account + deploy
[ ] 4-H2    Defence rehearsal — answer §98 aloud from your own figures
```

Everything not on this list runs without you.

---

## PROTOCOL

1. Session start: read CLAUDE.md, then this file. Find the FIRST
   unchecked `[ ]`. Announce it in one line. Begin.
2. A task is done only when its **Done when** is true AND you verified
   it by running something. Assertion is not verification.
3. On completion: commit and push per CLAUDE.md, tick the box with the
   date, commit this file, proceed to the next task WITHOUT asking.
4. ⛔ markers are hard stops. State what you need, end your turn. Never
   work past one, however confident you are of the answer.
5. Failure or newly-necessary work: add indented sub-tasks beneath.
   Never delete, reorder or reword existing tasks. Scope expansions go
   in the Deviation Log as proposals — keep moving.
6. Every figure written into any report must come from output produced
   in this repo. No recalled numbers. No estimates dressed as
   measurements. (§80, §95)
7. `CONDITIONAL:` tasks execute only if their stated condition holds.
   If it doesn't, tick with the reason. Never silently skip.
8. Context running long: finish current task, commit, tell the human
   to /clear. State survives here.
9. Log every surprise, correction and judgement call in the Deviation
   Log — one line, dated.

---

# PHASE 1 · DATA FOUNDATION

## Stage 1.0 — Feasibility ✔ COMPLETE

Sources graded · Sephora, Ulta, Walmart, Target excluded on quoted
terms · 3,333 products from 19 storefronts · quantity 11.4% strict,
0 of 1,098 drugstore · Shopify shipping-weight trap identified and
forbidden in unit_rules.yaml · OBF measured, adds ≤32 fuzzy candidates
· SerpApi: 12/20 candidate sizes on 5% of listings, conflicting —
hint only.

- [x] 1.0-R · T2a · T2b · T2c · T3a · T3b · T4 · T5 · Gate 1.0
- [x] 2026-08-26 **1.0-G Post-gate rewrite.** Update CLAUDE.md current-phase line
      to Stage 1.1. Confirm Stage 1.1 below matches the B+C branch.
      Done when: no BRANCH-DEPENDENT markers remain in Stage 1.1.
      - [x] 2026-08-26 Verified: the only BRANCH-DEPENDENT string left in
            this file is this task's own Done-when. CLAUDE.md has carried
            no current-phase line since the 2026-08-22 hygiene pass (it
            defers to this file), so there was nothing to update there.

---

## Stage 1.1 — C-TRACK · Disclosure asymmetry *(no new data)*

- [x] 2026-08-26 **1.1-C1 Tier and brand breakdown.** Quantity disclosure by
      tier across all 3,333. Then by brand within drugstore — confirm
      zero is uniform, not a few brands dragging an average. Then
      prestige excluding MAC and Tom Ford, to establish the 1.3%
      comparator honestly.
      Done when: a committed table shows n, n_with_quantity, pct per
      tier and per drugstore brand.
      - [x] 2026-08-26 Verified by re-run, byte-identical:
            `data/raw/feasibility/_tier_breakdown.json` carries by_tier and
            by_brand (n / with_quantity / coverage) and the non-drugstore
            figure excluding MAC and Tom Ford, 24 of 1,814 (1.3%). Tables
            are in reports/final_insights.md.

- [x] 2026-08-27 **1.1-C2 Category cut.** Same measurement by product category.
      Does disclosure vary by what the product is? Powders vs liquids
      is the interesting axis — liquids have volume printed for
      regulatory reasons more often than powders.
      Done when: committed table, and any pattern stated in one line.
      - [x] 2026-08-27 `_category_breakdown.json` + per-product
            `_category_assignments.csv`; tables and the one-line pattern in
            reports/final_insights.md. Drugstore 0 in all 19 categories;
            MAC + Tom Ford 85-100% in every category; other brands 3/211
            weight vs 2/218 volume. Powders-vs-liquids not supported.

- [x] 2026-08-27 **1.1-C3 Mechanism and limits.** Write the finding with its
      boundaries explicit: one channel (brand storefronts, not
      retailer listings), one market, no claim about intent, and the
      fact that prestige disclosure is also poor — 1.3% is not a
      flattering comparator, it is merely non-zero. State what a
      reader may and may not conclude.
      Done when: reports/final_insights.md contains finding #1 with
      figures traceable to 1.1-C1 and 1.1-C2 output.
      - [x] 2026-08-27 Finding 1 names its source file for every figure
            (C1 JSON, C2 JSON/CSV, PDP analysis); the "says / does not say"
            section bounds channel, market, intent and now product form.

- [x] 2026-08-27 **1.1-C4 Consumer-facing statement.** One paragraph, plain
      language: what this means for someone standing in a shop holding
      two products. This is the sentence that will open the README and
      the write-up.
      Done when: committed to reports/final_insights.md.
      - [x] 2026-08-27 "For a shopper, in one paragraph" under finding 1.
            README carries it at the next GATE refresh, per the README
            discipline rule.

---

## Stage 1.1 — B-TRACK · Quantity capture

- [x] 2026-08-26 **1.1-B1 Pre-register the capture list.** Fixed list of drugstore
      products to capture, chosen BEFORE any size is read, committed
      and git-timestamped. Selection rule stated (e.g. top-N by
      category coverage). This prevents choosing products whose sizes
      happen to support a conclusion. §4.
      Done when: docs/capture_list.md committed, with selection rule.
      - [x] 2026-08-26 CSVs registered by commit 07c7ca3 before any size
            was read (250 drawn, 50 per brand, 19 categories; 30-product
            OCR sample); re-run reproduces both CSVs byte for byte;
            docs/capture_list.md states the rule and the registering
            commit.

- [x] 2026-08-27 **1.1-B2 OCR feasibility test.** Product images from storefronts
      already crawled — permitted source, already collected. Packaging
      in product photos frequently prints net contents. Test OCR on 30
      drugstore products from the pre-registered list. Report measured
      hit rate and error modes. Do not proceed to manual capture
      before this number exists.
      Done when: measured hit rate committed to the report.
      - [x] 2026-08-27 8 of 30 (26.7%) under the pre-registered rule, 9 of
            30 (30.0%) under a labelled post-hoc amendment; 8 of 8 hits
            verified correct against their images; 19 of 22 misses have no
            size on the item photographed, so the ceiling with these images
            is 11 of 30 (36.7%), below the 40% threshold.
            reports/ocr_feasibility_report.md; outputs in data/raw/capture/
            (ocr/, _ocr_probe_summary.json, _ocr_probe_analysis.json,
            _ocr_probe_visual_audit.csv).

- [x] 2026-08-27 ⛔ **HUMAN — OCR go/no-go.** ~40%+ hit rate makes OCR the primary
      route and shop visits unnecessary. Below that, decide whether to
      proceed manually.
      - [x] 2026-08-27 Owner's decision: not viable — 8 of 30, ceiling 11 of
            30, 19 misses with no size in any image. Going manual. The 8
            verified OCR values are candidates to confirm against
            packaging, never data.

- [x] 2026-08-27 **1.1-B3 CONDITIONAL (OCR viable): OCR pipeline.** Extract at
      scale. Every extraction stores the source image URL and the
      cropped region. Confidence score per extraction. Low-confidence
      goes to human review, never auto-accepted.
      Done when: extraction complete for the pre-registered list, with
      per-item provenance and confidence.
      - [x] 2026-08-27 Condition not met: OCR judged not viable at the
            go/no-go. Not built.

- [ ] ⛔ **HUMAN — CONDITIONAL (OCR fails): shelf capture.** Photograph
      packaging + barcode for the pre-registered list. Kathmandu.
      Claude Code prepares the capture template first (see 1.1-B4).

- [x] 2026-08-27 **1.1-B4 CONDITIONAL: capture template.** CSV template plus
      instructions: barcode, net contents as printed, photo filename,
      capture date, shop. Designed so a stranger could re-audit the
      photos even if they cannot re-run the capture. §25, §89.
      Done when: template + instructions committed.
      - [x] 2026-08-27 data/raw/capture/shelf_capture_template.csv (250
            rows, fixed capture order, identity pre-filled, capture columns
            blank, no price field) built by
            src/ingest/build_capture_template.py from committed files,
            byte-identical on re-run; docs/shelf_capture_protocol.md holds
            the priority rule, the verbatim fields, the three photographs
            per product and the re-audit path.

- [ ] **1.1-B5 SKU identity verification.** Every captured quantity
      matched to its US listing by barcode. Unverifiable matches
      flagged `identity_unverified`, never assumed. Regional size
      differences are real and will otherwise corrupt the join.
      Done when: match rate reported; unverified items flagged.

- [x] 2026-08-26 **1.1-B6 Methodology rule — write before any join runs.**
      Physical capture supplies QUANTITY ONLY. Price always comes from
      the US snapshot. Nepal shelf prices carry an import premium that
      §96 treats as a separate research question; mixing them would
      silently corrupt every unit-price figure in the project.
      Done when: docs/methodology.md states this explicitly.
      - [x] 2026-08-26 docs/methodology.md rule 1, adopted at Gate 1.0
            before any capture: capture supplies quantity only, price from
            the US snapshot, no price field on any capture template.

- [ ] **1.1-B7 Merge and audit.** Captured quantities joined to the
      storefront spine. Collection audit (notebook 02): counts by
      tier, brand, category; duplicates; coverage vs §88 reported
      honestly, targets never moved.
      Done when: audit committed.

- [ ] ⛔ **GATE 1.1.** Report: total products with verified quantity,
      how many drugstore, coverage vs §9/§10, and whether §98 is now
      answerable. State plainly if it is not.

---

## Stage 1.2 — Cleaning · Units · Entity resolution

- [ ] **1.2-a Quantity parser.** Every format in §87. Weight-oz ≠
      fluid-oz. Multipacks → pack_count and total. Dual-unit labels
      prefer the explicit metric value. NEVER g↔mL. Shopify variant
      `grams` remains forbidden (unit_rules.yaml).
      Done when: parser handles every §87 case.

- [ ] **1.2-b tests/test_units.py.** Every §87 format, plus the traps
      found in 1.0: hash-fragment false positives (`029g`, `0MG`,
      `7G` from minified JS) and shipping weight masquerading as net
      contents. Known conversions asserted exactly.
      Done when: pytest green from a clean environment.

- [ ] **1.2-c Entity resolution.** §22 hierarchy, barcode first.
      match_confidence per pair. Thresholds: auto-merge / review /
      reject. Uncertain matches stored separately, never merged.
      Done when: tests/test_matching.py green on known same-product
      examples.

- [ ] **1.2-d Data quality flags.** §32 values on every row. Nothing
      silently dropped, ever.
      Done when: every row carries a flag; counts by flag reported.

- [ ] **1.2-e Validation rules.** §33: price > 0, quantity > 0, rating
      in scale, no incompatible mass/volume conversions, no accidental
      duplicates.
      Done when: tests/test_data_quality.py green.

- [ ] **1.2-f DuckDB build.** §21 schema. Offers separate from
      products — three retailers listing one product produce three
      rows, never an overwrite. §20.
      Done when: database rebuilds from processed data by one command.

- [ ] **1.2-g Audit sample sheet.** 50 random products, blank columns
      for the human to fill against source pages.
      Done when: committed and ready to hand over.

- [ ] ⛔ **HUMAN — 1.2-H manual audit (§34).** Verify 50 products by
      hand. Do not delegate this. It catches what no test can see.

- [ ] **1.2-h Reconciliation.** Diagnose every mismatch. Fix causes,
      not symptoms.
      Done when: ~95% critical-field accuracy, or the shortfall is
      diagnosed and its cost stated.

- [ ] ⛔ **GATE 1.2.** Tests green from clean environment, audit passed.

---

## Stage 1.3 — Core unit economics

- [ ] **1.3-a Pre-register hypotheses.** docs/hypotheses.md: expected
      direction for every §6 question this branch can answer.
      Committed BEFORE any metric is computed — the git timestamp is
      the entire point. §4.
      Done when: committed, and no metric code has run.

- [ ] **1.3-b Metrics.** §35-39: price_per_standard_unit, category unit
      price index, price_premium_pct, quantity_index.
      Done when: tests/test_features.py green on hand-worked examples.

- [ ] **1.3-c Bayesian weighted rating.** §40. Parameters documented
      and justified, not defaulted.
      Done when: formula and chosen m committed to methodology.

- [ ] **1.3-d SQL views.** §67 — one view behind each headline figure,
      so every number in the app traces to a query.
      Done when: sql/ contains views for category, brand, tier and
      hero-product retrieval.

- [ ] **1.3-e Tier comparison.** Drugstore vs prestige unit economics
      wherever disclosure permits. Sticker gap vs unit gap — the
      central contrast.
      Done when: the figure exists and is reproducible from SQL.

- [ ] ⛔ **GATE 1.3 · PHASE 1 COMPLETE.** §98 has a defensible number,
      or the reframed C-track question does. State which.

---

# PHASE 2 · ANALYSIS & FINDINGS

- [ ] **2-a Distributions first.** Inspect before testing. Normality,
      skew, outliers, sample sizes per cell. Choose tests from what
      you see, not from habit. §48.
      Done when: distribution notebook committed with test choices
      justified.

- [ ] **2-b Tier significance testing.** Mann-Whitney U / Welch /
      Kruskal-Wallis as the distributions dictate. ALWAYS report
      effect size and confidence interval alongside. A p-value alone
      is not a finding. Bootstrap CIs where parametric assumptions
      fail.
      Done when: every test reports statistic, effect size, CI and a
      one-line practical interpretation.

- [ ] **2-c Regression.** log(price_per_unit) ~ tier + category +
      log(quantity) + weighted_rating + log(review_count+1). §49.
      Interpretable, explanatory, not predictive. Report what premium
      survives controlling for category.
      Done when: model summary committed with diagnostics.

- [ ] **2-d Drugstore Illusion Index.** §43. sticker_ratio,
      unit_ratio, illusion_multiplier on matched comparable products.
      Done when: computed, with the worked example verified by hand.

- [ ] **2-e Value classifications.** §44: Genuine Bargain, Cheap Entry
      Price, False Economy, Luxury Value, Luxury Premium, Balanced.
      Thresholds transparent and data-informed, never chosen to
      produce a pleasing distribution.
      Done when: thresholds documented with their basis; counts per
      class reported.

- [ ] **2-f Mini Tax.** §45. MATCHED mini/full variants of the SAME
      product only. Median, mean, range, by brand, by category,
      distribution.
      Done when: computed, with n pairs stated. If n is small, say so
      loudly rather than reporting a median of six.

- [ ] **2-g Price vs rating.** §50. Spearman. State precisely what
      the correlation does and does not license you to claim. §83.
      Done when: computed with interpretation bounded.

- [ ] **2-h Brand value analysis.** §51. Minimum product count
      enforced — never rank a brand on two products.
      Done when: threshold stated; brands below it excluded and the
      exclusion visible.

- [ ] **2-i Category economics.** §52. Where is drugstore genuinely
      dominant, and where does the prestige premium shrink to nothing?
      Done when: per-category table committed.

- [ ] **2-j Cult product showdowns.** §47. Anchor vs alternatives:
      cheapest upfront, best quantity value, best reviewed value, best
      true value — these will often be different products, and that
      divergence is the point.
      Done when: showdowns for the strongest categories committed.

- [ ] **2-k Score against hypotheses.** Compare results to
      docs/hypotheses.md. Report hits AND misses with equal prominence.
      A wrong prediction honestly reported is worth more than a right
      one, because it proves the predictions were real.
      Done when: docs/hypotheses.md updated with outcomes.

- [ ] ⛔ **GATE 2.** 5-8 findings in reports/final_insights.md, each
      traceable to a calculation in this repo.

---

# PHASE 3 · DUPE INTELLIGENCE

- [ ] **3-a Candidate filtering.** §55 — BEFORE any similarity scoring.
      Same category, compatible form, compatible usage. Structurally
      different products never become candidates just because their
      marketing copy rhymes.
      Done when: filter implemented; candidate counts per anchor
      reported.

- [ ] **3-b Text similarity.** Sentence Transformer embeddings over
      name, description, claims, texture, finish, coverage. Cosine
      similarity. §56.
      Done when: embeddings built, deterministic seed set.

- [ ] **3-c CONDITIONAL (ingredients present): ingredient similarity.**
      Jaccard over ingredient sets. Never claim identical formulation
      from overlap alone. §56.
      Done when: implemented, or ticked with the reason data is absent.

- [ ] **3-d CONDITIONAL (shade data trustworthy): shade similarity.**
      Shade family, undertone, perceptual distance. §56.
      If data quality is insufficient: implement nothing, and ensure
      the phrase "exact dupe" appears NOWHERE in the repository —
      use "product-level alternative" throughout. §60.
      Done when: implemented, or the limitation is documented and the
      language audited repo-wide.

- [ ] **3-e Attribute similarity.** Finish, coverage, form, wear
      claims, waterproof, texture. §56.
      Done when: implemented.

- [ ] **3-f Category-specific weights.** §57. Shade matters for
      lipstick, is irrelevant for mascara. Start from the §57
      framework, adjust per category, document every final weight and
      its reason.
      Done when: config committed with per-category weights justified.

- [ ] **3-g tests/test_dupe_logic.py.** Price must not influence
      similarity. Assert similarity(a,b) is unchanged when b's price
      is perturbed. §54 — the project's single most important test.
      Done when: green.

- [ ] **3-h Benchmark set preparation.** 30-50 anchor products spanning
      categories and tiers, each with its filtered candidate list, laid
      out for human judgement.
      Done when: benchmark sheet committed and ready.

- [ ] ⛔ **HUMAN — 3-H benchmark labelling.** Judge each candidate:
      good dupe / plausible / wrong. This is the ground truth. Nobody
      else can supply it.

- [ ] **3-i Evaluation.** Precision@3, Precision@5, category
      correctness, form correctness. §59.
      Done when: metrics computed against human labels.

- [ ] **3-j Failure analysis.** Document what the model gets wrong and
      why. Failure cases are more persuasive than the successes —
      they prove you looked. §59.
      Done when: reports/dupe_failures.md committed.

- [ ] **3-k True-Value layer.** §61-62. Similarity dominates (~65%),
      then quantity-adjusted economics, then rating confidence. Test
      the weights rather than assuming them. Component scores exposed
      separately, never collapsed into one opaque number. §54.
      Done when: scoring implemented, components separable.

- [ ] **3-l Consumer decision outputs.** §63: Cheapest · Best Quantity
      Value · Best Reviewed Value · Best Dupe · Best True-Value Dupe.
      Kept distinct — they will often disagree.
      Done when: all five computed per anchor.

- [ ] ⛔ **GATE 3.** Benchmark numbers exist, failures documented,
      price-independence test green.

---

# PHASE 4 · DASHBOARD & DELIVERY

## The application (§69-77)

- [ ] **4-a App shell and design.** Reads precomputed artefacts, never
      the live database. Clean and deliberate — a beauty intelligence
      tool, not a homework dashboard. §69.
      Done when: shell runs, navigation works.

- [ ] **4-b Page 1 — Executive Overview.** §70. Real KPIs. Real
      headline findings. Zero placeholder conclusions.

- [ ] **4-c Page 2 — Category Economics.** §71. Filters: category,
      tier, brand, retailer. Distributions, medians, premiums,
      quantity-adjusted premiums.

- [ ] **4-d Page 3 — Drugstore Illusion.** §72. The value
      classifications, browsable.

- [ ] **4-e Page 4 — Mini Tax.** §73. Paired comparisons, by brand,
      by category, searchable.

- [ ] **4-f Page 5 — Cult Showdown.** §74. Anchor vs alternatives,
      full comparison.

- [ ] **4-g Page 6 — True-Value Dupe Finder.** §75. THE FLAGSHIP.
      Original product, then ranked alternatives showing similarity,
      checkout saving, unit saving, rating, true-value score,
      classification. The contrast between a False Economy and a
      Genuine Bargain at similar similarity is the entire point —
      make it visually unmissable.

- [ ] **4-h Page 7 — Brand Value Explorer.** §76.

- [ ] **4-i Page 8 — Methodology.** §77. Sources, exclusions with
      their clauses, unit conversions, rating adjustment, metric
      definitions, limitations. Transparency displayed as a feature,
      not buried.

- [ ] **4-j CONDITIONAL (C-track): Disclosure page.** The asymmetry
      finding deserves its own page if it survived as a headline.

## Verification and documentation

- [ ] **4-k Verification suite.** scripts/run_verifications.py: every
      figure in the README re-checked against repo output; data quality
      checks; full reproduction from raw; pytest. One command.
      Done when: it runs clean and prints per-stage counts.

- [ ] **4-l Identity assertion.** The app and the notebooks must import
      the SAME metric functions from src/, asserted by identity:
      `assert app.score is shared.score`. If anyone reimplements a
      metric inside the app, the test fails rather than silently
      diverging.
      Done when: green.

- [ ] **4-m0 Diagrams and screenshots.** diagrams/ containing:
      pipeline architecture (sources → raw → staging → processed →
      analytics → DuckDB → app), data model showing the products /
      offers / variants / sizes separation, and one screenshot per
      dashboard page. README_TEMPLATE.md references these; without
      them the README reads as a wall of text.
      Done when: every image referenced by README_TEMPLATE.md exists
      in diagrams/ and renders.

- [ ] **4-m README.** Built from docs/README_TEMPLATE.md. Before
      commit: `Select-String -Path README.md -Pattern "\{\{"` must
      return nothing. Every figure from measured output.
      Done when: grep clean, all figures traceable.

- [ ] **4-n Documentation set.** docs/methodology.md,
      docs/data_dictionary.md, docs/limitations.md. The limitations
      document should be the one you are proudest of.

- [ ] **4-o Reproducibility check.** Clone to a fresh directory,
      follow the README exactly, rebuild everything. Any hidden manual
      step is a bug. §89.
      Done when: a clean clone rebuilds and runs.

- [ ] **4-p Acceptance checklist.** Walk §92 line by line. Every box
      ticked or explicitly waived with a reason.

- [ ] ⛔ **HUMAN — 4-H deploy.** Streamlit Community Cloud account,
      deploy, link into the README.

- [ ] **4-q Write-up.** A short readable piece on the strongest
      finding, linked from the README. Recruiters click links; almost
      none clone repos.

- [ ] **4-r CONDITIONAL: contribute captured data back to Open Beauty
      Facts.** If shelf or OCR capture produced verified quantities,
      contribute them under ODbL. The project consumed open data and
      returned open data.

- [ ] ⛔ **HUMAN — 4-H2 defence rehearsal.** Answer §98 aloud in two
      sentences from your own figures, without notes. Then answer:
      why Bayesian rating adjustment? Why is price excluded from
      similarity? How does the parser handle `0.05 oz / 1.4 g`? What
      is the weakest claim in the project? If any answer needs
      looking up, that part is not yet yours.

- [ ] ⛔ **GATE 4 · FINISH.**

---

# PHASE 5 · EXTENSIONS *(only if Phase 4 is excellent)*

- [ ] Nepal import premium (§96) — the strongest of these. Does a
      drugstore product remain a drugstore product after import
      pricing? Nobody has answered this.
- [ ] Historical price comparison against the Sephora dataset (§17).
- [ ] Review NLP — do similar products draw similar complaints?
- [ ] Second price snapshot. One collection is a photograph; two are
      a measurement.

---

# FINISH LINE

Done when all four hold:

1. **§93 works.** A stranger names a product and receives a
   quantified, classified, evidence-based answer.
2. **§92 passes**, line by line.
3. **A clean clone rebuilds everything** with the documented commands.
4. **You can answer §98 aloud in two sentences** using figures from
   this repo, and defend every one of them.

---

# DEVIATION LOG *(newest first, one line, dated)*

- 2026-08-27 · 1.1-B4 judgement call: a priority order for partial
  capture was fixed before any pack is read — tier by the prestige
  comparator's measured disclosure in the same category
  (`_category_breakdown.json`: ≥5 → tier 1, 118 products; 1–4 → tier 2,
  127; 0 → tier 3, 5), brands interleaved by `brand_rank` within tier so
  a cut-short visit stays brand-balanced (`list_rank` is brand-blocked).
  Category-level and product-blind, so it cannot select on quantity. A
  proposal the owner can overrule before the first trip.
- 2026-08-27 · 1.1-B4: the storefront catalogue has no barcode field but a
  variant `sku` for 250 of 250 registered products; the pack's printed
  item number is captured as a second identity key for 1.1-B5 beside the
  barcode. ColourPop's SKUs are descriptive codes
  (`SoJuicyStick-DinnerDate`), unlikely to be printed on a pack.
- 2026-08-27 · 1.1-B4: nine OCR candidates pre-filled, not eight — the
  ninth is product 1's value read under the post-hoc rule and verified by
  eye; labelled `amended` on the sheet.
- 2026-08-27 · 1.1-B4: photographs are gitignored
  (`data/raw/capture/photos/`); a sha256 manifest is committed at 1.1-B7
  so the archive is verifiable without the files.
- 2026-08-27 · Go/no-go decided by the owner: OCR not viable (8 of 30,
  ceiling 11 of 30, 19 misses with no size in any image). Manual route;
  1.1-B3 ticked as condition not met.
- 2026-08-27 · 1.1-B2: `_ocr_probe_analysis.json` on disk had been written
  when 15 of 30 products had output (3 of 15); the probe itself had
  finished all 30. Re-run on all 30 before any figure was cited.
- 2026-08-27 · 1.1-B2 judgement call: the "amended" normalisation (space
  after a glued NET WT label, O-for-0 before a decimal) was written after
  reading the outputs. Post hoc — reported second and labelled, never as
  the headline.
- 2026-08-27 · 1.1-B2: misses classified by eye from the images (36
  inspected) and recorded per product in `_ocr_probe_visual_audit.csv`. A
  manual step — re-auditable from the image URLs in `ocr/*.json`, not
  re-runnable.
- 2026-08-27 · 1.1-B2 surprise: three of 30 category guesses are wrong
  (19 and 25 are palettes guessed eyeshadow_single; 20 is an eyeliner
  guessed primer, outside §7). Keyword rule; flagged for the 1.2-H audit;
  the registered list is not changed.
- 2026-08-27 · 1.1-B2: the report is a new file,
  `reports/ocr_feasibility_report.md`, not a section of the Stage 1.0
  source feasibility report, whose status line declares its measurements
  complete.
- 2026-08-27 · 1.1-C2 surprise: of the 24 non-drugstore disclosures
  outside MAC and Tom Ford, only 5 are §7 makeup products; 19 are perfume,
  skincare and face mists. On makeup the comparator is 5 of 503 (1.0%).
- 2026-08-27 · 1.1-C2 judgement call: the capture list's exclusion word
  list, reused unchanged for comparability, also catches makeup (lash,
  cream, oil, duo - 87 drugstore products on those words alone). Kept for
  this cut because every drugstore bucket is zero regardless; the list
  must not be reused as a makeup filter in Stage 1.2.
- 2026-08-26 · Plan replaced wholesale by the owner with the fully
  expanded version. Tasks already done under the old numbering (1.0-G,
  1.1-C1, 1.1-B0 now B6, 1.1-B1) were re-verified by running their
  Done-when checks and re-ticked with their original dates; the
  pre-replacement deviation log (14 entries) is preserved at git
  `0798cab:docs/EXECUTION_PLAN.md`.
- 2026-08-26 · Carried forward from that log, still open: seven prestige
  brands at 0% storefront disclosure (942 products) would need the same
  capture route as drugstore for a like-for-like §98 comparison; the
  B-track names drugstore only. Raise at Gate 1.1.
- 2026-08-26 · 1.1-B2 OCR probe found still running from the previous
  session (25-min cap, 9 of 30 products done when this session began);
  left to finish, then resumed from disk rather than restarted. C-track
  tasks were worked while it ran and are ticked in plan order.
- 2026-08-22 · Gate 1.0 decision: B+C, C first. Path A rejected —
  356 of 380 rows were two brands.
- 2026-08-22 · OBF site count unread (extension not connected);
  publisher dataset API count substituted, logged as such.
- 2026-08-22 · CSV/Parquet row gap resolved: stale snapshot, not
  truncation. Confirmed against Hugging Face datasets-server.
  Integrity check downgraded to WARN only when staleness AND external
  corroboration both hold.
- 2026-08-22 · SerpApi probe hung on sequential calls; result
  recorded as hint-quality only.
- 2026-08-22 · Walmart and Target excluded on quoted terms.
- 2026-08-22 · Stale figure corrected: 12.3% → 11.4% strict;
  ceiling ~410 → ~380.
- 2026-08-22 · Ulta terms at /company/terms-and-conditions; first URL
  served an interstitial that was wrongly accepted.