"""Stage 1.0 feasibility probe.

Measures real field coverage on candidate sources. This is throwaway
measurement tooling for the feasibility study, NOT the Stage 1.1 ingestion
pipeline - it deliberately does no cleaning, no parsing and no normalisation,
because the point is to find out what the sources actually return.

Only sources whose robots.txt permits the requested path are probed, and the
probe identifies itself honestly. Request volume is a handful of calls.

Raw responses land in data/raw/feasibility/ with provenance (spec §25).
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# Honest identification. Not a spoofed browser string.
USER_AGENT = "beauty-value-intelligence/0.1 (Stage 1.0 source feasibility study)"

# Seconds between requests. Deliberately conservative for a read-only probe.
REQUEST_DELAY = 2.0
TIMEOUT = 30

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "feasibility"

# Shopify storefronts whose robots.txt was read on 2026-08-22 and found to
# permit product paths. `products.json` is not disallowed on any of these.
# tier keys match config/tier_mapping.yaml.
SHOPIFY_BRANDS = [
    ("e.l.f.",                   "drugstore", "https://www.elfcosmetics.com"),
    ("Milani",                   "drugstore", "https://www.milanicosmetics.com"),
    ("Essence",                  "drugstore", "https://essencemakeup.com"),
    ("Wet n Wild",               "drugstore", "https://www.wetnwildbeauty.com"),
    ("ColourPop",                "drugstore", "https://colourpop.com"),
    ("Physicians Formula",       "drugstore", "https://www.physiciansformula.com"),
    ("Morphe",                   "mid_range", "https://www.morphe.com"),
    ("Juvia's Place",            "mid_range", "https://www.juviasplace.com"),
    ("Pixi",                     "mid_range", "https://www.pixibeauty.com"),
    ("MAC",                      "high_end",  "https://www.maccosmetics.com"),
    ("Rare Beauty",              "high_end",  "https://www.rarebeauty.com"),
    ("Fenty Beauty",             "high_end",  "https://fentybeauty.com"),
    ("Tarte",                    "high_end",  "https://tartecosmetics.com"),
    ("Anastasia Beverly Hills",  "high_end",  "https://www.anastasiabeverlyhills.com"),
    ("Huda Beauty",              "high_end",  "https://hudabeauty.com"),
    ("Saie",                     "high_end",  "https://saiehello.com"),
    ("Tower 28",                 "high_end",  "https://www.tower28beauty.com"),
    ("Makeup by Mario",          "high_end",  "https://www.makeupbymario.com"),
    ("Haus Labs",                "high_end",  "https://hauslabs.com"),
    ("Tom Ford Beauty",          "luxury",    "https://www.tomfordbeauty.com"),
]

PRODUCTS_PER_BRAND = 250  # Shopify's per-page maximum


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def probe_shopify(brand: str, tier: str, base_url: str) -> dict:
    """Fetch one page of a Shopify storefront's public product JSON."""
    url = f"{base_url}/products.json?limit={PRODUCTS_PER_BRAND}"
    record = {
        "source_name": brand,
        "market_tier": tier,
        "source_url": url,
        "source_type": "shopify_storefront_json",
        "extraction_method": "http_get",
        "collected_at": utcnow(),
        "http_status": None,
        "ok": False,
        "error": None,
        "product_count": 0,
        "payload": None,
    }
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=TIMEOUT,
        )
        record["http_status"] = resp.status_code
        resp.raise_for_status()
        data = resp.json()
        products = data.get("products", [])
        record["product_count"] = len(products)
        record["payload"] = data
        record["ok"] = True
    except Exception as exc:  # noqa: BLE001 - probe records failures, never raises
        record["error"] = f"{type(exc).__name__}: {exc}"
    return record


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    summary = []

    for brand, tier, base_url in SHOPIFY_BRANDS:
        record = probe_shopify(brand, tier, base_url)

        slug = brand.lower().replace(" ", "_").replace(".", "").replace("'", "")
        out = RAW_DIR / f"shopify_{slug}.json"
        with out.open("w", encoding="utf-8") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=2)

        summary.append(
            {
                "brand": brand,
                "tier": tier,
                "status": record["http_status"],
                "ok": record["ok"],
                "products": record["product_count"],
                "error": record["error"],
            }
        )
        flag = "ok" if record["ok"] else "FAIL"
        print(
            f"{flag:>4}  {brand:<26} {tier:<10} "
            f"status={record['http_status']} products={record['product_count']}"
            + (f"  {record['error']}" if record["error"] else "")
        )
        time.sleep(REQUEST_DELAY)

    with (RAW_DIR / "_probe_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(
            {"probed_at": utcnow(), "user_agent": USER_AGENT, "results": summary},
            fh,
            ensure_ascii=False,
            indent=2,
        )

    reached = sum(1 for s in summary if s["ok"])
    total_products = sum(s["products"] for s in summary)
    print(f"\nreached {reached}/{len(summary)} brands, {total_products} products retrieved")


if __name__ == "__main__":
    main()
