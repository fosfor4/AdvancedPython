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
    
    action = input('Enter action: ')
    data = input('Enter data: ')

    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }   
        
    str_request = json.dumps(request)
    sock.send(str_request.encode())
    logging.info(f'Client send data: {data}')    
    
    b_response = sock.recv(socket_config.get('buffersize'))
    logging.info(f'Server send data: {b_response.decode()}')
    logging.info('Client shutdown.')
 
except KeyboardInterrupt:
    logging.info('Client shutdown.')