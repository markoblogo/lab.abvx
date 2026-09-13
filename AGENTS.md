# AGENTS.md

This file is for coding agents (Codex/Claude/Cursor/etc.). Keep it strict and actionable.

## Repo-specific context

- Read `PRODUCT.md` and `DESIGN.md` before changing public pages, tool-page copy, or navigation.
- Keep catalog claims traceable to the owning repositories and keep snapshot surfaces read-only.
- Use detector waivers in `DESIGN.md` when a deliberate visual exception is necessary.

## Overview

<!-- AGENTSGEN:START section=overview -->
- **Project:** ABVX Lab
- **Stack:** static
- Keep changes small and verifiable.
<!-- AGENTSGEN:END section=overview -->

<!-- AGENTSGEN:START section=repo_context -->
### Repo context

- Project: ABVX Lab
- Stack: static
- Root: `.`
- Start with:
  - `README.md`
  - `docs/index.html`
  - `docs/tools/`
- CI: `.github/workflows/`
<!-- AGENTSGEN:END section=repo_context -->

<!-- AGENTSGEN:START section=guardrails -->
### Guardrails

- Work only within the requested scope and preserve local conventions.
- Prefer focused changes; use 300 changed lines as a review signal, not a hard limit.
- Never discard user files, handwritten content, migrations, or data.
- Never hardcode tokens/keys. Never print secrets; document required environment-variable names.
- Run side-effecting or destructive operations only with existing authorization.
- Before changing these areas, confirm intent unless the current task already authorizes it:
  - schema changes
  - auth/payments/crypto
  - deletions or large refactors
  - new build tooling/CI changes
  - new major dependencies
- A change is complete when behavior, relevant tests, and affected docs agree.
<!-- AGENTSGEN:END section=guardrails -->

<!-- AGENTSGEN:START section=workflow -->
### Workflow

1. Read the nearest instructions and reproduce the current behavior.
2. Implement the smallest coherent change and keep generated output reviewable.
3. Run the narrowest useful check, then the full project checks before finalizing.
4. Update docs and contracts when behavior changes.
5. Report changed behavior, verification, and any material limitation.
<!-- AGENTSGEN:END section=workflow -->

<!-- AGENTSGEN:START section=verification -->
### Verification

- Run the repository's full test suite or the closest documented equivalent.
- If a check cannot run, state why and name the remaining command.
<!-- AGENTSGEN:END section=verification -->

<!-- AGENTSGEN:START section=agentsgen_contract -->
### AGENTSGEN contract

- Scope: this repo keeps the agent contract intentionally compact and machine-readable.
- Authority rule: only explicitly listed files are auto-updatable by generated sections (`AGENTSGEN` markers).
- Files with markers: `AGENTS.md`, `RUNBOOK.md`, `docs/ai/task-contract.json`.
- PR gate: repository must pass agentsgen drift checks for `AGENTS.md`, `RUNBOOK.md`, and `docs/ai/task-contract.json`.
<!-- AGENTSGEN:END section=agentsgen_contract -->

<!-- AGENTSGEN:START section=task_contract -->
### Task contract (compact)

- Contract states: `accepted`, `used`, `confirmed`.
- Before `used`: keep a human-readable reason and expected output in `docs/ai/task-contract.json`.
- Before `confirmed`: evidence paths must include `docs/ai/how-to-run.md` and `docs/ai/how-to-test.md`.
- Route states must be explicit in local decisions: `accepted`, `used`, `confirmed`.
<!-- AGENTSGEN:END section=task_contract -->

<!-- AGENTSGEN:START section=style -->
### Style (static)

- Match existing naming, formatting, and module boundaries.
- Prefer direct code and explicit errors over new abstractions.
- Validate external input at system boundaries.
- Keep logs free of secrets and personal data.
- Add types or comments where they clarify a public or non-obvious contract.
- Reuse current dependencies unless a new one materially reduces complexity.
<!-- AGENTSGEN:END section=style -->

## Rules Of Engagement


<!-- AGENTSGEN:START section=motion-review -->
### Motion safety (animation-focused review)

For any CSS/JS changes that touch animation, transitions, parallax, or scroll effects:

- prefer transform properties (`x`, `y`, `scale`, `rotation`, `opacity`) over layout props (`top`, `left`, `width`, `height`)
- add `prefers-reduced-motion` fallback (skip/downgrade duration and movement)
- ensure teardown/cleanup on route change or unmount (`revert`, `kill`, `clearProps` where appropriate)
- avoid unbounded global selectors in animation setup (scope selectors)
- include a quick validation note in the related task evidence package
<!-- AGENTSGEN:END section=motion-review -->

<!-- AGENTSGEN:START section=rules -->
**DO**
- Prefer small diffs.
- Add or update tests when behavior changes.
- Run repo checks before finishing.

**DON'T**
- Do not rewrite unrelated code.
- Do not refactor without confirming intent.
- Do not commit secrets or local env files.

**If uncertain**
- Ask a short clarifying question before making big changes.

**Warnings**
- (none)
<!-- AGENTSGEN:END section=rules -->

## Commands

<!-- AGENTSGEN:START section=commands -->
- **Install:** `(not needed)`
- **Dev:** `python3 -m http.server 8000 --directory docs`
- **Test:** `python3 -m unittest discover -s tests -v`
- **Lint:** `python3 scripts/verify_site.py`
- **Build:** `python3 -m compileall -q scripts`

- **Run a single test:** (not specified)
- **Where configs live:** `docs/robots.txt`, `docs/sitemap.xml`
<!-- AGENTSGEN:END section=commands -->

<!-- AGENTSGEN:START section=static -->
## Static site / docs notes

### Safe edits
- Avoid large HTML/CSS refactors unless requested
- Prefer small layout changes with predictable impact
- If mobile layout changes: verify at least one narrow breakpoint

### Quick checks
- Run formatter (if present)
- Validate links (spot-check)
<!-- AGENTSGEN:END section=static -->

## Repo Structure

<!-- AGENTSGEN:START section=structure -->
- **Source:** `docs`
- **Config:** `docs/robots.txt`, `docs/sitemap.xml`
<!-- AGENTSGEN:END section=structure -->

## Output Protocol

<!-- AGENTSGEN:START section=output_protocol -->
When you finish work, include:
- Summary (1-3 bullets)
- Files changed (list paths)
- Verification (exact commands to run)
<!-- AGENTSGEN:END section=output_protocol -->
