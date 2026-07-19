from __future__ import annotations

import argparse
import html
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from datetime import datetime, timezone
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
START = '<!-- CORTEXABV_HOME_LEDGER:START -->'
END = '<!-- CORTEXABV_HOME_LEDGER:END -->'


def path_from_env(name: str, default: Path) -> Path:
    value = os.environ.get(name, '').strip()
    return Path(value) if value else default


def github_json(path: str) -> dict[str, object]:
    token = os.environ.get('SOURCE_REPOS_TOKEN', '').strip()
    if not token:
        raise SystemExit('SOURCE_REPOS_TOKEN is required for Lab home-ledger source reads')
    request = Request(
        f'https://api.github.com/{path}',
        headers={
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
            'User-Agent': 'cortex-abv-lab-home-ledger',
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as error:
        raise SystemExit(f'GitHub source read failed for {path}: HTTP {error.code}') from error
    except URLError as error:
        raise SystemExit(f'GitHub source read failed for {path}: {error.reason}') from error


def commit_for(entry: dict[str, object], offline: dict[str, object] | None) -> dict[str, str]:
    repository = str(entry['repository'])
    ref = str(entry.get('ref') or 'main')
    if offline is not None:
        payload = offline.get(repository)
        if not isinstance(payload, dict):
            raise SystemExit(f'offline evidence missing {repository}')
    else:
        payload = github_json(f'repos/{repository}/commits/{ref}')
    sha = payload.get('sha')
    commit = payload.get('commit')
    committer = commit.get('committer') if isinstance(commit, dict) else None
    timestamp = committer.get('date') if isinstance(committer, dict) else None
    if not isinstance(sha, str) or not isinstance(timestamp, str):
        raise SystemExit(f'invalid commit response for {repository}@{ref}')
    return {'repository': repository, 'ref': ref, 'sha': sha, 'committedAt': timestamp, 'date': timestamp[:10]}


def render_row(entry: dict[str, object], evidence: dict[str, str]) -> str:
    name = html.escape(str(entry['name']))
    summary = html.escape(str(entry['summary']))
    preset = html.escape(str(entry['preset']))
    state = html.escape(str(entry['state']))
    queue = html.escape(str(entry['queue']))
    href = html.escape(str(entry['href']), quote=True)
    return f'''            <a class="lab-b-ledger-row lab-b-ledger-link" href="{href}" aria-label="Open {name}">
              <div class="lab-b-ledger-name">
                <strong>{name}</strong>
                <span>{summary}</span>
              </div>
              <div class="lab-b-ledger-preset">{preset}</div>
              <div class="lab-b-ledger-date">{evidence['date']}</div>
              <div class="lab-b-ledger-state">{state}</div>
              <div class="lab-b-ledger-queue"><span class="lab-b-queue-pill ready">{queue}</span></div>
            </a>'''


def main() -> int:
    parser = argparse.ArgumentParser(description='Rebuild the Lab home control-plane ledger from allowlisted repository commit evidence.')
    parser.add_argument('--offline-evidence', type=Path, help='JSON object keyed by repository; use for deterministic tests.')
    args = parser.parse_args()
    source_path = path_from_env('LAB_HOME_LEDGER_SOURCES_PATH', LAB_ROOT / 'docs' / 'assets' / 'home-ledger-sources.v1.json')
    index_path = path_from_env('LAB_HOME_PAGE_PATH', LAB_ROOT / 'docs' / 'index.html')
    snapshot_path = path_from_env('LAB_HOME_LEDGER_SNAPSHOT_PATH', LAB_ROOT / 'docs' / 'assets' / 'home-ledger-snapshot.v1.json')
    config = json.loads(source_path.read_text())
    if config.get('schemaVersion') != 1 or config.get('authority') != 'read' or not isinstance(config.get('entries'), list):
        raise SystemExit('home ledger source config must be schemaVersion 1, read-only, and contain entries[]')
    offline = json.loads(args.offline_evidence.read_text()) if args.offline_evidence else None
    rows = []
    evidence = []
    for entry in config['entries']:
        if not isinstance(entry, dict):
            raise SystemExit('home ledger entries must be objects')
        item = commit_for(entry, offline)
        rows.append(render_row(entry, item))
        evidence.append({'id': entry['id'], **item})
    document = index_path.read_text()
    if document.count(START) != 1 or document.count(END) != 1:
        raise SystemExit('Lab home ledger markers are missing or ambiguous')
    replacement = f'{START}\n' + '\n'.join(rows) + f'\n            {END}'
    before, tail = document.split(START, 1)
    _, after = tail.split(END, 1)
    index_path.write_text(before + replacement + after)
    snapshot_path.write_text(json.dumps({
        'schemaVersion': 1,
        'kind': 'CortexABVLabHomeLedgerSnapshot',
        'authority': 'read',
        'generatedAt': datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z'),
        'sources': evidence,
    }, indent=2) + '\n')
    print(f'Wrote {index_path}')
    print(f'Wrote {snapshot_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
