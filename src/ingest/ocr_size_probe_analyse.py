"""Stage 1.1 task 1.1-B2: read the saved OCR output and report the hit rate
with its error modes.

    python src/ingest/ocr_size_probe_analyse.py

Reads data/raw/capture/ocr/*.json, written by ocr_size_probe.py. No OCR is
re-run and nothing touches the network, so this is reproducible from the
committed files alone. Two hit rates are reported, kept apart:

  primary   the rule the probe ran with - feasibility_pdp_analyse.find_sizes
            on ocr_size_probe.normalise_ocr text - exactly as recorded per
            image at run time. This is the pre-registered number.
  amended   the same saved texts under one extra normalisation written
            AFTER the first outputs were read, so it is post hoc and is
            labelled as such: a size glued to a label word
            ('TOTALNETWT.26.5g', 'NETWT10g') gets a space before the
            number, and a capital O standing in for zero before a decimal
            point ('O.95oz') is read as 0. The per-product token lists
            show exactly which readings the amendment adds.

Error modes, counted per image from the saved text:
  blank      OCR read nothing at all (swatch, model or texture shots)
  small      long side under 900 px, so the tiling pass did not run
  fragment   the text carries a unit or label word (oz, ml, g, fl, net,
             wt) but yields no plausible size under either rule; the
             snippets are listed so a reader can see what was missed

Output: data/raw/capture/_ocr_probe_analysis.json and a printed table.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from feasibility_pdp_analyse import find_sizes
from ocr_size_probe import MIN_LONG_SIDE_FOR_TILES, normalise_ocr

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "data" / "raw" / "capture"
OCR_DIR = CAPTURE / "ocr"
OUT = CAPTURE / "_ocr_probe_analysis.json"

GLUED_LABEL = re.compile(r"(?i)\b(TOTAL\s?NET\s?WT|NET\s?WT|NETWT|NET\s?W|WT|NET)\.?\s?(?=[0-9]|O\.)")
O_FOR_ZERO = re.compile(r"(?<![A-Za-z])O(?=\.\d)")
FRAGMENT = re.compile(r"(?i)(\d\s?(oz|ml|g|gr)\b|\bfl\.?\s?oz|\bnet\b|\bwt\b|\bml\b|\boz\b)")


def amend(text: str) -> str:
    t = GLUED_LABEL.sub(lambda m: m.group(1) + " ", text)
    t = O_FOR_ZERO.sub("0", t)
    return t


def snippets(text: str, width: int = 28) -> list[str]:
    out = []
    for m in FRAGMENT.finditer(text):
        a, b = max(0, m.start() - width), min(len(text), m.end() + width)
        out.append(text[a:b].strip())
    return out[:4]


def main() -> None:
    files = sorted(OCR_DIR.glob("*.json"))
    if not files:
        raise SystemExit("no OCR output - run ocr_size_probe.py first")

    rows = []
    for path in files:
        d = json.loads(path.read_text(encoding="utf-8"))
        primary, amended, images = set(), set(), []
        for im in d["per_image"]:
            if "error" in im:
                images.append({"index": im["index"], "error": im["error"]})
                continue
            texts = im.get("text", {})
            joined = " ".join(t for t in texts.values() if not t.startswith("!!"))
            p_tokens = sorted({h["token"] for h in im.get("hits", [])})
            a_tokens = sorted({tok for t in texts.values() if not t.startswith("!!")
                               for tok in find_sizes(normalise_ocr(amend(t)))})
            primary.update(p_tokens)
            amended.update(a_tokens)
            long_side = max(im.get("size") or [0, 0])
            blank = not joined.strip()
            frags = snippets(joined) if (not a_tokens and FRAGMENT.search(joined)) else []
            images.append({
                "index": im["index"],
                "long_side_px": long_side,
                "blank": blank,
                "small": long_side < MIN_LONG_SIDE_FOR_TILES,
                "primary_tokens": p_tokens,
                "amended_tokens": a_tokens,
                "fragments": frags,
            })
        rows.append({
            "sample_rank": d["sample_rank"],
            "brand": d["brand"],
            "handle": d["handle"],
            "category_guess": d["category_guess"],
            "images_ok": d["images_ok"],
            "primary_hit": bool(primary),
            "amended_hit": bool(amended),
            "primary_tokens": sorted(primary),
            "amended_tokens": sorted(amended),
            "blank_images": sum(1 for i in images if i.get("blank")),
            "small_images": sum(1 for i in images if i.get("small")),
            "fragment_images": sum(1 for i in images if i.get("fragments")),
            "images": images,
        })
    rows.sort(key=lambda r: r["sample_rank"])

    n = len(rows)
    p = sum(r["primary_hit"] for r in rows)
    a = sum(r["amended_hit"] for r in rows)
    all_images = [i for r in rows for i in r["images"] if "error" not in i]

    print(f"products with OCR output: {n} of 30 in the pre-registered sample\n")
    print(f"{'#':>2} {'brand':<19}{'category':<18}{'imgs':>4}{'blank':>6}{'small':>6}{'frag':>5}  primary -> amended")
    print("-" * 96)
    for r in rows:
        print(f"{r['sample_rank']:>2} {r['brand'][:18]:<19}{r['category_guess'][:17]:<18}{r['images_ok']:>4}"
              f"{r['blank_images']:>6}{r['small_images']:>6}{r['fragment_images']:>5}  "
              f"{'HIT' if r['primary_hit'] else '.  '} {r['primary_tokens'][:3]} -> "
              f"{'HIT' if r['amended_hit'] else '.  '} {r['amended_tokens'][:3]}")
    print("-" * 96)
    print(f"primary (pre-registered rule): {p}/{n} = {p / n:.1%}")
    print(f"amended (post hoc, labelled):  {a}/{n} = {a / n:.1%}")
    print(f"images: {len(all_images)} read; blank {sum(i['blank'] for i in all_images)}; "
          f"small {sum(i['small'] for i in all_images)}; with fragments and no size "
          f"{sum(1 for i in all_images if i['fragments'])}")

    print("\nFRAGMENTS - unit or label words with no plausible size under either rule:")
    for r in rows:
        for i in r["images"]:
            for s in i.get("fragments", []):
                print(f"  #{r['sample_rank']:<3}{r['brand'][:14]:<15}img {i['index']}: {s!r}")

    by_brand: dict[str, dict] = {}
    for r in rows:
        b = by_brand.setdefault(r["brand"], {"n": 0, "primary": 0, "amended": 0})
        b["n"] += 1
        b["primary"] += r["primary_hit"]
        b["amended"] += r["amended_hit"]

    out = {
        "source": "data/raw/capture/ocr/*.json from ocr_size_probe.py; no OCR re-run",
        "sample": "data/raw/capture/ocr_test_sample.csv (30 products, pre-registered)",
        "n_products_with_output": n,
        "primary": {"rule": "find_sizes(normalise_ocr(text)) as run", "hits": p,
                    "hit_rate": round(p / n, 4)},
        "amended": {"rule": "post hoc: space after a glued NET WT label; O-for-0 before a decimal",
                    "hits": a, "hit_rate": round(a / n, 4)},
        "threshold_from_plan": 0.40,
        "images": {
            "read": len(all_images),
            "blank": sum(i["blank"] for i in all_images),
            "small_no_tiling": sum(i["small"] for i in all_images),
            "fragment_no_size": sum(1 for i in all_images if i["fragments"]),
        },
        "by_brand": by_brand,
        "rows": rows,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
