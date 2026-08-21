"""Stage 1.0 coverage measurement.

Reads the raw probe responses and MEASURES field coverage against the spec §16
field table. Nothing here is estimated.

The decisive question is size. Shopify exposes no net-quantity field, so this
script measures where a size token actually appears - variant title, product
options, product title, or body text - and reports each separately, because
they are not equally trustworthy.

It deliberately does not parse or normalise. That is Stage 1.2 (§27-31).
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "feasibility"

# A size token: a number followed by a weight or volume unit.
# Intentionally permissive - this measures PRESENCE, not correctness.
SIZE_RE = re.compile(
    r"\d+(?:[.,]\d+)?\s*(?:fl\.?\s*oz|floz|oz|ml|mL|g\b|gr\b|gram|mg)",
    re.IGNORECASE,
)

TAG_RE = re.compile(r"<[^>]+>")


def has_size(text: str | None) -> bool:
    return bool(text) and bool(SIZE_RE.search(text))


def strip_html(html: str | None) -> str:
    return TAG_RE.sub(" ", html or "")


def main() -> None:
    files = sorted(p for p in RAW_DIR.glob("shopify_*.json"))
    if not files:
        raise SystemExit("no probe files found - run feasibility_probe.py first")

    rows = []
    for path in files:
        rec = json.loads(path.read_text(encoding="utf-8"))
        if not rec.get("ok"):
            continue
        brand, tier = rec["source_name"], rec["market_tier"]
        for p in rec["payload"].get("products", []):
            variants = p.get("variants") or []
            options = p.get("options") or []
            option_text = " ".join(
                str(v) for o in options for v in (o.get("values") or [])
            )
            variant_titles = " ".join(str(v.get("title") or "") for v in variants)
            body = strip_html(p.get("body_html"))

            prices = [v.get("price") for v in variants if v.get("price") not in (None, "")]
            grams = [v.get("grams") for v in variants if v.get("grams") not in (None, 0)]

            rows.append(
                {
                    "brand": brand,
                    "tier": tier,
                    "vendor": p.get("vendor"),
                    "product_type": p.get("product_type"),
                    "title": p.get("title"),
                    "handle": p.get("handle"),
                    "n_variants": len(variants),
                    "has_price": bool(prices),
                    "has_shipping_grams": bool(grams),
                    "size_in_title": has_size(p.get("title")),
                    "size_in_variant_title": has_size(variant_titles),
                    "size_in_options": has_size(option_text),
                    "size_in_body": has_size(body),
                }
            )

    n = len(rows)
    print(f"products analysed: {n}\n")

    def pct(key: str) -> str:
        c = sum(1 for r in rows if r[key])
        return f"{c:>5} / {n}  ({c / n * 100:5.1f}%)"

    print("SPEC 16 CRITICAL FIELDS - measured presence")
    print(f"  product_name          {pct('title')}")
    print(f"  brand (vendor)        {pct('vendor')}")
    print(f"  category (product_type){pct('product_type')}")
    print(f"  retail_price          {pct('has_price')}")
    print(f"  product_url (handle)  {pct('handle')}")

    print("\nSIZE - where a size token actually appears")
    print(f"  in variant title      {pct('size_in_variant_title')}")
    print(f"  in product options    {pct('size_in_options')}")
    print(f"  in product title      {pct('size_in_title')}")
    print(f"  in body/description   {pct('size_in_body')}")

    anywhere = sum(
        1
        for r in rows
        if r["size_in_variant_title"] or r["size_in_options"] or r["size_in_title"]
    )
    structured_ish = sum(
        1 for r in rows if r["size_in_variant_title"] or r["size_in_options"]
    )
    with_body = sum(
        1
        for r in rows
        if r["size_in_variant_title"]
        or r["size_in_options"]
        or r["size_in_title"]
        or r["size_in_body"]
    )
    print(
        f"\n  size in a STRUCTURED-ish slot (variant/options): "
        f"{structured_ish:>5} / {n}  ({structured_ish / n * 100:5.1f}%)"
    )
    print(
        f"  size in title/variant/options (no body):        "
        f"{anywhere:>5} / {n}  ({anywhere / n * 100:5.1f}%)"
    )
    print(
        f"  size anywhere INCLUDING free-text body:         "
        f"{with_body:>5} / {n}  ({with_body / n * 100:5.1f}%)"
    )

    print(f"\n  Shopify variant `grams` populated:            {pct('has_shipping_grams')}")
    print("  (shipping weight incl. packaging - NOT net content, must not be used)")

    print("\nFIELDS ABSENT FROM THIS SOURCE ENTIRELY")
    for f in ("rating", "review_count", "ingredients", "upc_ean", "finish", "coverage"):
        print(f"  {f:<14} absent")

    print("\nSIZE COVERAGE BY TIER (variant/options/title)")
    by_tier: dict[str, list] = {}
    for r in rows:
        by_tier.setdefault(r["tier"], []).append(r)
    for tier, rs in sorted(by_tier.items()):
        c = sum(
            1
            for r in rs
            if r["size_in_variant_title"] or r["size_in_options"] or r["size_in_title"]
        )
        print(f"  {tier:<10} {c:>5} / {len(rs):<5} ({c / len(rs) * 100:5.1f}%)")

    print("\nSIZE COVERAGE BY BRAND (variant/options/title)")
    by_brand: dict[str, list] = {}
    for r in rows:
        by_brand.setdefault(r["brand"], []).append(r)
    for brand, rs in sorted(
        by_brand.items(),
        key=lambda kv: -sum(
            1
            for r in kv[1]
            if r["size_in_variant_title"] or r["size_in_options"] or r["size_in_title"]
        )
        / len(kv[1]),
    ):
        c = sum(
            1
            for r in rs
            if r["size_in_variant_title"] or r["size_in_options"] or r["size_in_title"]
        )
        print(f"  {brand:<26} {c:>4} / {len(rs):<5} ({c / len(rs) * 100:5.1f}%)")

    print("\nTOP product_type VALUES (category signal)")
    for t, c in Counter(
        r["product_type"] or "(empty)" for r in rows
    ).most_common(20):
        print(f"  {c:>5}  {t}")


if __name__ == "__main__":
    main()
