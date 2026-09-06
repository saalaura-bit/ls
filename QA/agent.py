"""
agent.py - Agente QA especializado en testing web.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "agentes-ai"))

from llm import agent_loop
from tools import BASE_TOOLS

SYSTEM = """Sos un agente de QA senior especializado en testing de sitios web estáticos.

Tarea: dado un directorio de un proyecto web, analizás TODOS los archivos HTML y CSS
y generás un reporte completo de calidad.

## Checklist de validación

### 1. HTML Structure
- DOCTYPE declaration
- charset UTF-8
- viewport meta tag
- lang attribute on <html>
- <title> tag present and non-empty
- Valid nesting (tags properly closed)

### 2. SEO
- meta description (50-160 chars)
- Open Graph tags (og:title, og:description, og:image, og:url)
- Canonical link tag
- Single H1 per page
- Proper heading hierarchy (H1 > H2 > H3)

### 3. Links
- All internal links point to existing files
- External links use https://
- Links have aria-label or title for accessibility

### 4. Accessibility
- All images have alt attributes
- Navigation has aria-label
- Form elements have labels
- Color contrast considerations
- Semantic HTML usage (nav, main, section, article)

### 5. Consistency
- Navigation identical across all pages
- Footer consistent across all pages
- Branding (name, logo) consistent

### 6. i18n (EN/ES)
- Each .en element has a corresponding .es element
- No text identical in both languages (untranslated)
- Language toggle works correctly

### 7. Performance
- File size reasonable (< 100KB)
- Minimal inline styles
- External CSS/JS count reasonable

### 8. Bugs
- Duplicate IDs
- Unclosed tags
- JavaScript errors (reference to non-existent elements)
- CSS issues (missing classes, unused styles)

## Instructions
1. List all files in the project directory
2. Read each HTML file completely
3. Read the CSS file
4. Run all checks from the checklist above
5. Generate a structured report with:
   - Executive summary (pass/fail, score)
   - Issues by severity (error, warning, info)
   - Issues by file
   - Recommendations
   - Specific line numbers when possible

## Output format
Respond in Spanish. Use Markdown format for the report.
Include file:line references when reporting issues.
Score: 0-100 based on errors (-5 each), warnings (-2 each), info (-0.5 each).

IMPORTANT: Be thorough. Read every file completely before reporting.
"""


def run_web_qa(project_path):
    """Ejecuta el agente QA contra un proyecto web."""
    project_path = Path(project_path)
    if not project_path.exists():
        return f"Error: Directorio no encontrado: {project_path}"

    user_msg = f"""Analizá el proyecto web en: {project_path}

Pasos:
1. Usá list_files para ver todos los archivos del directorio
2. Leé cada archivo HTML (.html) completamente
3. Leé el archivo CSS (styles.css) completamente
4. Aplicá todo el checklist de validación
5. Generá el reporte completo en Markdown

Recordá: project_path = {project_path}"""

    result = agent_loop(SYSTEM, user_msg, BASE_TOOLS, max_steps=20)
    return result


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Ruta del proyecto web > ")

    print(f"\n🔍 Ejecutando QA Agent contra: {path}\n")
    report = run_web_qa(path)
    print(report)
