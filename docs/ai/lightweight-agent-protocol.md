# Lightweight Agent Protocol (LWP)

LWP is the desktop-first, lightweight OMX-like execution protocol in the ABVX stack.

## Intent

Provide a repeatable process for everyday single-repo delivery without full orchestration overhead.

## Core loop

1. Clarify
- Restate task scope and non-goals.
- Identify impacted files/routes/scripts.

2. Task brief
- Fill a short `TASK_BRIEF.md` before implementation.
- Capture risks, verification commands, and done criteria.

3. Execute
- Ship minimal diffs.
- Avoid unrelated refactors.

4. Verify
- Run relevant checks for touched areas.
- Confirm no regressions in critical paths.

5. Report
- List changed files.
- List commands run.
- State residual risks and unrun checks.

## Required artifacts

- `AGENTS.md` for repository guardrails.
- `TASK_BRIEF.md` for intake and completion criteria.

## Positioning in ABVX stack

- Use LWP by default for desktop execution.
- Add `agentsgen` when repo-doc scaffolding or marker management is required.
- Add `ID` when portable profile/hook behavior is required across tools.
- Add `SET` only when CI or multi-repo orchestration is needed.
