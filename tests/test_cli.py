"""CT-17: contrato observável da CLI e encerramento do servidor."""

import contextlib
import io
import runpy
import unittest
from unittest.mock import Mock, patch


class CliTests(unittest.TestCase):
    def execute(self, argv, server):
        output = io.StringIO()
        with patch("sys.argv", ["reservalab", *argv]), patch("reservalab.server.create_server", return_value=server) as create:
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                runpy.run_module("reservalab", run_name="__main__")
        return create, output.getvalue()

    def test_default_arguments_and_keyboard_interrupt_close_server(self):
        server = Mock(server_port=8000)
        server.serve_forever.side_effect = KeyboardInterrupt
        create, output = self.execute([], server)
        create.assert_called_once_with("data/reservalab.db", host="127.0.0.1", port=8000)
        server.server_close.assert_called_once()
        self.assertIn("Encerrando ReservaLab", output)

    def test_custom_arguments_and_unexpected_failure_close_server(self):
        server = Mock(server_port=8123)
        server.serve_forever.side_effect = RuntimeError("falha controlada")
        with self.assertRaisesRegex(RuntimeError, "falha controlada"):
            self.execute(["--host", "127.0.0.1", "--port", "8123", "--db", "temp.db"], server)
        server.server_close.assert_called_once()

    def test_invalid_port_is_rejected_before_starting_server(self):
        server = Mock()
        with self.assertRaises(SystemExit) as caught:
            self.execute(["--port", "abc"], server)
        self.assertEqual(caught.exception.code, 2)
        server.serve_forever.assert_not_called()

    def test_version_is_reported_without_starting_server(self):
        output = io.StringIO()
        with patch("sys.argv", ["reservalab", "--version"]), patch("reservalab.server.create_server") as create:
            with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as caught:
                runpy.run_module("reservalab", run_name="__main__")
        self.assertEqual(caught.exception.code, 0)
        self.assertEqual(output.getvalue().strip(), "ReservaLab 1.0.0")
        create.assert_not_called()
