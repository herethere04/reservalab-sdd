"""CT-16: evidência e código de saída do comando real de cobertura."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class CoverageProcessTests(unittest.TestCase):
    def fixture(self, test_body):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ["scripts", "tests", "reservalab"]:
                (root / folder).mkdir()
            for name in ["run_tests.py", "run_coverage.py"]:
                shutil.copyfile(Path(__file__).resolve().parents[1] / "scripts" / name, root / "scripts" / name)
            for package in ["tests", "reservalab"]:
                (root / package / "__init__.py").touch()
            (root / "reservalab" / "__init__.py").write_text('version = "fixture"\n', encoding="utf-8")
            (root / "reservalab" / "domain.py").write_text(
                '"""Docstring não deve inflar o denominador."""\n'
                'def used():\n    return 7\n\ndef not_used():\n    return 11\n', encoding="utf-8")
            (root / "reservalab" / "unimported.py").write_text(
                'value = 42\nclass Unimported:\n    def noop(self):\n        return 1\n', encoding="utf-8")
            (root / "tests" / "test_fixture.py").write_text(
                'import unittest\nfrom reservalab.domain import used\n'
                'class Fixture(unittest.TestCase):\n    def test_result(self):\n        ' + test_body + '\n', encoding="utf-8")
            process = subprocess.run([sys.executable, str(root / "scripts" / "run_coverage.py"),
                                      "--output-dir", str(root / "evidence")], cwd=root,
                                     text=True, capture_output=True, timeout=30)
            report = json.loads((root / "evidence" / "coverage.json").read_text(encoding="utf-8"))
            self.assertTrue((root / "evidence" / "index.html").is_file())
            self.assertTrue((root / "evidence" / "tests" / "tests.log").is_file())
            return process, report

    def test_missing_and_unimported_code_are_reported(self):
        process, report = self.fixture('self.assertEqual(used(), 7)')
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        modules = {row["path"]: row for row in report["modules"]}
        self.assertIn(6, modules["reservalab/domain.py"]["missing_lines"])
        self.assertNotIn(1, modules["reservalab/domain.py"]["missing_lines"])
        self.assertEqual(modules["reservalab/unimported.py"]["percent"], 0)
        self.assertEqual(modules["reservalab/__init__.py"]["percent"], 100)
        self.assertEqual(report["tests"]["tests_run"], 1)
        self.assertTrue(report["tests"]["success"])

    def test_failed_suite_keeps_failure_exit_and_coverage_evidence(self):
        process, report = self.fixture("self.fail('falha fictícia')")
        self.assertEqual(process.returncode, 1, process.stdout + process.stderr)
        self.assertEqual(report["tests"]["failures"], 1)
        self.assertFalse(report["tests"]["success"])
