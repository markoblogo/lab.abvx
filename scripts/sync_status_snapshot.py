from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]


def get_registry_snapshot_path() -> Path:
    value = os.environ.get('LAB_REGISTRY_SNAPSHOT_PATH', '').strip()
    return Path(value) if value else LAB_ROOT / 'docs' / 'assets' / 'registry-snapshot.json'


def get_status_snapshot_path() -> Path:
    value = os.environ.get('LAB_STATUS_SNAPSHOT_PATH', '').strip()
    return Path(value) if value else LAB_ROOT / 'docs' / 'assets' / 'status-snapshot.json'


def get_status_page_path() -> Path:
    value = os.environ.get('LAB_STATUS_PAGE_PATH', '').strip()
    return Path(value) if value else LAB_ROOT / 'docs' / 'status' / 'index.html'


def gh_api_json(path: str) -> dict[str, object]:
    proc = subprocess.run(
        ['gh', 'api', path],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_repos() -> list[dict[str, object]]:
    data = json.loads(get_registry_snapshot_path().read_text())
    repos = data.get('repos', [])
    if not isinstance(repos, list):
        raise SystemExit('registry snapshot does not contain repos[]')
    return repos


def fetch_status(repo_name: str) -> dict[str, object]:
    payload = gh_api_json(f'repos/{repo_name}/actions/runs?per_page=1')
    runs = payload.get('workflow_runs', [])
    if not runs:
        return {'repo': repo_name, 'status': 'none', 'conclusion': 'none', 'html_url': '', 'name': 'No runs yet'}
    run = runs[0]
    return {
        'repo': repo_name,
        'status': run.get('status', 'unknown'),
        'conclusion': run.get('conclusion') or 'in_progress',
        'html_url': run.get('html_url', ''),
        'name': run.get('name', 'workflow'),
        'head_branch': run.get('head_branch', ''),
        'event': run.get('event', ''),
        'updated_at': run.get('updated_at', ''),
    }


def build_page(entries: list[dict[str, object]]) -> str:
    cards = []
    for entry in entries:
        cards.append(
            f'''<section class="page-panel">
            <h2>{entry["repo"]}</h2>
            <p class="small-note">Workflow: {entry["name"]}</p>
            <ul class="bullet-list">
              <li>Status: {entry["status"]}</li>
              <li>Conclusion: {entry["conclusion"]}</li>
              <li>Branch: {entry.get("head_branch", "") or 'n/a'}</li>
              <li>Event: {entry.get("event", "") or 'n/a'}</li>
              <li>Updated: {entry.get("updated_at", "") or 'n/a'}</li>
            </ul>
            <div class="link-grid"><a class="button-secondary" href="{entry["html_url"]}">Latest run</a></div>
          </section>'''
        )
    cards_html = '\n'.join(cards)
    return f'''<!doctype html>
<html lang="en" data-style="ascii" data-ascii-mode="light">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Workflow Status | ABVX Lab</title>
    <meta name="description" content="Read-only workflow status snapshot for ABVX repos from GitHub Actions." />
    <link rel="canonical" href="https://lab.abvx.xyz/status/" />
    <meta property="og:title" content="Workflow Status | ABVX Lab" />
    <meta property="og:description" content="Read-only workflow status snapshot for ABVX repos from GitHub Actions." />
    <meta property="og:url" content="https://lab.abvx.xyz/status/" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://lab.abvx.xyz/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="stylesheet" href="../assets/asciitheme.css?v20260319d" />
    <link rel="stylesheet" href="../assets/styles.css?v20260320a" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Workflow Status","url":"https://lab.abvx.xyz/status/","description":"Read-only workflow status snapshot for ABVX repos from GitHub Actions."}}</script>
  </head>
  <body>
    <div class="site-shell">
      <div class="container page-layout">
        <header class="topbar">
          <div class="topbar-left">
            <a class="brand" href="../index.html">
              <img class="brand-logo" src="../assets/logo.png?v20260319d" alt="ABVX Lab logo" />
              <span class="brand-text">ABVX Lab</span>
            </a>
          </div>
          <nav class="topbar-nav" aria-label="Primary">
            <a href="../index.html">Home</a>
            <a href="../index.html#tools">Tools</a>
            <a href="https://github.com/markoblogo">GitHub profile</a>
          </nav>
          <div class="topbar-right">
            <div class="header-controls"></div>
          </div>
        </header>
        <main class="page-layout">
          <section class="hero-panel">
            <span class="kicker">ABVX control plane</span>
            <h1>Workflow status snapshot</h1>
            <p class="lead">Read-only view of the latest GitHub Actions run per registered repo.</p>
            <p class="small-note">Static snapshot generated via GitHub API. No repo mutation, no write automation.</p>
            <div class="link-grid"><a class="button" href="../registry/index.html">Registry snapshot</a><a class="button-secondary" href="../assets/status-snapshot.json">JSON snapshot</a></div>
          </section>
          {cards_html}
        </main>
        <footer class="footer footer--lab">
          <div class="footer-inner">
            <div class="footer-left">
              <div class="footer-title">ABVX Lab</div>
              <div class="footer-note">Small, readable, static pages for ABVX developer tools.</div>
            </div>
            <div class="social-icons" aria-label="Elsewhere">
              <a href="https://abvx.substack.com" aria-label="Substack"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M7 6h10v2H9v2h8a3 3 0 0 1 0 6H7v-2h10v-2H9a3 3 0 0 1 0-6h8V6H7z" fill="currentColor"/></svg></a>
              <a href="https://abvcreative.medium.com" aria-label="Medium"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M4 7h3l3.5 8L14 7h3l3 10h-2.5l-1.8-6-2.7 6H11l-2.7-6-1.8 6H4L7 7H4z" fill="currentColor"/></svg></a>
              <a href="https://x.com/abv_creative" aria-label="X"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M7 6h2.6l3 4 3-4H18l-4.2 5.4L18 18h-2.6l-3-4-3 4H7l4.2-6L7 6z" fill="currentColor"/></svg></a>
              <a href="https://www.linkedin.com/in/abvcreative" aria-label="LinkedIn"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M6 9h3v9H6V9zm1.5-4a1.7 1.7 0 1 1 0 3.4A1.7 1.7 0 0 1 7.5 5zM11 9h3v1.3c.6-.9 1.6-1.6 3.1-1.6 2.2 0 3.8 1.3 3.8 4.3V18h-3v-4.6c0-1.4-.6-2.2-1.8-2.2-1.1 0-2 .7-2 2.2V18h-3V9z" fill="currentColor"/></svg></a>
              <a href="https://bsky.app/profile/abvx.xyz" aria-label="Bluesky"><svg viewBox="0 0 24 24" role="img" aria-hidden="true"><path d="M12 6c2.6-2.4 6-3.4 6-1.1 0 2.5-2.2 4.2-4.6 5.2 2.4 1 4.6 2.7 4.6 5.2 0 2.3-3.4 1.3-6-1.1-2.6 2.4-6 3.4-6 1.1 0-2.5 2.2-4.2 4.6-5.2C8.2 9.1 6 7.4 6 4.9 6 2.6 9.4 3.6 12 6z" fill="currentColor"/></svg></a>
            </div>
          </div>
        </footer>
      </div>
    </div>
    <script src="../assets/ascii-theme.js?v20260319d"></script>
    <script>
      AsciiTheme.initAsciiTheme({{
        base: true,
        managedMode: true,
        addThemeToggle: true,
        addStyleToggle: false,
        mountSelector: '.header-controls',
      }});
    </script>
  </body>
</html>
'''


def main() -> int:
    repos = load_repos()
    statuses = [fetch_status(str(entry['repo'])) for entry in repos]
    snapshot = {
        'version': 1,
        'source': 'GitHub Actions status snapshot',
        'repos': statuses,
    }
    snapshot_path = get_status_snapshot_path()
    page_path = get_status_page_path()
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot, indent=2) + '\n')
    page_path.write_text(build_page(statuses))
    print(f'Wrote {snapshot_path}')
    print(f'Wrote {page_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
