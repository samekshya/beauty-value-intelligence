-- ============================================================================
-- Open Beauty Facts feasibility measurement
-- Stage 1.0 — runs the moment the export lands in data/raw/obf/
--
-- PURPOSE
--   Measure, not estimate, whether OBF can supply net quantity for US makeup.
--   This is the single open question blocking Stage 1.1.
--
-- INPUTS  (place in data/raw/obf/ — filenames are parameters below)
--   Route 2, primary:   Parquet export   -> obf.parquet
--                       CSV export       -> obf.csv
--   Route 1, corroboration: a product count from outside the files - read
--                           from the site by hand, or the row count the
--                           publisher advertises for the same export.
--
-- RUN ORDER
--   Part 0 must pass before anything in Parts 1-4 is believed.
--   Users have reported OBF exports arriving truncated (a CSV under 1,000
--   rows, JSONL dropping from ~4M to ~0.7M across days). A low fill rate
--   measured on a broken export is a finding about the export, not the
--   database. Part 0 exists so that mistake cannot be made silently.
--
-- SCHEMA ASSUMPTIONS  (from the Open Food Facts Parquet schema on Hugging
--   Face, read 2026-08-22; OBF shares the Product Opener schema. Verified
--   against the actual file in Part 0.4 — if a column is missing, stop.)
--     code                   string   barcode, EAN-13 / UPC-A
--     product_name           text
--     brands                 string   comma-separated free text
--     quantity               string   RAW label text, e.g. "30 ml", "0.14 oz / 4 g"
--     product_quantity       string   PRE-PARSED numeric as text, e.g. "30"
--     product_quantity_unit  string   unit for product_quantity, e.g. "ml"
--     countries_tags         list     e.g. ['en:united-states', 'en:france']
--     categories_tags        list     e.g. ['en:lipsticks', 'en:make-up']
--
-- The two quantity fields are measured SEPARATELY. product_quantity is the
-- structured one; quantity is the embedded one the §27-31 parser would eat.
-- Their disagreement rate is itself a data-quality finding.
-- ============================================================================

-- Parameters ------------------------------------------------------------------
SET VARIABLE parquet_path = 'data/raw/obf/obf.parquet';
SET VARIABLE csv_path     = 'data/raw/obf/obf.csv';
SET VARIABLE site_total   = NULL;   -- Route 1: fill in the count read from the site
SET VARIABLE tolerance    = 0.05;   -- 5% disagreement between flavours = suspect


-- ============================================================================
-- PART 0 — EXPORT INTEGRITY.  Nothing below is trusted until this passes.
-- ============================================================================

-- 0.1  Row counts per flavour. Loaded as raw text to avoid type-coercion
--      failures hiding rows.
CREATE OR REPLACE TABLE obf_parquet AS
  SELECT * FROM read_parquet(getvariable('parquet_path'));

CREATE OR REPLACE TABLE obf_csv AS
  SELECT * FROM read_csv(
    getvariable('csv_path'),
    delim = '\t',            -- OBF CSV exports are tab-separated
    header = true,
    all_varchar = true,      -- no coercion; we are counting, not typing
    ignore_errors = false,   -- a malformed row is a finding, not noise
    quote = ''               -- OBF TSV is unquoted; fields may contain "
  );

