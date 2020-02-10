Morikatron Engineer Blog の記事 「[Python のプログラムを並列処理で高速化する](公開されたURLを貼り付ける)」のサンプルコードです。  
詳しくはブログ記事を参照ください。

# ファイルリスト
* [sample1.py](sample1.py)
  * シングルスレッド、マルチスレッド、マルチプロセスで同じ処理をさせた時の速度比較用サンプルプログラム
* [sample2.py](sample2.py)
  * sample1.py を少し変更して、計算の途中で処理待ち (time.sleep) を挿入させたもの
* [sample3.py](sample3.py)
  * スレッド生成、プロセス生成のオーバーヘッドを確認用サンプルプログラム