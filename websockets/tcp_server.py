import socket
import json

host = "localhost"
port = 8001
receive_buffer_size = 4096
queue_size = 10

# サーバー立ち上げ
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(queue_size)

# クライアント接続待ち
client, address = server.accept()

while True:
    # 受信
    received_packet = client.recv(receive_buffer_size)
    if len(received_packet) == 0:
        #クライアントが切断した場合 recv() は 0Byte のByte列を返す
        print("connection Lost.")
        break
    dictionary = json.loads(received_packet.decode())
    print(dictionary)

    # 送信
    dictionary['message'] = 'Message from Server'
    dictionary['number'] = 128
    dictionary['bool'] = False
    packet = json.dumps(dictionary).encode()
    client.send(packet)

# 終了
client.close()
server.close()
print("Finish.")
