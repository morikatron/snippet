import asyncio
import websockets
import json

loop = asyncio.get_event_loop()

# 接続
uri = "ws://localhost:8001"
websocket = loop.run_until_complete(websockets.connect(uri))

# 送信
dictionary = {'message': 'Message from Client', 'number': 256, 'bool': True}
packet = json.dumps(dictionary).encode()
loop.run_until_complete(websocket.send(packet))

# 受信
received_packet = loop.run_until_complete(websocket.recv())
dictionary = json.loads(received_packet.decode())
print(dictionary)

# 終了
loop.run_until_complete(websocket.close())
loop.close()
print("Finish")
