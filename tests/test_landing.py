"""Checks for the self-contained GitHub Pages landing page."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def test_landing_page_content():
    page = ROOT / "index.html"
    assert page.is_file()
    html = page.read_text(encoding="utf-8")

    assert re.search(r"<title>\s*Problems\s*</title>", html, re.IGNORECASE)
    assert "A catalog of the world's problems, from mosquitoes to AI." in html
    csp = re.search(
        r'<meta\s+http-equiv="Content-Security-Policy"\s+content="([^"]+)"',
        html,
        re.IGNORECASE,
    )
    assert csp is not None
    assert "default-src 'self'" in csp.group(1)
    assert re.search(r'<img\b[^>]*\bsrc="assets/hero\.png"', html, re.IGNORECASE)
    assert "https://github.com/hopan/problems" in html
    assert "MIT" in html
    assert re.search(r'<a\b[^>]*\bhref="LICENSE"', html, re.IGNORECASE)

    external_urls = re.findall(r'(?:src|href)="(https?://[^"]+)"', html, re.IGNORECASE)
    assert all(url == "https://github.com/hopan/problems" for url in external_urls)
    assert "<script" not in html.lower()


def test_mit_license():
    license_file = ROOT / "LICENSE"
    assert license_file.is_file()
    assert "MIT License" in license_file.read_text(encoding="utf-8")
