# Beyond the Price Tag

Do current US makeup prices reflect what you actually get — quantity,
quality, and measurable value — or what the brand has convinced you it
is worth?

## Current phase

**Phase 1 · Stage 1.0 — Feasibility. BLOCKED, not started.**

Blocker: `docs/PROJECT_SPEC.md` does not exist. `docs/ROADMAP.md` treats
it as authoritative and cites ~30 sections (§12, §14, §16, §27-31, §32,
§65, §87 …) that define the Stage 1.0 deliverables. The user is
supplying the file. Do not build against guessed section content, and
do not author a substitute spec — that would manufacture false
authority (roadmap anti-goals).

Done so far: repo skeleton only — this file, `requirements.txt`,
`docs/ROADMAP.md`, `.gitignore`. No `src/`, no data, no configs; the
directory layout is defined by spec §65 and waits on it.

When the spec lands: read §65 first, build the structure it specifies,
then work Stage 1.0 top to bottom.

## Authority

`docs/PROJECT_SPEC.md` is authoritative. `docs/ROADMAP.md` sequences the
work and defines the gates. Where they disagree, the spec wins.

A phase is not complete until its gate is met. Do not start the next
phase early. Update `## Current phase` above when a gate passes.

## Environment

Python 3.13.12, venv at `.venv/` (Windows layout — `.venv/Scripts/`).

    .venv/Scripts/python.exe -m pip install -r requirements.txt
    .venv/Scripts/python.exe -m pytest

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
