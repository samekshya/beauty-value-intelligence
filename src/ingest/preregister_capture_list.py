"""Stage 1.1 task 1.1-B1: pre-register the drugstore quantity-capture list.

    python src/ingest/preregister_capture_list.py

Fixes, before any size is read, WHICH drugstore products will have their
net quantity captured (by OCR on storefront images or by hand). The list
is drawn by a seeded, deterministic rule from the drugstore storefront
catalogues already on disk, so re-running the script reproduces the same
files byte for byte. The git timestamp of the committed CSVs is the
pre-registration (spec §4, docs/methodology.md rule 3).

What the script does NOT do: read, guess or record any quantity. The
CSVs carry identity and provenance fields only.

Rule, in order:
  1. Universe: every product in a drugstore catalogue whose probe
     succeeded (data/raw/feasibility/shopify_*.json, market_tier
     'drugstore', ok true). These are the Stage 1.0 snapshots, capped at
     250 per brand by the endpoint, collected 2026-08-21.
  2. Exclude sets, kits, bundles, tools and non-makeup by title, handle
     and product_type (same word list as the Google Shopping probe).
  3. Category guess from product_type and title with the ordered keyword
     rules below; the rule that fired is recorded per row. Products that
     no §7 rule matches are out of scope and not drawn.
  4. Stratified draw, seed 20260826: per brand up to PER_BRAND products,
     taken round-robin across that brand's categories (categories and
     products both in seeded-shuffled order) so no category dominates.
  5. OCR test sample: the first OCR_SAMPLE_PER_BRAND products drawn for
     each brand, interleaved brand by brand -> 30 products.
"""

from __future__ import annotations

import csv
import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "feasibility"
OUT_DIR = ROOT / "data" / "raw" / "capture"
LIST_CSV = OUT_DIR / "drugstore_capture_list.csv"
SAMPLE_CSV = OUT_DIR / "ocr_test_sample.csv"
SUMMARY = OUT_DIR / "_capture_list_summary.json"

SEED = 20260826
PER_BRAND = 50
OCR_SAMPLE_PER_BRAND = 6
MAX_IMAGE_URLS = 8

EXCLUDE = re.compile(
    r"\b(set|sets|bundle|bundles|kit|kits|combo|gift|brush|brushes|sponge|bag|"
    r"pouch|mystery|vault|subscription|wipes|remover|tool|tools|duo|trio|"
    r"card|sample|freegift|case|clip|lash|lashes|nail|polish|oil|body|serum|"
    r"cleanser|moisturi[sz]er|cream|skincare)\b",
    re.I,
)

# (category key from config/categories.yaml, regex on "product_type | title").
# First match wins. Order matters: specific before general.
RULES: list[tuple[str, str]] = [
    ("setting_spray",      r"setting spray|fixing spray|finishing spray"),
    ("primer",             r"\bprimer"),
    ("mascara",            r"\bmascara"),
    ("brow",               r"\bbrow|eyebrow"),
    ("lip_liner",          r"lip ?liner|lip pencil|lip pen\b"),
    # eyeliner is not a §7 category: out of scope, and it must be caught
    # before the generic rules ("gel eyeliner" would otherwise match nothing
    # useful and "shadow & liner" would land in eyeshadow).
    ("out_of_scope",       r"eyeliner|eye liner|\bliner\b|kohl|kajal"),
    ("liquid_lipstick",    r"liquid lip|lip cr[eè]me|lip cream|lip velvet|lip mousse|liquid catsuit"),
    ("lip_gloss",          r"lip ?gloss|\bgloss\b|lip oil|lip lacquer|plumping"),
    ("lipstick",           r"lipstick|lip colou?r|lip stick|lip balm|lip tint|lip stain"),
    ("concealer",          r"concealer"),
    ("foundation",         r"foundation|skin tint|tinted moisturi[sz]er|bb cream|cc cream"),
    ("bronzer",            r"bronzer|bronzing"),
    ("highlighter",        r"highlight|illuminat|glow stick|strobe"),
    ("liquid_blush",       r"liquid blush|blush drops|blush tint"),
    ("cream_blush",        r"(cream|cr[eè]me|stick|stix|mousse|balm|jelly|gel)[^|]*blush|blush[^|]*(stick|stix|balm|jelly|mousse)"),
    ("powder_blush",       r"\bblush"),
    ("setting_powder",     r"setting powder|loose powder|finishing powder|translucent|baking powder|blurring"),
    ("pressed_powder",     r"pressed powder|compact powder|powder foundation|face powder|\bpowder\b"),
    ("eyeshadow_palette",  r"(shadow|eyeshadow|eye shadow)[^|]*palette|palette[^|]*(shadow|eye)"),
    ("eyeshadow_single",   r"eyeshadow|eye shadow|shadow stick|shadow stix|shadow"),
]


def guess_category(product_type: str, title: str) -> tuple[str, str]:
    text = f"{product_type} | {title}".lower()
    for key, pattern in RULES:
        m = re.search(pattern, text)
        if m:
            if key == "out_of_scope":
                return key, f"out of scope <- '{m.group(0)}' (not a §7 category)"
            return key, f"{key} <- '{m.group(0)}' in product_type|title"
    return "out_of_scope", "no §7 rule matched"


