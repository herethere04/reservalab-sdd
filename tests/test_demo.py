"""CT-17: o roteiro executável atravessa o servidor HTTP real."""

from pathlib import Path
import subprocess
import sys
import unittest


class DemoProcessTests(unittest.TestCase):
    def test_real_demo_completes_all_expected_http_steps(self):
        root = Path(__file__).resolve().parents[1]
        process = subprocess.run([sys.executable, str(root / "scripts" / "demo.py")],
                                 cwd=root, text=True, capture_output=True, timeout=20)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertIn("DEMONSTRAÇÃO APROVADA", process.stdout)
        for status in ["HTTP 201", "HTTP 409", "HTTP 400", "HTTP 200"]:
            self.assertIn(status, process.stdout)
