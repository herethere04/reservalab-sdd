"""Executa o harness real e mede linhas da aplicação com a biblioteca padrão."""

import argparse
import ast
import dis
import hashlib
import html
import json
import sys
import trace
import types
from pathlib import Path

import run_tests as harness


ROOT = Path(__file__).resolve().parents[1]
CRITICAL = {"domain.py", "repository.py", "service.py", "server.py"}


class ApplicationTrace(trace.Trace):
    """Evita o cache por nome curto do trace ignorar __init__ de pacotes locais."""

    def __init__(self):
        super().__init__(count=True, trace=False)
        self.package = (ROOT / "reservalab").resolve()
        self.globaltrace = self.application_trace

    def application_trace(self, frame, event, arg):
        if event == "call":
            filename = frame.f_code.co_filename
            if not filename.startswith("<") and Path(filename).resolve().is_relative_to(self.package):
                return self.localtrace
        return None


def executable_lines(path):
    """Linhas do bytecode CPython, sem docstrings; não é cobertura de branches."""
    source = path.read_text(encoding="utf-8")
    excluded = set()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                if isinstance(body[0].value.value, str):
                    excluded.update(range(body[0].lineno, body[0].end_lineno + 1))
    lines = set()

    def collect(code):
        lines.update(line for _, line in dis.findlinestarts(code) if line is not None and line > 0)
        for value in code.co_consts:
            if isinstance(value, types.CodeType):
                collect(value)

    collect(compile(source, str(path), "exec"))
    return lines - excluded


def measure(counts):
    modules = []
    for path in sorted((ROOT / "reservalab").rglob("*.py")):
        executable = executable_lines(path)
        hit = {line for (name, line), count in counts.items()
               if Path(name).resolve() == path.resolve() and count > 0} & executable
        modules.append({
            "path": path.relative_to(ROOT).as_posix(),
            "critical": path.name in CRITICAL,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "executable_lines": len(executable),
            "covered_lines": len(hit),
            "missing_lines": sorted(executable - hit),
            "covered_line_numbers": sorted(hit),
            "percent": round(100 * len(hit) / len(executable), 2) if executable else None,
        })
    return modules


def aggregate(modules):
    total = sum(row["executable_lines"] for row in modules)
    covered = sum(row["covered_lines"] for row in modules)
    return {"executable_lines": total, "covered_lines": covered,
            "percent": round(100 * covered / total, 2) if total else None}


def write_reports(output, report):
    output.mkdir(parents=True, exist_ok=True)
    (output / "coverage.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    rows = ["# Cobertura real de linhas - ReservaLab", "", report["method"], "",
            "| Módulo | Executadas / executáveis | Cobertura | Linhas ausentes |",
            "| --- | --- | --- | --- |"]
    table = []
    annotations = []
    for item in report["modules"]:
        percent = f"{item['percent']:.2f}%" if item["percent"] is not None else "sem linhas executáveis"
        missing = ", ".join(map(str, item["missing_lines"])) or "nenhuma"
        ratio = f"{item['covered_lines']} / {item['executable_lines']}"
        rows.append(f"| {item['path']} | {ratio} | {percent} | {missing} |")
        table.append(f"<tr><td>{item['path']}</td><td>{ratio}</td><td>{percent}</td><td>{missing}</td></tr>")
        source = (ROOT / item["path"]).read_text(encoding="utf-8").splitlines()
        hits, absent = set(item["covered_line_numbers"]), set(item["missing_lines"])
        annotated = []
        plain = []
        for number, line in enumerate(source, 1):
            state = "hit" if number in hits else "miss" if number in absent else "neutral"
            mark = "+" if state == "hit" else "!" if state == "miss" else " "
            plain.append(f"{mark} {number:4} {line}")
            annotated.append(f'<span class="{state}">{number:4} {html.escape(line)}</span>')
        (output / (item["path"].replace("/", ".") + ".cover")).write_text("\n".join(plain) + "\n", encoding="utf-8")
        annotations.append(f"<h2>{item['path']}</h2><pre>" + "\n".join(annotated) + "</pre>")
    for key, title in [("critical", "Unidades críticas"), ("total", "Aplicação completa")]:
        item = report[key]
        rows += ["", f"{title}: {item['covered_lines']}/{item['executable_lines']} linhas ({item['percent']}%)."]
    rows += ["", "A suíte e o log estão em tests/summary.json e tests/tests.log. Linhas ausentes são preservadas.",
             "Subprocessos de fixtures não são instrumentados. Código externo, bibliotecas nativas e branches não são medidos.",
             "Os testes HTTP em threads criadas durante a execução são instrumentados."]
    (output / "coverage.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    page = """<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>ReservaLab - cobertura</title>
<style>body{font:16px sans-serif;max-width:1100px;margin:36px auto;color:#172d46}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ced8df;padding:8px;text-align:left}th{background:#eaf3f5}pre{background:#f4f7f9;padding:16px;overflow:auto;font-size:13px}.hit{background:#e4f4ea;display:block}.miss{background:#ffe2e2;display:block}.neutral{display:block}</style>
<h1>ReservaLab - cobertura real de linhas</h1><p>""" + html.escape(report["method"]) + "</p>"
    page += f"<p>Suíte: {report['tests']['tests_run']} testes; sucesso: {report['tests']['success']}. Críticos: {report['critical']['percent']}%; aplicação: {report['total']['percent']}%.</p>"
    page += "<table><tr><th>Módulo</th><th>Linhas</th><th>Cobertura</th><th>Ausentes</th></tr>" + "".join(table) + "</table>" + "".join(annotations) + "</html>"
    (output / "index.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "evidence" / "coverage")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    tracer = ApplicationTrace()
    previous = sys.argv
    try:
        sys.argv = [str(ROOT / "scripts" / "run_tests.py"), "--output-dir", str(output / "tests")]
        context = {"harness": harness}
        tracer.runctx("exit_code = harness.main()", context, context)
    finally:
        sys.argv = previous
    tests = json.loads((output / "tests" / "summary.json").read_text(encoding="utf-8"))
    modules = measure(tracer.results().counts)
    report = {"method": "CPython trace + tabelas de linhas do bytecode, docstrings excluídas; cobertura de linhas, não de branches.",
              "timestamp_utc": tests["timestamp_utc"], "python": tests["python"],
              "git": tests["git"], "source_snapshot": tests["source_snapshot"],
              "tests": {key: tests[key] for key in ["tests_run", "failures", "errors", "skipped", "success"]},
              "modules": modules, "critical": aggregate([row for row in modules if row["critical"]]),
              "total": aggregate(modules)}
    write_reports(output, report)
    print(f"\nCobertura das unidades críticas: {report['critical']['percent']}%")
    print(f"Cobertura de toda a aplicação: {report['total']['percent']}%")
    print(f"Relatório: {output / 'index.html'}")
    return context["exit_code"] if report["total"]["executable_lines"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
