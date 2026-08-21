"""Stage 1.0: strict re-measurement of size presence on saved product pages.

The first pass regexed raw HTML and produced false positives from minified JS
and CSS ("029g", "0MG", "5Ml", "7G"). Those are hash and identifier fragments,
not sizes. Counting them would fabricate coverage.

This pass:
  - drops <script>, <style>, <noscript> before looking at anything
  - reads visible text only
  - requires a plausible size shape and a plausible magnitude
  - reports JSON-LD and <meta> separately, since structured placement is more
    trustworthy than prose

Still measurement only. No parsing, no normalisation.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "feasibility"
PDP_DIR = RAW_DIR / "pdp"

# A plausible printed size: number, optional space, unit, hard word boundary.
# Unit case is respected for g/mg/ml to avoid matching "5G" style identifiers.
SIZE_RE = re.compile(
    r"(?<![\w.])"
    r"(\d{1,3}(?:\.\d{1,2})?)"
    r"\s?"
    r"(fl\.?\s?oz\.?|oz\.?|mL|ml|mg|g)"
    r"(?![\w])"
)

# Magnitude sanity, mirroring config/unit_rules.yaml sanity_ranges.
PLAUSIBLE = {
    "g": (0.05, 500),
    "mg": (1, 5000),
    "ml": (0.5, 500),
    "ml_alt": (0.5, 500),
    "oz": (0.01, 20),
    "floz": (0.01, 20),
}


def norm_unit(u: str) -> str:
    u = u.lower().replace(".", "").replace(" ", "")
    if u.startswith("floz"):
        return "floz"
    if u == "oz":
        return "oz"
    if u == "ml":
        return "ml"
    if u == "mg":
        return "mg"
    return "g"


def plausible(value: str, unit: str) -> bool:
    try:
        v = float(value)
    except ValueError:
        return False
    lo, hi = PLAUSIBLE.get(unit, (0.01, 500))
    return lo <= v <= hi


def find_sizes(text: str) -> list[str]:
    out = []
    for m in SIZE_RE.finditer(text):
        val, unit_raw = m.group(1), m.group(2)
        unit = norm_unit(unit_raw)
        if plausible(val, unit):
            out.append(f"{val} {unit_raw.strip()}")
    return out


def main() -> None:
    files = sorted(PDP_DIR.glob("*.html"))
    if not files:
        raise SystemExit("no saved PDPs - run feasibility_pdp_probe.py first")

    rows = []
    for path in files:
        html = path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(html, "lxml")

        jsonld_hits = []
        for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
            jsonld_hits += find_sizes(tag.get_text() or "")

        meta_hits = []
        for tag in soup.find_all("meta"):
            content = tag.get("content") or ""
            if content:
                meta_hits += find_sizes(content)

        for bad in soup(["script", "style", "noscript"]):
            bad.decompose()
        visible = soup.get_text(" ", strip=True)
        visible_hits = find_sizes(visible)

        brand = path.name.split("__")[0].replace("_", " ").title()
        rows.append(
            {
                "file": path.name,
                "brand": brand,
                "visible": sorted(set(visible_hits))[:6],
                "jsonld": sorted(set(jsonld_hits))[:6],
                "meta": sorted(set(meta_hits))[:6],
                "has_visible": bool(visible_hits),
                "has_jsonld": bool(jsonld_hits),
            }
        )

    n = len(rows)
    print(f"pages analysed: {n}\n")
    print(f"{'brand':<26} {'vis':<4} {'ld':<4} sizes found in visible text")
    print("-" * 96)
    for r in rows:
        print(
            f"{r['brand'][:25]:<26} "
            f"{'Y' if r['has_visible'] else '.':<4} "
            f"{'Y' if r['has_jsonld'] else '.':<4} "
            f"{r['visible']}"
        )

    vis = sum(1 for r in rows if r["has_visible"])
    ld = sum(1 for r in rows if r["has_jsonld"])
    print("-" * 96)
    print(f"size in visible page text : {vis}/{n} ({vis / n * 100:.1f}%)")
    print(f"size in JSON-LD           : {ld}/{n} ({ld / n * 100:.1f}%)")

    by_brand: dict[str, list] = {}
    for r in rows:
        by_brand.setdefault(r["brand"], []).append(r)
    print("\nby brand (visible text):")
    for b, rs in sorted(by_brand.items()):
        c = sum(1 for r in rs if r["has_visible"])
        print(f"  {b:<26} {c}/{len(rs)}")

    with (RAW_DIR / "_pdp_strict_analysis.json").open("w", encoding="utf-8") as fh:
        json.dump(rows, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
