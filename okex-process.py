#!./env/bin/python3

import socket
import zlib
import json
from datetime import datetime
import pytz


def process_message(message):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    dec_messge = decompress.decompress(message)
    data_dct = json.loads(dec_messge.decode())
    if 'data' in data_dct:
        data = data_dct['data'][0]
        data['stream'] = data_dct['table'] + ':' + data.pop('instrument_id')
        data['id'] = int(data.pop('trade_id'))
        data['amount'] = float(data.pop('size'))
        data['price'] = float(data['price'])
        data['exchange'] = 'OKEX'
        data['exchange_time'] = datetime.fromisoformat(data.pop('timestamp')[:-1]+'+00:00')
        data['local_time'] = datetime.now(tz=pytz.timezone('Europe/Moscow'))
        message_out(data)
        return


def message_out(message):
    print(message)


def listen_udsocket(server_address):
    
    while True:
        # Wait for a connection
        # print('waiting for a connection')
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(server_address)
                data = s.recv(1024)
                process_message(data)
        except Exception as e:
            print(f'UDSocket error {e}')
            raise SystemExit
            
if __name__ == "__main__":
    # Create a UDS socket
    server_address = './uds_socket'
    listen_udsocket(server_address)