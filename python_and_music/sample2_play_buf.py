"""
sample2_play_buf.py

© Morikatron Inc. 2020
written by matsubara@morikatron.co.jp

numpyでメモリ上に作ったサイン波を、
PyAudioのstreamで順次再生するサンプルコード。
これでドミソドーっと鳴ります。
"""
import numpy as np  # install : conda install numpy
import pyaudio      # install : conda install pyaudio

# サンプリングレートを定義
SAMPLE_RATE = 44100


# 指定ストリームで、指定周波数のサイン波を、指定秒数再生する関数
def play(s: pyaudio.Stream, freq: float, duration: float):
    # 指定周波数のサイン波を指定秒数分生成
    samples = np.sin(np.arange(int(duration * SAMPLE_RATE)) * freq * np.pi * 2 / SAMPLE_RATE)
    # ストリームに渡して再生
    s.write(samples.astype(np.float32).tostring())


# PyAudio開始
p = pyaudio.PyAudio()

# ストリームを開く
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=1024,
                output=True)

# ドミソドーを再生
play(stream, 261.626, 0.3)  # note#60 C4 ド
play(stream, 329.628, 0.3)  # note#64 E4 ミ
play(stream, 391.995, 0.3)  # note#67 G4 ソ
play(stream, 523.251, 0.6)  # note#72 C5 ド

# ストリームを閉じる
stream.close()

# PyAudio終了
p.terminate()