"""Stage 1.0: quantity coverage by market tier and by brand within tier.

Reads the raw probe responses already on disk. No new requests.

"Quantity present" means a plausible size token appears in a structured-ish
slot - variant title, product options, or product title. Body/description
text is reported separately and NOT counted, because a size in prose may
describe a different product (a bundle component, a recommendation).

Same plausibility rules as feasibility_pdp_analyse.py, so the numbers are
comparable.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "feasibility"

SIZE_RE = re.compile(
    r"(?<![\w.])"
    r"(\d{1,3}(?:\.\d{1,2})?)"
    r"\s?"
    r"(fl\.?\s?oz\.?|oz\.?|mL|ml|mg|g)"
    r"(?![\w])"
)
PLAUSIBLE = {"g": (0.05, 500), "mg": (1, 5000), "ml": (0.5, 500), "oz": (0.01, 20), "floz": (0.01, 20)}
TAG_RE = re.compile(r"<[^>]+>")

TIER_ORDER = ["drugstore", "mid_range", "high_end", "luxury"]


def norm_unit(u: str) -> str:
    u = u.lower().replace(".", "").replace(" ", "")
    if u.startswith("floz"):
        return "floz"
    return {"oz": "oz", "ml": "ml", "mg": "mg"}.get(u, "g")


def has_size(text: str | None) -> bool:
    if not text:
        return False
    for m in SIZE_RE.finditer(text):
        unit = norm_unit(m.group(2))
        lo, hi = PLAUSIBLE[unit]
        try:
            if lo <= float(m.group(1)) <= hi:
                return True
        except ValueError:
            continue
    return False


def load_rows() -> list[dict]:
    rows = []
    for path in sorted(RAW_DIR.glob("shopify_*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        if not rec.get("ok"):
            continue
        for p in rec["payload"].get("products", []):
            variants = p.get("variants") or []
            options = p.get("options") or []
            vtitles = " ".join(str(v.get("title") or "") for v in variants)
            otext = " ".join(str(v) for o in options for v in (o.get("values") or []))
            body = TAG_RE.sub(" ", p.get("body_html") or "")
            structured = has_size(vtitles) or has_size(otext) or has_size(p.get("title"))
            rows.append(
                {
                    "brand": rec["source_name"],
                    "tier": rec["market_tier"],
                    "q_structured": structured,
                    "q_body_only": (not structured) and has_size(body),
                }
            )
    return rows


def pct(c: int, n: int) -> str:
    return f"{c / n * 100:5.1f}%" if n else "  n/a"


def main() -> None:
    rows = load_rows()
    n_all = len(rows)
    print(f"products: {n_all}\n")

    print("QUANTITY COVERAGE BY TIER  (structured slot = variant/options/title)")
    print(f"{'tier':<11}{'n':>6}{'with qty':>10}{'coverage':>10}{'body-only':>11}")
    print("-" * 48)
    tier_tot = {}
    for t in TIER_ORDER:
        rs = [r for r in rows if r["tier"] == t]
        c = sum(r["q_structured"] for r in rs)
        b = sum(r["q_body_only"] for r in rs)
        tier_tot[t] = (len(rs), c)
        print(f"{t:<11}{len(rs):>6}{c:>10}{pct(c, len(rs)):>10}{b:>11}")
    c_all = sum(r["q_structured"] for r in rows)
    print("-" * 48)
    print(f"{'all':<11}{n_all:>6}{c_all:>10}{pct(c_all, n_all):>10}")

    print("\nDRUGSTORE - COVERAGE BY BRAND")
    print(f"{'brand':<22}{'n':>6}{'with qty':>10}{'coverage':>10}{'body-only':>11}")
    print("-" * 59)
    ds = [r for r in rows if r["tier"] == "drugstore"]
    for brand in sorted({r["brand"] for r in ds}):
        rs = [r for r in ds if r["brand"] == brand]
        c = sum(r["q_structured"] for r in rs)
        b = sum(r["q_body_only"] for r in rs)
        print(f"{brand:<22}{len(rs):>6}{c:>10}{pct(c, len(rs)):>10}{b:>11}")

    print("\nNON-DRUGSTORE - COVERAGE BY BRAND")
    print(f"{'brand':<24}{'tier':<11}{'n':>6}{'with qty':>10}{'coverage':>10}")
    print("-" * 61)
    nd = [r for r in rows if r["tier"] != "drugstore"]
    brands = sorted({(r["tier"], r["brand"]) for r in nd}, key=lambda x: (TIER_ORDER.index(x[0]), x[1]))
    for tier, brand in brands:
        rs = [r for r in nd if r["brand"] == brand]
        c = sum(r["q_structured"] for r in rs)
        print(f"{brand:<24}{tier:<11}{len(rs):>6}{c:>10}{pct(c, len(rs)):>10}")

    # Excluding the two brands that drive the non-drugstore number.
    nd_ex = [r for r in nd if r["brand"] not in ("MAC", "Tom Ford Beauty")]
    c = sum(r["q_structured"] for r in nd_ex)
    print(f"\nnon-drugstore EXCLUDING MAC and Tom Ford: {c}/{len(nd_ex)} ({pct(c, len(nd_ex)).strip()})")

    def summ(rs: list[dict]) -> dict:
        c = sum(r["q_structured"] for r in rs)
        b = sum(r["q_body_only"] for r in rs)
        return {
            "n": len(rs),
            "with_quantity": c,
            "body_only": b,
            "coverage": round(c / len(rs), 4) if rs else None,
        }

    by_brand: dict[str, dict] = {}
    for tier in TIER_ORDER:
        for brand in sorted({r["brand"] for r in rows if r["tier"] == tier}):
            by_brand[brand] = {"tier": tier, **summ([r for r in rows if r["brand"] == brand])}

    out = {
        "method": "strict: a plausible size token in a variant title, option value or "
                  "product title counts; body text is reported as body_only and not counted",
        "by_tier": {t: summ([r for r in rows if r["tier"] == t]) for t in TIER_ORDER},
        "by_brand": by_brand,
        "non_drugstore_excluding_mac_and_tom_ford": summ(nd_ex),
        "all": summ(rows),
    }
    (RAW_DIR / "_tier_breakdown.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
