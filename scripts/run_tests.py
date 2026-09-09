"""Executa unittest e preserva evidências reais, sem dependências externas."""

import argparse
import contextlib
import hashlib
import io
import json
import platform
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class Tee(io.TextIOBase):
    def __init__(self, *streams):
        self.streams = streams

    def write(self, text):
        for stream in self.streams:
            stream.write(text)
            stream.flush()
        return len(text)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def git_metadata():
    def git(*args):
        try:
            process = subprocess.run(["git", "-C", str(ROOT), *args],
                                     capture_output=True, text=True, check=False, timeout=10)
            return process.stdout.strip() if process.returncode == 0 else None
        except (OSError, subprocess.TimeoutExpired):
            return None
    top_level = git("rev-parse", "--show-toplevel")
    if top_level is None or Path(top_level).resolve() != ROOT:
        return {"head": None, "working_tree_dirty": None,
                "repository_at_project_root": False}
    head = git("rev-parse", "HEAD")
    status = git("status", "--porcelain", "--untracked-files=normal")
    return {"head": head, "working_tree_dirty": bool(status) if status is not None else None,
            "repository_at_project_root": True}


def source_snapshot():
    """Identifica o conteúdo efetivamente testado, mesmo antes de um commit."""
    candidates = []
    for directory in ["reservalab", "tests", "scripts", ".github/workflows"]:
        folder = ROOT / directory
        if folder.is_dir():
            candidates.extend(path for path in folder.rglob("*")
                              if path.is_file() and path.suffix in {".py", ".ps1", ".sh", ".yml", ".yaml"})
    for name in ["Dockerfile", "compose.yaml", "compose.yml", "docker-compose.yml", "pyproject.toml"]:
        path = ROOT / name
        if path.is_file():
            candidates.append(path)
    files = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
             for path in sorted(candidates, key=lambda item: item.relative_to(ROOT).as_posix())}
    manifest = "".join(f"{path}\0{digest}\n" for path, digest in files.items()).encode("utf-8")
    return {"algorithm": "sha256", "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
            "file_count": len(files), "files": files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "evidence" / "latest",
                        help="Diretório de tests.log e summary.json")
    args = parser.parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    metadata = git_metadata()
    snapshot = source_snapshot()
    started = time.perf_counter()
    with (output_dir / "tests.log").open("w", encoding="utf-8", newline="\n") as log:
        tee = Tee(sys.stdout, log)
        with contextlib.redirect_stdout(tee), contextlib.redirect_stderr(tee):
            print("ReservaLab | execução real do harness unittest")
            print(f"UTC: {timestamp}")
            print(f"Python: {platform.python_version()} ({platform.python_implementation()})")
            print(f"Platform: {platform.platform()}")
            print(f"Git HEAD: {metadata['head'] or 'indisponível'}")
            print(f"Working tree dirty: {metadata['working_tree_dirty']}")
            print(f"Source manifest SHA-256: {snapshot['manifest_sha256']}")
            print()
            suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))
            result = unittest.TextTestRunner(stream=tee, verbosity=2).run(suite)
            success = result.wasSuccessful() and result.testsRun > 0
            summary = {
                "timestamp_utc": timestamp,
                "python": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "platform": platform.platform(),
                "git": metadata,
                "source_snapshot": snapshot,
                "elapsed_seconds": round(time.perf_counter() - started, 3),
                "tests_run": result.testsRun,
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(result.skipped),
                "expected_failures": len(result.expectedFailures),
                "unexpected_successes": len(result.unexpectedSuccesses),
                "success": success,
            }
            if result.testsRun == 0:
                print("ERRO: nenhum teste foi descoberto; execução considerada reprovada.")
            print("\nResumo verificável:")
            print(json.dumps(summary, indent=2, ensure_ascii=False))
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                                           encoding="utf-8")
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
