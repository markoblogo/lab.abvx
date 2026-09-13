from __future__ import annotations

import json
import os
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SET_REGISTRY = LAB_ROOT.parent / 'SET' / 'registry' / 'repos'


def get_registry_dir() -> Path:
    value = os.environ.get('SET_REGISTRY_DIR', '').strip()
    return Path(value) if value else DEFAULT_SET_REGISTRY


def get_snapshot_path() -> Path:
    value = os.environ.get('LAB_REGISTRY_SNAPSHOT_PATH', '').strip()
    return Path(value) if value else LAB_ROOT / 'docs' / 'assets' / 'registry-snapshot.json'


def get_page_path() -> Path:
    value = os.environ.get('LAB_REGISTRY_PAGE_PATH', '').strip()
    return Path(value) if value else LAB_ROOT / 'docs' / 'registry' / 'index.html'


def load_registry(registry_dir: Path) -> list[dict[str, object]]:
    if not registry_dir.is_dir():
        raise SystemExit(
            f'SET registry not found at {registry_dir}. '
            'Set SET_REGISTRY_DIR to a checked-out SET/registry/repos directory.'
        )
    entries: list[dict[str, object]] = []
    for path in sorted(registry_dir.glob('*.json')):
        data = json.loads(path.read_text())
        entries.append(data)
    return entries


def format_tools(tools: dict[str, object]) -> list[str]:
    lines: list[str] = []
    agentsgen = tools.get('agentsgen') if isinstance(tools, dict) else None
    if isinstance(agentsgen, dict):
        enabled = []
        for key in ('init', 'pack', 'check', 'repomap', 'snippets'):
            if agentsgen.get(key) is True:
                enabled.append(key)
        if agentsgen.get('analyze_url'):
            enabled.append('analyze')
        if agentsgen.get('meta_url'):
            enabled.append('meta')
        if enabled:
            lines.append(f"agentsgen: {', '.join(enabled)}")
    git_tweet = tools.get('git_tweet') if isinstance(tools, dict) else None
    if isinstance(git_tweet, dict) and git_tweet.get('enabled') is True:
        lines.append('git_tweet: enabled')
    return lines


def build_page(entries: list[dict[str, object]]) -> str:
    cards = []
    for entry in entries:
        repo = entry['repo']
        site = ''
        site_data = entry.get('site')
        if isinstance(site_data, dict) and site_data.get('url'):
            site = f'<div class="small-note">Site: <a href="{site_data["url"]}">{site_data["url"]}</a></div>'
        presets = ', '.join(entry.get('presets', [])) or 'none'
        tool_lines = ''.join(f'<li>{line}</li>' for line in format_tools(entry.get('tools', {})))
        cards.append(
            f'''<section class="page-panel">
            <h2>{repo}</h2>
            <p class="small-note">Presets: {presets}</p>
            {site}
            <ul class="bullet-list">{tool_lines}</ul>
          </section>'''
        )
    cards_html = '\n'.join(cards)
    return f'''<!doctype html>
<html lang="en" data-style="ascii" data-ascii-mode="light">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Registry Snapshot | ABVX Lab</title>
    <meta name="description" content="Read-only snapshot of the SET central registry for ABVX repos and enabled tool baselines." />
    <link rel="canonical" href="https://lab.abvx.xyz/registry/" />
    <meta property="og:title" content="Registry Snapshot | ABVX Lab" />
    <meta property="og:description" content="Read-only snapshot of the SET central registry for ABVX repos and enabled tool baselines." />
    <meta property="og:url" content="https://lab.abvx.xyz/registry/" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://lab.abvx.xyz/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="stylesheet" href="../assets/asciitheme.css?v20260319d" />
    <link rel="stylesheet" href="../assets/styles.css?v20260320a" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Registry Snapshot","url":"https://lab.abvx.xyz/registry/","description":"Read-only snapshot of the SET central registry for ABVX repos and enabled tool baselines."}}</script>
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
            <h1>Registry snapshot</h1>
            <p class="lead">Read-only view of the current SET registry: repo baselines, enabled tool families, and site-aware inputs.</p>
            <p class="small-note">Static snapshot generated from <a href="https://github.com/markoblogo/SET/tree/main/registry/repos">SET/registry</a>. No write automation yet.</p>
            <div class="link-grid"><a class="button" href="https://github.com/markoblogo/SET/tree/main/registry/repos">View registry on GitHub</a><a class="button-secondary" href="../assets/registry-snapshot.json">JSON snapshot</a><a class="button-secondary" href="../status/index.html">Workflow status</a></div>
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
    registry_dir = get_registry_dir()
    snapshot_path = get_snapshot_path()
    page_path = get_page_path()
    entries = load_registry(registry_dir)
    snapshot = {
        'version': 1,
        'source': 'SET registry snapshot',
        'registry_source': 'https://github.com/markoblogo/SET/tree/main/registry/repos',
        'repos': entries,
    }
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.parent.mkdir(parents=True, exist_ok=True)
    snapshot_path.write_text(json.dumps(snapshot, indent=2) + '\n')
    page_path.write_text('\n'.join(line.rstrip() for line in build_page(entries).splitlines()) + '\n')
    print(f'Wrote {snapshot_path}')
    print(f'Wrote {page_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
