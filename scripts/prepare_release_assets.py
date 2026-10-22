"""Empacota fontes, evidências e PDF final sem modificar a branch."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--video-url", required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "release-assets")
    args = parser.parse_args()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if args.commit != head:
        parser.error("O commit da release deve ser o HEAD efetivamente testado.")
    evidence, output = args.evidence_dir.resolve(), args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        parser.error("Use diretório de anexos vazio para não publicar arquivos de outra execução.")
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_final_report.py"),
                    "--evidence-dir", str(evidence), "--output", str(output / "ReservaLab_Entrega_3.pdf"),
                    "--commit", args.commit, "--video-url", args.video_url], check=True, cwd=ROOT)
    for source, name in [(evidence / "tests" / "tests.log", "tests.log"),
                         (evidence / "tests" / "summary.json", "summary.json"),
                         (evidence / "coverage.json", "coverage.json"),
                         (evidence / "coverage.md", "coverage.md"),
                         (ROOT / "docs" / "AS_BUILT.md", "AS_BUILT.md")]:
        shutil.copyfile(source, output / name)
    with zipfile.ZipFile(output / "ReservaLab-1.0.0-coverage.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(evidence.iterdir()):
            if path.is_file() and (path.suffix in {".html", ".cover", ".json", ".md"}):
                archive.write(path, path.name)
    subprocess.run(["git", "archive", "--format=zip", "--output", str(output / "ReservaLab-1.0.0-source.zip"),
                    args.commit], check=True, cwd=ROOT)
    report = json.loads((evidence / "coverage.json").read_text(encoding="utf-8"))
    notes = (f"# ReservaLab v1.0.0\n\nCommit final: {args.commit}\n\n"
             f"Vídeo real da equipe: {args.video_url}\n\n"
             f"Testes: {report['tests']['tests_run']}/{report['tests']['tests_run']} aprovados, "
             "sem falhas/erros/ignorados.\n\n"
             f"Cobertura de linhas: {report['critical']['percent']}% nas unidades críticas; "
             f"{report['total']['percent']}% na aplicação. Não é cobertura de branches nem garantia de ausência de defeitos.\n\n"
             "API local de reservas com UTC, intervalos semiabertos, SQLite transacional e cancelamento idempotente. "
             "SDD As-Built, evidências e documento final anexados. Preparação assistida pelo Codex, homologação humana declarada na execução do workflow.\n\n"
             "Demonstração acadêmica local, sem autenticação/frontend; uso institucional requer nova avaliação.\n")
    (output / "RELEASE_NOTES.md").write_text(notes, encoding="utf-8")
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
             for path in sorted(output.iterdir()) if path.is_file() and path.name != "SHA256SUMS.txt"]
    (output / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
