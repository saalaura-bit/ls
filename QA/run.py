"""
run.py - Entry point para el agente QA web.
Proyecto: 001-portfolio-web
"""
import sys
from pathlib import Path
from datetime import datetime

from agent import run_web_qa
from checks import run_all_checks, generate_summary
from report import generate_report


def main():
    if len(sys.argv) > 1:
        project_path = Path(sys.argv[1])
    else:
        default_path = Path(__file__).resolve().parent.parent
        project_path = Path(input(f"Ruta del proyecto [{default_path}] > ") or str(default_path))

    if not project_path.exists():
        print(f"Error: Directorio no encontrado: {project_path}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  QA Agent - Proyecto: {project_path.name}")
    print(f"  Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    print("📋 Ejecutando checks estáticos...")
    static_issues = run_all_checks(project_path)
    summary = generate_summary(static_issues)

    print(f"   Encontrados: {summary['errors']} errores, {summary['warnings']} warnings, {summary['info']} info\n")

    print("🤖 Ejecutando agente QA con LLM...")
    llm_report = run_web_qa(project_path)

    print("\n📄 Generando reporte final...")
    report_path = generate_report(
        project_name=project_path.name,
        project_path=str(project_path),
        static_issues=static_issues,
        summary=summary,
        llm_report=llm_report,
    )

    print(f"\n✅ Reporte guardado en: {report_path}")
    print(f"\n{'='*60}")
    print(f"  RESUMEN")
    print(f"{'='*60}")
    print(f"  Score: {max(0, 100 - summary['errors']*5 - summary['warnings']*2 - summary['info']*0.5):.0f}/100")
    print(f"  Errores: {summary['errors']}")
    print(f"  Warnings: {summary['warnings']}")
    print(f"  Info: {summary['info']}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
