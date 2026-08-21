# Beyond the Price Tag

Do current US makeup prices reflect what you actually get — quantity,
quality, and measurable value — or what the brand has convinced you it
is worth?

## Current phase

**Phase 1 · Stage 1.0 — Feasibility. In progress.**

Stage 1.0 ends with a DECISION about data sources, not with data. Not in
scope: collecting the dataset, the ingestion pipeline, the quantity
parser, the app.

Done: `docs/PROJECT_SPEC.md` received and read in full (99 sections).
Repo structure built per §65. `config/` populated from the spec —
`categories.yaml` (§7, §31), `unit_rules.yaml` (§28-30),
`tier_mapping.yaml` (§11, §12), `usage_assumptions.yaml` (§42, values
deliberately null pending sourcing), `data_sources.yaml` (§16 schema,
no entries yet). README written.

Next: source landscape research, then a feasibility test measuring real
field coverage across ~20 products per source, then a recommendation in
`reports/source_feasibility_report.md`.

GATE (§16, roadmap): primary + fallback source named; real quantity-field
coverage measured rather than assumed; legal status documented per source
with the exact clause read.

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

After every meaningful unit of work, commit and push:

    git add -A
    git commit -m "<type>: <what changed>"
    git push

Types: feat, fix, data, docs, test, refactor, chore, analysis
One logical change per commit. Never bundle unrelated work.
Never commit files matched by .gitignore.
Do not add attribution trailers to commit messages.

## Anti-goals

Do not: fabricate data · convert g↔mL · use price for tier or
similarity · scrape prohibited sources · report p-values without
effect sizes · over-engineer · add tools that don't earn their place.

Never print API keys or full request URLs in notebook cells.
Clear notebook outputs before committing anything under notebooks/.

GIT WORKFLOW — applies for the rest of this project, every session.

After EVERY completed step — a file created, a config populated, a
function written, a test passing, a doc section finished — immediately:

  git add -A
  git commit -m "<type>: <what changed>"
  git push

Do not batch work. Do not wait until a task is "done." If you created
a file, that is a commit. If you fixed a typo, that is a commit. Small
and frequent, always pushed.

Types: feat, fix, data, docs, test, refactor, chore, analysis

ATTRIBUTION — strict.

- No Co-Authored-By trailer on any commit.
- No "Generated with Claude Code" line, in commits or PRs.
- Never write "Claude", "AI", "assistant", "agent", or any tool name in
  a commit message, PR description, code comment, docstring, or README.
- Commit messages describe the change only. Never who or what made it.
- All commits author as the configured git user. Do not override
  user.name or user.email for any reason.

Confirm you have read this, then continue.