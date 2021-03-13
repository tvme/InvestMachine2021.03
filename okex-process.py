#!/home/user/InvestMachine2021.03/env/bin/python3

import socket
import sys


def process_message(message):
    message_out(message)


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