"""Stage 1.1 task 1.1-C2: quantity disclosure by product category.

    python src/ingest/feasibility_category_breakdown.py

Reads the saved catalogue responses (data/raw/feasibility/shopify_*.json)
only - no network. Two rules already in the repository are reused
unchanged, so the figures are comparable with every other coverage figure:

  * "quantity disclosed" is feasibility_tier_breakdown.has_size on the
    structured slots (variant titles, option values, product title); a
    size that appears only in body text is reported as body_only and not
    counted;
  * "category" is preregister_capture_list.guess_category - the ordered
    keyword rules on product_type|title that pre-registered the capture
    list - applied here to every product in every tier, with the same
    exclusion word list (sets, kits, tools, non-makeup).

The category is a keyword match, not a verified label. Its precision is
unmeasured until the §34 audit; the per-product CSV written alongside the
JSON records the rule that fired for every product so each guess can be
checked.

Every product lands in exactly one bucket: a §7 category; `out_of_scope`
(a rule says it is not a §7 product - eyeliner); `unclassified` (no rule
matched, typically a product named without a category word, e.g. a MAC
shade name under product_type "Lips"); or `excluded` (set / kit / tool /
non-makeup word list). Nothing is dropped; bucket counts sum to the
product count.

Written to data/raw/feasibility/:
  _category_breakdown.json     the cuts below
  _category_assignments.csv    one row per product: bucket, rule, flags

Cuts, each by category and collapsed to the category's unit basis from
config/categories.yaml (weight = g, volume = mL, form_dependent =
split_required):
  all           every product
  drugstore     the five drugstore brands
  prestige_ex   non-drugstore excluding MAC and Tom Ford Beauty
  mac_tf        MAC and Tom Ford Beauty - the two brands that disclose
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

from feasibility_tier_breakdown import RAW_DIR, TAG_RE, has_size
from preregister_capture_list import EXCLUDE, guess_category

ROOT = Path(__file__).resolve().parents[2]
CATEGORIES_YAML = ROOT / "config" / "categories.yaml"
OUT_JSON = RAW_DIR / "_category_breakdown.json"
OUT_CSV = RAW_DIR / "_category_assignments.csv"

TWO = ("MAC", "Tom Ford Beauty")
NON_CATEGORY_BUCKETS = ["out_of_scope", "unclassified", "excluded"]
GROUPS = {
    "all": lambda r: True,
    "drugstore": lambda r: r["tier"] == "drugstore",
    "prestige_ex": lambda r: r["tier"] != "drugstore" and r["brand"] not in TWO,
    "mac_tf": lambda r: r["brand"] in TWO,
}


def category_config() -> tuple[list[str], dict[str, str]]:
    cfg = yaml.safe_load(CATEGORIES_YAML.read_text(encoding="utf-8"))
    order = [c["key"] for c in cfg["categories"]]
    basis = {c["key"]: (c["unit_basis"] or "form_dependent") for c in cfg["categories"]}
    return order, basis


def load_rows() -> list[dict]:
    rows = []
    for path in sorted(RAW_DIR.glob("shopify_*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if not rec.get("ok"):
            continue
        for p in rec["payload"].get("products", []):
            title = (p.get("title") or "").strip()
            ptype = (p.get("product_type") or "").strip()
            handle = p.get("handle") or ""
            variants = p.get("variants") or []
            options = p.get("options") or []
            vtitles = " ".join(str(v.get("title") or "") for v in variants)
            otext = " ".join(str(v) for o in options for v in (o.get("values") or []))
            body = TAG_RE.sub(" ", p.get("body_html") or "")
            structured = has_size(vtitles) or has_size(otext) or has_size(title)
            excluded = any(EXCLUDE.search(s) for s in (title, handle, ptype))
            cat, basis = guess_category(ptype, title)
            if excluded:
                bucket = "excluded"
                basis = "excluded by the set/kit/tool/non-makeup word list"
            elif cat == "out_of_scope":
                bucket = "unclassified" if basis.startswith("no §7 rule") else "out_of_scope"
            else:
                bucket = cat
            rows.append({
                "brand": rec["source_name"],
                "tier": rec["market_tier"],
                "product_id": p.get("id"),
                "handle": handle,
                "title": title,
                "product_type": ptype,
                "bucket": bucket,
                "category_basis": basis,
                "q_structured": structured,
                "q_body_only": (not structured) and has_size(body),
            })
    return rows


def summ(rs: list[dict]) -> dict:
    c = sum(r["q_structured"] for r in rs)
    b = sum(r["q_body_only"] for r in rs)
    return {"n": len(rs), "with_quantity": c, "body_only": b,
            "coverage": round(c / len(rs), 4) if rs else None}


def pct(c: int, n: int) -> str:
    return f"{c / n * 100:5.1f}%" if n else "  n/a"


def print_table(title: str, rows: list[dict], order: list[str], basis: dict[str, str]) -> None:
    print(f"\n{title}  (n={len(rows)})")
    print(f"{'category':<20}{'basis':<16}{'n':>6}{'with qty':>10}{'coverage':>10}{'body-only':>11}")
    print("-" * 73)
    for key in order + NON_CATEGORY_BUCKETS:
        rs = [r for r in rows if r["bucket"] == key]
        if not rs:
            continue
        s = summ(rs)
        print(f"{key:<20}{basis.get(key, '-'):<16}{s['n']:>6}{s['with_quantity']:>10}"
              f"{pct(s['with_quantity'], s['n']):>10}{s['body_only']:>11}")
    s = summ(rows)
    print("-" * 73)
    print(f"{'total':<36}{s['n']:>6}{s['with_quantity']:>10}{pct(s['with_quantity'], s['n']):>10}{s['body_only']:>11}")


def main() -> None:
    order, basis = category_config()
    rows = load_rows()
    print(f"products: {len(rows)}")

    for name, pred in GROUPS.items():
        print_table(f"QUANTITY DISCLOSURE BY CATEGORY - {name}", [r for r in rows if pred(r)], order, basis)

    bases = ["weight", "volume", "form_dependent"] + NON_CATEGORY_BUCKETS
    print("\nBY UNIT BASIS OF THE CATEGORY  (with qty / n, coverage)")
    print(f"{'basis':<16}" + "".join(f"{g:>22}" for g in GROUPS))
    print("-" * (16 + 22 * len(GROUPS)))
    for b in bases:
        line = f"{b:<16}"
        for name, pred in GROUPS.items():
            rs = [r for r in rows if pred(r) and basis.get(r["bucket"], r["bucket"]) == b]
            s = summ(rs)
            line += f"{s['with_quantity']:>6}/{s['n']:<5}{pct(s['with_quantity'], s['n']):>9} "
        print(line)

    print("\nUNCLASSIFIED BY BRAND  (no keyword rule matched product_type|title)")
    unc = [r for r in rows if r["bucket"] == "unclassified"]
    by_brand: dict[str, list[dict]] = {}
    for r in unc:
        by_brand.setdefault(r["brand"], []).append(r)
    for brand, rs in sorted(by_brand.items(), key=lambda kv: -len(kv[1])):
        n_brand = sum(1 for r in rows if r["brand"] == brand)
        print(f"  {brand:<24}{len(rs):>5} of {n_brand:<5} with qty {sum(r['q_structured'] for r in rs)}")

    # The exclusion word list is the capture list's, reused unchanged for
    # comparability. Some of its words also catch makeup (lash, cream, oil,
    # duo), so the excluded bucket is reported word by word rather than as
    # one number.
    print("\nEXCLUDED BUCKET BY EXCLUSION WORD  (a product counts under every word that fired)")
    excluded_by_word: dict[str, int] = {}
    for r in rows:
        if r["bucket"] != "excluded":
            continue
        words = {m.group(1).lower() for s in (r["title"], r["handle"], r["product_type"])
                 for m in EXCLUDE.finditer(s)}
        for w in words:
            excluded_by_word[w] = excluded_by_word.get(w, 0) + 1
    for w, n in sorted(excluded_by_word.items(), key=lambda kv: -kv[1]):
        print(f"  {w:<14}{n:>6}")

    # Every non-drugstore disclosure outside MAC and Tom Ford, listed, so the
    # 1.3% comparator can be read product by product.
    hits_ex = [r for r in rows if GROUPS["prestige_ex"](r) and r["q_structured"]]
    hits_ex_in_cat = [r for r in hits_ex if r["bucket"] in order]
    print(f"\nNON-DRUGSTORE DISCLOSURES OUTSIDE MAC AND TOM FORD: {len(hits_ex)}, "
          f"of which in a §7 category: {len(hits_ex_in_cat)}")
    for r in hits_ex:
        print(f"  {r['brand'][:16]:<16}{r['bucket']:<16}{r['product_type'][:18]:<18} | {r['title'][:60]}")

    out = {
        "method": {
            "quantity": "strict: a plausible size token in a variant title, option value or "
                        "product title counts; body text reported as body_only, not counted "
                        "(feasibility_tier_breakdown.has_size)",
            "category": "keyword rules on product_type|title from preregister_capture_list."
                        "guess_category, plus its exclusion word list; the rule that fired is "
                        "recorded per product in _category_assignments.csv; precision unmeasured "
                        "until the §34 audit",
            "unit_basis": "config/categories.yaml unit_basis; split_required -> form_dependent",
            "groups": {"all": "every product", "drugstore": "drugstore tier",
                       "prestige_ex": "non-drugstore excluding MAC and Tom Ford Beauty",
                       "mac_tf": "MAC and Tom Ford Beauty"},
        },
        "n_products": len(rows),
        "category_unit_basis": {k: basis[k] for k in order},
        "by_category": {
            name: {key: summ([r for r in rows if pred(r) and r["bucket"] == key])
                   for key in order + NON_CATEGORY_BUCKETS
                   if any(pred(r) and r["bucket"] == key for r in rows)}
            for name, pred in GROUPS.items()
        },
        "by_unit_basis": {
            name: {b: summ([r for r in rows if pred(r) and basis.get(r["bucket"], r["bucket"]) == b])
                   for b in bases}
            for name, pred in GROUPS.items()
        },
        "unclassified_by_brand": {
            brand: {"n": len(rs), "of": sum(1 for r in rows if r["brand"] == brand),
                    "with_quantity": sum(r["q_structured"] for r in rs)}
            for brand, rs in sorted(by_brand.items())
        },
        "totals": {name: summ([r for r in rows if pred(r)]) for name, pred in GROUPS.items()},
        "excluded_by_word": dict(sorted(excluded_by_word.items(), key=lambda kv: -kv[1])),
        "prestige_ex_disclosures": {
            "n": len(hits_ex),
            "in_a_category": len(hits_ex_in_cat),
            "categorised_prestige_ex_products": sum(1 for r in rows if GROUPS["prestige_ex"](r) and r["bucket"] in order),
            "products": [{"brand": r["brand"], "title": r["title"], "product_type": r["product_type"],
                          "bucket": r["bucket"]} for r in hits_ex],
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fields = ["brand", "tier", "product_id", "handle", "title", "product_type", "bucket",
              "category_basis", "q_structured", "q_body_only"]
    with OUT_CSV.open("w", encoding="utf-8", newline="\n") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"\n-> {OUT_JSON.relative_to(ROOT)}, {OUT_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
