# ABVX Lab

<img src="docs/assets/og.svg" alt="ABVX Lab cover" width="100%" />

Static GitHub Pages hub for ABVX developer tools, published at [lab.abvx.xyz](https://lab.abvx.xyz/).

## What this repo is

ABVX Lab is a small static catalog for developer tools related to AI-assisted coding.

Current shape:
- Home page with a tools grid in `docs/index.html`
- Per-tool SEO pages in `docs/tools/<slug>/index.html`
- GitHub Pages deployment from `/docs` on `main`
- AsciiTheme as the visual baseline, with a small local overrides layer

## Structure

- `docs/index.html` - home page and tools grid
- `docs/assets/asciitheme.css` - vendored AsciiTheme base preset
- `docs/assets/ascii-theme.js` - vendored AsciiTheme UMD toggle script
- `docs/assets/styles.css` - Lab-specific overrides only
- `docs/assets/og.svg` - README / project cover art
- `docs/assets/og.png` - OG image used by pages
- `docs/assets/logo.png` - header logo asset
- `docs/tools/<slug>/index.html` - per-tool landing / SEO pages
- `docs/robots.txt` - crawler rules
- `docs/sitemap.xml` - published URL list

## Tool pages

Current tool URLs:
- `/tools/agentsgen/`
- `/tools/agentsgen-init/`
- `/tools/agentsgen-update/`
- `/tools/agentsgen-pack/`
- `/tools/agentsgen-check/`
- `/tools/agentsgen-detect/`
- `/tools/abvx-shortener/`
- `/tools/sitelen-layer-plugin/`
- `/tools/git-tweet/`
- `/tools/asciitheme/`

## Visual system

Lab uses AsciiTheme as the foundation, not a redesign from scratch.

Keep this split:
- `docs/assets/asciitheme.css` stays a vendored copy of AsciiTheme base preset
- `docs/assets/ascii-theme.js` stays the vendored toggle script
- `docs/assets/styles.css` is the only place for Lab-specific polish

Do not reimplement the baseline in local CSS.

## Add a new tool

1. Copy an existing tool folder from `docs/tools/<slug>/`.
2. Update the page title, one-liner, links, bullets, metadata, and canonical URL.
3. Add the new card to `docs/index.html`.
4. Move the newly added card to the first position in the home grid.
5. Give the newly added card the `NEW` sticker.
6. Remove the `NEW` sticker from the previous card so only one tool is marked `NEW` at a time.
7. If the tool has a live site, add its `Live` button on both the home card and the tool page.
8. Add the new published URL to `docs/sitemap.xml`.

## Editing rules

When updating this site:
- Keep URLs and slugs stable unless there is an explicit migration.
- Prefer small HTML changes and put visual tweaks in `docs/assets/styles.css`.
- Keep footer markup identical across home and tool pages.
- Keep the theme toggle wiring intact.
- If you change static asset URLs, use a cache-busting query suffix in HTML so GitHub Pages clients refresh reliably.

## Deploy

GitHub Pages should publish from `/docs` on `main`.

In practice:
- commit to `main`
- push to GitHub
- wait for Pages/CDN refresh
- if static assets changed, verify the current cache-busting suffix is present in HTML
