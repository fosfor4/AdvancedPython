import json
import socket
from argparse import ArgumentParser
import time

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

    msg = {
        "action": "presence",
        "time": time.ctime(time.time()),
        "type": "status",
        "user": {
            "account_name": "fosfor",
            "status": "fosfor на связи"
        }
    }

    bad_msg = {
        "action": "presence_error",
        "time": time.ctime(time.time()),
        "type": "status",
        "user": {
            "account_name": "fosfor",
            "status": "fosfor на связи"
        }   
    }
    
    json_msg = json.dumps(msg, ensure_ascii = False)
 
    json_bad_msg = json.dumps(bad_msg, ensure_ascii = False)
    
    msg_type = input('Send correct message?')
    
    if msg_type == 'yes' or msg_type == 'y':
        sock.send(json_msg.encode())
        print('Presence message sent')
    else:
        sock.send(json_bad_msg.encode())
        print('Wrong message sent')    
    
    b_response = sock.recv(socket_config.get('buffersize'))
    
    json_msg = json.loads(b_response.decode())
    msg_time = json_msg['time']
    msg_response = json_msg['response']

    if msg_response == 200:
        print(f'Registration completed at { msg_time }')
        print(f'Server message: { msg_response }')
    else:
        print('Error, not registered')
        print(f'Server message: { msg_response }')

except KeyboardInterrupt:
    print('Client shutdown.')