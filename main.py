from http.server import HTTPServer
from alarm.http import Handler
from alarm.store import alarm


def main():
    global alarm
    with HTTPServer(("0.0.0.0", 2666), Handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
