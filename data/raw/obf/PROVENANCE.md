# Open Beauty Facts exports — provenance

Both files are git-ignored (large, ODbL-licensed, re-downloadable). They were
downloaded by hand by the project owner on 2026-08-26 and placed here. Nothing
in this repository fetches from the Open Beauty Facts hosts.

| File | Bytes | Canonical location | Data as of |
| --- | ---: | --- | --- |
| `beauty.parquet` | 59,406,016 | Hugging Face dataset `openfoodfacts/product-database`, file `beauty.parquet` | newest edit in file: 2026-08-24 |
| `en.openbeautyfacts.org.products.csv` | 167,614,987 | Open Beauty Facts bulk CSV export (tab-separated) | newest edit in file: 2026-05-07; server file date 2026-05-08 |

Verification performed on 2026-08-26:

- The Hugging Face datasets-server `size` endpoint reports the `beauty` split
  at 73,747 rows and 59,406,016 Parquet bytes. The local file has exactly
  that byte size and exactly that row count.
- The CSV export is a snapshot roughly 3.5 months older than the Parquet.
  The row-count difference between flavours is snapshot age, not
  truncation; see the integrity section of
  `reports/source_feasibility_report.md`.

Licence: Open Database License (ODbL) for the database, Database Contents
License for individual contents. Attribution: Open Beauty Facts contributors.

Measurement: `python src/ingest/obf_feasibility.py --parquet data/raw/obf/beauty.parquet --csv data/raw/obf/en.openbeautyfacts.org.products.csv --site-total 73747 --total-source "Hugging Face datasets-server size endpoint, 2026-08-26"`
