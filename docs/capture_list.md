# Drugstore quantity-capture list — pre-registration

Registered by commit `07c7ca3` (2026-08-26), which committed the two CSVs
below before any product's size had been read by any method. The git
timestamp of that commit is the registration (spec §4; `docs/methodology.md`
rule 3). This page documents the rule; it does not change the list.

## Files

| File | Rows | Contents |
| --- | ---: | --- |
| `data/raw/capture/drugstore_capture_list.csv` | 250 | the products whose net quantity will be captured |
| `data/raw/capture/ocr_test_sample.csv` | 30 | the first six drawn per brand, interleaved — the 1.1-B2 OCR test sample |
| `data/raw/capture/_capture_list_summary.json` | — | counts at every step of the rule, per brand and per category |

Fields: `list_rank`, `brand_rank`, `brand`, `product_id`, `handle`, `title`,
`product_type`, `category_guess`, `category_basis`, `storefront_url`,
`image_count`, `image_urls`, `catalogue_file`, `catalogue_collected_at`.
Identity and provenance only — no quantity field, no price field
(methodology rule 1).

## Selection rule

Implemented in `src/ingest/preregister_capture_list.py`, seed `20260826`.
Re-running the script reproduces both CSVs byte for byte.

1. **Universe.** Every product in a drugstore catalogue whose Stage 1.0
   probe succeeded — ColourPop, essence, Milani, Physicians Formula,
   Wet n Wild — from `data/raw/feasibility/shopify_*.json`, collected
   2026-08-21 and capped at 250 per brand by the endpoint. **1,098
   products.**
2. **Exclusions.** Sets, kits, bundles, tools, brushes and non-makeup,
   by a fixed word list applied to title, handle and product_type.
   **331 excluded.**
3. **Category guess.** Ordered keyword rules on product_type and title,
   mapping to the §7 categories in `config/categories.yaml`; the rule
   that fired is recorded per row in `category_basis`. Products no rule
   matches, or that a rule marks out of scope (eyeliner is not a §7
   category), are not drawn. **136 out of scope; 631 eligible.**
4. **Stratified draw.** Per brand, up to 50 products taken round-robin
   across that brand's categories, with categories and products both in
   seeded-shuffled order, so no category dominates a brand's share.
   **250 drawn — 50 per brand, 19 categories.**
5. **OCR test sample.** The first six drawn per brand, interleaved brand
   by brand. **30 products.**

Per-brand and per-category counts of the eligible, drawn and sampled
products are in the summary JSON.

## What this prevents

The list fixes *which* products are measured before any measurement, so
captured quantities cannot be chosen — deliberately or not — to suit a
conclusion. If the list must change, the change is committed with its
reason and this page is updated; the original stays in history.
