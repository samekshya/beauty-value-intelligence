# Shelf capture protocol — net quantity from packaging in hand

**Stage:** Phase 1 · Stage 1.1 — task 1.1-B4
**Written:** 2026-08-27, before any pack was read, after the OCR go/no-go
(`reports/ocr_feasibility_report.md`: 8 of 30 read, ceiling 11 of 30,
decision: manual).
**Authority:** `docs/methodology.md` rules 1–4; spec §4 (neutrality),
§25 (provenance), §89 (reproducibility).

The capture supplies **net quantity and unit only**, read off packaging
held in hand, for the 250 products fixed in advance by
`docs/capture_list.md`. Price comes from the US storefront snapshot and
from nowhere else. A stranger cannot repeat the shop visit; they must be
able to re-audit it — every value on the sheet must trace to a photograph,
a date and a shop.

## Files

| File | What it is |
| --- | --- |
| `data/raw/capture/shelf_capture_template.csv` | 250 rows, one per registered product, in capture order. Built by `python src/ingest/build_capture_template.py` from committed files; re-running reproduces it byte for byte. Identity columns pre-filled, capture columns blank. |
| `data/raw/capture/_shelf_capture_template_summary.json` | counts per tier, brand and category, and the priority rule with its source figures |
| `data/raw/capture/shelf_capture_log.csv` | **the filled sheet** — a copy of the template with the capture columns filled in the shop. Committed after every trip. The template itself is never edited. |
| `data/raw/capture/photos/` | photographs, named as below. Gitignored (bulky, personal-device originals); a sha256 manifest of every file is committed at 1.1-B7. |

There is no price column on any of these and there will not be one
(methodology rule 1).

## Before going out

1. Copy `shelf_capture_template.csv` to `shelf_capture_log.csv` (once;
   later trips fill the same log).
2. Load the log on the phone or print it. Rows are already in
   `capture_order`.
3. Camera: highest resolution, HDR and filters off, flash off unless the
   shop is dark. Photos stay as the device writes them — no editing, no
   re-encoding, no cropping.
4. Decide one short label per shop (`shop` column) and use it
   consistently.

## Priority rule — which products first

Fixed here so that partial capture in a shop that does not stock
everything cannot be steered by what the packs say.

A drugstore quantity is only useful for the tier contrast (spec §98) if
the same category has a prestige comparator whose quantity is already
known. The comparator count per category is measured in
`data/raw/feasibility/_category_breakdown.json` (MAC and Tom Ford Beauty
plus every other non-drugstore brand, structured-slot rule). From it:

| Tier | Rule | Categories | Products on the list |
| --- | --- | --- | ---: |
| **1** | comparator with quantity ≥ 5 | lipstick, lip gloss, eyeshadow singles, brow, bronzer, liquid lipstick, powder blush, foundation | 118 |
| **2** | comparator with quantity 1–4 | highlighter, concealer, mascara, eyeshadow palettes, setting spray, primer, lip liner, setting powder, pressed powder, cream blush | 127 |
| **3** | comparator with quantity 0 | liquid blush | 5 |

Within a tier the five brands are interleaved by `brand_rank` — the seeded
draw order inside each brand — so a visit cut short at any point has
covered the brands about equally. (`list_rank` is brand-blocked and would
have put all of ColourPop first.) The sheet's `capture_order` column is
exactly this.

In the shop:

- Work down `capture_order`. For each row, look for the product; capture
  it if stocked; mark `not_stocked` if not.
- **Capture every product the shop stocks.** Never skip a stocked product
  because of what its pack says, how it looks, or how long it takes.
- If time runs out, stop and record the last `capture_order` reached in
  the plan's deviation log. Rows after it stay blank. Coverage is
  reported as achieved, never padded.
- Products not on the list are not captured, whatever they are.
- Finishing tier 1 in a shop matters more than starting tier 2 there;
  finishing a brand does not matter — brands are already balanced in
  the draw.

## Per product — what to read, what to write

Everything is copied **verbatim from the pack**: same digits, same
punctuation, same units, same order. Nothing is converted, rounded,
corrected or completed from memory. If it is not printed, the cell stays
blank.

