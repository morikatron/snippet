import asyncio
import websockets
import json
import threading

def thread_func(num):

    # イベントループを各スレッドごとに用意する必要があります。
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 接続
    uri = "ws://localhost:8001" + "/client{}".format(num)
    websocket = loop.run_until_complete(websockets.connect(uri))
    print("Connect Success.")

    # 受信
    dictionary = {'message': 'Message from Client', 'number': num, 'bool': True}
    packet = json.dumps(dictionary).encode()  # Python の文字列は UTF-8 なので、BYTE 型に変換して送信する
    loop.run_until_complete(websocket.send(packet))

    # 受信
    received_packet = loop.run_until_complete(websocket.recv())
    dictionary = json.loads(received_packet.decode())
    print(dictionary)

    loop.run_until_complete(websocket.close())
    loop.close()
    print("Finish")


# threading で同時に
threads = []
for i in range(10):
    thread = threading.Thread(target=thread_func, args=(i,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

print("Done.")
