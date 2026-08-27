"""Stage 1.1 task 1.1-B4: build the shelf-capture template from committed files.

    python src/ingest/build_capture_template.py

Reads only files already in the repository - no network - and writes

    data/raw/capture/shelf_capture_template.csv
    data/raw/capture/_shelf_capture_template_summary.json

one row per product in the pre-registered capture list
(data/raw/capture/drugstore_capture_list.csv, 250 rows, registered by commit
07c7ca3). The registered list is not changed: this sheet adds identity
columns to check against the pack, a fixed capture order, and blank columns
for what is read off the packaging. Re-running reproduces the file byte for
byte.

Pre-filled columns (identity, never quantity):
  capture_order       1..250 - priority_tier, then brand_rank with brands
                      interleaved, then brand name
  priority_tier       1, 2 or 3, from the prestige comparator's measured
                      disclosure in the same category (see PRIORITY RULE)
  list_rank, brand, product_id, handle, title, product_type, category_guess,
  storefront_url      copied from the registered list
  unit_basis          config/categories.yaml (weight / volume / form_dependent)
  storefront_sku      the variant SKU(s) the US storefront lists for this
                      product - drugstore packs print an item number that
                      often matches it; a second identity key beside the
                      barcode (methodology rule 2)
  ocr_candidate       the printed text read by the OCR probe and verified by
                      eye (_ocr_probe_visual_audit.csv) - a value to CONFIRM
                      against the pack, never data
  ocr_candidate_rule  primary (pre-registered rule) or amended (post hoc)
  photo_stem          the filename stem for this product's photographs

Blank columns are filled in the shop; docs/shelf_capture_protocol.md says how.
There is no price column and there will not be one (methodology rule 1).

PRIORITY RULE - fixed here, before any pack is read, so that partial capture
in a shop that does not stock everything cannot be steered by what the packs
say. A drugstore quantity is only useful for the tier contrast (spec 98) if
the same category has a prestige comparator with a known quantity. The
comparator count per category is measured in
data/raw/feasibility/_category_breakdown.json (MAC + Tom Ford Beauty plus
every other non-drugstore brand, structured-slot rule):
  tier 1  comparator with quantity >= 5 products
  tier 2  comparator with quantity 1-4 products
  tier 3  comparator with quantity 0
Within a tier, brands are interleaved by brand_rank (the seeded draw order
within each brand), so a visit cut short at any point has covered the five
brands about equally; list_rank is brand-blocked and would not. In the
shop: work down the sheet in capture_order, capture every product the shop
stocks, skip nothing that is stocked.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "data" / "raw" / "capture"
FEAS = ROOT / "data" / "raw" / "feasibility"
LIST_CSV = CAPTURE / "drugstore_capture_list.csv"
AUDIT_CSV = CAPTURE / "_ocr_probe_visual_audit.csv"
BREAKDOWN = FEAS / "_category_breakdown.json"
CATEGORIES = ROOT / "config" / "categories.yaml"
OUT_CSV = CAPTURE / "shelf_capture_template.csv"
OUT_SUMMARY = CAPTURE / "_shelf_capture_template_summary.json"

TIER_1_MIN = 5
MAX_SKUS_SHOWN = 6

PREFILLED = [
    "capture_order", "priority_tier", "list_rank", "brand_rank", "brand", "product_id", "handle",
    "title", "product_type", "category_guess", "unit_basis", "storefront_url",
    "storefront_sku", "ocr_candidate", "ocr_candidate_rule", "photo_stem",
]
CAPTURE_FIELDS = [
    "capture_status",            # captured | not_stocked | stocked_not_captured
    "capture_date",              # YYYY-MM-DD
    "shop",                      # one short name per shop, used consistently
    "captured_by",               # initials
    "product_name_as_printed",   # verbatim from the pack
    "shade_as_printed",          # verbatim; blank if none
    "item_number_as_printed",    # manufacturer item / SKU code on the pack, verbatim
    "barcode_digits",            # the digits printed under the bars, no spaces
    "barcode_source",            # printed_on_pack | importer_sticker | none
    "sold_with_carton",          # Y | N
    "net_contents_as_printed",   # verbatim, every unit shown, e.g. NET WT. 7.65g (0.27oz)
    "net_contents_location",     # front | back | base | carton | blister | none_visible
    "pack_count",                # number of units if a multipack; blank otherwise
    "form_as_seen",              # powder | cream | liquid | gel | pencil | pomade | stick | other
    "origin_line_as_printed",    # Made in / Distributed by line, verbatim
    "photo_front",               # filename
    "photo_net_contents",        # filename
    "photo_barcode",             # filename
    "photo_other",               # filenames, pipe-separated
    "ocr_candidate_confirmed",   # Y | N | blank when no candidate or not captured
    "notes",
]
FIELDS = PREFILLED + CAPTURE_FIELDS


def brand_slug(brand: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", brand.lower()).strip("_")


def load_unit_basis() -> dict[str, str]:
    cfg = yaml.safe_load(CATEGORIES.read_text(encoding="utf-8"))
    out = {}
    for c in cfg["categories"]:
        out[c["key"]] = c["unit_basis"] or "form_dependent"
    return out


def load_tiers() -> tuple[dict[str, int], dict[str, dict]]:
    d = json.loads(BREAKDOWN.read_text(encoding="utf-8"))
    by_cat = d["by_category"]
    comparator = {}
    cats = set(by_cat["mac_tf"]) | set(by_cat["prestige_ex"])
    for cat in cats:
        if cat in ("out_of_scope", "unclassified", "excluded"):
            continue
        n = by_cat["mac_tf"].get(cat, {}).get("with_quantity", 0) + \
            by_cat["prestige_ex"].get(cat, {}).get("with_quantity", 0)
        comparator[cat] = {
            "mac_tf_with_quantity": by_cat["mac_tf"].get(cat, {}).get("with_quantity", 0),
            "prestige_ex_with_quantity": by_cat["prestige_ex"].get(cat, {}).get("with_quantity", 0),
            "comparator_with_quantity": n,
        }
    tiers = {}
    for cat, c in comparator.items():
        n = c["comparator_with_quantity"]
        tiers[cat] = 1 if n >= TIER_1_MIN else (2 if n >= 1 else 3)
        c["tier"] = tiers[cat]
    return tiers, comparator


def load_skus() -> dict[str, str]:
    """product_id -> pipe-joined distinct variant SKUs from the saved catalogue."""
    skus: dict[str, str] = {}
    for path in sorted(FEAS.glob("shopify_*.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        if d.get("market_tier") != "drugstore" or not d.get("ok"):
            continue
        for p in d["payload"]["products"]:
            seen: list[str] = []
            for v in p.get("variants", []):
                s = (v.get("sku") or "").strip()
                if s and s not in seen:
                    seen.append(s)
            if len(seen) > MAX_SKUS_SHOWN:
                shown = seen[:MAX_SKUS_SHOWN] + [f"+{len(seen) - MAX_SKUS_SHOWN} more"]
            else:
                shown = seen
            skus[str(p["id"])] = "|".join(shown)
    return skus


def load_ocr_candidates() -> dict[tuple[str, str], tuple[str, str]]:
    """(brand, handle) -> (printed text as seen, rule) for verified OCR readings."""
    out = {}
    with AUDIT_CSV.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["classification"] not in ("hit_verified", "present_read_rejected_by_rule"):
                continue
            rule = "primary" if r["primary_tokens"] else "amended"
            out[(r["brand"], r["handle"])] = (r["printed_text_as_seen"], rule)
    return out


def main() -> None:
    unit_basis = load_unit_basis()
    tiers, comparator = load_tiers()
    skus = load_skus()
    ocr = load_ocr_candidates()

    with LIST_CSV.open(encoding="utf-8", newline="") as fh:
        products = list(csv.DictReader(fh))
    if len(products) != 250:
        raise SystemExit(f"expected 250 registered products, found {len(products)}")

    rows = []
    for p in products:
        cat = p["category_guess"]
        if cat not in tiers:
            raise SystemExit(f"no comparator entry for category {cat!r} (list_rank {p['list_rank']})")
        cand = ocr.get((p["brand"], p["handle"]), ("", ""))
        row = {k: "" for k in FIELDS}
        row.update({
            "priority_tier": tiers[cat],
            "list_rank": int(p["list_rank"]),
            "brand_rank": int(p["brand_rank"]),
            "brand": p["brand"],
            "product_id": p["product_id"],
            "handle": p["handle"],
            "title": p["title"],
            "product_type": p["product_type"],
            "category_guess": cat,
            "unit_basis": unit_basis[cat],
            "storefront_url": p["storefront_url"],
            "storefront_sku": skus.get(p["product_id"], ""),
            "ocr_candidate": cand[0],
            "ocr_candidate_rule": cand[1],
            "photo_stem": f"{int(p['list_rank']):03d}_{brand_slug(p['brand'])}_{p['handle']}",
        })
        rows.append(row)

    rows.sort(key=lambda r: (r["priority_tier"], r["brand_rank"], r["brand"]))
    for i, r in enumerate(rows, 1):
        r["capture_order"] = i

    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

    def count(key):
        out: dict[str, int] = {}
        for r in rows:
            out[str(r[key])] = out.get(str(r[key]), 0) + 1
        return dict(sorted(out.items()))

    by_tier_brand: dict[str, dict[str, int]] = {}
    for r in rows:
        t = by_tier_brand.setdefault(f"tier_{r['priority_tier']}", {})
        t[r["brand"]] = t.get(r["brand"], 0) + 1
    by_tier_cat: dict[str, dict[str, int]] = {}
    for r in rows:
        t = by_tier_cat.setdefault(f"tier_{r['priority_tier']}", {})
        t[r["category_guess"]] = t.get(r["category_guess"], 0) + 1

    summary = {
        "source_list": str(LIST_CSV.relative_to(ROOT)),
        "rows": len(rows),
        "priority_rule": {
            "basis": "comparator_with_quantity = MAC + Tom Ford Beauty + every other non-drugstore brand, "
                     "products with a structured-slot quantity in the same category, from "
                     "data/raw/feasibility/_category_breakdown.json",
            "tier_1": f">= {TIER_1_MIN}",
            "tier_2": "1-4",
            "tier_3": "0",
            "within_tier": "brand_rank (seeded draw order within each brand), brands interleaved, "
                           "then brand name - so a truncated visit covers the five brands about equally",
        },
        "comparator_by_category": dict(sorted(comparator.items())),
        "by_tier": count("priority_tier"),
        "by_tier_brand": by_tier_brand,
        "by_tier_category": {k: dict(sorted(v.items())) for k, v in by_tier_cat.items()},
        "with_storefront_sku": sum(1 for r in rows if r["storefront_sku"]),
        "with_ocr_candidate": sum(1 for r in rows if r["ocr_candidate"]),
        "ocr_candidates": [
            {"list_rank": r["list_rank"], "brand": r["brand"], "handle": r["handle"],
             "printed": r["ocr_candidate"], "rule": r["ocr_candidate_rule"]}
            for r in sorted(rows, key=lambda r: r["list_rank"]) if r["ocr_candidate"]
        ],
        "capture_fields": CAPTURE_FIELDS,
        "note": "identity and provenance only; no quantity, no price",
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"rows: {len(rows)} -> {OUT_CSV.relative_to(ROOT)}")
    print("by tier:", summary["by_tier"])
    for t, brands in by_tier_brand.items():
        print(f"  {t}: {brands}")
    print("tier by category:")
    for cat, c in sorted(comparator.items(), key=lambda kv: (kv[1]["tier"], kv[0])):
        drawn = by_tier_cat.get(f"tier_{c['tier']}", {}).get(cat, 0)
        print(f"  tier {c['tier']}  {cat:<18} comparator with quantity {c['comparator_with_quantity']:>3}  drawn {drawn}")
    print(f"storefront sku present: {summary['with_storefront_sku']}/{len(rows)}")
    print(f"ocr candidates: {summary['with_ocr_candidate']}")
    print(f"-> {OUT_SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
