"""Stage 1.1 task 1.1-B2: can OCR read net quantity off storefront product images?

    python src/ingest/ocr_size_probe.py [--max-minutes 25] [--max-images 6]

For each product in the pre-registered OCR sample
(data/raw/capture/ocr_test_sample.csv) this script:

  1. downloads the product images the storefront catalogue lists (brand
     CDN, already referenced in data/raw/; images are git-ignored and
     re-downloadable; a provenance sidecar per product records every
     fetch);
  2. runs RapidOCR on each image twice - the full frame, and a 2x2 grid
     of overlapping tiles so small print on packaging is not lost to the
     detector's downscaling;
  3. applies the strict size rule (imported from feasibility_pdp_analyse,
     the same rule as every other coverage figure in this project) to the
     recognised text, after a small OCR-specific normalisation that is
     printed alongside each hit;
  4. writes per-product OCR output to data/raw/capture/ocr/ and a summary
     to data/raw/capture/_ocr_probe_summary.json.

Hit rate = products with at least one image yielding a plausible size
token. Tokens are recorded for later verification, not used as data.

Bounded like every external call in this project: per-request timeouts,
a wall-clock cap on the whole run, no retries, resume from files already
on disk.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import requests
from PIL import Image

from feasibility_pdp_analyse import find_sizes

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "data" / "raw" / "capture"
SAMPLE_CSV = CAPTURE / "ocr_test_sample.csv"
IMG_DIR = CAPTURE / "images"
OCR_DIR = CAPTURE / "ocr"
SUMMARY = CAPTURE / "_ocr_probe_summary.json"
USER_AGENT = "beauty-value-intelligence/0.1 (Stage 1.1 OCR feasibility test)"

MIN_LONG_SIDE_FOR_TILES = 900
TILE_OVERLAP = 0.15
ROW_FIELDS = ["sample_rank", "brand", "handle", "title", "category_guess", "images_listed",
              "images_ok", "images_with_hit", "hit", "tokens"]


def normalise_ocr(text: str) -> str:
    """OCR-specific normalisation, deliberately narrow.

    Packaging prints units in capitals ('NET WT 0.28 OZ', '30 ML', 'FL OZ')
    and OCR confuses a capital O with zero ('0Z'). The strict rule is
    case-sensitive on purpose (to reject '5G' identifiers on web pages), so
    these forms are lowered here - only these, only after a number.
    """
    t = re.sub(r"(\d)\s?[O0]Z\b", r"\1 oz", text)
    t = re.sub(r"(\d)\s?FL\.?\s?[O0]Z\b", r"\1 fl oz", t)
    t = re.sub(r"\bFL\.?\s?[O0]Z\b", "fl oz", t)
    t = re.sub(r"(\d)\s?ML\b", r"\1 ml", t)
    t = re.sub(r"(\d),(\d{1,2})\s?(ml|g|oz|fl oz)\b", r"\1.\2 \3", t)
    return t


def ocr_engine():
    from rapidocr_onnxruntime import RapidOCR
    try:
        return RapidOCR(det_limit_side_len=1600, det_limit_type="max"), "det_limit_side_len=1600"
    except Exception:  # noqa: BLE001 - kwarg support is version-dependent; tiling covers small print
        return RapidOCR(), "default detector limits; 2x2 tiling compensates"


def run_ocr(engine, img) -> list[tuple[str, float]]:
    result, _ = engine(img)
    if not result:
        return []
    return [(str(r[1]), float(r[2])) for r in result]


def tiles(im: Image.Image) -> list[tuple[str, Image.Image]]:
    w, h = im.size
    if max(w, h) < MIN_LONG_SIDE_FOR_TILES:
        return []
    tw, th = int(w * (0.5 + TILE_OVERLAP)), int(h * (0.5 + TILE_OVERLAP))
    out = []
    for i, x in enumerate((0, w - tw)):
        for j, y in enumerate((0, h - th)):
            out.append((f"tile{i}{j}", im.crop((x, y, x + tw, y + th))))
    return out


def to_bgr(im: Image.Image) -> np.ndarray:
    return np.array(im.convert("RGB"))[:, :, ::-1].copy()


def download(url: str, dest: Path) -> dict:
    rec = {"source_url": url, "collected_at": datetime.now(timezone.utc).isoformat(),
           "method": "http_get", "file": dest.name}
    if dest.exists():
        rec.update(http_status=None, bytes=dest.stat().st_size, reused=True)
        return rec
    try:
        r = requests.get(url, timeout=(10, 30), headers={"User-Agent": USER_AGENT})
        rec["http_status"] = r.status_code
        if r.status_code == 200 and r.content:
            dest.write_bytes(r.content)
            rec["bytes"] = len(r.content)
        else:
            rec["error"] = f"http {r.status_code}"
    except requests.RequestException as exc:
        rec["http_status"] = 0
        rec["error"] = f"transport: {type(exc).__name__}"
    return rec


def ext_of(url: str) -> str:
    path = url.split("?")[0].lower()
    for e in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
        if path.endswith(e):
            return e
    return ".img"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-minutes", type=float, default=25.0)
    ap.add_argument("--max-images", type=int, default=6)
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)
    deadline = time.monotonic() + args.max_minutes * 60

    with SAMPLE_CSV.open(encoding="utf-8", newline="") as fh:
        sample = list(csv.DictReader(fh))
    print(f"sample: {len(sample)} products from {SAMPLE_CSV.relative_to(ROOT)}")

    engine, engine_note = ocr_engine()
    print(f"engine: RapidOCR ({engine_note})")
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    OCR_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    started = datetime.now(timezone.utc).isoformat()
    try:
        for p in sample:
            if time.monotonic() > deadline:
                print(f"!! run cap of {args.max_minutes} min reached; stopping", flush=True)
                break
            key = re.sub(r"[^a-z0-9]+", "_", p["brand"].lower()) + "__" + p["handle"]
            out_path = OCR_DIR / f"{key}.json"
            if out_path.exists():
                prev = json.loads(out_path.read_text(encoding="utf-8"))
                rows.append({k: prev[k] for k in ROW_FIELDS})
                print(f"  {prev['sample_rank']:>2} {prev['brand'][:18]:<18} reused {out_path.name}")
                continue
            pdir = IMG_DIR / key
            pdir.mkdir(exist_ok=True)
            urls = [u for u in p["image_urls"].split("|") if u][: args.max_images]
            fetches, images = [], []
            for i, url in enumerate(urls):
                dest = pdir / f"{i:02d}{ext_of(url)}"
                rec = download(url, dest)
                fetches.append(rec)
                if "error" not in rec:
                    images.append((i, url, dest))
                if not rec.get("reused"):
                    time.sleep(0.5)
            (pdir / "_provenance.json").write_text(
                json.dumps({"product": p, "fetches": fetches}, indent=2, ensure_ascii=False),
                encoding="utf-8")

            per_image = []
            for i, url, dest in images:
                try:
                    im = Image.open(dest)
                    im.load()
                except Exception as exc:  # noqa: BLE001
                    per_image.append({"index": i, "url": url, "error": f"decode: {type(exc).__name__}"})
                    continue
                passes = [("full", str(dest))] + [(name, to_bgr(t)) for name, t in tiles(im)]
                hits, texts = [], {}
                for name, img in passes:
                    try:
                        lines = run_ocr(engine, img)
                    except Exception as exc:  # noqa: BLE001
                        texts[name] = f"!! ocr error: {type(exc).__name__}"
                        continue
                    text = " ".join(t for t, _ in lines)
                    texts[name] = text
                    for token in find_sizes(normalise_ocr(text)):
                        hits.append({"pass": name, "token": token})
                per_image.append({"index": i, "url": url, "size": list(im.size),
                                  "hits": hits, "text": texts})

            tokens = sorted({h["token"] for im in per_image for h in im.get("hits", [])})
            row = {
                "sample_rank": int(p["sample_rank"]),
                "brand": p["brand"],
                "handle": p["handle"],
                "title": p["title"],
                "category_guess": p["category_guess"],
                "images_listed": len(urls),
                "images_ok": len(images),
                "images_with_hit": sum(1 for im in per_image if im.get("hits")),
                "hit": bool(tokens),
                "tokens": tokens,
            }
            rows.append(row)
            out_path.write_text(
                json.dumps({**row, "per_image": per_image}, indent=2, ensure_ascii=False),
                encoding="utf-8")
            print(f"  {row['sample_rank']:>2} {row['brand'][:18]:<18} imgs={row['images_ok']}/{row['images_listed']} "
                  f"hit_imgs={row['images_with_hit']} {'HIT ' if row['hit'] else '.   '}{tokens[:4]}")
    finally:
        n = len(rows)
        hits = sum(r["hit"] for r in rows)
        by_brand: dict[str, list[int]] = {}
        for r in rows:
            by_brand.setdefault(r["brand"], [0, 0])
            by_brand[r["brand"]][0] += r["hit"]
            by_brand[r["brand"]][1] += 1
        summary = {
            "started_at": started,
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "engine": f"rapidocr_onnxruntime ({engine_note}); full frame + 2x2 tiles with {TILE_OVERLAP:.0%} overlap",
            "size_rule": "feasibility_pdp_analyse.find_sizes after normalise_ocr (OZ/FL OZ/ML case, O-for-0, comma decimals)",
            "max_images_per_product": args.max_images,
            "n_products": n,
            "products_with_hit": hits,
            "hit_rate": round(hits / n, 4) if n else None,
            "images_ok": sum(r["images_ok"] for r in rows),
            "images_with_hit": sum(r["images_with_hit"] for r in rows),
            "by_brand": {b: {"hits": v[0], "n": v[1]} for b, v in sorted(by_brand.items())},
            "rows": rows,
        }
        SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nproducts with at least one plausible size token: {hits}/{n}"
              + (f" ({hits / n:.0%})" if n else ""))
        print("by brand:", {b: f"{v[0]}/{v[1]}" for b, v in sorted(by_brand.items())})
        print(f"summary -> {SUMMARY.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
