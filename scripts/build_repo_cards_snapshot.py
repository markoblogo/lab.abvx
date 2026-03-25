from __future__ import annotations

import json
import os
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]


def _path(env_name: str, default: Path) -> Path:
    value = os.environ.get(env_name, '').strip()
    return Path(value) if value else default


def main() -> int:
    registry_path = _path('LAB_REGISTRY_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'registry-snapshot.json')
    status_path = _path('LAB_STATUS_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'status-snapshot.json')
    planning_path = _path('LAB_PLANNING_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'planning-snapshot.json')
    output_json = _path('LAB_REPO_CARDS_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'repo-cards-snapshot.json')
    output_html = _path('LAB_REPO_CARDS_PAGE_PATH', LAB_ROOT / 'docs' / 'repos' / 'index.html')

    registry = json.loads(registry_path.read_text())
    status = json.loads(status_path.read_text())
    planning = json.loads(planning_path.read_text()) if planning_path.exists() else {'repos': []}
    status_map = {entry['repo']: entry for entry in status.get('repos', [])}
    planning_map = {entry['repo']: entry for entry in planning.get('repos', [])}

    cards = []
    for entry in registry.get('repos', []):
        repo = entry['repo']
        tools = entry.get('tools', {})
        presets = entry.get('presets', [])
        site = (entry.get('site') or {}).get('url') if isinstance(entry.get('site'), dict) else None
        workflow = status_map.get(repo, {})
        planning_entry = planning_map.get(repo, {})
        agentsgen = tools.get('agentsgen', {}) if isinstance(tools, dict) else {}
        enabled = []
        for key in ('init', 'pack', 'check', 'repomap', 'snippets'):
            if agentsgen.get(key) is True:
                enabled.append(key)
        if agentsgen.get('analyze_url'):
            enabled.append('analyze')
        if agentsgen.get('meta_url'):
            enabled.append('meta')
        cards.append(
            {
                'repo': repo,
                'presets': presets,
                'site_url': site,
                'agentsgen_enabled': enabled,
                'workflow': workflow,
                'planning': planning_entry,
            }
        )

    payload = {'version': 1, 'source': 'Lab aggregated repo cards', 'repos': cards}
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2) + '\n')

    sections = []
    for card in cards:
        workflow = card['workflow']
        planning = card.get('planning', {}) if isinstance(card.get('planning'), dict) else {}
        latest_run = workflow.get('html_url', '')
        latest_run_button = (
            f'<a class="button-secondary" href="{latest_run}">Latest run</a>' if latest_run else ''
        )
        site_line = (
            f'<div class="small-note">Site: <a href="{card["site_url"]}">{card["site_url"]}</a></div>'
            if card.get('site_url')
            else ''
        )
        tool_line = ', '.join(card['agentsgen_enabled']) if card['agentsgen_enabled'] else 'none'
        presets = ', '.join(card['presets']) or 'none'
        workflow_sync_status = planning.get('workflow_sync_status', 'not-checked')
        operator_queue = planning.get('operator_queue', 'review-later')
        repomap_snapshot = planning.get('repomap_snapshot', {}) if isinstance(planning.get('repomap_snapshot'), dict) else {}
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
        sections.append(
            f'''<section class="page-panel">
            <h2>{card['repo']}</h2>
            <p class="small-note">Presets: {presets}</p>
            {site_line}
            <ul class="bullet-list">
              <li>Agentsgen baseline: {tool_line}</li>
              <li>Workflow status: {workflow.get('status', 'unknown')}</li>
              <li>Conclusion: {workflow.get('conclusion', 'unknown')}</li>
              <li>Workflow: {workflow.get('name', 'n/a')}</li>
              <li>Workflow sync: {workflow_sync_status}</li>
              <li>Operator queue: {operator_queue}</li>
              {repomap_line}
              {slice_line}
            </ul>
            {top_ranked_html}
            <div class="link-grid"><a class="button" href="../registry/index.html">Registry</a><a class="button-secondary" href="../status/index.html">Status</a>{latest_run_button}</div>
          </section>'''
        )

    sections_html = ' '.join(sections)
    html = f'''<!doctype html>
<html lang="en" data-style="ascii" data-ascii-mode="light">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Repo Cards | ABVX Lab</title>
    <meta name="description" content="Aggregated read-only repo cards combining SET registry baselines and latest GitHub Actions status." />
    <link rel="canonical" href="https://lab.abvx.xyz/repos/" />
    <meta property="og:title" content="Repo Cards | ABVX Lab" />
    <meta property="og:description" content="Aggregated read-only repo cards combining SET registry baselines and latest GitHub Actions status." />
    <meta property="og:url" content="https://lab.abvx.xyz/repos/" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://lab.abvx.xyz/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="stylesheet" href="../assets/asciitheme.css?v20260319d" />
    <link rel="stylesheet" href="../assets/styles.css?v20260320a" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Repo Cards","url":"https://lab.abvx.xyz/repos/","description":"Aggregated read-only repo cards combining SET registry baselines and latest GitHub Actions status."}}</script>
  </head>
  <body>
    <div class="site-shell">
      <div class="container page-layout">
        <header class="topbar">
          <div class="topbar-left"><a class="brand" href="../index.html"><img class="brand-logo" src="../assets/logo.png?v20260319d" alt="ABVX Lab logo" /><span class="brand-text">ABVX Lab</span></a></div>
          <nav class="topbar-nav" aria-label="Primary"><a href="../index.html">Home</a><a href="../index.html#tools">Tools</a><a href="https://github.com/markoblogo">GitHub profile</a></nav>
          <div class="topbar-right"><div class="header-controls"></div></div>
        </header>
        <main class="page-layout">
          <section class="hero-panel">
            <span class="kicker">ABVX control plane</span>
            <h1>Repo cards</h1>
            <p class="lead">Aggregated read-only cards combining SET registry baselines and latest GitHub Actions workflow status.</p>
            <p class="small-note">Static snapshot only. Good for visibility, not for automation.</p>
            <div class="link-grid"><a class="button" href="../registry/index.html">Registry snapshot</a><a class="button-secondary" href="../status/index.html">Workflow status</a><a class="button-secondary" href="../assets/repo-cards-snapshot.json">JSON snapshot</a></div>
          </section>
          {sections_html}
        </main>
        <footer class="footer footer--lab"><div class="footer-inner"><div class="footer-left"><div class="footer-title">ABVX Lab</div><div class="footer-note">Small, readable, static pages for ABVX developer tools.</div></div></div></footer>
      </div>
    </div>
    <script src="../assets/ascii-theme.js?v20260319d"></script>
    <script>
      AsciiTheme.initAsciiTheme({{ base: true, managedMode: true, addThemeToggle: true, addStyleToggle: false, mountSelector: '.header-controls' }});
    </script>
  </body>
</html>
'''
    output_html.write_text(html)
    print(f'Wrote {output_json}')
    print(f'Wrote {output_html}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
