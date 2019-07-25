import json
import socket
from argparse import ArgumentParser
from datetime import datetime

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

    print('Client was started')
    
    action = input('Enter action: ')
    data = input('Enter data: ')

    request = {
        'action': action,
        'time': datetime.now().timestamp(),
        'data': data
    }   
        
    str_request = json.dumps(request)
    sock.send(str_request.encode())
    print(f'Client send data: {data}')    
    
    b_response = sock.recv(socket_config.get('buffersize'))
    print(f'Server send data: {b_response.decode()}')
 
except KeyboardInterrupt:
    print('Client shutdown.')