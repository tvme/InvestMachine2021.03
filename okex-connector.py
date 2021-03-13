#!/home/user/InvestMachine2021.03/env/bin/python3

import socket
import os
import websocket
import json
import zlib

def start_uds_server(server_address):
    # Make sure the socket does not already exist
    try:
        os.unlink(server_address)
    except OSError:
        if os.path.exists(server_address):
            raise

    # Create a UDS socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Bind the socket to the address
    print(f'starting up on {server_address}')
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    return sock



def send_to_udsocket(sock, message):
    conn, addr = sock.accept()
    # Send data
    with conn:
        # print('Connected by', addr)
        conn.sendall(message)


def on_open(ws):
    print('Set run.flag')
    open('./run.flag', 'a').close()
    print(f"opened {ws.url}")
    channel_data =  {
                    "op": "subscribe", 
                    "args": ["spot/trade:ETH-USDT"]
                    }

    ws.send(json.dumps(channel_data))


def on_message(ws, message):
    if os.path.isfile('./run.flag'):
        decompress = zlib.decompressobj(-zlib.MAX_WBITS)
        dec_messge = decompress.decompress(message)
        if dec_messge:  # sending not empty message
            send_to_udsocket(sock, dec_messge)
    else:
        ws.close()
        raise SystemExit


def on_close(ws):
    channel_data = {
                    "op": "unsubscribe", 
                    "args": ["spot/trade:ETH-USDT"]
                   }
    ws.send(json.dumps(channel_data))
    print("closed connection")



if __name__ == "__main__":
    # # Create a UDS socket
    server_address='./uds_socket'
    sock = start_uds_server(server_address)

    ws_url = "wss://real.okex.com:8443/ws/v3"
    ws = websocket.WebSocketApp(ws_url, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever()

