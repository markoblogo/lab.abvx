from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_site import verify_site


class VerifySiteTests(unittest.TestCase):
    def test_accepts_a_complete_minimal_site(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<title>Example</title><meta name="description" content="Example site">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<link rel="canonical" href="https://example.test/">'
                '<a href="about/">About</a><img src="logo.svg" alt="Logo">'
            )
            (root / "about").mkdir()
            (root / "about" / "index.html").write_text(
                '<title>About</title><meta name="description" content="About example">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<link rel="canonical" href="https://example.test/about/">'
                '<a href="../">Home</a>'
            )
            (root / "logo.svg").write_text("<svg></svg>")
            (root / "robots.txt").write_text("User-agent: *\nSitemap: https://example.test/sitemap.xml\n")
            (root / "sitemap.xml").write_text(
                '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                '<url><loc>https://example.test/</loc></url>'
                '<url><loc>https://example.test/about/</loc></url></urlset>'
            )
            (root / "manifest.json").write_text(json.dumps({"version": 1}))

            self.assertEqual([], verify_site(root, "https://example.test"))

    def test_reports_broken_links_and_missing_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text('<a href="missing/">Missing</a>')
            (root / "robots.txt").write_text("User-agent: *\n")
            (root / "sitemap.xml").write_text(
                '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                '<url><loc>https://example.test/</loc></url></urlset>'
            )

            errors = verify_site(root, "https://example.test")

            self.assertTrue(any("broken local reference" in error for error in errors))
            self.assertTrue(any("missing <title>" in error for error in errors))
            self.assertTrue(any("missing canonical" in error for error in errors))

    def test_rejects_local_user_paths_in_public_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(
                '<title>Example</title><meta name="description" content="Example site">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<link rel="canonical" href="https://example.test/">'
            )
            (root / "robots.txt").write_text("Sitemap: https://example.test/sitemap.xml\n")
            (root / "sitemap.xml").write_text(
                '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                '<url><loc>https://example.test/</loc></url></urlset>'
            )
            (root / "snapshot.json").write_text('{"source": "/Users/example/project"}')

            errors = verify_site(root, "https://example.test")

            self.assertTrue(any("contains a local user path" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
