# ABVX Lab

A static hub of ABVX developer tools, with per-tool pages for discovery and links.

This repo contains the published GitHub Pages site, the per-tool landing pages, and the small maintenance workflow for keeping the catalog current.

Live: [lab.abvx.xyz](https://lab.abvx.xyz/)

<img src="docs/assets/og.svg" alt="ABVX Lab cover" width="100%" />

## Tools

A short list of what’s currently in the lab (each tool has a page + links).

New: agentsgen snippets — canonical README snippet extraction with CI drift checks.

- **agentsgen snippets** — extract canonical README snippets with deterministic CI drift checks  
  https://lab.abvx.xyz/tools/agentsgen-snippets/

- **agentsgen presets** — copy-paste repo setup for common stacks (no autodetect, explicit commands)  
  https://lab.abvx.xyz/tools/agentsgen-presets/

- **agentsgen** — safe repo docs toolchain for coding agents (AGENTS.md/RUNBOOK.md + PR Guard + LLMO Pack)  
  https://lab.abvx.xyz/tools/agentsgen/

- **agentsgen init** — bootstrap AGENTS.md/RUNBOOK.md + .agentsgen.json (safe markers)  
  https://lab.abvx.xyz/tools/agentsgen-init/

- **agentsgen update** — marker-only updates; never overwrite handwritten docs  
  https://lab.abvx.xyz/tools/agentsgen-update/

- **agentsgen pack** — generate AI/LLMO docs bundle; supports --check and --print-plan  
  https://lab.abvx.xyz/tools/agentsgen-pack/

- **agentsgen check** — validate core docs/config/markers and optionally aggregate pack/snippets drift for CI  
  https://lab.abvx.xyz/tools/agentsgen-check/

- **agentsgen detect** — heuristic repo scan (no execution); JSON output supported  
  https://lab.abvx.xyz/tools/agentsgen-detect/

- **agentsgen status** — instant repo overview: managed files, markers, generated fallbacks, and drift  
  https://lab.abvx.xyz/tools/agentsgen-status/

- **ABVX Shortener** — minimal URL shortener (Cloudflare Worker + KV)  
  https://lab.abvx.xyz/tools/abvx-shortener/

- **sitelen-layer-plugin** — sitelen-layer rendering plugin (toki pona tooling)  
  https://lab.abvx.xyz/tools/sitelen-layer-plugin/

- **git-tweet** — turn git changes into tweet-sized release notes (with context + links)  
  https://lab.abvx.xyz/tools/git-tweet/

- **AsciiTheme** — tiny CSS theme kit for clean, readable dev pages  
  https://lab.abvx.xyz/tools/asciitheme/


## What's inside

- Home page: `docs/index.html`
- Tool pages: `docs/tools/<slug>/index.html`
- SEO basics: `docs/robots.txt` and `docs/sitemap.xml`
- Theme assets: `docs/assets/asciitheme.css`, `docs/assets/ascii-theme.js`, `docs/assets/styles.css`

## Tool pages (routing)

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

## Visual system

ABVX Lab uses a split setup based on AsciiTheme:

- `docs/assets/asciitheme.css` is a vendored copy of the AsciiTheme base preset
- `docs/assets/ascii-theme.js` is the vendored theme-toggle script
- `docs/assets/styles.css` is the Lab-only override layer
- Do not rebuild the baseline locally in `styles.css`

## How to add a new tool

Use this checklist:

- Create a new tool page from an existing `docs/tools/<slug>/index.html`
- Update the title, one-liner, links, metadata, and canonical URL
- Add the card to `docs/index.html`
- Move the new card to the first position on the home grid
- Add the `NEW` sticker to the new card and remove it from the previous one so only one tool is marked `NEW`
- Add the tool URL to `docs/sitemap.xml`
- If the tool has a live site, add its `Live` link on both the home card and the tool page

## Deploy

GitHub Pages publishes this site from `/docs` on `main`.

Flow: commit -> push -> wait for Pages.

If you change asset URLs or ship a static asset that browsers may cache aggressively, add or update the cache-busting query suffix in the HTML.
