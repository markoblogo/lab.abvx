# ABVX Lab

A static hub for ABVX developer tools and small product pages.
It keeps live links, per-tool docs, and lightweight landing pages in one place.
Multiple agentsgen commands are listed separately for discoverability, but they ship as one package.

Live: [lab.abvx.xyz](https://lab.abvx.xyz/)

<img src="docs/assets/og.svg" alt="ABVX Lab cover" width="100%" />

## Tools

- [repomap](https://lab.abvx.xyz/tools/repomap/) — Deterministic repo map + import graph artifacts (read-only).
- [agentsgen snippets](https://lab.abvx.xyz/tools/agentsgen-snippets/) — Canonical README snippet extraction with deterministic CI drift checks.
- [agentsgen presets](https://lab.abvx.xyz/tools/agentsgen-presets/) — Copy-paste setup for common stacks (explicit commands, no guesswork).
- [agentsgen](https://lab.abvx.xyz/tools/agentsgen/) — Safe repo docs toolchain for coding agents (AGENTS/RUNBOOK + PR Guard + AI docs bundle).
- [agentsgen init](https://lab.abvx.xyz/tools/agentsgen-init/) — Bootstrap .agentsgen.json + AGENTS/RUNBOOK with safe marker sections.
- [agentsgen update](https://lab.abvx.xyz/tools/agentsgen-update/) — Patch marker sections only; never overwrite handwritten docs.
- [agentsgen pack](https://lab.abvx.xyz/tools/agentsgen-pack/) — Generate AI docs bundle; supports --check, --print-plan, and site mode.
- [agentsgen check](https://lab.abvx.xyz/tools/agentsgen-check/) — Validate repo is agentsgen-ready; CI-friendly drift signals.
- [agentsgen detect](https://lab.abvx.xyz/tools/agentsgen-detect/) — Heuristic repo scan (no execution); emits stable JSON output.
- [agentsgen status](https://lab.abvx.xyz/tools/agentsgen-status/) — Instant repo overview: managed files, markers, generated fallbacks, and drift.
- [ABVX Shortener](https://lab.abvx.xyz/tools/abvx-shortener/) — Minimal URL shortener (Cloudflare Worker + KV).
- [sitelen-layer-plugin](https://lab.abvx.xyz/tools/sitelen-layer-plugin/) — sitelen-layer rendering plugin (toki pona tooling).
- [git-tweet](https://lab.abvx.xyz/tools/git-tweet/) — Turn git changes into tweet-sized release notes (with context + links).
- [AsciiTheme](https://lab.abvx.xyz/tools/asciitheme/) — Tiny CSS theme kit for clean, readable dev pages.

## Agentsgen family naming

Agentsgen commands are presented here as separate tool pages for discoverability.
They still ship together as one package: `agentsgen`.

## Maintenance

### What's inside

- Home page: `docs/index.html`
- Tool pages: `docs/tools/<slug>/index.html`
- SEO basics: `docs/robots.txt` and `docs/sitemap.xml`
- Theme assets: `docs/assets/asciitheme.css`, `docs/assets/ascii-theme.js`, `docs/assets/styles.css`

### Tool pages (routing)

- [repomap](https://lab.abvx.xyz/tools/repomap/)
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

### Visual system

ABVX Lab uses a split setup based on AsciiTheme:

- `docs/assets/asciitheme.css` is a vendored copy of the AsciiTheme base preset
- `docs/assets/ascii-theme.js` is the vendored theme-toggle script
- `docs/assets/styles.css` is the Lab-only override layer
- Do not rebuild the baseline locally in `styles.css`

### How to add a new tool

Use this checklist:

- Create a new tool page from an existing `docs/tools/<slug>/index.html`
- Update the title, one-liner, links, metadata, and canonical URL
- Add the card to `docs/index.html`
- Move the new card to the first position on the home grid
- Add the `NEW` sticker to the new card and remove it from the previous one so only one tool is marked `NEW`
- Add the tool URL to `docs/sitemap.xml`
- If the tool has a live site, add its `Live` link on both the home card and the tool page

### Deploy

GitHub Pages publishes this site from `/docs` on `main`.

Flow: commit -> push -> wait for Pages.

If you change asset URLs or ship a static asset that browsers may cache aggressively, add or update the cache-busting query suffix in the HTML.
