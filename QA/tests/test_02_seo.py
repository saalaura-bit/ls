"""
test_seo.py - Tests de SEO.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checks import check_seo

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent


def get_html_files():
    return list(PROJECT_DIR.glob("*.html"))


class TestSEO:
    def test_meta_description_exists(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_seo(content, f.name)
            desc_issues = [i for i in issues if "meta description" in i["message"].lower() and i["severity"] == "error"]
            assert len(desc_issues) == 0, f"{f.name}: Missing meta description"

    def test_meta_description_length(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_seo(content, f.name)
            length_issues = [i for i in issues if "description" in i["message"].lower() and "short" in i["message"].lower()]
            assert len(length_issues) == 0, f"{f.name}: Meta description too short"

    def test_h1_exists(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_seo(content, f.name)
            h1_issues = [i for i in issues if "H1" in i["message"] and i["severity"] == "error"]
            assert len(h1_issues) == 0, f"{f.name}: No H1 tag"

    def test_single_h1(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            h1_count = len(re.findall(r"<h1\b", content, re.IGNORECASE))
            assert h1_count <= 1, f"{f.name}: Multiple H1 tags ({h1_count})"

    def test_og_tags(self):
        required_og = ["og:title", "og:description"]
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            for tag in required_og:
                assert tag in content, f"{f.name}: Missing {tag}"

    def test_title_contains_name(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"<title>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
            assert match, f"{f.name}: No title tag"
            title = match.group(1)
            assert "Maria Laura" in title or "Saavedra" in title, \
                f"{f.name}: Title doesn't contain name: {title}"
