"""
sample3_play_all.py

© Morikatron Inc. 2020
written by matsubara@morikatron.co.jp

numpyでメモリ上に一気に作ったサイン波のデータ（トラック）を、
PyAudioのstreamで一気に再生するサンプルコード。
"""
import numpy as np  # install : conda install numpy
import pyaudio  # install : conda install pyaudio

# サンプリングレートを定義
SAMPLE_RATE = 44100


# 指定ノート番号のサイン波を、指定秒数生成してnumpy配列で返す関数
def notenumber2wave(notenumber: int, duration: float) -> np.array:
    # MIDIのノート番号を周波数に変換
    freq = 440.0 * 2 ** ((notenumber - 69) / 12)
    # 指定周波数のサイン波を指定秒数分生成
    samples = np.sin(np.arange(int(duration * SAMPLE_RATE)) * freq * np.pi * 2 / SAMPLE_RATE)
    # 波形の頭とお尻を最大100サンプル(約0.002秒)をフェード処理する（つなぎ目のプチノイズ軽減のため）
    fade_len = min(100, samples.size)  # フェード処理するサンプル数
    slope = (np.arange(fade_len) - 1) / fade_len  # フェードインのスロープ計算
    samples[:fade_len] = samples[:fade_len] * slope  # サンプル先頭とスロープを掛けてフェードイン
    slope = ((fade_len - 1) - np.arange(fade_len)) / fade_len  # フェードアウトのスロープ計算
    samples[-fade_len:] = samples[-fade_len:] * slope  # サンプル末尾とスロープを掛けてフェードアウト
    return samples


# PyAudio開始
p = pyaudio.PyAudio()

# ストリームを開く
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=1024,
                output=True)

# ドミソドーの波形を作る
track = np.array([])
track = np.append(track, notenumber2wave(60, 0.3))  # note#60 C4 ドを追加
track = np.append(track, notenumber2wave(64, 0.3))  # note#64 E4 ミを追加
track = np.append(track, notenumber2wave(67, 0.3))  # note#67 G4 ソを追加
# l1 = track.size
track = np.append(track, notenumber2wave(72, 0.6))  # note#72 C5 ドを追加

# 再生
stream.write(track.astype(np.float32).tostring())

# ストリームを閉じる
stream.close()

# PyAudio終了
p.terminate()

# 47行目あたりにあるl1 = track.sizeで記録しておいた位置を中心にグラフをプロットする（波形のつなぎ目で見たい場合）
# import matplotlib.pyplot as plt
# plt.figure(figsize=(6,3))
# plt.plot(track[l1 - 200:l1 + 200])
# plt.show()
