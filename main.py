import logging
from concurrent.futures.thread import ThreadPoolExecutor
from http.server import HTTPServer

from env.environment import HTTP_HOST, HTTP_PORT
from src.servers.http_server import HttpServer
from src.servers.socket_server import SocketServer

log = logging.getLogger()


def run_http_server():
    server_address = (HTTP_HOST, HTTP_PORT)
    http = HTTPServer(server_address, HttpServer)
    try:
        log.info('Running HTTP Server')
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server():
    log.info('Running Socket Server')
    SocketServer().serve_forever()


def main():
    with ThreadPoolExecutor(max_workers=2) as pool:
        pool.submit(run_socket_server)
        pool.submit(run_http_server)


if __name__ == '__main__':
    main()
