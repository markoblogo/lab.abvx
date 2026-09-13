from __future__ import annotations

import json
import os
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]


def _path(env_name: str, default: Path) -> Path:
    value = os.environ.get(env_name, '').strip()
    return Path(value) if value else default


def get_planning_snapshot_path() -> Path:
    return _path('LAB_PLANNING_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'planning-snapshot.json')


def get_output_json_path() -> Path:
    return _path('LAB_PROOF_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'proof-snapshot.json')


def get_output_page_path() -> Path:
    return _path('LAB_PROOF_PAGE_PATH', LAB_ROOT / 'docs' / 'proof' / 'index.html')


def load_planning_snapshot() -> dict[str, object]:
    return json.loads(get_planning_snapshot_path().read_text())


def proof_queue(entry: dict[str, object]) -> str:
    proof = entry.get('proof_snapshot', {}) if isinstance(entry.get('proof_snapshot'), dict) else {}
    if not proof or proof.get('status') in {'disabled', 'missing-config'}:
        return 'disabled'
    if str(proof.get('decision', 'unknown')) == 'review-ready':
        return 'review-ready'
    if int(proof.get('blocking_count', 0) or 0) > 0 or str(proof.get('decision', 'unknown')) == 'blocked':
        return 'blocked'
    return 'in-progress'


def sort_key(entry: dict[str, object]) -> tuple[int, str]:
    order = {'review-ready': 0, 'blocked': 1, 'in-progress': 2, 'disabled': 3}
    return (order.get(str(entry.get('proof_queue', 'disabled')), 9), str(entry.get('repo', '')))


def build_snapshot(planning: dict[str, object]) -> dict[str, object]:
    repos = []
    for entry in planning.get('repos', []):
        if not isinstance(entry, dict) or not isinstance(entry.get('repo'), str):
            continue
        proof = entry.get('proof_snapshot', {}) if isinstance(entry.get('proof_snapshot'), dict) else {}
        repos.append(
            {
                'repo': entry['repo'],
                'proof_queue': proof_queue(entry),
                'workflow_sync_status': entry.get('workflow_sync_status', 'not-checked'),
                'operator_queue': entry.get('operator_queue', 'review-later'),
                'proof_snapshot': proof,
                'target_workflow': entry.get('target_workflow', '.github/workflows/set.yml'),
            }
        )
    repos.sort(key=sort_key)
    return {
        'version': 1,
        'source': 'Lab proof snapshot',
        'repo_count': len(repos),
        'repos': repos,
    }


def build_page(snapshot: dict[str, object]) -> str:
    sections = {'review-ready': [], 'blocked': [], 'in-progress': [], 'disabled': []}
    for entry in snapshot.get('repos', []):
        sections.setdefault(str(entry.get('proof_queue', 'disabled')), []).append(entry)

    titles = {
        'review-ready': 'Review ready',
        'blocked': 'Blocked',
        'in-progress': 'In progress',
        'disabled': 'Disabled',
    }
    notes = {
        'review-ready': 'Proof bundles with complete evidence and no explicit blockers, waiting on human review.',
        'blocked': 'Proof bundles with explicit blockers or incomplete evidence that should be cleared first.',
        'in-progress': 'Proof-enabled repos that have partial or still-forming proof state.',
        'disabled': 'Repos that are not using proof-loop yet.',
    }

    cards: list[str] = []
    for queue in ('review-ready', 'blocked', 'in-progress', 'disabled'):
        entries = sections.get(queue, [])
        if not entries:
            continue
        cards.append(f'<section class="page-panel"><h2>{titles[queue]}</h2><p class="small-note">{notes[queue]}</p></section>')
        for entry in entries:
            proof = entry.get('proof_snapshot', {}) if isinstance(entry.get('proof_snapshot'), dict) else {}
            checks = proof.get('check_summary', {}) if isinstance(proof.get('check_summary'), dict) else {}
            artifacts = proof.get('artifact_summary', {}) if isinstance(proof.get('artifact_summary'), dict) else {}
            blockers = proof.get('blocking_details', []) if isinstance(proof.get('blocking_details'), list) else []
            blocker_html = ''
            if blockers:
                items = ''.join(
                    f'<li><strong>{item.get("severity", "medium")}</strong>: {item.get("message", "unspecified blocker")}</li>'
                    for item in blockers
                    if isinstance(item, dict)
                )
                blocker_html = f'<div class="small-note">Proof blockers:</div><ul class="bullet-list">{items}</ul>'
            recommendation = str(proof.get('recommendation', '') or '')
            cards.append(
                f'''<section class="page-panel">
            <h2>{entry["repo"]}</h2>
            <p class="small-note">Proof queue: {entry["proof_queue"]} | Workflow sync: {entry.get("workflow_sync_status", "not-checked")} | Operator queue: {entry.get("operator_queue", "review-later")}</p>
            <ul class="bullet-list">
              <li>Task id: {proof.get("task_id") or 'n/a'}</li>
              <li>Proof status: {proof.get("status", "disabled")}</li>
              <li>Verdict: {proof.get("verdict_status", "none")}</li>
              <li>Decision: {proof.get("decision", "unknown")}</li>
              <li>Evidence status: {proof.get("evidence_status", "none")}</li>
              <li>Review ready: {str(proof.get("review_ready", False)).lower()}</li>
              <li>Ready for apply: {str(proof.get("ready_for_apply", False)).lower()}</li>
              <li>Checks: passed {checks.get("passed", 0)}, failed {checks.get("failed", 0)}, pending {checks.get("pending", 0)}</li>
              <li>Artifacts: present {artifacts.get("present", 0)} / total {artifacts.get("total", 0)}</li>
              <li>Target workflow: {entry.get("target_workflow", ".github/workflows/set.yml")}</li>
            </ul>
            {'<div class="small-note">Recommendation: ' + recommendation + '</div>' if recommendation else ''}
            {blocker_html}
            <div class="link-grid"><a class="button" href="../planning/index.html">Planning</a><a class="button-secondary" href="../repos/index.html">Repo cards</a><a class="button-secondary" href="../status/index.html">Status</a><a class="button-secondary" href="../assets/proof-snapshot.json">JSON snapshot</a></div>
          </section>'''
            )

    cards_html = '\n'.join(cards)
    return f'''<!doctype html>
<html lang="en" data-style="ascii" data-ascii-mode="light">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Proof Queue | ABVX Lab</title>
    <meta name="description" content="Read-only proof-loop queue for ABVX repos." />
    <link rel="canonical" href="https://lab.abvx.xyz/proof/" />
    <meta property="og:title" content="Proof Queue | ABVX Lab" />
    <meta property="og:description" content="Read-only proof-loop queue for ABVX repos." />
    <meta property="og:url" content="https://lab.abvx.xyz/proof/" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://lab.abvx.xyz/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="stylesheet" href="../assets/asciitheme.css?v20260319d" />
    <link rel="stylesheet" href="../assets/styles.css?v20260320a" />
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
            <h1>Proof queue</h1>
            <p class="lead">Read-only queue for proof-loop contracts, evidence bundles, blockers, and review-ready tasks.</p>
            <p class="small-note">This surface helps separate proof readiness from the broader planning/operator queue.</p>
            <div class="link-grid"><a class="button" href="../planning/index.html">Planning</a><a class="button-secondary" href="../repos/index.html">Repo cards</a><a class="button-secondary" href="../status/index.html">Status</a><a class="button-secondary" href="../assets/proof-snapshot.json">JSON snapshot</a></div>
          </section>
          {cards_html}
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


def main() -> int:
    snapshot = build_snapshot(load_planning_snapshot())
    output_json = get_output_json_path()
    output_html = get_output_page_path()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(snapshot, indent=2) + '\n')
    output_html.write_text('\n'.join(line.rstrip() for line in build_page(snapshot).splitlines()) + '\n')
    print(f'Wrote {output_json}')
    print(f'Wrote {output_html}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
