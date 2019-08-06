import json
import socket
from argparse import ArgumentParser
import logging
import select

from actions import resolve
from protocol import validate_request, make_response
from handlers import handle_default_request

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)


parser = ArgumentParser()

parser.add_argument('-a', '--addr', type=str, required=False, help='Server ip-address, if none <All_interfaces> used')
parser.add_argument('-p', '--port', type=int, required=False, help='Server ip-address, if none port 7777 used')

args = parser.parse_args()

socket_config = {
    'host': '',
    'port': 7777,
    'buffersize': 1024
}

if args.addr:
    socket_config['host'] = args.addr

if args.port:
    socket_config['port'] = args.port

host, port = socket_config.get('host'), socket_config.get('port')

requests = []
connections = []

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.setblocking(False)
    sock.settimeout(0)
    sock.listen(5)

    if args.addr:
        logging.info(f'Server started with <{ host }>:{ port }')
    else:
        logging.info(f'Server started with <All_interfaces>:{ port }')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Client was detected { address[0] }:{ address[1] }')
            connections.append(client)
        except:
            pass
        
        rlist, wlist, xlist = select.select(
            connections, connections, connections, 0
        )

        for read_client in rlist:
            bytes_request = read_client.recv(socket_config.get('buffersize'))
            requests.append(bytes_request)

        if requests:
            bytes_request = requests.pop()
            bytes_response = handle_default_request(bytes_request)
            for write_client in wlist:
                write_client.send(bytes_response)
       
except KeyboardInterrupt:
    logging.info('Server shutdown.')