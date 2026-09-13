from __future__ import annotations

import json
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "https://lab.abvx.xyz"


def fetch(path: str) -> tuple[int, str]:
    request = Request(f"{BASE_URL}{path}", headers={"User-Agent": "abvx-lab-live-verifier/1"})
    with urlopen(request, timeout=20) as response:
        return response.status, response.read().decode("utf-8")


def main() -> int:
    checks = {
        "/": ("Turn a GitHub repo into an AI-ready workspace.", 'rel="canonical" href="https://lab.abvx.xyz/"'),
        "/repos/": ("Repo cards",),
        "/planning/": ("Planning",),
        "/proof/": ("Proof",),
        "/registry/": ("Registry",),
        "/status/": ("Workflow",),
        "/llms.txt": ("Project: ABVX Lab",),
        "/robots.txt": ("Sitemap: https://lab.abvx.xyz/sitemap.xml",),
        "/sitemap.xml": ("https://lab.abvx.xyz/tools/agentsgen/",),
    }
    errors: list[str] = []
    for path, markers in checks.items():
        try:
            status, body = fetch(path)
        except (HTTPError, URLError, TimeoutError) as error:
            errors.append(f"{path}: request failed ({error})")
            continue
        if status != 200:
            errors.append(f"{path}: returned HTTP {status}")
        for marker in markers:
            if marker not in body:
                errors.append(f"{path}: missing marker {marker!r}")
        if "/Users/" in body or "\\Users\\" in body:
            errors.append(f"{path}: exposes a local user path")

    for path in ("/.well-known/agent-card.json", "/.well-known/integrations.json", "/.well-known/agent-skills/index.json"):
        try:
            status, body = fetch(path)
            if status != 200:
                errors.append(f"{path}: returned HTTP {status}")
            json.loads(body)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
            errors.append(f"{path}: invalid discovery response ({error})")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Live verification passed: {BASE_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
