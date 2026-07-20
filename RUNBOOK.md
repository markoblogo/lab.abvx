# RUNBOOK.md

## Quickstart

<!-- AGENTSGEN:START section=quickstart -->
```sh
(not needed)
```
```sh
python3 -m http.server 8000 --directory docs
```
```sh
(not needed)
```
```sh
(not needed)
```
<!-- AGENTSGEN:END section=quickstart -->

## Common Tasks

<!-- AGENTSGEN:START section=common_tasks -->
- Run tests: `(not needed)`
- Lint: `(not needed)`
- Build: `(not needed)`
<!-- AGENTSGEN:END section=common_tasks -->

## Troubleshooting

<!-- AGENTSGEN:START section=troubleshooting -->
- If dependencies fail: verify the expected Node/Python version for this repo.
- If tests are flaky: re-run once, then isolate and fix the root cause.
- If environment is unclear: ask for the expected OS/tooling versions.
<!-- AGENTSGEN:END section=troubleshooting -->

<!-- AGENTSGEN:START section=contracts -->
## Contract checks

- Validate agent docs contract on changed files:

```sh
python3 -m pip install -q agentsgen
agentsgen check . --files AGENTS.md,RUNBOOK.md --autodetect
```

- Validate pack payload:

```sh
agentsgen pack --check --autodetect --output docs/ai
```
<!-- AGENTSGEN:END section=contracts -->

## Repo-specific notes

- Preview locally: `python3 -m http.server 8000 --directory docs` then open `http://localhost:8000/`.
- Deploy: GitHub Pages publishes from `/docs` on `main`; push to `main` and wait for Pages/CDN refresh.
- Edit tool pages in `docs/tools/<slug>/index.html` and keep `docs/sitemap.xml` in sync with published URLs.
