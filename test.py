# import asyncio
import websocket
import json
import zlib
import datetime
import pytz

def on_open(ws):
    print("opened")
    channel_data =  {
                    "op": "subscribe", 
                    "args": ["spot/trade:ETH-USDT"]
                    }

    ws.send(json.dumps(channel_data))


def on_message(ws, message):
    decompress = zlib.decompressobj(-zlib.MAX_WBITS)
    print(decompress.decompress(message))
    print(f"received a message in current time {datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))}")

def on_close(ws):
    channel_data = {
                    "op": "unsubscribe", 
                    "args": ["spot/trade:ETH-USDT"]
                   }
    ws.send(json.dumps(channel_data))
    print("closed connection")

url = "wss://real.okex.com:8443/ws/v3"

ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()