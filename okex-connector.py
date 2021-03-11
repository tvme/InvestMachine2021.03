#!/home/user/InvestMachine2021.03/env/bin/python3

import socket
import sys
import websocket
import json
import zlib


def connect_socket(sock, server_address):
    # Connect the socket to the port where the server is listening
    
    print('connecting to {}'.format(server_address))
    try:
        sock.connect(server_address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)


def send_to_socket(sock, message):
    try:

        # Send data
        print('sending {!r}'.format(message))
        sock.sendall(message)

    finally:
        print('closing Unix Domain socket')
        sock.close()
        print('closing Web socket')
        # ws.close()


def on_open(ws):
    print("opened")
    channel_data =  {
                    "op": "subscribe", 
                    "args": ["spot/trade:ETH-USDT"]
                    }

    ws.send(json.dumps(channel_data))


def on_message(ws, message):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    send_to_socket(sock, decompress.decompress(message))

def on_close(ws):
    channel_data = {
                    "op": "unsubscribe", 
                    "args": ["spot/trade:ETH-USDT"]
                   }
    ws.send(json.dumps(channel_data))
    print("closed connection")



if __name__ == "__main__":
    # Create a UDS socket
    server_address='./uds_socket'
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connect_socket(sock, server_address)

    ws_url = "wss://real.okex.com:8443/ws/v3"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()

