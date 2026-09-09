"""Adaptador HTTP JSON para uso local e demonstração acadêmica."""

from collections.abc import Callable
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlsplit

from .domain import DomainError
from .service import BookingService


MAX_BODY_BYTES = 16 * 1024


def create_server(
    db_path: str | Path,
    host: str = "127.0.0.1",
    port: int = 8000,
    now: Callable[[], datetime] | None = None,
) -> ThreadingHTTPServer:
    """Cria o servidor sem bloquear; chame serve_forever para executá-lo."""
    service = BookingService(db_path, now=now)

    class Handler(BaseHTTPRequestHandler):
        server_version = "ReservaLab/0.1"

        def _send_json(self, status: int, payload: dict, allow: str | None = None):
            body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            if allow is not None:
                self.send_header("Allow", allow)
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _read_json(self):
            content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if content_type != "application/json":
                raise DomainError("unsupported_media_type", "Envie Content-Type: application/json.", 415)
            if self.headers.get("Transfer-Encoding"):
                raise DomainError("invalid_json", "Envie o tamanho do corpo em Content-Length.")
            try:
                length = int(self.headers.get("Content-Length", ""))
                if length < 0:
                    raise ValueError
            except ValueError as exc:
                raise DomainError("invalid_json", "Content-Length ausente ou inválido.") from exc
            if length > MAX_BODY_BYTES:
                raise DomainError("body_too_large", "O corpo da requisição excede 16 KiB.", 413)
            try:
                payload = self.rfile.read(length)
                if len(payload) != length:
                    raise ValueError("Corpo incompleto")
                return json.loads(payload.decode("utf-8"), parse_constant=self._reject_constant)
            except (UnicodeDecodeError, ValueError, RecursionError) as exc:
                raise DomainError("invalid_json", "O corpo deve conter JSON válido em UTF-8.") from exc

        @staticmethod
        def _reject_constant(value):
            raise ValueError(f"Constante JSON inválida: {value}")

        def _dispatch(self):
            path = urlsplit(self.path).path
            is_booking = path.startswith("/bookings/") and len(path.split("/")) == 3 and bool(path.split("/")[-1])
            routes = {"/health": "GET", "/rooms": "GET", "/bookings": "GET, POST"}
            allowed = "DELETE" if is_booking else routes.get(path)
            try:
                if allowed is None:
                    raise DomainError("not_found", "Rota não encontrada.", 404)
                if self.command not in allowed.split(", "):
                    self._send_json(405, {"error": {"code": "method_not_allowed", "message": "Método não permitido nessa rota."}}, allow=allowed)
                    return
                if path == "/health":
                    self._send_json(200, {"status": "ok"})
                elif path == "/rooms":
                    self._send_json(200, {"rooms": service.list_rooms()})
                elif path == "/bookings" and self.command == "GET":
                    self._send_json(200, {"bookings": service.list_bookings()})
                elif path == "/bookings":
                    self._send_json(201, service.create_booking(self._read_json()))
                else:
                    self._send_json(200, service.cancel_booking(path.rsplit("/", 1)[1]))
            except DomainError as exc:
                self._send_json(exc.status, {"error": {"code": exc.code, "message": exc.message}})

        do_GET = _dispatch
        do_POST = _dispatch
        do_DELETE = _dispatch
        do_PUT = _dispatch
        do_PATCH = _dispatch
        do_HEAD = _dispatch
        do_OPTIONS = _dispatch
        do_TRACE = _dispatch

    server = ThreadingHTTPServer((host, port), Handler)
    server.daemon_threads = True
    return server
