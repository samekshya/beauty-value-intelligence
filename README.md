# Beyond the Price Tag

### A Data-Driven Analysis of True Value in Beauty

---

## The problem

Beauty shoppers compare products by sticker price. A $12 drugstore blush
next to a $35 prestige blush reads as an easy decision.

But package sizes in makeup vary enormously, and the label rarely makes
that comparable. $12 for 2 g is $6.00/g. $35 for 10 g is $3.50/g. The
cheaper item at the till is the more expensive one per gram — by 71%.

## The question

> When consumers pay less for a beauty product, are they actually getting
> better value, or are they sometimes simply buying less product?

And, for the application built on top of it:

> If I want an alternative to this expensive product, which one is not only
> similar and cheaper at checkout, but genuinely better value?

## Status

**Phase 1 · Stage 1.0 — source feasibility. In progress.**

No data has been collected and no findings exist yet. This README will
carry results only once there are results; every number in it will trace
to a calculation in this repository.

Stage 1.0 ends with a decision about where the data comes from — not with
data. It is deliberately the slowest part of the project, because the
credibility of everything downstream depends on it.

## Approach

The central measurement problem is that a price is only comparable once
you know how much product it buys. That makes quantity parsing, not
modelling, the load-bearing technical work:

- Weight ounces and fluid ounces are different units and stay separate.
- Grams are never converted to millilitres. That conversion needs density,
  density is not on the label, and inventing it would silently corrupt
  every downstream comparison.
- Multipacks (`2 x 4 g`) resolve to a pack count and a total, not a
  per-item quantity mistaken for the whole.
- Dual-unit labels (`0.05 oz / 1.5 g`) prefer the manufacturer's explicit
  metric value over a conversion.

Market tier is assigned from brand positioning and never from price.
Deriving tier from price and then analysing price by tier would make the
result circular by construction.

## Repository layout

```
config/      category, unit, tier and usage rules; source registry
data/        raw -> staging -> processed -> analytics
database/    schema and the DuckDB build
src/         ingest, cleaning, matching, units, validation, features,
             analytics, modelling, utils
sql/         analytical queries and views
notebooks/   01 feasibility ... 12 business insights
app/         application entry point and pages
tests/       units, matching, features, data quality, dupe logic
reports/     feasibility report, final insights, figures
docs/        specification, roadmap, methodology, data dictionary, limitations
```

Raw data is immutable. Nothing downstream writes back into `data/raw/`.

## Setup

Requires Python 3.13.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` currently carries Phase 1 dependencies only. Later
phases add their own as they begin.

## Documentation

| Document | Purpose |
| --- | --- |
| `docs/PROJECT_SPEC.md` | Full specification. Authoritative. |
| `docs/ROADMAP.md` | Phase structure and the gate each phase must pass. |
| `reports/source_feasibility_report.md` | Which sources are usable, and why. |

## Limitations

Recorded as they are discovered, in `docs/limitations.md`. Prices are a
dated market snapshot, not permanent values, and are labelled as such.
