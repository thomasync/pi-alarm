from http.server import HTTPServer
from pialarm.http import Handler
from pialarm.store import alarm


def main():
    global alarm
    with HTTPServer(("0.0.0.0", 2666), Handler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
