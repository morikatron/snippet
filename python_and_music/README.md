Morikatron Engineer Blog の記事 「[Pythonと音楽と...（１）音を出す](https://tech.morikatron.ai/entry/2020/07/28/100000)」シリーズで使うサンプルコードです。  
詳しくはブログ記事を参照ください。

# ファイルリスト
* [sample1_play_file.py](sample1_play_file.py)
  * ドの音程で1秒の長さのwavファイルを保存し、再生するサンプルコード
* [sample2_play_buf.py](sample2_play_buf.py)
  * numpyでメモリ上に作ったサイン波を、PyAudioのstreamで順次再生するサンプルコード
* [sample3_play_all.py](sample3_play_all.py)
  * numpyでメモリ上に一気に作ったサイン波のデータ（トラック）を、PyAudioのstreamで一気に再生するサンプルコード。（連載第二回で解説予定）
* [sample4_play_all_tracks.py](sample4_play_all_tracks.py)
  * numpyでメモリ上に作った３つのトラックを合成して再生するサンプルコード。（連載第二回で解説予定）



