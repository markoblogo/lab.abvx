# ABVX Lab

<img src="docs/assets/logo.png" alt="ABVX Lab logo" width="120" />

Static GitHub Pages hub for ABVX developer tools.

## Structure

- `docs/index.html` - home page with the tools grid
- `docs/assets/styles.css` - shared site styling
- `docs/tools/<slug>/index.html` - per-tool SEO page
- `docs/robots.txt` and `docs/sitemap.xml` - basic crawl metadata

## Add a new tool

1. Copy an existing tool folder from `docs/tools/<slug>/`.
2. Update the page title, one-liner, links, bullets, and metadata.
3. Add the new card to `docs/index.html`.
4. Move the newly added card to the first position in the home grid.
5. Give the newly added card the `NEW` sticker and remove that sticker from the previous card so only one tool is marked `NEW` at a time.
6. Add the new URL to `docs/sitemap.xml`.
7. If the tool has a live site, add its `Live` button on the card and tool page.

## Deploy

GitHub Pages should publish from `/docs` on `main`.
