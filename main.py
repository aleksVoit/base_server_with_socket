from datetime import datetime
import json
import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import logging
import socket
from threading import Thread
from sockets_server import run_socket_server

logging.basicConfig(level='DEBUG')

UDP_IP = '0.0.0.0'
UDP_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/contact':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        # read the number of binary elements which found in 'Content-Length' header
        data_parse = urllib.parse.unquote_plus(data.decode())
        # parse data from data after binary data decode
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        # pack data to dictionary
        key_to_send = str(datetime.now())
        data_to_send = {'username': data_dict['username'], 'message': data_dict['message']}
        json_data = json.dumps(data_to_send)  # pack dict to json

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = (UDP_IP, UDP_PORT)
        sock.sendto(key_to_send.encode(), server)
        logging.debug(f'{key_to_send} was sent to {server}')
        sock.sendto(json_data.encode(), server)
        logging.debug(f'{data_to_send} was sent to {server}')

        response, address = sock.recvfrom(1024)
        logging.debug(f'{datetime.now()} - Response from {server}: {response.decode()}')

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('0.0.0.0', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def main():
    server_thread = Thread(target=run)
    server_thread.start()
    socket_thread = Thread(target=run_socket_server)
    socket_thread.start()


if __name__ == '__main__':
    main()
