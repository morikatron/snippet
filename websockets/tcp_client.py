import socket
import json

host = "localhost"
port = 8001
receive_buffer_size = 4096

# 接続
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
print("Connect Success.")

# 送信
dictionary = {'message': 'Message from Client', 'number': 256, 'bool': True}
packet = json.dumps(dictionary).encode()
client.send(packet)

# 受信
received_packet = client.recv(receive_buffer_size)
dictionary = json.loads(received_packet.decode())
print(dictionary)

# 終了
client.close()
print("Finish.")
