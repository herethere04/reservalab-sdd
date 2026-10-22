"""Demonstração HTTP real com dados fictícios e banco temporário descartável."""

import argparse
from datetime import datetime, timedelta, timezone
import http.client
import json
from pathlib import Path
import sys
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reservalab import __version__
from reservalab.server import create_server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pause", type=float, default=0, help="Pausa entre etapas, em segundos (0 a 30)")
    args = parser.parse_args()
    if not 0 <= args.pause <= 30:
        parser.error("--pause deve estar entre 0 e 30")
    with tempfile.TemporaryDirectory(prefix="reservalab-demo-") as directory:
        server = create_server(Path(directory) / "demo.db", port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print(f"ReservaLab {__version__} | demonstração HTTP real | dados fictícios", flush=True)
        print(f"UTC: {datetime.now(timezone.utc).isoformat()} | porta local: {server.server_port}", flush=True)
        print("Banco temporário novo; nenhum dado de uso normal é alterado.\n", flush=True)

        def request(title, method, path, expected, payload=None):
            print(f"=== {title} ===\n{method} {path}", flush=True)
            body = json.dumps(payload).encode() if payload is not None else None
            connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
            try:
                connection.request(method, path, body=body,
                                   headers={"Content-Type": "application/json"} if body is not None else {})
                response = connection.getresponse()
                value = json.loads(response.read())
                print(f"HTTP {response.status}\n{json.dumps(value, ensure_ascii=False, indent=2)}\n", flush=True)
                if response.status != expected:
                    raise RuntimeError(f"Esperado {expected}, observado {response.status}")
                if args.pause:
                    time.sleep(args.pause)
                return value
            finally:
                connection.close()

        try:
            request("1. Saúde da aplicação", "GET", "/health", 200)
            request("2. Salas e capacidades", "GET", "/rooms", 200)
            start = (datetime.now(timezone.utc) + timedelta(days=1)).replace(second=0, microsecond=0)
            payload = {"room_id": 1, "student_name": "Grupo Demonstração", "participants": 3,
                       "starts_at": start.isoformat(), "ends_at": (start + timedelta(hours=1)).isoformat()}
            booking = request("3. Reserva válida", "POST", "/bookings", 201, payload)
            request("4. Conflito impedido", "POST", "/bookings", 409, payload)
            request("5. Cancelamento libera horário", "DELETE", f"/bookings/{booking['id']}", 200)
            request("6. Mesmo horário disponível novamente", "POST", "/bookings", 201, payload)
            request("7. Capacidade da sala respeitada", "POST", "/bookings", 400, {**payload, "participants": 5})
            request("8. Histórico preservado", "GET", "/bookings", 200)
            print("DEMONSTRAÇÃO APROVADA: todas as respostas reais corresponderam ao contrato.", flush=True)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
