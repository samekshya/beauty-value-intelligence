# Beyond the Price Tag

Do current US makeup prices reflect what you actually get — quantity,
quality, and measurable value — or what the brand has convinced you it
is worth?

## Current phase

**Phase 1 · Stage 1.0 — Feasibility. Complete except for one decision.**

Stage 1.0 ended with a decision, as intended — but one piece of it is not
mine to make. Full findings: `reports/source_feasibility_report.md`.
Structured record: `config/data_sources.yaml`.

What was measured (2026-08-22, 3,333 products, 19 brand storefronts):
name / brand / list price / URL / retailer at 100%. **Quantity at 11.4%
overall and 0.0% for drugstore.** Drugstore brands do not publish size on
their own storefronts — confirmed by two independent methods, including
e.l.f. and Wet n Wild product pages read directly. This is an absence of
data, not a parsing gap.

Decisions made: primary spine = brand-owned Shopify storefronts.
Fallback = manual quantity capture on an expanded §26 anchor set.
Rejected with evidence: Amazon PA-API (deprecated, 403), Google Content API
(wrong direction), Sephora (403 at edge), Ulta and Target (terms prohibit —
clauses quoted), Walmart (terms behind CAPTCHA), eBay (unsuitable), Impact
(dropped). Every US retailer carrying drugstore makeup is closed.

**OPEN — blocks Stage 1.1:** the quantity source for the drugstore tier.
Open Beauty Facts is the only identified route to structured quantity. It
is untested: its hosts blanket-block automated fetching from this session,
so the schema could not be read and no workaround was sought. **The test
is written and self-tested** — `sql/obf_feasibility.sql` via
`python src/ingest/obf_feasibility.py --site-total <N>`. It needs the
owner to place `obf.parquet` and `obf.csv` in `data/raw/obf/` (both
git-ignored). Part 0 cross-checks the two flavours for truncation and
halts on failure before any fill rate is reported. The decisive output is
`obf_by_tier.drugstore.parsed_with_unit_pct`.

Measured state (strict): 380 products with quantity of 3,333 (11.4%);
213 are MAC and 143 Tom Ford; **0 drugstore**. Three paths reassessed in
the report (prestige-only / manual capture / disclosure-asymmetry
reframe) — tradeoffs written, none chosen. OBF result is the last evidence
that moves the choice.

SerpApi: skipped — no `.env` / `SERPAPI_KEY` present.

Also open, owner's call: the luxury tier has 2 reachable brands of 7. See
the platform-reachability risk in the report — three options laid out, no
recommendation made.

Do not start Stage 1.1 ingestion until the quantity source is named.

## Hazards discovered in Stage 1.0

- **Shopify `variants[].grams` is shipping weight, not net content.** It is
  populated on 55.7% of products — over 4x real size coverage — and would
  yield plausible, uniformly wrong price-per-unit figures. Never use it as
  quantity. Enforced in `config/unit_rules.yaml`.
- **robots.txt is not permission.** Ulta permits product pages to every
  crawler and prohibits collecting listings and prices in its terms. Check
  both; the terms govern.
- **Regex on raw HTML fabricates coverage.** A first pass matched `029g`,
  `0MG`, `7G` inside minified scripts and reported 18/21. Strict
  measurement on visible text gave 2/21. Strip scripts, require plausible
  magnitude, and report the method.

## Authority

`docs/PROJECT_SPEC.md` is authoritative. `docs/ROADMAP.md` sequences the
work and defines the gates. Where they disagree, the spec wins.

A phase is not complete until its gate is met. Do not start the next
phase early. Update `## Current phase` above when a gate passes.

## Environment

Python 3.13.12, venv at `.venv/` (Windows layout — `.venv/Scripts/`).

    Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    pytest

Activate the environment rather than calling the interpreter path
directly. PowerShell here is 5.1 — `;` chains, not `&&`.

`requirements.txt` carries Phase 1 dependencies only. Later phases add
their own (stats in Phase 2, embeddings in Phase 3, Streamlit in
Phase 4) — add them when that phase starts, not before.

## Git workflow

After EVERY completed step — a file created, a config populated, a
function written, a test passing, a doc section finished — immediately:

    git add -A
    git commit -m "<type>: <what changed>"
    git push

Do not batch. Do not wait until a task is "done". A created file is a
commit; a fixed typo is a commit. Small and frequent, always pushed.

Types: feat, fix, data, docs, test, refactor, chore, analysis
One logical change per commit. Never bundle unrelated work.
Never commit files matched by .gitignore.

Attribution — strict. No Co-Authored-By trailer. No "Generated with"
line in commits or PRs. Never name a tool, model or assistant in a
commit message, PR description, code comment, docstring or README.
Commit messages describe the change only, never who or what made it.
All commits author as the configured git user; never override
user.name or user.email.

## Anti-goals

Do not: fabricate data · convert g↔mL · use price for tier or
similarity · scrape prohibited sources · report p-values without
effect sizes · over-engineer · add tools that don't earn their place.

Never print API keys or full request URLs in notebook cells.
Clear notebook outputs before committing anything under notebooks/.