| Column | Write |
| --- | --- |
| `capture_status` | `captured` · `not_stocked` · `stocked_not_captured` (say why in `notes`) |
| `capture_date` | `YYYY-MM-DD` |
| `shop` | the shop label |
| `captured_by` | initials |
| `product_name_as_printed` | the name on the principal panel |
| `shade_as_printed` | shade name and number as printed; blank if none |
| `item_number_as_printed` | the manufacturer's item or SKU code printed on the pack (e.g. Wet n Wild `1115501`, Physicians Formula `PF10575`, essence `9618690001`). Verbatim, even if it differs from the pre-filled `storefront_sku` — the difference is information. |
| `barcode_digits` | every digit printed under the bars, no spaces. If the item and its carton carry different barcodes, record the one on the piece that carries the net-contents line and put the other in `notes`. |
| `barcode_source` | `printed_on_pack` — part of the manufacturer's artwork · `importer_sticker` — a label added by the importer or shop (Nepali importers add their own stickers; a sticker barcode is **not** the manufacturer's GTIN; record it anyway and say so) · `none` |
| `sold_with_carton` | `Y` / `N` |
| `net_contents_as_printed` | the whole net-contents line, verbatim, every unit shown: `NET WT. 7.65g (0.27oz)`, `4.7g/Net Wt. 0.16 oz.`, `2 x 4 g`, `10 g ℮`. If the pack prints different values in different places, write all of them separated by ` \|\| ` and explain in `notes`. Never pick one. |
| `net_contents_location` | `front` · `back` · `base` · `carton` · `blister` · `none_visible` |
| `pack_count` | number of units if a multipack or a set prints a count or an `x`; for palettes, the pan count if printed. Blank otherwise. |
| `form_as_seen` | `powder` · `cream` · `liquid` · `gel` · `pencil` · `pomade` · `stick` · `other`. **Required** for highlighter, brow and cream blush (their unit depends on form); welcome for every row. |
| `origin_line_as_printed` | the "Made in …" / "Distributed by …" line — it identifies the regional variant of the pack |
| `photo_front`, `photo_net_contents`, `photo_barcode` | filenames — all three required for a captured product |
| `photo_other` | further filenames, pipe-separated |
| `ocr_candidate_confirmed` | only for rows with a pre-filled `ocr_candidate`: `Y` if the printed line matches it exactly, `N` if not. The candidate is never copied into `net_contents_as_printed`; what the pack says is what goes there, in both cases. Blank if not captured. |
| `notes` | anything a stranger would need to understand the row |

The pre-filled `storefront_sku` and `ocr_candidate` columns are there to
be checked against, never copied from.

## Photographs

Three per captured product, named from the row's `photo_stem`:

| File | Frame |
| --- | --- |
| `<photo_stem>_front.jpg` | the principal panel in one frame: brand, product name, shade — identity |
| `<photo_stem>_net.jpg` | the net-contents line filling the frame, legible at full size |
| `<photo_stem>_barcode.jpg` | bars and the printed digits, legible |
| `<photo_stem>_other1.jpg`, `_other2.jpg` … | optional: carton back, base, origin line, item number, a second barcode |

Rules:

- Straight-on, in focus, the whole line inside the frame. Glare on the
  net-contents line: tilt the pack, not the phone. Check each photo on
  the phone before the next product; retake rather than annotate.
- One frame may serve two columns if both elements are legible in it;
  list the same filename in both.
- If the product is sold loose and the component carries no
  net-contents line, still take `_front` and `_barcode`, set
  `net_contents_location` to `none_visible`, and photograph the base as
  `_other1` — the line is sometimes moulded there.
- No people in frame. No editing. No re-naming other than to the pattern
  above.
- Do not include the shelf price tag in any frame referenced from the
  sheet. If shelf prices are wanted for the §96 extension (Nepal import
  premium), that is a separate capture with its own folder, never linked
  from this sheet.

## After each trip

1. Copy the photos, unmodified, into `data/raw/capture/photos/`.
2. Fill in the filenames; check every `captured` row has three.
3. Commit `shelf_capture_log.csv`:
   `data: shelf capture <date>, <shop>, <n> products`.
4. One line in the plan's deviation log: date, shop, rows reached,
   anything odd.

What happens next is not part of the capture: 1.1-B5 checks each row's
barcode against the US listing's JSON-LD `gtin12` (ColourPop, essence,
Milani expose one; Wet n Wild and Physicians Formula do not — those rows
fall back to item number and normalised name and are flagged
`identity_unverified`), and 1.1-B7 joins verified quantities to the
storefront spine.

## How a stranger re-audits this

Take any `captured` row. Open its three photographs. Check that the name,
the barcode digits and the net-contents text on the sheet are what the
photographs show, and that the date and shop are recorded. Then check the
barcode against the US listing as 1.1-B5 did. Nothing on the sheet should
need the person who was in the shop.
