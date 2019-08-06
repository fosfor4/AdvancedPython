import zlib
import json
import socket
from argparse import ArgumentParser
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler('client.log'),
        logging.StreamHandler()
    ]
)

WRITE_MODE = 'write'
READ_MODE = 'read'

def make_request (action, data):
    return {
        'user': name,
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }

parser = ArgumentParser()

parser.add_argument('-a', '--addr', type=str, required=False, help='Server ip-address, if none Localhost used')
parser.add_argument('-p', '--port', type=int, required=False, help='Server ip-address, if none port 7777 used')
parser.add_argument('-m', '--mode', type=str, default=WRITE_MODE, help='Sets client mode, default mode WRITE')

args = parser.parse_args()

socket_config = {
    'host': 'Localhost',
    'port': 7777,
    'buffersize': 1024
}

if args.addr:
    socket_config['host'] = args.addr

if args.port:
    socket_config['port'] = args.port

host, port = socket_config.get('host'), socket_config.get('port')

try:
    sock = socket.socket()
    sock.connect((host, port))
    logging.info('Client was started')
    if args.mode == WRITE_MODE:
        name = input('Enter your name: ')
        print()
        print(f'Hello { name }!')
        print('-' * 27)
        print('Choose your action: ')
        print('echo - server echo response')
        print('send - send message')
        print('clock - server time')
        print('-' * 27)

    while True:
        if args.mode == WRITE_MODE:
            action = input('Enter action: ')
            data = input('Enter data: ')
            request = make_request(action, data)
            str_request = json.dumps(request)
            bytes_request = zlib.compress(str_request.encode())

            sock.send(bytes_request)    
            logging.info(f'User { name } send action: {action}, with data: { data }')
            print('-' * 27)
        elif args.mode == READ_MODE:
            response = sock.recv(socket_config.get('buffersize'))
            bytes_response = zlib.decompress(response)
            logging.info(f'Server send data { bytes_response.decode() }')

except KeyboardInterrupt:
    logging.info('Client shutdown.')