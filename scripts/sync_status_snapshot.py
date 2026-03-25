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


def get_planning_snapshot_path() -> Path:
    value = os.environ.get('LAB_PLANNING_SNAPSHOT_PATH', '').strip()
    return Path(value) if value else LAB_ROOT / 'docs' / 'assets' / 'planning-snapshot.json'


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


def load_planning_map() -> dict[str, dict[str, object]]:
    path = get_planning_snapshot_path()
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    repos = data.get('repos', [])
    if not isinstance(repos, list):
        return {}
    result: dict[str, dict[str, object]] = {}
    for entry in repos:
        if isinstance(entry, dict) and isinstance(entry.get('repo'), str):
            result[str(entry['repo'])] = entry
    return result


def fetch_status(repo_name: str, planning_map: dict[str, dict[str, object]]) -> dict[str, object]:
    payload = gh_api_json(f'repos/{repo_name}/actions/runs?per_page=1')
    runs = payload.get('workflow_runs', [])
    planning = planning_map.get(repo_name, {})
    workflow_sync_status = planning.get('workflow_sync_status', 'not-checked') if isinstance(planning, dict) else 'not-checked'
    operator_queue = planning.get('operator_queue', 'review-later') if isinstance(planning, dict) else 'review-later'
    repomap_snapshot = planning.get('repomap_snapshot', {}) if isinstance(planning, dict) else {}
    if not runs:
        return {'repo': repo_name, 'status': 'none', 'conclusion': 'none', 'html_url': '', 'name': 'No runs yet', 'workflow_sync_status': workflow_sync_status, 'operator_queue': operator_queue, 'repomap_snapshot': repomap_snapshot}
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
        'workflow_sync_status': workflow_sync_status,
        'operator_queue': operator_queue,
        'repomap_snapshot': repomap_snapshot,
    }


def build_page(entries: list[dict[str, object]]) -> str:
    cards = []
    for entry in entries:
        repomap_snapshot = entry.get('repomap_snapshot', {}) if isinstance(entry.get('repomap_snapshot'), dict) else {}
        repomap_line = ''
        slice_line = ''
        if repomap_snapshot:
            repomap_line = (
                f'<li>Compact repomap: {repomap_snapshot.get("status", "not-checked")} '
                f'(budget {repomap_snapshot.get("compact_budget", "n/a")}, top files {repomap_snapshot.get("top_ranked_limit", "n/a")})</li>'
            )
            active_slice = repomap_snapshot.get('active_slice', {}) if isinstance(repomap_snapshot.get('active_slice'), dict) else {}
            focus = active_slice.get('focus')
            mode = active_slice.get('mode', 'full')
            files_count = active_slice.get('slice_files_count', 0)
            slice_label = mode if not focus else f"{mode} ({focus})"
            slice_line = f'<li>Active slice: {slice_label}; ranked files: {files_count}</li>'
        top_ranked = repomap_snapshot.get('top_ranked_files', []) if isinstance(repomap_snapshot, dict) else []
        top_ranked_html = ''
        if top_ranked:
            items = ''.join(
                f'<li><code>{item.get("path", "")}</code> (score {item.get("score", 0)})</li>'
                for item in top_ranked
                if isinstance(item, dict) and item.get('path')
            )
            top_ranked_html = f'<div class="small-note">Top ranked files:</div><ul class="bullet-list">{items}</ul>'
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
              <li>Workflow sync: {entry.get("workflow_sync_status", "not-checked")}</li>
              <li>Operator queue: {entry.get("operator_queue", "review-later")}</li>
              {repomap_line}
              {slice_line}
            </ul>
            {top_ranked_html}
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
            <p class="small-note">Static snapshot generated via GitHub API and local planning snapshot. No repo mutation, no write automation.</p>
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
    planning_map = load_planning_map()
    statuses = [fetch_status(str(entry['repo']), planning_map) for entry in repos]
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
