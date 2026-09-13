from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.has_title = False
        self.has_description = False
        self.has_viewport = False
        self.canonical: str | None = None
        self.references: list[str] = []
        self.images_without_alt = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "title":
            self.has_title = True
        if tag == "meta" and values.get("name", "").lower() == "description" and values.get("content", "").strip():
            self.has_description = True
        if tag == "meta" and values.get("name", "").lower() == "viewport":
            self.has_viewport = True
        if tag == "link" and "canonical" in values.get("rel", "").lower().split():
            self.canonical = values.get("href")
        if tag in {"a", "link"} and values.get("href"):
            self.references.append(values["href"] or "")
        if tag in {"img", "script", "source"} and values.get("src"):
            self.references.append(values["src"] or "")
        if tag == "img" and "alt" not in values:
            self.images_without_alt += 1


def _local_target(root: Path, page: Path, reference: str) -> Path | None:
    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    clean = unquote(parsed.path)
    if not clean:
        return None
    target = root / clean.lstrip("/") if clean.startswith("/") else page.parent / clean
    target = target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return target
    if clean.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def verify_site(root: Path, base_url: str) -> list[str]:
    root = root.resolve()
    base_url = base_url.rstrip("/")
    errors: list[str] = []
    canonical_urls: set[str] = set()

    for path in sorted(root.rglob("*.html")):
        relative = path.relative_to(root)
        parser = PageParser()
        try:
            source = path.read_text(encoding="utf-8")
            parser.feed(source)
        except (OSError, UnicodeError) as error:
            errors.append(f"{relative}: unreadable HTML ({error})")
            continue
        if not parser.has_title:
            errors.append(f"{relative}: missing <title>")
        if not parser.has_description:
            errors.append(f"{relative}: missing meta description")
        if not parser.has_viewport:
            errors.append(f"{relative}: missing viewport metadata")
        if not parser.canonical:
            errors.append(f"{relative}: missing canonical URL")
        elif not parser.canonical.startswith(f"{base_url}/"):
            errors.append(f"{relative}: canonical URL is outside {base_url}")
        else:
            canonical_urls.add(parser.canonical)
        if parser.images_without_alt:
            errors.append(f"{relative}: {parser.images_without_alt} image(s) missing alt text")
        if "/Users/" in source or "\\Users\\" in source:
            errors.append(f"{relative}: contains a local user path")
        for reference in parser.references:
            target = _local_target(root, path, reference)
            if target is not None and (not target.is_relative_to(root) or not target.exists()):
                errors.append(f"{relative}: broken local reference {reference}")

    for path in sorted(root.rglob("*.json")):
        try:
            source = path.read_text(encoding="utf-8")
            json.loads(source)
            if "/Users/" in source or "\\Users\\" in source:
                errors.append(f"{path.relative_to(root)}: contains a local user path")
        except (json.JSONDecodeError, OSError, UnicodeError) as error:
            errors.append(f"{path.relative_to(root)}: invalid JSON ({error})")

    sitemap_path = root / "sitemap.xml"
    sitemap_urls: set[str] = set()
    try:
        tree = ET.parse(sitemap_path)
        sitemap_urls = {element.text.strip() for element in tree.findall("{*}url/{*}loc") if element.text}
    except (ET.ParseError, OSError) as error:
        errors.append(f"sitemap.xml: invalid sitemap ({error})")
    for url in sorted(canonical_urls - sitemap_urls):
        errors.append(f"sitemap.xml: missing canonical page {url}")
    for url in sorted(sitemap_urls - canonical_urls):
        errors.append(f"sitemap.xml: URL has no matching canonical page {url}")

    robots_path = root / "robots.txt"
    try:
        robots = robots_path.read_text(encoding="utf-8")
        if f"Sitemap: {base_url}/sitemap.xml" not in robots:
            errors.append("robots.txt: missing canonical sitemap declaration")
    except OSError as error:
        errors.append(f"robots.txt: unreadable ({error})")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the ABVX Lab static site before publishing.")
    parser.add_argument("root", nargs="?", type=Path, default=Path("docs"))
    parser.add_argument("--base-url", default="https://lab.abvx.xyz")
    args = parser.parse_args()
    errors = verify_site(args.root, args.base_url)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Site verification failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Site verification passed: {args.root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
