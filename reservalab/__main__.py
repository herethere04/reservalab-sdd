"""Ponto de entrada: python -m reservalab."""

import argparse

from .server import create_server


def main():
    parser = argparse.ArgumentParser(description="API local de reservas de salas de estudo")
    parser.add_argument("--host", default="127.0.0.1", help="Interface de rede (padrão: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Porta HTTP (padrão: 8000)")
    parser.add_argument("--db", default="data/reservalab.db", help="Arquivo SQLite (padrão: data/reservalab.db)")
    args = parser.parse_args()
    server = create_server(args.db, host=args.host, port=args.port)
    print(f"ReservaLab em http://{args.host}:{server.server_port} | banco: {args.db}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando ReservaLab.", flush=True)
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
