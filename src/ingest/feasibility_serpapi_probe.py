"""Stage 1.0 task 1.0-T4: does Google Shopping carry inline size for drugstore makeup?

    python src/ingest/feasibility_serpapi_probe.py --dry-run   # show the products; no request
    python src/ingest/feasibility_serpapi_probe.py             # run; free tier only

Measures, for 20 drugstore products drawn from the saved Shopify catalogues,
whether Google Shopping result titles carry a plausible inline size. The size
rule is imported from feasibility_pdp_analyse so this figure is measured the
same way as the storefront figure it will be compared with.

Budget discipline. The account endpoint is read first; the run aborts unless
the plan is the free one and at least SEARCHES plus a margin remain. Each
product is exactly one request. Nothing is retried. The run stops at the
first error response. Raw responses are stored under
data/raw/feasibility/serpapi/ with provenance and the key scrubbed.

Selection rule, fixed before any query was sent: every drugstore brand whose
storefront probe succeeded contributes its first PER_BRAND products in handle
order, skipping titles that look like sets, bundles, kits, tools, gift items
or non-makeup. Shade suffixes after " | " are dropped from the query so the
search targets the product, not one shade; the Shopify product_type is
appended only when the title names no product type at all (ColourPop titles
are bare shade names); a product whose query duplicates an earlier one is
skipped.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

from feasibility_pdp_analyse import find_sizes

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "feasibility"
OUT_DIR = RAW_DIR / "serpapi"
SUMMARY = RAW_DIR / "_serpapi_summary.json"

SEARCHES = 20
PER_BRAND = 4
MARGIN = 5
ENGINE = {"engine": "google_shopping", "gl": "us", "hl": "en"}
USER_AGENT = "beauty-value-intelligence/0.1 (Stage 1.0 source feasibility study)"

EXCLUDE = re.compile(
    r"\b(set|sets|bundle|bundles|kit|kits|combo|gift|brush|brushes|sponge|bag|"
    r"pouch|mystery|vault|subscription|wipes|remover|tool|tools|duo|trio|"
    r"card|sample|freegift|case|clip|lash|lashes|nail|polish|oil|body|serum|"
    r"cleanser|moisturi[sz]er|cream|skincare)\b",
    re.I,
)

# A title that contains one of these already names its product type.
NOUN = re.compile(
    r"\b(lip|lips|lipstick|lipliner|gloss|liner|eyeliner|mascara|powder|palette|"
    r"shadow|eyeshadow|blush|bronzer|bronzing|highlighter|foundation|concealer|"
    r"primer|tint|spray|pencil|brow|cr[eè]me|balm|drops|stick|stix|contour|"
    r"setting)\b",
    re.I,
)


def load_catalogue_products() -> list[dict]:
    """First PER_BRAND eligible products per drugstore brand, handle order."""
    chosen: list[dict] = []
    seen: set[str] = set()
    for path in sorted(RAW_DIR.glob("shopify_*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if doc.get("market_tier") != "drugstore" or not doc.get("ok"):
            continue
        brand = doc["source_name"]
        products = sorted(doc["payload"]["products"], key=lambda p: p["handle"])
        taken = 0
        for p in products:
            title = p["title"].strip()
            ptype = (p.get("product_type") or "").strip()
            if any(EXCLUDE.search(s) for s in (title, p["handle"], ptype)):
                continue
            query_name = title.split(" | ")[0].strip()
            if ptype and not NOUN.search(query_name):
                query_name = f"{query_name} {ptype}"
            query = f"{brand} {query_name}"
            if query in seen:
                continue
            seen.add(query)
            chosen.append(
                {
                    "brand": brand,
                    "handle": p["handle"],
                    "title": title,
                    "product_type": ptype,
                    "query": query,
                    "storefront_url": doc["source_url"].split("/products.json")[0]
                    + "/products/"
                    + p["handle"],
                }
            )
            taken += 1
            if taken == PER_BRAND:
                break
    return chosen


def account(key: str) -> dict:
    r = requests.get(
        "https://serpapi.com/account.json",
        params={"api_key": key},
        timeout=30,
        headers={"User-Agent": USER_AGENT},
    )
    r.raise_for_status()
    d = r.json()
    return {
        "plan_name": d.get("plan_name"),
        "searches_per_month": d.get("searches_per_month"),
        "plan_searches_left": d.get("plan_searches_left"),
        "this_month_usage": d.get("this_month_usage"),
    }


def search(key: str, query: str) -> tuple[int, dict]:
    r = requests.get(
        "https://serpapi.com/search.json",
        params={**ENGINE, "q": query, "api_key": key},
        timeout=60,
        headers={"User-Agent": USER_AGENT},
    )
    try:
        body = r.json()
    except ValueError:
        body = {"error": f"non-json response ({len(r.text)} bytes)"}
    return r.status_code, body


def brand_in(title: str, brand: str) -> bool:
    norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())  # noqa: E731
    return norm(brand) in norm(title)


def measure(product: dict, body: dict) -> dict:
    results = list(body.get("shopping_results") or []) + list(
        body.get("inline_shopping_results") or []
    )
    titles = [r.get("title", "") for r in results]
    sized = [t for t in titles if find_sizes(t)]
    brand_titles = [t for t in titles if brand_in(t, product["brand"])]
    brand_sized = [t for t in brand_titles if find_sizes(t)]
    first_brand_title = brand_titles[0] if brand_titles else None
    return {
        **product,
        "n_results": len(results),
        "n_results_with_size": len(sized),
        "n_brand_results": len(brand_titles),
        "n_brand_results_with_size": len(brand_sized),
        "any_size": bool(sized),
        "brand_result_has_size": bool(brand_sized),
        "first_brand_result_title": first_brand_title,
        "first_brand_result_has_size": bool(first_brand_title and find_sizes(first_brand_title)),
        "sizes_seen": sorted({s for t in brand_sized for s in find_sizes(t)})[:8],
        "example_sized_titles": brand_sized[:3],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="list the selection; send nothing")
    args = ap.parse_args()

    products = load_catalogue_products()
    print(f"selected {len(products)} products from "
          f"{len({p['brand'] for p in products})} drugstore brands")
    for p in products:
        print(f"  {p['brand']:<20} {p['query']}")
    if len(products) != SEARCHES:
        sys.exit(f"selection produced {len(products)} products, expected {SEARCHES}")
    if args.dry_run:
        return

    load_dotenv(ROOT / ".env")
    key = os.environ.get("SERPAPI_KEY", "").strip()
    if not key:
        sys.exit("SERPAPI_KEY not set in .env")

    before = account(key)
    print(f"\naccount before: {before}")
    if "free" not in str(before["plan_name"]).lower():
        sys.exit("not on the free plan - refusing to spend searches")
    if (before["plan_searches_left"] or 0) < SEARCHES + MARGIN:
        sys.exit("fewer than SEARCHES + MARGIN searches left - refusing to run")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows, used = [], 0
    for p in products:
        if used >= SEARCHES:
            break
        collected_at = datetime.now(timezone.utc).isoformat()
        status, body = search(key, p["query"])
        used += 1
        scrubbed = json.loads(json.dumps(body).replace(key, "<redacted>"))
        record = {
            "source_name": "SerpApi Google Shopping",
            "source_type": "commercial_serp_api",
            "extraction_method": "http_get",
            "engine_params": ENGINE,
            "query": p["query"],
            "product": p,
            "collected_at": collected_at,
            "http_status": status,
            "payload": scrubbed,
        }
        fname = re.sub(r"[^a-z0-9]+", "_", p["brand"].lower()) + "__" + p["handle"] + ".json"
        (OUT_DIR / fname).write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if status != 200 or "error" in body:
            print(f"!! stopping: status {status}, error {body.get('error')!r} on {p['query']}")
            rows.append({**p, "error": body.get("error"), "http_status": status})
            break
        rows.append(measure(p, body))
        r = rows[-1]
        print(f"  {r['brand'][:18]:<18} results={r['n_results']:>2} brand={r['n_brand_results']:>2} "
              f"sized(any)={r['n_results_with_size']:>2} sized(brand)={r['n_brand_results_with_size']:>2} "
              f"{r['sizes_seen'][:3]}")
        time.sleep(1.5)

    after = account(key)
    ok = [r for r in rows if "error" not in r]
    n = len(ok)
    summary = {
        "probed_at": datetime.now(timezone.utc).isoformat(),
        "engine_params": ENGINE,
        "selection_rule": "first PER_BRAND eligible products per drugstore brand in handle order",
        "per_brand": PER_BRAND,
        "searches_used": used,
        "account_before": before,
        "account_after": after,
        "n_products": n,
        "products_with_any_sized_title": sum(r["any_size"] for r in ok),
        "products_with_brand_matched_sized_title": sum(r["brand_result_has_size"] for r in ok),
        "products_with_first_brand_result_sized": sum(r["first_brand_result_has_size"] for r in ok),
        "products_with_no_brand_result": sum(r["n_brand_results"] == 0 for r in ok),
        "total_results": sum(r["n_results"] for r in ok),
        "total_results_with_size": sum(r["n_results_with_size"] for r in ok),
        "total_brand_results": sum(r["n_brand_results"] for r in ok),
        "total_brand_results_with_size": sum(r["n_brand_results_with_size"] for r in ok),
        "rows": rows,
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nsearches used: {used}   account after: {after}")
    if n:
        print(f"products with ANY result title carrying a size      : "
              f"{summary['products_with_any_sized_title']}/{n}")
        print(f"products with a BRAND-MATCHED title carrying a size : "
              f"{summary['products_with_brand_matched_sized_title']}/{n}")
        print(f"products whose FIRST brand-matched title has a size : "
              f"{summary['products_with_first_brand_result_sized']}/{n}")
        print(f"products with no brand-matched result at all        : "
              f"{summary['products_with_no_brand_result']}/{n}")
        print(f"result titles with a size (all / brand-matched)     : "
              f"{summary['total_results_with_size']}/{summary['total_results']} / "
              f"{summary['total_brand_results_with_size']}/{summary['total_brand_results']}")
    print(f"summary -> {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
