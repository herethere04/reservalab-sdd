"""CT-15: verifica o processo real do harness em projetos temporários."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class HarnessProcessTests(unittest.TestCase):
    def run_fixture(self, test_body=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "tests").mkdir()
            (root / "tests" / "__init__.py").touch()
            shutil.copyfile(Path(__file__).resolve().parents[1] / "scripts" / "run_tests.py",
                            root / "scripts" / "run_tests.py")
            if test_body is not None:
                (root / "tests" / "test_fixture.py").write_text(
                    "import unittest\n\nclass Fixture(unittest.TestCase):\n"
                    "    def test_observable_result(self):\n        " + test_body + "\n",
                    encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(root / "scripts" / "run_tests.py"),
                 "--output-dir", str(root / "evidence")],
                cwd=root, capture_output=True, text=True, timeout=20)
            summary = json.loads((root / "evidence" / "summary.json").read_text(encoding="utf-8"))
            log = (root / "evidence" / "tests.log").read_text(encoding="utf-8")
            self.assertIsNone(summary["git"]["head"])
            self.assertFalse(summary["git"]["repository_at_project_root"])
            self.assertEqual(len(summary["source_snapshot"]["manifest_sha256"]), 64)
            return result, summary, log

    def test_success_writes_evidence_and_exits_zero(self):
        result, summary, log = self.run_fixture("self.assertEqual(2 + 2, 4)")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(summary["success"])
        self.assertEqual((summary["tests_run"], summary["failures"], summary["errors"]), (1, 0, 0))
        self.assertIn("OK", log)

    def test_assertion_failure_writes_evidence_and_exits_one(self):
        result, summary, log = self.run_fixture("self.fail('falha fictícia controlada')")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(summary["success"])
        self.assertEqual((summary["tests_run"], summary["failures"], summary["errors"]), (1, 1, 0))
        self.assertIn("falha fictícia controlada", log)

    def test_unexpected_error_writes_evidence_and_exits_one(self):
        result, summary, log = self.run_fixture("raise RuntimeError('erro fictício controlado')")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(summary["success"])
        self.assertEqual((summary["tests_run"], summary["failures"], summary["errors"]), (1, 0, 1))
        self.assertIn("erro fictício controlado", log)

    def test_empty_suite_is_rejected_even_without_failures(self):
        result, summary, log = self.run_fixture()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(summary["success"])
        self.assertEqual((summary["tests_run"], summary["failures"], summary["errors"]), (0, 0, 0))
        self.assertIn("nenhum teste foi descoberto", log)
