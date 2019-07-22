import json
import socket
from argparse import ArgumentParser
import time


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
        request_action = request['action']

        if request_action == 'presence':
            msg = {
                "response": 200,
                "time": timestr,
            }
            json_msg = json.dumps(msg)

            #msg = 'Привет, ' + request['user']['account_name']
            client.send(json_msg.encode())
            client.close()
        else:
            msg = {
                "response": 400,
                "time": timestr,
            }
            json_msg = json.dumps(msg)

            client.send(json_msg.encode())
            client.close()
except KeyboardInterrupt:
    print('Server shutdown.')