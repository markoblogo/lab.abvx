# ABVX Lab

A static hub for the ABVX stack: the repo and workflow layer around AI-assisted coding. It helps turn a GitHub repo into an AI-ready workspace with repo docs, agent surfaces, repo maps, workflows, and checks. ABVX is not another in-editor autocomplete tool; it is the grounding layer around Copilot, Cursor, Continue, and API-driven agents.

ABVX treats MCP, CLI, Skills, and harness gates as separate layers of one agent workflow: MCP provides access to external systems, CLI handles local and heavy execution, Skills/AGENTS.md encode project discipline, and harness gates enforce loops, permissions, proposal-first settlement, sandboxing, observability, and evals.

Live: [lab.abvx.xyz](https://lab.abvx.xyz/)

Agent discovery: [lab.abvx.xyz/.well-known/integrations.json](https://lab.abvx.xyz/.well-known/integrations.json)

About the builder: [lab.abvx.xyz/about/](https://lab.abvx.xyz/about/)

## Who this is for

- Solo developers who want one repo setup path that quickly produces AGENTS.md, `llms.txt`, docs, maps, and checks.
- Teams who want multi-repo workflow visibility, proof loops, registry baselines, and CI-driven repo maintenance.
- Tool builders who want portable human context and reusable agent capabilities that can plug into existing workflows.

## Start here

- [SET](https://lab.abvx.xyz/tools/set/) for one CI entrypoint that keeps repo AI surfaces up to date and exports proposal lifecycle contracts plus memory, diversity, context-budget, and loop-readiness hints for external runners.
- [agentsgen](https://lab.abvx.xyz/tools/agentsgen/) for `AGENTS.md`, reversible-work rules, `llms.txt`, `docs/ai`, bundles, checks, and the canonical product discovery surface on [agentsmd.abvx.xyz](https://agentsmd.abvx.xyz/).
- [ABVX Agent Skills](https://lab.abvx.xyz/tools/abvx-agent-skills/) for validation-gated workflow rules that decide when to use MCP, when to use CLI, when to keep output reversible, enrich durable knowledge, establish product context, capture material agent friction locally, and apply proof, review, or loop-readiness gates.
- [ID](https://lab.abvx.xyz/tools/id/) when human and operator context must travel across repos and tools.
- [Agent Learning Layer](https://lab.abvx.xyz/tools/agent-learning-layer/) for the ABVX position on what actually learns in an agent: model weights rarely change; practical learning usually lives in context, skills, scripts, gates, and evals.

The live site uses the `alt-b` production shell: `SET` is the orchestration entrypoint, `ID` is the portable profile-and-hook layer, `LWP` is the lightweight desktop execution protocol, the home page opens with a tracked-repos snapshot plus a quieter supporting-tools directory, and tool pages share the same product-sheet layout.

## Home page structure

- `SET`, `agentsgen`, `ID`, `repomap`, `LWP`, and ABVX Agent Skills are featured first as the visible core stack.
- The control plane is summarized as a tracked-repos ledger with queue state, then followed by a quieter directory of supporting tools and secondary surfaces.
- Featured tiles and tracked repo rows are clickable and route to internal tool pages or GitHub where no first-class internal surface exists.
- Detailed read-only surfaces still live below that summary:
  - [What to review next](https://lab.abvx.xyz/planning/)
  - [Proof queue](https://lab.abvx.xyz/proof/)
  - [Repo cards](https://lab.abvx.xyz/repos/)
  - [Repo matrix](docs/repos/repo-matrix.md)
  - [Registry snapshot](https://lab.abvx.xyz/registry/)
  - [Workflow status snapshot](https://lab.abvx.xyz/status/)
- Tools are grouped into product families instead of a flat card grid.

## Cleanup status

- `homebrew-core` has been archived after the upstream Homebrew PR was closed.
- `mn7r-showcase`, `revenue-os`, `Orbitory`, and the old profile repo `markoblogo` have been removed after review.
- Temporary upstream-contribution forks are still kept while their PRs remain open.
- The current portfolio classification lives in [docs/repos/repo-matrix.md](docs/repos/repo-matrix.md).

## Portfolio groups

- `AI coding tools stack` with `lab.abvx` as the public hub, backed by `AGENTS.md_generator`, `SET`, `ID`, `abvx-agent-skills`, and `homebrew-tap`.
- `toki pona / sitelen` with `sitelen-layer-plugin` as the package hub, backed by `sitelen-emoji-truth` and related language/content repos.
- `commodity systems` with `index` as the public infra hub and `mn7r` as the internal operating workspace.

## Tool groups

### Orchestration

- [SET](https://lab.abvx.xyz/tools/set/) — Thin GitHub Action entrypoint for presets, repo-docs, site-ai flows, registry-driven review, proof-loop orchestration, proposal-first runner handoffs, and review-only hints for memory, diversity, context budgets, and loop readiness.

### Repo docs & agent context

- [agentsgen](https://lab.abvx.xyz/tools/agentsgen/) — Agent contract layer for AI-ready repos, now with reversible-work rules, readiness reports, safe fixes, fleet scans, versioned CLI/MCP contracts, and opt-in LLM enhancement.
- [ID](https://lab.abvx.xyz/tools/id/) — Portable human-AI profile protocol plus repo-local hooks for SET-compatible orchestration flows.
- [LWP](https://lab.abvx.xyz/tools/lwp/) — Lightweight Workflow Protocol for desktop-first agent development.
- [ABVX Agent Skills](https://lab.abvx.xyz/tools/abvx-agent-skills/) — Portable, validation-gated skills for coding, research, frontend, audits, debugging, token economy, repo onboarding, evidence-backed product context, bounded proposal-first growth loops, local agent-friction ledgers, reversible agent tasks, knowledge-base enrichment, context degradation review, tool-contract review, bounded evaluation, loop readiness, delivery gates from idea to release, social publishing approval gates, PRDs, issue slicing, triage, handoffs, browser verification, and standalone HTML artifact delivery, installable from PyPI as `abvx-agent-skills` or from the ABVX Homebrew tap.
- [Agent Learning Layer](https://lab.abvx.xyz/tools/agent-learning-layer/) — Explainer for routing agent learning into model, context/memory/skills, or harness/workflow layers without pretending every improvement trains the model.
- `lfnovo/open-notebook` — External reference only for a possible self-hosted research corpus, source-grounded search, and future Cardputer reader preparation; not an ABVX dependency or installed local service.
- `andyrewlee/awesome-agent-orchestrators` — External discovery catalog for selecting and auditing runners; compare isolation, human gates, persistence, verification, rollback, and provider support before installing anything.
- [Goal Loop Designer](https://lab.abvx.xyz/tools/goal-loop-designer/) — ABVX Agent Skills capability for compiling raw `/goal` prompts into bounded loop harnesses with rubrics, judge prompts, budgets, YAML, JSON, and Mermaid.
- [Local Inference Tuning](https://lab.abvx.xyz/tools/local-inference-tuning/) — ABVX Agent Skills capability for selecting and tuning local LLM engines, cache policy, KV cache, batching, smoke benchmarks, and OpenAI-compatible endpoints.
- [agentsgen init](https://lab.abvx.xyz/tools/agentsgen-init/) — Bootstrap `.agentsgen.json` + AGENTS/RUNBOOK marker sections.
- [agentsgen update](https://lab.abvx.xyz/tools/agentsgen-update/) — Patch managed marker sections only.
- [agentsgen pack](https://lab.abvx.xyz/tools/agentsgen-pack/) — Generate AI docs bundle with repo/site mode, contract-backed drift checks, and machine-readable manifests.
- [agentsgen snippets](https://lab.abvx.xyz/tools/agentsgen-snippets/) — Canonical README snippet extraction with deterministic drift checks.
- [agentsgen presets](https://lab.abvx.xyz/tools/agentsgen-presets/) — Copy-paste setup for common stacks.

### Validation & CI

- [agentsgen check](https://lab.abvx.xyz/tools/agentsgen-check/) — Validate repo readiness, drift, and readiness-report remediation.
- [agentsgen detect](https://lab.abvx.xyz/tools/agentsgen-detect/) — Heuristic repo scan with stable JSON output.
- [agentsgen status](https://lab.abvx.xyz/tools/agentsgen-status/) — Instant repo overview of markers, managed files, and fallbacks.

### Analysis & LLMO

- [repomap](https://lab.abvx.xyz/tools/repomap/) — Token-budgeted repo map + import graph artifacts with relevance ranking and slice modes.
- `agentsgen analyze` — Shipped CLI surface for AI-visibility scoring of a public URL.
- `agentsgen meta` — Shipped CLI surface for SEO + AI metadata generation.

### Agent discovery

- Lab publishes hub-level discovery at `https://lab.abvx.xyz/llms.txt`, `https://lab.abvx.xyz/.well-known/integrations.json`, `https://lab.abvx.xyz/.well-known/agent-card.json`, and `https://lab.abvx.xyz/.well-known/agent-skills/index.json`.
- Product-level discovery for agentsgen lives on `agentsmd.abvx.xyz`: `https://agentsmd.abvx.xyz/.well-known/integrations.json`.
- Lab should point to product-owned discovery files instead of duplicating runtime claims. For example, agentsgen's public declaration states that `agentsgen mcp` is local stdio, not a hosted remote MCP endpoint.

### Agent workflow layers

- **Access:** MCP and integration discovery connect agents to external systems without copying service-specific auth rules into every repo.
- **Execution:** CLI surfaces such as `agentsgen`, `SET`, GitHub Actions, and local scripts run deterministic, reviewable work.
- **Discipline:** `AGENTS.md` plus ABVX Agent Skills define when access and execution are allowed, when output must remain a proposal, which checks are mandatory, and how repeated workflows become reusable gates.
- **Harness gates:** agent runtimes enforce loop budgets, tool registries, permissions, sandbox boundaries, observability, scheduling, evals, and inspect/apply/discard settlement for retained outputs.

### Decision & strategy protocols

- [DecisionMap](https://lab.abvx.xyz/tools/decisionmap/) — Protocol + prompt toolkit for turning complex business, product, market, and marketing decisions into strategy maps, validated JSON outputs, and cascade-log update loops.

### Release & publishing

- [git-tweet](https://lab.abvx.xyz/tools/git-tweet/) — Turn git changes into tweet-sized release notes.

### Utilities

- [ABVX Shortener](https://lab.abvx.xyz/tools/abvx-shortener/) — Minimal URL shortener.
- [sitelen-layer-plugin](https://lab.abvx.xyz/tools/sitelen-layer-plugin/) — sitelen-layer rendering plugin.
- [AsciiTheme](https://lab.abvx.xyz/tools/asciitheme/) — Tiny CSS theme kit for readable dev pages.

## Agentsgen family naming

Agentsgen commands are presented here as separate tool pages for discoverability.
They still ship together as one package: `agentsgen`.

## Control plane surfaces

- [What to review next](https://lab.abvx.xyz/planning/) — Read-only planning queue with status, priority, workflow-sync hints, operator queue, and richer proof-loop readiness signals from the SET planner.
- [Proof queue](https://lab.abvx.xyz/proof/) — Read-only proof-loop queue for blockers, review-ready tasks, evidence quality, and recommendations.
- [Repo cards](https://lab.abvx.xyz/repos/) — Aggregated view combining registry baselines, latest workflow status, workflow sync, repomap metadata, and proof status.
- [Registry snapshot](https://lab.abvx.xyz/registry/) — Read-only view of repo baselines from the SET central registry.
- [Workflow status snapshot](https://lab.abvx.xyz/status/) — Read-only latest GitHub Actions run per registered repo plus sync state, operator queue, and proof status.

## Maintenance

### What's inside

- Registry snapshot generator: `scripts/sync_registry_snapshot.py`
- Workflow status generator: `scripts/sync_status_snapshot.py`
- Repo cards generator: `scripts/build_repo_cards_snapshot.py`
- Planning snapshot generator: `scripts/sync_planning_snapshot.py`
- Proof snapshot generator: `scripts/sync_proof_snapshot.py`
- Snapshot outputs:
  - `docs/registry/index.html`
  - `docs/assets/registry-snapshot.json`
  - `docs/status/index.html`
  - `docs/assets/status-snapshot.json`
  - `docs/repos/index.html`
  - `docs/assets/repo-cards-snapshot.json`
  - `docs/planning/index.html`
  - `docs/assets/planning-snapshot.json`
  - `docs/proof/index.html`
  - `docs/assets/proof-snapshot.json`
- Home page: `docs/index.html`
- Tool pages: `docs/tools/<slug>/index.html`
- SEO basics: `docs/robots.txt` and `docs/sitemap.xml`
- Agent discovery basics:
  - `docs/llms.txt`
  - `docs/.well-known/integrations.json`
  - `docs/.well-known/agent-card.json`
  - `docs/.well-known/agent-skills/index.json`
- Theme assets: `docs/assets/asciitheme.css`, `docs/assets/ascii-theme.js`

### Snapshot behavior

- Planning, repo cards, and status surfaces can include workflow sync state and operator queue when planning artifacts are present.
- Planning, repo cards, and status surfaces can also show compact repomap status, policy modes, active slices, slice source labels, and top ranked files when local repo artifacts are available.
- Proof queue and related surfaces remain snapshot-based: they reflect the latest local rebuild, not a browser-side live GitHub read.

### Tool pages (routing)

- [repomap](https://lab.abvx.xyz/tools/repomap/)
- [set](https://lab.abvx.xyz/tools/set/)
- [id](https://lab.abvx.xyz/tools/id/)
- [lwp](https://lab.abvx.xyz/tools/lwp/)
- [decisionmap](https://lab.abvx.xyz/tools/decisionmap/)
- [agentsgen](https://lab.abvx.xyz/tools/agentsgen/)
- [agentsgen-init](https://lab.abvx.xyz/tools/agentsgen-init/)
- [agentsgen-update](https://lab.abvx.xyz/tools/agentsgen-update/)
- [agentsgen-pack](https://lab.abvx.xyz/tools/agentsgen-pack/)
- [agentsgen-check](https://lab.abvx.xyz/tools/agentsgen-check/)
- [agentsgen-detect](https://lab.abvx.xyz/tools/agentsgen-detect/)
- [agentsgen-status](https://lab.abvx.xyz/tools/agentsgen-status/)
- [agentsgen-presets](https://lab.abvx.xyz/tools/agentsgen-presets/)
- [agentsgen-snippets](https://lab.abvx.xyz/tools/agentsgen-snippets/)
- [abvx-shortener](https://lab.abvx.xyz/tools/abvx-shortener/)
- [sitelen-layer-plugin](https://lab.abvx.xyz/tools/sitelen-layer-plugin/)
- [git-tweet](https://lab.abvx.xyz/tools/git-tweet/)
- [asciitheme](https://lab.abvx.xyz/tools/asciitheme/)
- [abvx-agent-skills](https://lab.abvx.xyz/tools/abvx-agent-skills/)
- [agent-learning-layer](https://lab.abvx.xyz/tools/agent-learning-layer/)
- [goal-loop-designer](https://lab.abvx.xyz/tools/goal-loop-designer/)
- [local-inference-tuning](https://lab.abvx.xyz/tools/local-inference-tuning/)

### Visual system

ABVX Lab currently uses the `alt-b` production shell:

- `docs/assets/lab-alt-b.css` is the live stylesheet for the home page and tool pages
- Control-plane pages (`planning`, `proof`, `registry`, `repos`, `status`) also use `lab-alt-b.css` through a compatibility layer over their existing snapshot markup
- The old AsciiTheme assets remain in the repo for older/internal surfaces, but they are no longer the main live shell for the public catalog

### How to add a new tool

Use this checklist:

- Create a new tool page from an existing `docs/tools/<slug>/index.html`
- Update the title, one-liner, links, metadata, and canonical URL
- Add the tool entry to `docs/index.html` in the right group
- If it is the newest tool, move it to the top of its group and optionally mark it `NEW`
- Add the tool URL to `docs/sitemap.xml`
- If the tool has a live site, add its `live` link on both the home entry and the tool page

### Deploy

GitHub Pages publishes this site from `/docs` on `main`.

Flow: commit -> push -> wait for Pages.

If you change asset URLs or ship a static asset that browsers may cache aggressively, add or update the cache-busting query suffix in the HTML.

## Ecosystem links

- Repo matrix: https://github.com/markoblogo/lab.abvx/blob/main/docs/repos/repo-matrix.md
- About page: https://lab.abvx.xyz/about/
- SET orchestration: https://github.com/markoblogo/SET
- ID protocol repo: https://github.com/markoblogo/ID
- agentsgen repo: https://github.com/markoblogo/AGENTS.md_generator
- ABVX Agent Skills: https://github.com/markoblogo/abvx-agent-skills
- ABVX Agent Skills on PyPI: https://pypi.org/project/abvx-agent-skills/
- ABVX Homebrew tap: https://github.com/markoblogo/homebrew-tap
