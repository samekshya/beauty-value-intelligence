# OCR feasibility test — net quantity from storefront product images

**Project:** Beyond the Price Tag — Beauty Value Intelligence Engine
**Stage:** Phase 1 · Stage 1.1 — task 1.1-B2
**Measured:** probe run 2026-08-26 in bounded sessions (25-minute cap,
resumed from files on disk; final session 18:18–18:49 UTC per the summary);
analysis re-run and visual audit 2026-08-27.
**Decision this feeds:** the OCR go/no-go (⛔ after 1.1-B2). The plan's
threshold for OCR as the primary quantity route is about 40%.

Every figure below names the file it comes from. Nothing is recalled or
estimated.

| File | What it holds |
| --- | --- |
| `data/raw/capture/_ocr_probe_summary.json` | the run: engine, rule, per-product rows, hit rate |
| `data/raw/capture/_ocr_probe_analysis.json` | `src/ingest/ocr_size_probe_analyse.py` re-run on all 30: primary and amended rules, per-image blank / small / fragment counts |
| `data/raw/capture/_ocr_probe_visual_audit.csv` | every product classified by eye against its images: what is printed, what was read, why it missed |
| `data/raw/capture/ocr/*.json` | per product: every image's URL, size, recognised text per pass, hits |

The images themselves are gitignored (bulky, re-downloadable); each one's
source URL is in the per-product JSON, so a stranger can re-fetch and
re-audit.

---

## The question

Brand storefronts publish no net quantity for drugstore products (0 of
1,098 — `reports/final_insights.md`). Packaging prints it. The storefronts
photograph the packaging. Can OCR on those photographs — a permitted
source, already collected — supply the number?

## Method

- **Sample.** The 30-product OCR sample in
  `data/raw/capture/ocr_test_sample.csv`, six per brand (ColourPop,
  essence, Milani, Physicians Formula, Wet n Wild), registered by commit
  `07c7ca3` before any size was read (`docs/capture_list.md`).
- **Images.** Up to six per product from the image list in the storefront
  catalogue. 156 listed within that cap, 156 fetched and decoded.
- **Engine.** RapidOCR (`rapidocr-onnxruntime` 1.2.3), run on the full
  frame and on a 2×2 grid of overlapping tiles (15% overlap) for images
  with a long side of 900 px or more, so small print is not lost to the
  detector's downscaling.
- **Rule.** The same strict size rule as every coverage figure in this
  project (`feasibility_pdp_analyse.find_sizes`: a number, a unit in
  `g` / `mg` / `mL` / `ml` / `oz` / `fl oz`, a hard word boundary, and the
  plausibility bounds of `config/unit_rules.yaml`), applied after a narrow
  OCR normalisation fixed before the run: upper-case `OZ` / `FL OZ` / `ML`
  lowered, a capital `O` after a digit read as zero, comma decimals. This
  is the **primary** rule — the pre-registered number.
- **Amended rule, post hoc.** After the first outputs were read, two more
  normalisations were written: a space after a label glued to the number
  (`TOTALNETWT.26.5g`, `NETWT.7.65g`) and a capital `O` before a decimal
  point read as zero (`O.95oz`). It was written after seeing the data, so
  it is labelled post hoc and reported second.
- **Hit.** A product counts as a hit when at least one image yields a
  plausible size token. Tokens are recorded for verification, not used as
  data.
- **Visual audit.** Every hit was checked by eye against the image that
  produced it, and every miss against its images (36 images inspected in
  total, listed per product in the audit CSV), to separate *no size on
  the item photographed* from *size present but unreadable* from *misread*.
  This is a manual step; it is re-auditable, not re-runnable.

---

## Headline

**A net quantity was read for 8 of 30 products (26.7%) under the
pre-registered rule.** Under the post-hoc amended rule, 9 of 30 (30.0%).
Both are below the plan's ~40% threshold for OCR as the primary route.

Of 156 images: 13 produced a hit; 50 were blank — OCR found no text at all
(swatches, model shots, texture close-ups); 13 were under 900 px and got
no tiling pass; 1 carried a unit-like fragment and no size.

| Rule | Hits | Rate |
| --- | ---: | ---: |
| Primary (pre-registered) | 8 / 30 | 26.7% |
| Amended (post hoc, labelled) | 9 / 30 | 30.0% |
| Plan threshold for OCR-primary | — | ~40% |

## Precision: every hit was right

All 8 primary tokens — and the amended tokens for product 1 — match a
value printed on the pack in the image (`_ocr_probe_visual_audit.csv`,
`hit_verified` rows). **No token was a wrong value.** Two limitations sit
inside the hits:

- **The imperial half of a dual-unit line was dropped in 6 of 8.** The
  metric value survived every time; the second value was lost to
  mixed-case units the case-sensitive rule does not match (`0.48 Oz.`,
  `0.19 Fl. Oz.`), to OCR misreads (`2.2 FL. OZ.` → `FL O7`; `0.28 oz.` →
  `0.280L`), to one value not read at all (`0.16 oz.`), and to one below
  the 0.01 oz plausibility floor (`0.008 OZ.`). For this project that is
  the right half to lose — the Stage 1.2 parser prefers the explicit
  metric value on dual-unit labels — but it means an OCR token list is
  not the whole label.
- **One spurious partial token.** Product 12 lists `7 g` beside `4.7 g`
  because the full-frame pass read `4. 7g` with a space. A pipeline that
  takes "any token" would be wrong here; a product with more than one
  token must go to review, never be auto-accepted.

