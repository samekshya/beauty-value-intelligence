"""Run the Open Beauty Facts feasibility measurement.

    python src/ingest/obf_feasibility.py [--site-total N] [--selftest]

Executes sql/obf_feasibility.sql statement by statement against DuckDB and
prints every result set. Stops at Part 0 if the export integrity check does
not PASS - nothing downstream is reported on a broken export.

--selftest builds a tiny synthetic Parquet+CSV pair under the scratch
directory and runs the whole script against it, so the SQL is known to
execute before the real file arrives. Synthetic rows are obviously fake
(brand 'TESTBRAND', code '0000…') and never touch data/raw/.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[2]
SQL_PATH = ROOT / "sql" / "obf_feasibility.sql"


def _strip_comment(line: str) -> str:
    """Drop a trailing `--` comment, but only outside single quotes.

    Paths and literals can legitimately contain `--` (this repo's scratch
    directory does), so a naive split corrupts them.
    """
    in_quote = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == "'":
            in_quote = not in_quote
        elif not in_quote and line.startswith("--", i):
            return line[:i].rstrip()
        i += 1
    return line.rstrip()


def split_statements(sql: str) -> list[str]:
    """Split into statements on line-ending semicolons, comment-aware."""
    stmts, buf = [], []
    for line in sql.splitlines():
        code = _strip_comment(line)
        if not code.strip():
            continue
        buf.append(code)
        if code.endswith(";"):
            stmts.append("\n".join(buf)[:-1].strip())
            buf = []
    if buf:
        stmts.append("\n".join(buf).strip())
    return [s for s in stmts if s]


def run(con: duckdb.DuckDBPyConnection, sql: str, stop_on_integrity_fail: bool = True) -> None:
    for stmt in split_statements(sql):
        head = stmt[:70].replace("\n", " ")
        try:
            res = con.execute(stmt)
        except Exception as exc:  # noqa: BLE001
            print(f"\n!! FAILED: {head}\n   {type(exc).__name__}: {exc}")
            sys.exit(2)

        if stmt.lstrip().upper().startswith("SELECT"):
            df = res.fetchdf()
            print(f"\n-- {head}")
            with_pd_opts(lambda: print(df.to_string(index=False)))

            if stop_on_integrity_fail and "obf_integrity" in stmt and "verdict" in df.columns:
                verdict = str(df["verdict"].iloc[0])
                if not verdict.startswith("PASS"):
                    print(f"\n!! EXPORT INTEGRITY: {verdict}")
                    print("   Stopping. Nothing below Part 0 is reported on a suspect export.")
                    sys.exit(3)


def with_pd_opts(fn) -> None:
    import pandas as pd

    with pd.option_context("display.max_columns", None, "display.width", 200,
                           "display.max_colwidth", 60):
        fn()


def build_selftest(tmp: Path) -> tuple[Path, Path]:
    """Synthetic export pair, written by DuckDB itself (no extra deps).

    Obviously fake rows; exercises every code path including list columns.
    """
    pq = tmp / "obf.parquet"
    csv = tmp / "obf.csv"
    con = duckdb.connect()
    con.execute(
        """
        CREATE TABLE fake AS
        SELECT
          lpad(CAST(i AS VARCHAR), 13, '0')                               AS code,
          ['TESTPRODUCT ' || i]                                           AS product_name,
          CASE WHEN i % 5 = 0 THEN 'TESTBRAND Milani' ELSE 'TESTBRAND MAC' END AS brands,
          CASE WHEN i % 4 = 0 THEN '' ELSE '30 ml' END                    AS quantity,
          CASE WHEN i % 4 = 0 THEN '' ELSE '30' END                       AS product_quantity,
          CASE WHEN i % 4 = 0 THEN '' ELSE 'ml' END                       AS product_quantity_unit,
          CASE WHEN i % 3 = 0 THEN ['en:france'] ELSE ['en:united-states'] END AS countries_tags,
          CASE WHEN i % 2 = 0 THEN ['en:make-up','en:lipsticks'] ELSE ['en:shampoos'] END AS categories_tags
        FROM range(1200) t(i)
        """
    )
    con.execute(f"COPY fake TO '{pq.as_posix()}' (FORMAT PARQUET)")
    # CSV flavour: lists flattened, tab-separated, unquoted - like OBF's TSV.
    con.execute(
        f"""
        COPY (
          SELECT code,
                 list_aggregate(product_name, 'string_agg', ',')   AS product_name,
                 brands, quantity, product_quantity, product_quantity_unit,
                 list_aggregate(countries_tags, 'string_agg', ',')  AS countries_tags,
                 list_aggregate(categories_tags, 'string_agg', ',') AS categories_tags
          FROM fake
        ) TO '{csv.as_posix()}' (FORMAT CSV, DELIMITER '\t', HEADER, QUOTE '')
        """
    )
    con.close()
    return pq, csv


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-total", type=int, default=None,
                    help="Route 1 corroboration: product count read from the site")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--parquet", default="data/raw/obf/obf.parquet")
    ap.add_argument("--csv", default="data/raw/obf/obf.csv")
    args = ap.parse_args()

    sql = SQL_PATH.read_text(encoding="utf-8")

    if args.selftest:
        scratch = Path(os.environ.get("SCRATCH_DIR", tempfile.gettempdir())) / "obf_selftest"
        scratch.mkdir(parents=True, exist_ok=True)
        pq, csv = build_selftest(scratch)
        sql = sql.replace("'data/raw/obf/obf.parquet'", f"'{pq.as_posix()}'")
        sql = sql.replace("'data/raw/obf/obf.csv'", f"'{csv.as_posix()}'")
        # self-test must not write to data/staging
        sql = sql.replace("'data/staging/obf_us_makeup.parquet'",
                          f"'{(scratch / 'staging.parquet').as_posix()}'")
        print(f"SELFTEST against synthetic export in {scratch}\n")
    else:
        sql = sql.replace("'data/raw/obf/obf.parquet'", f"'{args.parquet}'")
        sql = sql.replace("'data/raw/obf/obf.csv'", f"'{args.csv}'")
        for p in (args.parquet, args.csv):
            if not (ROOT / p).exists():
                sys.exit(f"missing export: {p}")

    if args.site_total is not None:
        sql = sql.replace("SET VARIABLE site_total   = NULL;",
                          f"SET VARIABLE site_total   = {args.site_total};")

    os.chdir(ROOT)
    con = duckdb.connect()
    run(con, sql)
    print("\ndone.")


if __name__ == "__main__":
    main()
