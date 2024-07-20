import logging
import socket
from concurrent import futures as cf

from env.environment import SOCKET_HOST, SOCKET_PORT
from src.db.messages_db import MessagesDb

log = logging.getLogger()


class SocketServer:

    def __init__(self):
        self.db = MessagesDb()

    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SOCKET_HOST, SOCKET_PORT))
        server_socket.listen(10)

        with cf.ThreadPoolExecutor(10) as client_pool:
            try:
                while True:
                    new_sock, address = server_socket.accept()
                    client_pool.submit(self.handle, new_sock)
            except KeyboardInterrupt:
                log.info('Destroying Socket Server.')
            finally:
                server_socket.close()

    def handle(self, sock: socket.socket):
        while True:
            received = sock.recv(1024)
            if not received:
                break
            data = received.decode()
            log.info(f'Socket Server received data: {data}')
            self.db.insert_message(data)

        sock.close()
        log.info('Socket Server closed connection.')
