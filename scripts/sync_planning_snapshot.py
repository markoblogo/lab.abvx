from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SET_PLANNER = Path('/Users/antonbiletskiy-volokh/Downloads/Projects/SET/scripts/plan_config_apply.py')
DEFAULT_REPO_ROOTS = {
    'markoblogo/lab.abvx': '/Users/antonbiletskiy-volokh/Downloads/Projects/Lab',
    'markoblogo/AGENTS.md_generator': '/Users/antonbiletskiy-volokh/Downloads/Projects/AGENTS.md Generator',
}


def _path(env_name: str, default: Path) -> Path:
    value = os.environ.get(env_name, '').strip()
    return Path(value) if value else default


def get_planner_path() -> Path:
    return _path('SET_PLANNER_SCRIPT', DEFAULT_SET_PLANNER)


def get_snapshot_path() -> Path:
    return _path('LAB_PLANNING_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'planning-snapshot.json')


def get_page_path() -> Path:
    return _path('LAB_PLANNING_PAGE_PATH', LAB_ROOT / 'docs' / 'planning' / 'index.html')


def get_repo_roots() -> dict[str, str]:
    raw = os.environ.get('LAB_REPO_ROOTS_JSON', '').strip()
    if raw:
        loaded = json.loads(raw)
        if isinstance(loaded, dict):
            return {str(key): str(value) for key, value in loaded.items()}
    return dict(DEFAULT_REPO_ROOTS)


def load_repomap_snapshot(
    *,
    repo_root: Path | None,
    repomap_enabled: bool,
    repomap_policy: dict[str, object] | None,
) -> dict[str, object]:
    compact_budget = (
        int(repomap_policy.get('compact_budget', 4000))
        if isinstance(repomap_policy, dict)
        else 4000
    )
    top_ranked_limit = (
        int(repomap_policy.get('top_ranked_files', 5))
        if isinstance(repomap_policy, dict)
        else 5
    )
    if not repomap_enabled:
        return {
            'status': 'disabled',
            'compact_budget': compact_budget,
            'top_ranked_limit': top_ranked_limit,
            'top_ranked_files': [],
        }
    if repo_root is None:
        return {
            'status': 'not-checked',
            'compact_budget': compact_budget,
            'top_ranked_limit': top_ranked_limit,
            'top_ranked_files': [],
        }

    compact_path = repo_root / 'docs' / 'ai' / 'repomap.compact.md'
    knowledge_path = repo_root / 'agents.knowledge.json'
    top_ranked_files: list[dict[str, object]] = []
    if knowledge_path.exists():
        try:
            knowledge = json.loads(knowledge_path.read_text())
        except Exception:
            knowledge = {}
        relevance = knowledge.get('relevance', [])
        if isinstance(relevance, list):
            for item in relevance[:top_ranked_limit]:
                if not isinstance(item, dict):
                    continue
                top_ranked_files.append(
                    {
                        'path': str(item.get('path', '')),
                        'score': int(item.get('score', 0) or 0),
                        'changed': bool(item.get('changed', False)),
                        'entrypoint': bool(item.get('entrypoint', False)),
                    }
                )

    return {
        'status': 'present' if compact_path.exists() else 'missing',
        'compact_budget': compact_budget,
        'top_ranked_limit': top_ranked_limit,
        'top_ranked_files': top_ranked_files,
    }


def run_planner() -> dict[str, object]:
    planner = get_planner_path()
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_roots = get_repo_roots()
        command = ['python3', str(planner), '--all', '--export-dir', tmpdir, '--format', 'json']
        for repo, path in sorted(repo_roots.items()):
            command.extend(['--repo-root', f'{repo}={path}'])
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
        batch_summary = json.loads((Path(tmpdir) / 'batch-summary.json').read_text())
        repos = []
        for repo_entry in batch_summary.get('repos', []):
            repo = repo_entry['repo']
            repo_dir = Path(tmpdir) / repo.replace('/', '-')
            plan = json.loads((repo_dir / 'plan.json').read_text())
            repo_root = Path(repo_roots[repo]) if repo in repo_roots else None
            workflow_with = plan['proposed_changes'][0]['workflow']['with']
            repomap_enabled = workflow_with.get('repomap') == 'true'
            repos.append(
                {
                    **repo_entry,
                    'plan': plan,
                    'repomap_snapshot': load_repomap_snapshot(
                        repo_root=repo_root,
                        repomap_enabled=repomap_enabled,
                        repomap_policy=plan.get('repomap_policy'),
                    ),
                    'files': [path.name for path in sorted(repo_dir.iterdir())],
                }
            )
        return {
            'version': 1,
            'source': 'SET planning snapshot',
            'planner': str(planner),
            'repo_count': len(repos),
            'repos': repos,
        }


def sort_key(entry: dict[str, object]) -> tuple[int, int, int, str]:
    queue_order = {'ready-now': 0, 'blocked-by-orchestrator': 1, 'review-later': 2}
    priority_order = {'high': 0, 'medium': 1, 'normal': 2}
    status_order = {'ready-for-review': 0, 'needs-wiring': 1}
    return (
        queue_order.get(str(entry.get('operator_queue')), 9),
        priority_order.get(str(entry.get('priority_hint')), 9),
        status_order.get(str(entry.get('status_hint')), 9),
        str(entry.get('repo')),
    )


def build_page(snapshot: dict[str, object]) -> str:
    repos = sorted(snapshot.get('repos', []), key=sort_key)
    sections = {'ready-now': [], 'blocked-by-orchestrator': [], 'review-later': []}
    first_blocked_slug = None
    for entry in repos:
        queue = str(entry.get('operator_queue') or entry.get('plan', {}).get('review_payload', {}).get('operator_queue') or 'review-later')
        sections.setdefault(queue, []).append(entry)
        blocked_by = entry.get('blocked_by') or entry.get('plan', {}).get('review_payload', {}).get('blocked_by') or []
        if first_blocked_slug is None and blocked_by:
            first_blocked_slug = entry['repo'].replace('/', '-')
    cards = []
    section_titles = {
        'ready-now': 'Ready now',
        'blocked-by-orchestrator': 'Blocked by orchestrator',
        'review-later': 'Review later',
    }
    section_notes = {
        'ready-now': 'Repos that are ready for manual review/apply right now.',
        'blocked-by-orchestrator': 'Repos whose requested capabilities still need SET wiring or orchestration support.',
        'review-later': 'Repos that are valid plans, but lower urgency than the ready-now queue.',
    }
    item_index = 1
    for queue in ('ready-now', 'blocked-by-orchestrator', 'review-later'):
        entries = sections.get(queue, [])
        if not entries:
            continue
        cards.append(f'''<section class="page-panel"><h2>{section_titles[queue]}</h2><p class="small-note">{section_notes[queue]}</p></section>''')
        for entry in entries:
            index = item_index
            item_index += 1
        plan = entry['plan']
        card_slug = entry['repo'].replace('/', '-')
        workflow = plan['proposed_changes'][0]['workflow']
        review_payload = plan['review_payload']
        gh_pr = review_payload['gh_pr_create']
        apply_sim = review_payload['apply_simulation']
        next_action_label = entry.get('next_action_label') or review_payload.get('next_action_label') or 'Next step'
        recommended_step = entry.get('recommended_operator_step') or review_payload.get('recommended_operator_step') or 'n/a'
        next_command = entry.get('next_shell_command') or review_payload.get('next_shell_command') or 'n/a'
        apply_readiness = entry.get('apply_readiness') or review_payload.get('apply_readiness') or 'unknown'
        workflow_sync_status = entry.get('workflow_sync_status') or 'not-checked'
        blocked_by = entry.get('blocked_by') or review_payload.get('blocked_by') or []
        capabilities = plan.get('capabilities', [])
        wiring_gaps = entry.get('wiring_gaps') or [cap.get('wiring_gap') for cap in capabilities if isinstance(cap, dict) and cap.get('wiring_gap')]
        repomap_snapshot = entry.get('repomap_snapshot', {}) if isinstance(entry.get('repomap_snapshot'), dict) else {}
        manual_steps = apply_sim.get('manual_steps', [])
        full_sequence = '\n'.join(manual_steps)
        pr_command = manual_steps[-1] if manual_steps else 'n/a'
        unmapped = plan.get('unmapped', [])
        blocked_html = ''
        if blocked_by:
            items = ''.join(f'<li>{item}</li>' for item in blocked_by)
            blocked_html = f'<div id="{card_slug}-blocked" class="small-note">Blocked by:</div><ul class="bullet-list">{items}</ul>'
        wiring_gap_html = ''
        if wiring_gaps:
            items = ''.join(
                f'<li><code>{gap.get("capability", "unknown")}</code>: {gap.get("message", "missing orchestrator wiring")}</li>'
                for gap in wiring_gaps
                if isinstance(gap, dict)
            )
            wiring_gap_html = f'<div class="small-note">Missing in orchestrator:</div><ul class="bullet-list">{items}</ul>'
        repomap_html = ''
        if repomap_snapshot:
            top_ranked = repomap_snapshot.get('top_ranked_files', [])
            ranked_html = ''
            if top_ranked:
                ranked_items = ''.join(
                    f"<li><code>{item['path']}</code> (score {item['score']})</li>"
                    for item in top_ranked
                    if isinstance(item, dict) and item.get('path')
                )
                ranked_html = f'<div class="small-note">Top ranked files:</div><ul class="bullet-list">{ranked_items}</ul>'
            repomap_html = (
                f"<div class=\"small-note\">Compact repomap: {repomap_snapshot.get('status', 'not-checked')} "
                f"(budget {repomap_snapshot.get('compact_budget', 'n/a')}, top files {repomap_snapshot.get('top_ranked_limit', 'n/a')})</div>"
                f"{ranked_html}"
            )
        cards.append(
            f'''<section id="{card_slug}" class="page-panel">
            <h2>{index}. {entry['repo']}</h2>
            <p class="small-note">Queue: {entry.get('operator_queue', review_payload.get('operator_queue', 'review-later'))} | Status: {entry['status_hint']} | Priority: {entry['priority_hint']} | Apply: {apply_readiness} | Workflow sync: {workflow_sync_status}</p>
            <p class="small-note"><a href="#status-{entry['status_hint']}">Why {entry['status_hint']}?</a> | <a href="#priority-{entry['priority_hint']}">Why {entry['priority_hint']}?</a>{' | <a href="#' + card_slug + '-blocked">Show blockers</a>' if blocked_by or wiring_gaps else ''}</p>
            <ul class="bullet-list">
              <li>Workflow preset: {workflow['with'].get('workflow_preset', 'none')}</li>
              <li>Target workflow: {entry['target_workflow']}</li>
              <li>Suggested branch: {gh_pr['head']}</li>
              <li>Suggested title: {gh_pr['title']}</li>
              <li>{next_action_label}: {recommended_step}</li>
              <li>Workflow sync status: {workflow_sync_status}</li>
            </ul>
            <div class="small-note">Copy next command:</div>
            <pre><code>{next_command}</code></pre>
            <div class="small-note">Copy PR command:</div>
            <pre><code>{pr_command}</code></pre>
            <div class="small-note">Copy full sequence:</div>
            <pre><code>{full_sequence}</code></pre>
            {repomap_html}
            {blocked_html}
            {wiring_gap_html}
            <div class="link-grid"><a class="button" href="../repos/index.html">Repo cards</a><a class="button-secondary" href="../registry/index.html">Registry</a><a class="button-secondary" href="../status/index.html">Status</a><a class="button-secondary" href="../assets/planning-snapshot.json">JSON snapshot</a></div>
          </section>'''
        )
    cards_html = '\n'.join(cards)
    blocked_link = f'<a class="button-secondary" href="#{first_blocked_slug}-blocked">Show blockers first</a>' if first_blocked_slug else ''
    return f'''<!doctype html>
<html lang="en" data-style="ascii" data-ascii-mode="light">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Planning Snapshot | ABVX Lab</title>
    <meta name="description" content="Read-only planning queue for SET config-apply review across registered repos." />
    <link rel="canonical" href="https://lab.abvx.xyz/planning/" />
    <meta property="og:title" content="Planning Snapshot | ABVX Lab" />
    <meta property="og:description" content="Read-only planning queue for SET config-apply review across registered repos." />
    <meta property="og:url" content="https://lab.abvx.xyz/planning/" />
    <meta property="og:type" content="website" />
    <meta property="og:image" content="https://lab.abvx.xyz/assets/og.png" />
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="stylesheet" href="../assets/asciitheme.css?v20260319d" />
    <link rel="stylesheet" href="../assets/styles.css?v20260320a" />
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"CollectionPage","name":"Planning Snapshot","url":"https://lab.abvx.xyz/planning/","description":"Read-only planning queue for SET config-apply review across registered repos."}}</script>
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
            <h1>What to review next</h1>
            <p class="lead">Read-only planning queue generated from SET config-apply plans across registered repos.</p>
            <p class="small-note">This is an operator view only: priority/status hints, suggested branches, and manual next steps. No repo mutation.</p>
            <div class="link-grid"><a class="button" href="../repos/index.html">Repo cards</a><a class="button-secondary" href="../registry/index.html">Registry</a><a class="button-secondary" href="../status/index.html">Status</a><a class="button-secondary" href="../assets/planning-snapshot.json">JSON snapshot</a>{blocked_link}</div>
            <p class="small-note">Queue counts: ready-now={len(sections.get('ready-now', []))}, blocked-by-orchestrator={len(sections.get('blocked-by-orchestrator', []))}, review-later={len(sections.get('review-later', []))}</p>
          </section>
          <section class="page-panel">
            <h2>Semantics</h2>
            <ul class="bullet-list">
              <li id="status-ready-for-review"><strong>ready-for-review</strong>: no unmapped fields in the current SET contract; manual PR review can start now.</li>
              <li id="status-needs-wiring"><strong>needs-wiring</strong>: registry asks for capabilities not yet exposed by SET action inputs.</li>
              <li id="priority-high"><strong>high</strong>: central repo or site-heavy flow worth reviewing first.</li>
              <li id="priority-medium"><strong>medium</strong>: useful plan, but still blocked by missing wiring or follow-up work.</li>
              <li id="priority-normal"><strong>normal</strong>: valid planning candidate without urgency signal.</li>
              <li id="apply-ready"><strong>apply: ready</strong>: no current blockers in the planner contract.</li>
              <li id="apply-blocked"><strong>apply: blocked</strong>: planner sees explicit blockers that should be cleared before apply review.</li>
              <li><strong>Missing in orchestrator</strong>: requested capabilities that exist in registry config but are not yet wired into SET action inputs.</li>
            </ul>
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
    snapshot = run_planner()
    output_json = get_snapshot_path()
    output_html = get_page_path()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(snapshot, indent=2) + '\n')
    output_html.write_text(build_page(snapshot))
    print(f'Wrote {output_json}')
    print(f'Wrote {output_html}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
