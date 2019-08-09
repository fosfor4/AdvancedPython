import zlib
import json
import socket
from argparse import ArgumentParser
from datetime import datetime
import logging
import threading
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler('client.log'),
        logging.StreamHandler()
    ]
)

server_response = ''

def read(sock, buffersize):
    while True:
        response = sock.recv(buffersize)
        bytes_response = zlib.decompress(response)
        logging.info(f'Server send data: { bytes_response.decode() }')
        print('-' * 27)
         
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
    name = input('Enter your name: ')
    print()
    print(f'Hello { name }!')
    print('-' * 27)
    print('Choose your action: ')
    print('echo - server echo response')
    print('send - send message')
    print('clock - server time')
    print('-' * 27)

    read_thread = threading.Thread(
        target=read, args=(sock, socket_config.get('buffersize'))
    )
    read_thread.start()
    
    while True:
        time.sleep(0.5)
        action = input('Enter action: ')
        data = input('Enter data: ')
        print('-' * 27)
        
        request = make_request(action, data)
        str_request = json.dumps(request)
        bytes_request = zlib.compress(str_request.encode())

        sock.send(bytes_request)    
        logging.info(f'User { name } send action: {action}, with data: { data }')
        print('-' * 27)
            
except KeyboardInterrupt:
    logging.info('Client shutdown.')