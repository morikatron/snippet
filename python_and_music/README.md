Morikatron Engineer Blogのサンプルコードです。  
詳しくは以下のブログ記事を参照ください。

## ブログ（解説記事）のリスト
*　[Pythonと音楽と...（１）音を出す](https://tech.morikatron.ai/entry/2020/07/28/100000)  
*　[Pythonと音楽と...（２）トラックとミックス](https://tech.morikatron.ai/entry/2020/08/10/100000)  
*　[Pythonと音楽と...（３）MIDIファイルの再生](https://tech.morikatron.ai/entry/2020/08/17/100000)  
*　[Pythonと音楽と...（４）MDIをtoioで演奏する](https://tech.morikatron.ai/entry/2021/2/1/100000)  

## ファイルリスト
* [sample1_play_file.py](sample1_play_file.py)
  * ドの音程で1秒の長さのwavファイルを保存し、再生するサンプルコード
* [sample2_play_buf.py](sample2_play_buf.py)
  * numpyでメモリ上に作ったサイン波を、PyAudioのstreamで順次再生するサンプルコード
* [sample3_play_all.py](sample3_play_all.py)
  * numpyでメモリ上に一気に作ったサイン波のデータ（トラック）を、PyAudioのstreamで一気に再生するサンプルコード。（連載第二回で解説）
* [sample4_play_all_tracks.py](sample4_play_all_tracks.py)
  * numpyでメモリ上に作った３つのトラックを合成して再生するサンプルコード。（連載第二回で解説）
* [sample5_play_midi.py](sample5_play_midi.py)
  * MIDIファイルを読み込み、解析して再生するサンプルコード。（連載第三回で解説）
* [sample6_midi2toio.py](sample6_midi2toio.py)
  * MIDIファイルを読み込んで　toio™コア キューブ　で再生できるフォーマットのC#配列に変換するサンプルコード。（連載第四回で解説）
