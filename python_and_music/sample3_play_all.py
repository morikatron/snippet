"""
sample3_play_all.py

© Morikatron Inc. 2019
written by matsubara@morikatron.co.jp

numpyでメモリ上に一気に作ったサイン波のデータ（トラック）を、
pyaudioのstreamで一気に再生するサンプルコード。
"""
import numpy as np  # install : conda install numpy
import pyaudio      # install : conda install pyaudio

# サンプリングレートを定義
SAMPLE_RATE = 44100


# 指定ノート番号のサイン波を、指定秒数生成してnumpy配列で返す関数
def notenumber2wave(notenumber: int, duration: float) -> np.array:
    # MIDIのノート番号を周波数に変換
    freq = 440.0 * 2 ** ((notenumber-69) / 12)
    # 指定周波数のサイン波を指定秒数分生成
    return np.sin(np.arange(int(duration * SAMPLE_RATE)) * freq * np.pi * 2 / SAMPLE_RATE)


# pyaudio開始
p = pyaudio.PyAudio()

# ストリームを開く
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=1024,
                output=True)

# ドミソドーの波形を作る
song = np.array([])
song = np.append(song, notenumber2wave(60, 0.3))  # note#60 C4 ド
song = np.append(song, notenumber2wave(64, 0.3))  # note#64 E4 ミ
song = np.append(song, notenumber2wave(67, 0.3))  # note#67 G4 ソ
song = np.append(song, notenumber2wave(72, 0.6))  # note#72 C5 ド

# 再生
stream.write(song.astype(np.float32).tostring())

# ストリームを閉じる
stream.close()

# pyaudio終了
p.terminate()
