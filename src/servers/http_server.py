import json
import logging
import os
import socket
import urllib.parse
from http.server import BaseHTTPRequestHandler
from os.path import join

from env.environment import SOCKET_HOST, SOCKET_PORT

log = logging.getLogger()


class HttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_file('index.html', 'text/html')
        elif pr_url.path == '/message':
            self.send_file('message.html', 'text/html')
        elif pr_url.path == '/logo.png':
            self.send_file('logo.png', 'image/png')
        elif pr_url.path == '/style.css':
            self.send_file('style.css', 'text/css')
        else:
            self.send_file('error.html', 'text/html', 404)

    def do_POST(self):
        pr_url = urllib.parse.urlparse(self.path)

        if pr_url.path == '/message':
            data = self.rfile.read(int(self.headers['Content-Length']))

            log.info(f'HTTP Server received message: {data}')

            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

            self.send_to_socket(data_dict)

            self.send_file('message-sent.html', 'text/html')

    def send_file(self, filename, content_type, status=200):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()

        file_path = join(os.getcwd(), 'front-init', filename)

        with open(file_path, 'rb') as fd:
            self.wfile.write(fd.read())

    @staticmethod
    def send_to_socket(data):
        log.info(f'HTTP Server sending data to Socket Server: {data}')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            while True:
                try:
                    s.connect((SOCKET_HOST, SOCKET_PORT))
                    encoded_data = json.dumps(data).encode("utf-8")
                    s.sendall(encoded_data)
                    break
                except ConnectionRefusedError as e:
                    log.error(f'HTTP Server failed to connect to Socket Server: {e}')
                except:
                    log.error(f'Error occurred when sending data to Socket Server: {e}')
