# Methodology rules

Rules that shape every number in this project. Each exists because a
measured failure mode made it necessary; the date says when. Spec
authority: §4 (neutrality), §19 (list price), §25 (provenance), §32
(flags, never drops), §96 (cross-market pricing is future work).

## 1. Quantity and price come from different places, by design

*Adopted 2026-08-26 at Gate 1.0.*

Physical capture — reading a package in hand, whether a person with a
camera or OCR on a storefront product image — supplies **net quantity
and unit only**. Price always comes from the **US storefront snapshot**
for the same SKU, at the snapshot's `collected_at`.

Why: the capture happens where the product can be held, which for this
project is Nepal. Nepal shelf prices carry an import premium that §96
treats as a separate, future question ("Nepal import premium"). A Nepal
price inside a US unit-price figure would corrupt every downstream
comparison, and the error would be invisible — the number looks
plausible.

Consequences:

- No capture template, form, sheet or table has a price field.
- A captured quantity with no matching US snapshot price has no unit
  price. The row is kept and flagged `no_us_price`; it is not filled
  from any other source.
- A quantity read from a package sold in another market is the
  quantity *of that package*. It is attached to the US SKU only after
  rule 2 verifies the two are the same SKU.

## 2. SKU identity is verified by barcode, or flagged

The captured package and the US listing must be the same SKU — same
product, same net content. Verification is by barcode: the GTIN read
from the package against the GTIN the US listing exposes.

What the US listings expose, measured on the pages saved in Stage 1.0:

| Where | Barcode present |
| --- | --- |
| Shopify catalogue endpoint (`products.json`) | never — no barcode field |
| Product-page JSON-LD `gtin12` | ColourPop, essence, Milani: yes · Wet n Wild, Physicians Formula: no |
| Open Beauty Facts | every row, but only 10 US-tagged drugstore makeup rows exist |

Rules:

- A match is **verified** only when a package GTIN equals a listing
  GTIN (leading-zero normalised).
- Where the listing exposes no barcode, the match is by brand and
  normalised product name and is flagged `identity_unverified`. The row
  is kept, reported, and excluded from headline figures until verified.
  Never assume a match.
- A verified barcode match with a *different* net content from the US
  page is recorded as a cross-market packaging difference, with both
  values. It is a finding, not an error to correct.

## 3. Pre-registration before reading (§4)

The list of products whose quantity will be captured is fixed,
committed and timestamped before any size is read. Selection is by a
seeded, deterministic rule written in code and re-runnable. If the list
must change, the change is committed with its reason; the original stays
in history. The OCR test sample is drawn from the same pre-registered
list so that the test cannot steer the selection.

## 4. Provenance on every captured value (§25)

Each captured quantity carries: source (image URL or photo file), method
(`ocr` or `manual`), `collected_at`, who or what read it, the raw token
as read, and the verification status from rule 2. OCR readings are
`ocr_unverified` until the §34 audit confirms them.

## 5. Standing rules, restated

From `config/unit_rules.yaml`, `config/categories.yaml` and
`docs/DEVELOPMENT.md`: tier never from price; never g↔mL; weight oz and
fluid oz stay distinct; multipacks resolve to a count and a total;
Shopify `variants[].grams` is shipping weight and forbidden as quantity;
nothing is silently dropped — flag it.
