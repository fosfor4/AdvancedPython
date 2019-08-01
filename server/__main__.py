import json
import socket
from argparse import ArgumentParser
import time
import logging

from actions import resolve
from protocol import validate_request, make_response

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

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(5)

    if args.addr:
        logging.info(f'Server started with <{ host }>:{ port }')
    else:
        logging.info(f'Server started with <All_interfaces>:{ port }')

    while True:
        client, address = sock.accept()
        logging.info(f'Client was detected { address[0] }:{ address[1] }')

        timestr = time.ctime(time.time())

        b_request = client.recv(socket_config.get('buffersize'))
        request = json.loads(b_request.decode())
        
        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    logging.debug(f'Client send valid request {request}')
                    response = controller(request)
                except Exception as err:
                    logging.error(f'Internal server error: {err}')
                    response = make_response(request, 500, data='Internal server error')
            else:
                logging.debug(f'Controller with action name {action_name} does not exists')
                response = make_response(request, 404, 'Action not found')
        
        else:
            logging.debug(f'Client send invalid request {request}')
            response = make_responce(request, 404, 'Wrong request')

        str_response = json.dumps(response)            
        client.send(str_response.encode())
        logging.debug(f'Server response message: {response}')
        #client.close()
        
except KeyboardInterrupt:
    logging.info('Server shutdown.')