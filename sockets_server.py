import json
import os
import socket
import logging
from pathlib import Path

UDP_IP = '0.0.0.0'
UDP_PORT = 5000

logging.basicConfig(level='DEBUG')


def run_socket_server():
    print('run socket server')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = UDP_IP, UDP_PORT
    sock.bind(server)
    try:
        while True:
            b_key, address = sock.recvfrom(1024)
            b_value, address = sock.recvfrom(1024)
            key = b_key.decode()
            value = json.loads(b_value.decode())

            logging.debug(f'Received data: {key}  and {value} from: {address}')

            if not os.path.exists('storage/data.json'):
                with open('storage/data.json', 'w') as file:
                    file.write('{}')

            with open('storage/data.json', 'r') as file:
                existing_json_file = json.load(file)

            existing_json_file[key] = value

            with open('storage/data.json', 'w') as file:
                json.dump(existing_json_file, file, indent=4, ensure_ascii=False)

            logging.debug(f'{key}: {value} were added to file')
            sock.sendto(f'{key}: {value} were added to json file'.encode(), address)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


if __name__ == '__main__':
    run_socket_server()