-- 0.2  Flavour agreement. This is Route 2: no external number required.
--      Exception: exports are generated on different schedules, so a fresh
--      flavour can legitimately out-count a stale one. That disagreement is
--      downgraded to WARN only when the csv is at least 30 days staler AND
--      an external total (Route 1) agrees with the parquet. Otherwise FAIL.
CREATE OR REPLACE VIEW obf_integrity AS
WITH c AS (
  SELECT
    (SELECT count(*) FROM obf_parquet)                         AS parquet_rows,
    (SELECT count(*) FROM obf_csv)                             AS csv_rows,
    (SELECT count(DISTINCT code) FROM obf_parquet)             AS parquet_distinct_codes,
    (SELECT count(DISTINCT code) FROM obf_csv)                 AS csv_distinct_codes,
    (SELECT max(last_modified_t) FROM obf_parquet)             AS parquet_last_edit_t,
    (SELECT max(try_cast(last_modified_t AS BIGINT)) FROM obf_csv)
                                                               AS csv_last_edit_t,
    getvariable('site_total')                                  AS site_total
), d AS (
  SELECT
    parquet_rows, csv_rows, parquet_distinct_codes, csv_distinct_codes, site_total,
    to_timestamp(parquet_last_edit_t)::DATE                    AS parquet_last_edit,
    to_timestamp(csv_last_edit_t)::DATE                        AS csv_last_edit,
    ((parquet_last_edit_t - csv_last_edit_t) // 86400)::INTEGER
                                                               AS snapshot_gap_days,
    abs(parquet_rows - csv_rows) * 1.0 / greatest(parquet_rows, csv_rows)
                                                               AS flavour_disagreement,
    CASE WHEN site_total IS NULL THEN NULL
         ELSE abs(parquet_rows - site_total) * 1.0 / site_total END
                                                               AS external_disagreement
  FROM c
)
SELECT
  *,
  CASE
    WHEN least(parquet_rows, csv_rows) < 1000
      THEN 'FAIL: a flavour has under 1,000 rows - truncated export'
    WHEN external_disagreement > getvariable('tolerance')
      THEN 'FAIL: parquet disagrees with the external total by more than tolerance'
    WHEN flavour_disagreement > getvariable('tolerance')
         AND external_disagreement IS NOT NULL
         AND snapshot_gap_days >= 30
      THEN 'WARN: flavours disagree, but the csv is a stale snapshot (see snapshot_gap_days) and the parquet matches the external total - proceeding on the parquet only'
    WHEN flavour_disagreement > getvariable('tolerance')
      THEN 'FAIL: flavours disagree by more than tolerance and nothing explains it - re-download both'
    WHEN parquet_distinct_codes < parquet_rows * 0.95
      THEN 'WARN: >5% duplicate barcodes in parquet - check before trusting'
    ELSE 'PASS'
  END AS verdict
FROM d;


SELECT * FROM obf_integrity;

-- 0.3  Overlap. Two complete exports of the same database should share
--      nearly every barcode. Low overlap = at least one is partial.
SELECT
  count(*)                                                     AS codes_in_both,
  (SELECT count(DISTINCT code) FROM obf_parquet)               AS parquet_codes,
  (SELECT count(DISTINCT code) FROM obf_csv)                   AS csv_codes,
  count(*) * 1.0 / (SELECT count(DISTINCT code) FROM obf_parquet)
                                                               AS share_of_parquet_in_csv
FROM (SELECT code FROM obf_parquet INTERSECT SELECT code FROM obf_csv);

-- 0.4  Required columns present. A missing column here means the schema
--      assumption above is wrong - stop and re-read the file, do not guess.
SELECT
  column_name,
  data_type
FROM information_schema.columns
WHERE table_name = 'obf_parquet'
  AND column_name IN ('code','product_name','brands','quantity',
                      'product_quantity','product_quantity_unit',
                      'countries_tags','categories_tags')
ORDER BY column_name;
-- expect 8 rows. Fewer = stop.


-- ============================================================================
-- PART 1 — SCOPE: identify US makeup in a global cosmetics database
-- ============================================================================
-- Two filters, applied independently and then intersected, so each one's
-- contribution is visible. Both are reported at every stage.
--
-- US:      countries_tags contains 'en:united-states'. This is contributor-
--          entered "where is this sold", not a manufacturer field. It under-
--          counts US products (a US product entered by a French contributor
--          may carry only 'en:france'). Under-counting is the safe direction:
--          it shrinks n, it does not pollute the sample.
--
-- Makeup:  categories_tags contains a tag matching the project's §7 scope.
--          OBF uses a taxonomy with language-prefixed tags; the en: forms
--          below are the ones that map onto config/categories.yaml. Matched
--          on prefix so sub-categories ('en:matte-lipsticks') are included.
--          'en:make-up' alone is too broad (includes brushes, removers) and is
--          NOT used as a sufficient match - it only counts if a specific
--          product-type tag is also present.

CREATE OR REPLACE TABLE obf_scope AS
SELECT
  code,
  product_name,
  brands,
  quantity,
  product_quantity,
  product_quantity_unit,
  countries_tags,
  categories_tags,
  -- US flag
  list_contains(countries_tags, 'en:united-states')            AS is_us,
  -- makeup flag (strict): a tag naming a §7 product type. Tags are
  -- case-folded and space->hyphen normalised first, because contributor
  -- tags outside the taxonomy keep their spelling ('en:Volumizing
  -- mascaras', 'en:Face powders'). Removers, brushes, tools and lash/brow
  -- growth serums are excluded by name. Nail products are not in §7.
  len(list_filter(list_transform(categories_tags, t -> replace(lower(t), ' ', '-')), n ->
     (   n LIKE 'en:foundation%'        OR n LIKE 'en:concealer%'
      OR n LIKE 'en:%blush%'            OR n LIKE 'en:bronzer%'
      OR n LIKE 'en:%highlighter%'      OR n LIKE 'en:face-powder%'
      OR n LIKE 'en:setting-powder%'    OR n LIKE 'en:pressed-powder%'
      OR n LIKE 'en:loose-powder%'      OR n LIKE 'en:compact-powder%'
      OR n LIKE 'en:translucent-powder%' OR n LIKE 'en:make-up-powder%'
      OR n LIKE 'en:lip-liner%'         OR n LIKE 'en:lip-pencil%'
      OR n LIKE 'en:%lipstick%'
      OR n LIKE 'en:lip-gloss%'         OR n LIKE 'en:lipgloss%'
      OR n LIKE 'en:mascara%'           OR n LIKE 'en:%-mascaras'
      OR n LIKE 'en:eyebrow%'           OR n LIKE 'en:brow-%'
      OR n LIKE 'en:primer%'            OR n LIKE 'en:makeup-primer%'
      OR n LIKE 'en:setting-spray%'     OR n LIKE 'en:fixing-spray%'
      OR n LIKE 'en:eyeshadow%'         OR n LIKE 'en:eye-shadow%'
     )
     AND NOT (n LIKE '%remover%' OR n LIKE '%brush%'  OR n LIKE '%growth%'
           OR n LIKE '%treatment%' OR n LIKE '%accessor%' OR n LIKE '%tool%')
  )) > 0                                                       AS is_makeup,
  -- makeup flag (family): an OBF makeup *family* tag - "this is makeup"
  -- without saying which §7 type. Counted as makeup, but such a row needs
  -- name-based classification before it could join a category. Exact
  -- match, not prefix, so 'en:eye-makeup-remover' does not qualify.
  len(list_filter(list_transform(categories_tags, t -> replace(lower(t), ' ', '-')), n ->
        n IN ('en:makeup', 'en:make-up',
              'en:face-makeup', 'en:face-make-up',
              'en:eyes-makeup', 'en:eye-makeup', 'en:eye-make-up',
              'en:lip-makeup', 'en:lip-make-up', 'en:lip-cosmetics')
  )) > 0                                                       AS has_family_tag,
  -- no category at all: the row is invisible to both flags
  categories_tags IS NULL OR len(categories_tags) = 0         AS no_category
FROM obf_parquet;

-- 1.1  Funnel. Every stage reported so the filters can be audited.
SELECT
  count(*)                                                     AS all_rows,
  count(*) FILTER (WHERE is_us)                                AS us_rows,
  count(*) FILTER (WHERE is_makeup)                            AS makeup_rows,
  count(*) FILTER (WHERE has_family_tag)                       AS family_tag_rows,
  count(*) FILTER (WHERE is_makeup OR has_family_tag)          AS makeup_broad_rows,
  count(*) FILTER (WHERE is_makeup AND is_us)                  AS us_makeup_rows,
  count(*) FILTER (WHERE is_us AND (is_makeup OR has_family_tag))
                                                               AS us_makeup_broad_rows,
  count(*) FILTER (WHERE is_us AND no_category)                AS us_rows_without_category
FROM obf_scope;
-- us_rows_without_category: rows no category filter can see. If this is a
-- large share of us_rows, the makeup counts above are a floor, not a count.

-- 1.2  What category tags do US makeup rows actually carry? Needed to map
--      onto config/categories.yaml and to catch stems the filter missed.
SELECT tag, count(*) AS n
FROM obf_scope, unnest(categories_tags) AS u(tag)
WHERE is_us AND (is_makeup OR has_family_tag) AND lower(tag) LIKE 'en:%'
GROUP BY tag
ORDER BY n DESC
LIMIT 60;

-- 1.3  Brands present in US makeup. Cross-check against config/tier_mapping.yaml
--      - this is how many §11 brands OBF can actually serve.
SELECT brands, count(*) AS n
FROM obf_scope
WHERE is_us AND (is_makeup OR has_family_tag)
GROUP BY brands
ORDER BY n DESC
LIMIT 80;


-- ============================================================================
-- PART 2 — QUANTITY FILL RATE.  The number that decides Stage 1.1.
-- ============================================================================

CREATE OR REPLACE VIEW obf_quantity_fill AS
SELECT
  scope,
  n,
  n_raw_quantity,
  round(n_raw_quantity * 100.0 / n, 1)                         AS raw_quantity_pct,
  n_parsed_quantity,
  round(n_parsed_quantity * 100.0 / n, 1)                      AS parsed_quantity_pct,
  n_parsed_with_unit,
  round(n_parsed_with_unit * 100.0 / n, 1)                     AS parsed_with_unit_pct,
  n_either,
  round(n_either * 100.0 / n, 1)                               AS either_pct
FROM (
  SELECT
    scope,
    count(*)                                                                 AS n,
    count(*) FILTER (WHERE nullif(trim(quantity), '') IS NOT NULL)          AS n_raw_quantity,
    count(*) FILTER (WHERE try_cast(product_quantity AS DOUBLE) > 0)        AS n_parsed_quantity,
    count(*) FILTER (WHERE try_cast(product_quantity AS DOUBLE) > 0
                       AND nullif(trim(product_quantity_unit), '') IS NOT NULL) AS n_parsed_with_unit,
    count(*) FILTER (WHERE nullif(trim(quantity), '') IS NOT NULL
                        OR try_cast(product_quantity AS DOUBLE) > 0)        AS n_either
  FROM (
    SELECT 'all'            AS scope, * FROM obf_scope
    UNION ALL
    SELECT 'us'             AS scope, * FROM obf_scope WHERE is_us
    UNION ALL
    SELECT 'makeup'         AS scope, * FROM obf_scope WHERE is_makeup
    UNION ALL
    SELECT 'us_makeup'      AS scope, * FROM obf_scope WHERE is_makeup AND is_us
    UNION ALL
    SELECT 'us_makeup_broad' AS scope, * FROM obf_scope WHERE is_us AND (is_makeup OR has_family_tag)
  )
  GROUP BY scope
)
ORDER BY CASE scope WHEN 'all' THEN 1 WHEN 'us' THEN 2 WHEN 'makeup' THEN 3
                    WHEN 'us_makeup' THEN 4 ELSE 5 END;

SELECT * FROM obf_quantity_fill;
-- The rows that matter are us_makeup and us_makeup_broad. Read n first.
-- Against §88's 90% target. Against the 50% switch trigger in the report.

-- 2.1  Unit vocabulary on parsed quantities. Must map onto
--      config/unit_rules.yaml unit_tokens; anything else is a parser task.
SELECT product_quantity_unit, count(*) AS n
FROM obf_scope
WHERE is_us AND (is_makeup OR has_family_tag) AND try_cast(product_quantity AS DOUBLE) > 0
GROUP BY 1 ORDER BY n DESC;

-- 2.2  Raw vs parsed disagreement. If product_quantity is derived from
--      quantity, they should agree. Where raw exists and parsed is null, the
--      upstream parser gave up - those rows are §27-31 parser work.
SELECT
  count(*) FILTER (WHERE raw_ok AND parsed_ok)                 AS both_present,
  count(*) FILTER (WHERE raw_ok AND NOT parsed_ok)             AS raw_only,
  count(*) FILTER (WHERE NOT raw_ok AND parsed_ok)             AS parsed_only,
  count(*) FILTER (WHERE NOT raw_ok AND NOT parsed_ok)         AS neither
FROM (
  SELECT
    nullif(trim(quantity), '') IS NOT NULL                     AS raw_ok,
    coalesce(try_cast(product_quantity AS DOUBLE) > 0, FALSE)  AS parsed_ok
  FROM obf_scope WHERE is_us AND (is_makeup OR has_family_tag)
);

-- 2.3  Sample of raw quantity strings - what the parser will face.
SELECT quantity, count(*) AS n
FROM obf_scope
WHERE is_us AND (is_makeup OR has_family_tag) AND nullif(trim(quantity), '') IS NOT NULL
GROUP BY 1 ORDER BY n DESC
LIMIT 50;


-- ============================================================================
-- PART 3 — FILL RATE BY TIER.  Does OBF fix the DRUGSTORE hole specifically?
-- ============================================================================

CREATE OR REPLACE TABLE tier_brands (brand VARCHAR, tier VARCHAR);
INSERT INTO tier_brands VALUES
  ('e.l.f.','drugstore'),('maybelline','drugstore'),('nyx','drugstore'),
  ('l''oréal paris','drugstore'),('l''oreal paris','drugstore'),
  ('milani','drugstore'),('essence','drugstore'),('wet n wild','drugstore'),
  ('revlon','drugstore'),('covergirl','drugstore'),('colourpop','drugstore'),
  ('physicians formula','drugstore'),
  ('morphe','mid_range'),('juvia''s place','mid_range'),('pixi','mid_range'),
  ('kiko','mid_range'),
  ('mac','high_end'),('nars','high_end'),('rare beauty','high_end'),
  ('fenty beauty','high_end'),('benefit','high_end'),('tarte','high_end'),
  ('too faced','high_end'),('urban decay','high_end'),
  ('anastasia beverly hills','high_end'),('huda beauty','high_end'),
  ('makeup by mario','high_end'),('haus labs','high_end'),('saie','high_end'),
  ('tower 28','high_end'),
  ('dior','luxury'),('ysl','luxury'),('yves saint laurent','luxury'),
  ('armani','luxury'),('givenchy','luxury'),('tom ford','luxury'),
  ('chanel','luxury'),('guerlain','luxury');

-- Brand match is word-bounded ("mac" must not match "pharmacy") on the
-- free-text brands field, case-folded. Still crude: multi-brand strings
-- ("L'Oréal, L'Oreal Consumer products, L'Oréal Paris") match on any part.
-- "Broad" = strict §7 tag OR a makeup family tag; "strict" = §7 tag only.
CREATE OR REPLACE VIEW obf_by_tier AS
SELECT
  t.tier,
  count(DISTINCT s.code) FILTER (WHERE s.is_makeup)                        AS n_strict,
  count(DISTINCT s.code) FILTER (WHERE s.is_makeup
        AND try_cast(s.product_quantity AS DOUBLE) > 0
        AND nullif(trim(s.product_quantity_unit), '') IS NOT NULL)         AS n_strict_parsed_with_unit,
  count(DISTINCT s.code)                                                   AS n_broad,
  count(DISTINCT s.code) FILTER (WHERE try_cast(s.product_quantity AS DOUBLE) > 0
        AND nullif(trim(s.product_quantity_unit), '') IS NOT NULL)         AS n_broad_parsed_with_unit,
  round(count(DISTINCT s.code) FILTER (WHERE try_cast(s.product_quantity AS DOUBLE) > 0
        AND nullif(trim(s.product_quantity_unit), '') IS NOT NULL)
        * 100.0 / count(DISTINCT s.code), 1)                               AS broad_parsed_with_unit_pct,
  count(DISTINCT s.code) FILTER (WHERE nullif(trim(s.quantity), '') IS NOT NULL)
                                                                           AS n_broad_raw_quantity
FROM obf_scope s
JOIN tier_brands t
  ON regexp_matches(lower(s.brands),
                    '(^|[^a-z])' || replace(t.brand, '.', '\.') || '([^a-z]|$)')
WHERE s.is_us AND (s.is_makeup OR s.has_family_tag)
GROUP BY t.tier
ORDER BY CASE t.tier WHEN 'drugstore' THEN 1 WHEN 'mid_range' THEN 2
                     WHEN 'high_end' THEN 3 ELSE 4 END;

SELECT * FROM obf_by_tier;
-- drugstore / n_broad_parsed_with_unit is the single number Stage 1.1 is
-- waiting on. Read n before the percentage: a rate on a handful of rows
-- is not a rate.

-- 3.1  Per-brand within drugstore, US-tagged rows.
SELECT
  t.brand,
  count(DISTINCT s.code)                                                  AS n_broad,
  count(DISTINCT s.code) FILTER (WHERE s.is_makeup)                       AS n_strict,
  count(DISTINCT s.code) FILTER (WHERE try_cast(s.product_quantity AS DOUBLE) > 0
        AND nullif(trim(s.product_quantity_unit), '') IS NOT NULL)        AS n_parsed_with_unit
FROM obf_scope s
JOIN tier_brands t
  ON regexp_matches(lower(s.brands),
                    '(^|[^a-z])' || replace(t.brand, '.', '\.') || '([^a-z]|$)')
WHERE s.is_us AND (s.is_makeup OR s.has_family_tag) AND t.tier = 'drugstore'
GROUP BY t.brand
ORDER BY n_broad DESC;

-- 3.2  The same, with the US filter REMOVED. Reported because the US tag
--      under-counts, but read with care: a row tagged to another market
--      carries THAT market's pack size, and pack sizes differ across
--      markets for the same product name. With no barcode on the spine
--      side, such a quantity cannot be verified as the US size. This is a
--      ceiling on what OBF holds, not a supply of usable US quantities.
SELECT
  t.tier,
  count(DISTINCT s.code)                                                  AS n_broad_any_country,
  count(DISTINCT s.code) FILTER (WHERE s.is_us)                           AS n_us_tagged,
  count(DISTINCT s.code) FILTER (WHERE try_cast(s.product_quantity AS DOUBLE) > 0
        AND nullif(trim(s.product_quantity_unit), '') IS NOT NULL)        AS n_parsed_with_unit_any_country,
  count(DISTINCT t.brand)                                                 AS brands_present
FROM obf_scope s
JOIN tier_brands t
  ON regexp_matches(lower(s.brands),
                    '(^|[^a-z])' || replace(t.brand, '.', '\.') || '([^a-z]|$)')
WHERE (s.is_makeup OR s.has_family_tag)
GROUP BY t.tier
ORDER BY CASE t.tier WHEN 'drugstore' THEN 1 WHEN 'mid_range' THEN 2
                     WHEN 'high_end' THEN 3 ELSE 4 END;

-- 3.3  Drugstore per brand, any country, with where those rows are tagged.
SELECT
  t.brand,
  count(DISTINCT s.code)                                                  AS n_broad_any_country,
  count(DISTINCT s.code) FILTER (WHERE s.is_us)                           AS n_us_tagged,
  count(DISTINCT s.code) FILTER (WHERE try_cast(s.product_quantity AS DOUBLE) > 0
        AND nullif(trim(s.product_quantity_unit), '') IS NOT NULL)        AS n_parsed_with_unit_any_country,
  (SELECT string_agg(c || ':' || k, ' ' ORDER BY k DESC) FROM (
     SELECT replace(u.c, 'en:', '') AS c, count(*) AS k
     FROM obf_scope s2, unnest(s2.countries_tags) AS u(c)
     WHERE (s2.is_makeup OR s2.has_family_tag)
       AND regexp_matches(lower(s2.brands),
                          '(^|[^a-z])' || replace(t.brand, '.', '\.') || '([^a-z]|$)')
     GROUP BY 1 ORDER BY k DESC LIMIT 3))                                 AS top_countries
FROM obf_scope s
JOIN tier_brands t
  ON regexp_matches(lower(s.brands),
                    '(^|[^a-z])' || replace(t.brand, '.', '\.') || '([^a-z]|$)')
WHERE (s.is_makeup OR s.has_family_tag) AND t.tier = 'drugstore'
GROUP BY t.brand
ORDER BY n_broad_any_country DESC;


-- ============================================================================
-- PART 4 — JOINABILITY.  Can OBF rows be matched to the Shopify spine?
-- ============================================================================
-- The spine has no barcodes (UPC/EAN absent, measured). So the join is by
-- normalised brand + fuzzy product name - §22 tiers 2-3, not tier 1.
-- This part only measures what OBF offers for that: how many US makeup rows
-- (broad scope) have a non-empty product_name AND a non-empty brand.

SELECT
  count(*)                                                                AS us_makeup_rows,
  count(*) FILTER (WHERE nullif(trim(brands), '') IS NOT NULL)           AS with_brand,
  count(*) FILTER (WHERE len(product_name) > 0)                          AS with_name,
  count(*) FILTER (WHERE nullif(trim(brands), '') IS NOT NULL
                     AND len(product_name) > 0
                     AND try_cast(product_quantity AS DOUBLE) > 0)       AS joinable_with_quantity
FROM obf_scope
WHERE is_us AND (is_makeup OR has_family_tag);
-- joinable_with_quantity is the ceiling on what OBF can add to the spine.


-- ============================================================================
-- PART 5 — PERSIST.  Raw scope table to staging for inspection. Read-only
-- on data/raw/ - nothing here writes back into the export.
-- ============================================================================
COPY (SELECT * FROM obf_scope WHERE is_us AND (is_makeup OR has_family_tag))
  TO 'data/staging/obf_us_makeup.parquet' (FORMAT PARQUET);
