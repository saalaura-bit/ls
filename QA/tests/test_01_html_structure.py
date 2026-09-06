"""
test_html.py - Tests de estructura HTML.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checks import check_html_structure, check_links, check_performance

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
HTML_FILES = list(PROJECT_DIR.glob("*.html"))


def get_html_files():
    return [f for f in HTML_FILES if f.suffix == ".html"]


class TestHTMLStructure:
    def test_has_doctype(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_html_structure(content, f.name)
            doctype_issues = [i for i in issues if "DOCTYPE" in i["message"]]
            assert len(doctype_issues) == 0, f"{f.name}: Missing DOCTYPE"

    def test_has_charset(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            assert 'charset="UTF-8"' in content or "charset=utf-8" in content.lower(), \
                f"{f.name}: Missing charset"

    def test_has_viewport(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            assert 'name="viewport"' in content, f"{f.name}: Missing viewport meta"

    def test_has_lang(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            assert 'lang="' in content, f"{f.name}: Missing lang attribute"

    def test_has_title(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_html_structure(content, f.name)
            title_issues = [i for i in issues if "title" in i["message"].lower() and i["severity"] == "error"]
            assert len(title_issues) == 0, f"{f.name}: Missing title"

    def test_title_not_empty(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            import re
            match = re.search(r"<title>(.*?)</title>", content, re.DOTALL | re.IGNORECASE)
            assert match and match.group(1).strip(), f"{f.name}: Empty title"

    def test_all_html_files_exist(self):
        expected = ["index.html", "qa-lead.html", "ba.html", "scrum-master.html", "mentoring.html", "privacy.html"]
        for name in expected:
            assert (PROJECT_DIR / name).exists(), f"Missing file: {name}"

    def test_css_file_exists(self):
        assert (PROJECT_DIR / "styles.css").exists(), "Missing styles.css"

    def test_links_valid(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_links(html_content=content, base_path=PROJECT_DIR, filename=f.name)
            broken = [i for i in issues if i["severity"] == "error"]
            assert len(broken) == 0, f"{f.name}: Broken links: {[i['message'] for i in broken]}"

    def test_file_size(self):
        for f in get_html_files():
            content = f.read_text(encoding="utf-8", errors="ignore")
            issues = check_performance(content, f.name)
            size_issues = [i for i in issues if "Large HTML" in i["message"]]
            assert len(size_issues) == 0, f"{f.name}: File too large"
