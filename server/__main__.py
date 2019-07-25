import json
import socket
from argparse import ArgumentParser
import time

from actions import resolve
from protocol import validate_request, make_response


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
        print(f'Server started with <{ host }>:{ port }')
    else:
        print(f'Server started with <All_interfaces>:{ port }')

    while True:
        client, address = sock.accept()
        print(f'Client was detected { address[0] }:{ address[1] }')

        timestr = time.ctime(time.time())

        b_request = client.recv(socket_config.get('buffersize'))
        request = json.loads(b_request.decode())
        
        if validate_request(request):
            action_name = request.get('action')
            controller = resolve(action_name)
            if controller:
                try:
                    print(f'Client send valid request {request}')
                    response = controller(request)
                except Exception as err:
                    print(f'Internal server error: {err}')
                    response = make_response(request, 500, data='Internal server error')
            else:
                print(f'Controller with action name {action_name} does not exists')
                response = make_response(request, 404, 'Action not found')
        
        else:
            print(f'Client send invalid request {request}')
            response = make_responce(request, 404, 'Wrong request')

        str_response = json.dumps(response)            
        client.send(str_response.encode())
        #client.close()
        
except KeyboardInterrupt:
    print('Server shutdown.')