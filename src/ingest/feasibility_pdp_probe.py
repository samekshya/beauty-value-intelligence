"""Stage 1.0 follow-up probe: is size on the product detail page?

products.json showed 0% size coverage for drugstore brands. That result is
ambiguous: for a single-size product the Shopify variant title carries the
SHADE, not the size, so absence there does not mean the brand withholds size.

This probe fetches a small sample of product detail pages and checks whether a
size token appears in the page HTML at all. It distinguishes:
  - size in a JSON-LD / structured block
  - size anywhere in the rendered HTML

Small sample, conservative delay. Measurement only.
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

USER_AGENT = "beauty-value-intelligence/0.1 (Stage 1.0 source feasibility study)"
REQUEST_DELAY = 3.0
TIMEOUT = 30
SAMPLE_PER_BRAND = 3

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "feasibility"
OUT_DIR = RAW_DIR / "pdp"

SIZE_RE = re.compile(
    r"\d+(?:[.,]\d+)?\s*(?:fl\.?\s*oz|floz|oz|ml|mL|g\b|gr\b|gram|mg)",
    re.IGNORECASE,
)

# Brands that returned 0% size in products.json.
TARGET_BRANDS = {
    "Milani": "https://www.milanicosmetics.com",
    "Essence": "https://essencemakeup.com",
    "Wet n Wild": "https://www.wetnwildbeauty.com",
    "ColourPop": "https://colourpop.com",
    "Physicians Formula": "https://www.physiciansformula.com",
    "Anastasia Beverly Hills": "https://www.anastasiabeverlyhills.com",
    "Saie": "https://saiehello.com",
}

# Skip obvious non-single-item listings when sampling.
SKIP_WORDS = ("bundle", "set", "kit", "gift", "duo", "trio", "collection")


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def pick_handles(brand: str) -> list[str]:
    slug = brand.lower().replace(" ", "_").replace(".", "").replace("'", "")
    path = RAW_DIR / f"shopify_{slug}.json"
    if not path.exists():
        return []
    rec = json.loads(path.read_text(encoding="utf-8"))
    handles = []
    for p in rec["payload"].get("products", []):
        title = (p.get("title") or "").lower()
        if any(w in title for w in SKIP_WORDS):
            continue
        if p.get("handle"):
            handles.append(p["handle"])
        if len(handles) >= SAMPLE_PER_BRAND:
            break
    return handles


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    for brand, base in TARGET_BRANDS.items():
        for handle in pick_handles(brand):
            url = f"{base}/products/{handle}"
            row = {
                "brand": brand,
                "handle": handle,
                "source_url": url,
                "collected_at": utcnow(),
                "http_status": None,
                "size_in_html": False,
                "size_in_jsonld": False,
                "matches": [],
                "error": None,
            }
            try:
                resp = requests.get(
                    url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT
                )
                row["http_status"] = resp.status_code
                resp.raise_for_status()
                html = resp.text

                found = SIZE_RE.findall(html)
                # findall with non-capturing groups returns full matches
                all_matches = [m.group(0) for m in SIZE_RE.finditer(html)]
                row["size_in_html"] = bool(all_matches)
                row["matches"] = sorted(set(all_matches))[:12]

                for block in re.findall(
                    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
                    html,
                    re.DOTALL | re.IGNORECASE,
                ):
                    if SIZE_RE.search(block):
                        row["size_in_jsonld"] = True
                        break

                slug = f"{brand.lower().replace(' ', '_')}__{handle}"[:120]
                (OUT_DIR / f"{slug}.html").write_text(html, encoding="utf-8")
            except Exception as exc:  # noqa: BLE001
                row["error"] = f"{type(exc).__name__}: {exc}"

            results.append(row)
            print(
                f"{brand:<26} {handle[:34]:<34} "
                f"status={row['http_status']} html={row['size_in_html']} "
                f"jsonld={row['size_in_jsonld']} {row['matches'][:5]}"
            )
            time.sleep(REQUEST_DELAY)

    with (RAW_DIR / "_pdp_probe_summary.json").open("w", encoding="utf-8") as fh:
        json.dump(
            {"probed_at": utcnow(), "user_agent": USER_AGENT, "results": results},
            fh,
            ensure_ascii=False,
            indent=2,
        )

    ok = [r for r in results if r["error"] is None]
    if ok:
        hit = sum(1 for r in ok if r["size_in_html"])
        print(f"\nsize token present in HTML: {hit}/{len(ok)} pages")


if __name__ == "__main__":
    main()