## Error modes for the 22 misses

Classified by eye from the images; every row in
`_ocr_probe_visual_audit.csv` names the image inspected and what it shows.

| Mode | Products | Which |
| --- | ---: | --- |
| **Net quantity is not on the item photographed** | **19** | 2, 3, 4, 5, 6, 7, 9, 11, 13, 14, 16, 17, 18, 23, 24, 25, 26, 28, 30 |
| Present but unreadable — mirrored text | 1 | 22: the size is printed on the palette lid and photographed through the open transparent lid from behind, so it appears mirror-imaged; OCR read `oitih` |
| Present but unreadable — micro-print | 1 | 8: a second line of micro-print on each stick barrel in a group shot, unresolvable at the 2,000 px original; whether it is the net weight cannot be confirmed |
| Present and read, rejected by the strict rule | 1 | 1: `TOTALNETWT.26.5g (O.95oz)` — glued label and O-for-0; recovered by the amended rule |
| Misread to a wrong value | 0 | — |

The dominant mode is not an OCR failure. In 19 of 22 misses the storefront
photographs the bare component — a tube, a stick, a pen, a compact lid, a
jar — and the net-contents line is on the carton, the base or the back,
none of which appears in any of the 156 images. The only two cartons in
the set (product 1, box front; product 21, box side) both carry the line
and both were read. Wet n Wild's eyeliner (20) was read only because the
storefront photographed the blister card, not the pencil.

One false positive was correctly refused: on product 26 the shade-chart
caption `3 OG FAVES` was read as `30G FAVES`, and the case-sensitive rule
rejected it — the same trap as the `029g` / `0MG` / `7G` fragments in the
Stage 1.0 page analysis.

## Does it cluster?

**By brand** (primary rule): Wet n Wild 3 of 6, Physicians Formula 2 of 6,
essence 2 of 6, ColourPop 1 of 6 (2 of 6 amended), Milani 0 of 6. Milani's
six products are all photographed as bare components with no size line on
the face shown. Wet n Wild's three hits are a blister card and two bottles
that print the size on the front.

**By product form** (from the `form` column of the audit CSV):

| Form | Products | Hits (primary) | Hits (amended) |
| --- | ---: | ---: | ---: |
| Compact or palette | 10 | 4 | 5 |
| Bottle or jar | 5 | 2 | 2 |
| Stick, tube or pen | 15 | 2 | 2 |

Both stick/tube/pen hits are exceptions: the blister card (20) and a tube
that prints its volume on the label (29). The pattern in one line: **the
hit is decided by whether the brand prints net contents on the face it
photographs; compacts and bottles sometimes do, sticks and tubes almost
never.** Form matters more than brand, and brand differences mostly track
form mix. These are counts on 30 products, six per brand and one to three
per form within a brand — not estimates of a rate.

Three of the 30 category guesses are wrong on inspection (19 and 25 are
palettes guessed as `eyeshadow_single`; 20 is an eyeliner guessed as
`primer`, outside §7 scope). The guesses are keyword rules already flagged
as unverified; they are noted for the Stage 1.2 audit and the list is not
changed.

## Would more images or preprocessing move the number?

- **Preprocessing — bounded and small.** The amended rule adds product 1
  (→ 30.0%). A horizontal flip would present product 22's mirrored lid
  the right way round (→ 33.3%). A higher-resolution or super-resolved
  image might resolve product 8's micro-print, if it is the net weight
  (→ 36.7% at most). **11 of 30 is the ceiling with the images fetched,
  and it is still below 40%.** The remaining 19 have no size in any image
  to recover.
- **More images from the same storefront — unmeasured, unlikely.**
  Thirteen products list more images than the six fetched (`image_count`
  in the sample CSV: seven to nine for nine of them; 18, 64, 67 and 91
  for four Milani products, which are shade-variant images of the same
  packshot). They were not fetched, so this is a judgement: nothing in
  the 156 images fetched shows a carton back, a base or a back panel, and
  a seventh image from the same photographer is unlikely to.
- **Other image sources.** The retailers whose listings routinely show
  back panels — Ulta, Target, Walmart, Amazon — are excluded on their
  terms (`reports/source_feasibility_report.md`). Open Beauty Facts
  carries photographs for its rows, of which ten are US drugstore makeup.
- **Read:** this is a ceiling set by what the brands photograph, not by
  the engine or the rule. Better OCR would not have changed the 19.

## What this finding says — and what it does not

It says: on drugstore brands' own storefront images, OCR reads a net
quantity for about a quarter of products, and when it reads one it is
right — 8 of 8 here, small n.

It does **not** say anything about packaging in hand (that is the
shelf-capture route, 1.1-B4), anything about precision at scale (8
verified hits), or anything about prestige brands' images (not probed).

## For the go/no-go

Measured 26.7%; 30.0% post hoc; 36.7% the most preprocessing could reach.
The plan's threshold is ~40%. **The number does not support OCR as the
primary route.** Whether to proceed to manual capture is the owner's
decision at the ⛔. If it proceeds, the 8 verified OCR values (9 amended)
carry image provenance and can seed the capture sheet as candidates to
confirm on the packaging — not as data.

## Reproduce

    python src/ingest/ocr_size_probe.py            # network; bounded; resumes from disk
    python src/ingest/ocr_size_probe_analyse.py    # no network; reads data/raw/capture/ocr/

The visual audit is a by-eye step: open each image named in
`_ocr_probe_visual_audit.csv` (URL in the product's `ocr/*.json`) and
compare against the row.
