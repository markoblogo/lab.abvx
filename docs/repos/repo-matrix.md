# Repo Matrix

This document is a working portfolio map for `markoblogo` repositories.

It is not a deletion script. It is a categorization pass to reduce repo sprawl and make later cleanup decisions easier.

## Categories

- `Core` — keep visible and actively shape as primary public lines.
- `Satellite` — keep, but position as secondary or companion projects.
- `Merge later` — extract the valuable parts into a stronger repo or umbrella later.
- `Archive/delete candidate` — low-current-value repo, abandoned line, or replaced surface.
- `Temporary fork/remove after PR` — operational fork created for upstream PR work.

## AI coding tools / agent engineering

| Repo | Category | Reason |
| --- | --- | --- |
| `AGENTS.md_generator` | Core | Strongest repo-doc and AI-ready workspace entrypoint. |
| `abvx-agent-skills` | Core | Clear reusable skillpack layer with validation and packaging. |
| `ID` | Core | Distinct portable human-context layer in the stack. |
| `SET` | Core | Clear orchestration/control-plane role across the ecosystem. |
| `lab.abvx` | Core | Best public hub for the ecosystem and repo navigation. |
| `homebrew-tap` | Core | Official package distribution surface for the tooling stack. |
| `decision-map` | Satellite | Useful protocol/toolkit, but not a primary ecosystem anchor. |
| `git-tweet` | Satellite | Small companion publishing tool, not a portfolio center. |
| `llmo-abvx` | Merge later | Valuable ideas should move into `AGENTS.md_generator`, not stay separate. |

Suggested umbrella direction:

- `ai-coding-toolkit`
- `agent-engineering-kit`
- `agent-workflow-stack`

## toki pona / sitelen

| Repo | Category | Reason |
| --- | --- | --- |
| `sitelen-layer-plugin` | Core | Strong standalone frontend package with clear product shape. |
| `sitelen-emoji-truth` | Core | Canonical mapping/data layer for the language/symbol line. |
| `toki-pona-translator` | Satellite | Useful app surface, but not the main platform layer. |
| `dao-toki` | Satellite | Thematic/public-facing content repo within the language line. |
| `toki-free-kit` | Satellite | Campaign/content repo, useful but not a main pillar. |
| `stoic-wisdom-series` | Satellite | Another content-led expression of the same cluster. |
| `pictiq` | Satellite | Paused, but still strategically close to the symbolic language line. |

Suggested umbrella direction:

- `toki pona / sitelen`
- `symbolic language tools`

## agro / commodity / trading systems

| Repo | Category | Reason |
| --- | --- | --- |
| `mn7r` | Core | Looks like an active internal operating workspace, not a side experiment. |
| `index` | Core | Clear infrastructure/data layer for commodity benchmarks. |
| `TS` | Satellite | Product/site surface inside the broader agro cluster. |
| `liqua` | Satellite | Related product-facing surface, but not the infrastructure core. |
| `cropto-v0` | Merge later | Important idea line, but likely to be restructured rather than continued as-is. |

Suggested umbrella direction:

- `commodity systems`
- `agro trading stack`

## standalone public sites

| Repo | Category | Reason |
| --- | --- | --- |
| `azurmenton` | Satellite | Clean standalone site with a clear independent audience. |
| `ukrainian-modernism` | Satellite | Standalone editorial/landing surface with a narrow scope. |
| `ABVXsite` | Merge later | Personal/public web presence likely overlaps with other hub surfaces. |

## abandoned or unclear lines

| Repo | Category | Reason |
| --- | --- | --- |
| `mn7r-showcase` | Archive/delete candidate | Archived; public showcase for a line that no longer looks primary. |
| `revenue-os` | Archive/delete candidate | Archived; thin/unclear surface with no strong current identity. |
| `Orbitory` | Archive/delete candidate | Archived; no clear current role and weak naming/positioning signal. |
| `markoblogo` | Archive/delete candidate | If only used as profile README, likely replaceable by a better public hub. |

## operational and temporary forks

| Repo | Category | Reason |
| --- | --- | --- |
| `awesome-llm-agents` | Temporary fork/remove after PR | Upstream contribution fork, not a product repo. |
| `Awesome-CSS-Resources` | Temporary fork/remove after PR | Upstream contribution fork, not a product repo. |
| `awesome-web-components` | Temporary fork/remove after PR | Upstream contribution fork, not a product repo. |
| `awesome-ui-component-library` | Temporary fork/remove after PR | Upstream contribution fork, not a product repo. |
| `Awesome-Prompt-Engineering` | Temporary fork/remove after PR | Upstream contribution fork, not a product repo. |
| `awesome-prompts` | Temporary fork/remove after PR | Upstream contribution fork, not a product repo. |
| `homebrew-core` | Temporary fork/remove after PR | Archived; upstream PR closed, fork no longer needed as active surface. |
| `staged-recipes` | Temporary fork/remove after PR | Operational conda-forge submission fork only. |

## Current cleanup order

1. Remove temporary forks after upstream PR outcomes are settled.
2. Delete on explicit confirmation:
   `markoblogo`, `mn7r-showcase`, `revenue-os`, `Orbitory`, and later the temporary forks once their upstream PRs are resolved.
3. Pull the useful `llmo-abvx` pieces into `AGENTS.md_generator`.
4. Decide and name the top-level AI coding tools umbrella.
5. Decide and name the top-level agro / commodity umbrella.
6. Revisit whether some satellites should remain separate repos or move into broader hubs.
