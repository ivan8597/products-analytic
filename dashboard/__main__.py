import argparse

from dashboard.app import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Products Analytics Dashboard")
    parser.add_argument("--host", default="127.0.0.1", help="Адрес сервера (0.0.0.0 — доступ из локальной сети)")
    parser.add_argument("--port", type=int, default=8050, help="Порт")
    parser.add_argument("--no-debug", action="store_true", help="Отключить режим отладки")
    args = parser.parse_args()

    run(host=args.host, port=args.port, debug=not args.no_debug)
