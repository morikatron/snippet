Morikatron Engineer Blog の記事 「[WebSocket を TCP の代わりに使ってみる](https://tech.morikatron.ai/entry/2020/07/20/100000)」のサンプルコードです。  
詳しくはブログ記事を参照ください。

# ファイルリスト
* [tcp_server.py](tcp_server.py)
  * ごく簡単な TCP サーバーのサンプルプログラムです。 同一PC上で動く tcp_client.py と通信します。
* [tcp_client.py](tcp_client.py)
  * ごく簡単な TCP クライアントのサンプルプログラムです。 同一PC上で動く tcp_server.py と通信します。
* [ws_server.py](ws_server.py)
  * websockets モジュールを使った WebSocket サーバーのサンプルプログラムです。 同一PC上で動く ws_client.py および ws_client_multithread と通信します。
* [ws_client.py](ws_client.py)
  * websockets モジュールを使った WebSocket サーバーのサンプルプログラムです。 同一PC上で動く ws_server.py と通信します。
* [ws_client_multithread.py](ws_client_multithread.py)
  * websockets モジュールを使った WebSocket サーバーのサンプルプログラムです。 同一PC上で動く ws_server.py と通信します。