def load_universe() -> tuple[list[dict], list[dict]]:
    rows, sources = [], []
    for path in sorted(RAW_DIR.glob("shopify_*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc.get("market_tier") != "drugstore" or not doc.get("ok"):
            continue
        brand = doc["source_name"]
        base = doc["source_url"].split("/products.json")[0]
        sources.append({"brand": brand, "file": path.name, "source_url": doc["source_url"],
                        "collected_at": doc["collected_at"], "product_count": doc["product_count"]})
        for p in doc["payload"]["products"]:
            title = (p.get("title") or "").strip()
            ptype = (p.get("product_type") or "").strip()
            excluded = any(EXCLUDE.search(s) for s in (title, p["handle"], ptype))
            cat, basis = guess_category(ptype, title)
            images = [im.get("src") for im in (p.get("images") or []) if im.get("src")]
            rows.append({
                "brand": brand,
                "product_id": p["id"],
                "handle": p["handle"],
                "title": title,
                "product_type": ptype,
                "category_guess": cat,
                "category_basis": basis,
                "excluded": excluded,
                "storefront_url": f"{base}/products/{p['handle']}",
                "image_count": len(images),
                "image_urls": "|".join(images[:MAX_IMAGE_URLS]),
                "catalogue_file": path.name,
                "catalogue_collected_at": doc["collected_at"],
            })
    return rows, sources


def draw(rows: list[dict]) -> list[dict]:
    rng = random.Random(SEED)
    eligible = [r for r in rows if not r["excluded"] and r["category_guess"] != "out_of_scope"]
    drawn: list[dict] = []
    for brand in sorted({r["brand"] for r in eligible}):
        by_cat: dict[str, list[dict]] = {}
        for r in sorted((r for r in eligible if r["brand"] == brand), key=lambda r: r["handle"]):
            by_cat.setdefault(r["category_guess"], []).append(r)
        cats = sorted(by_cat)
        rng.shuffle(cats)
        for c in cats:
            rng.shuffle(by_cat[c])
        taken, i = 0, 0
        while taken < PER_BRAND and any(by_cat.values()):
            c = cats[i % len(cats)]
            i += 1
            if by_cat[c]:
                r = by_cat[c].pop()
                drawn.append({"list_rank": len(drawn) + 1, "brand_rank": taken + 1, **r})
                taken += 1
    return drawn


def ocr_sample(drawn: list[dict]) -> list[dict]:
    brands = sorted({r["brand"] for r in drawn})
    sample = []
    for k in range(1, OCR_SAMPLE_PER_BRAND + 1):
        for b in brands:
            hit = [r for r in drawn if r["brand"] == b and r["brand_rank"] == k]
            sample.extend(hit)
    return [{"sample_rank": i + 1, **r} for i, r in enumerate(sample)]


FIELDS = ["list_rank", "brand_rank", "brand", "product_id", "handle", "title", "product_type",
          "category_guess", "category_basis", "storefront_url", "image_count", "image_urls",
          "catalogue_file", "catalogue_collected_at"]


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    rows, sources = load_universe()
    drawn = draw(rows)
    sample = ocr_sample(drawn)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(LIST_CSV, drawn, FIELDS)
    write_csv(SAMPLE_CSV, sample, ["sample_rank"] + FIELDS)

    def count(rs, key):
        out: dict[str, int] = {}
        for r in rs:
            out[r[key]] = out.get(r[key], 0) + 1
        return dict(sorted(out.items()))

    eligible = [r for r in rows if not r["excluded"] and r["category_guess"] != "out_of_scope"]
    summary = {
        "written_at": datetime.now(timezone.utc).isoformat(),
        "seed": SEED,
        "per_brand": PER_BRAND,
        "ocr_sample_per_brand": OCR_SAMPLE_PER_BRAND,
        "sources": sources,
        "universe": len(rows),
        "excluded_by_word_list": sum(r["excluded"] for r in rows),
        "out_of_scope_after_exclusion": sum(1 for r in rows if not r["excluded"] and r["category_guess"] == "out_of_scope"),
        "eligible": len(eligible),
        "eligible_by_brand": count(eligible, "brand"),
        "eligible_by_category": count(eligible, "category_guess"),
        "drawn": len(drawn),
        "drawn_by_brand": count(drawn, "brand"),
        "drawn_by_category": count(drawn, "category_guess"),
        "ocr_sample": len(sample),
        "ocr_sample_by_brand": count(sample, "brand"),
        "ocr_sample_by_category": count(sample, "category_guess"),
        "fields": FIELDS,
        "note": "identity and provenance only; no quantity, no price",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"universe {len(rows)}  excluded {summary['excluded_by_word_list']}  "
          f"out of scope {summary['out_of_scope_after_exclusion']}  eligible {len(eligible)}")
    print("eligible by category:", summary["eligible_by_category"])
    print(f"drawn {len(drawn)} by brand {summary['drawn_by_brand']}")
    print("drawn by category:", summary["drawn_by_category"])
    print(f"ocr sample {len(sample)} by brand {summary['ocr_sample_by_brand']}")
    print("ocr sample by category:", summary["ocr_sample_by_category"])
    print(f"-> {LIST_CSV.relative_to(ROOT)}, {SAMPLE_CSV.relative_to(ROOT)}, {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
