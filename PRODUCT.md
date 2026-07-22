# ABVX Lab Product Context

ABVX Lab is the public hub for the ABVX agent-workflow stack. It explains the repo/workflow layer around AI-assisted coding and points users to the tools that make a repository agent-ready.

## Audience

- solo developers who want a practical repo setup path for AI coding agents;
- teams that need visible workflow state, proof loops, registry baselines, and CI-driven repo maintenance;
- tool builders evaluating portable agent contracts, skills, MCP access, and deterministic CLI layers.

## Primary Jobs

- explain the ABVX stack without promising a hosted agent runtime;
- route visitors to SET, agentsgen, ID, ABVX Agent Skills, and related tool pages;
- show repo/workflow status as a read-only control-plane surface;
- keep public claims aligned with repository-owned docs and generated snapshots.

## Surface Types

- brand/product hub: `docs/index.html`;
- product-sheet pages: `docs/tools/*/index.html`;
- read-only control-plane pages: planning, proof, repos, registry, status;
- machine-readable discovery: `llms.txt`, `.well-known/*`, sitemap, robots.

## Source Boundaries

- GitHub repositories and their README/docs are the source of truth for tool claims.
- Snapshot pages reflect the latest local rebuild, not live browser-side GitHub state.
- Lab should link to product-owned discovery files instead of duplicating runtime claims.
- Do not claim production execution, scheduling, remote MCP, hosted policy runtime, or autonomous agent action unless a source repo and deployed surface prove it.

## Non-Goals

- no SaaS dashboard positioning;
- no hosted agent runtime claims;
- no marketing claims detached from repo evidence;
- no broad redesign that hides the tool directory, repo ledger, or proof surfaces.
