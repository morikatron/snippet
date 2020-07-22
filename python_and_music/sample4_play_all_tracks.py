"""
sample4_play_all_tracks.py

© Morikatron Inc. 2019
written by matsubara@morikatron.co.jp

numpyでメモリ上に作った３つのトラックを合成して再生するサンプルコード。
"""
import numpy as np  # install : conda install numpy
import pyaudio      # install : conda install pyaudio

# サンプリングレートを定義
SAMPLE_RATE = 44100


# 指定ノート番号のサイン波を、指定秒数生成してnumpy配列で返す関数
def notenumber2wave(notenumber: int, duration: float) -> np.array:
    # MIDIのノート番号を周波数に変換
    freq = 440.0 * 2 ** ((notenumber - 69) / 12)
    # 指定周波数のサイン波を指定秒数分生成
    return np.sin(np.arange(int(duration * SAMPLE_RATE)) * freq * np.pi * 2 / SAMPLE_RATE)


# 音名（C5とかC#5とか）のサイン波を、指定秒数生成してnumpy配列で返す関数
def name2wave(name: str, duration: float) -> np.array:
    notenumber: int = 0  # 該当する音名がなかった場合は無音区間とする
    if len(name) > 0:
        name = name.upper()
        # 末尾の数字（-1 ~ 9）を得る。数字がなければ5とする。
        octave = 5
        if name[-2] == "-1":
            octave = -1
            name = name[:-2]  # 後ろ2文字を削除
        elif name[-1].isdigit():
            octave = int(name[-1])
            name = name[:-1]  # 後ろ1文字を削除
        names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        for i, n in enumerate(names):
            if name == n:
                # 音名とオクターブからノート番号が確定
                notenumber = (octave + 1) * 12 + i
                break
    return notenumber2wave(notenumber, duration)


# 曲＝[(音名,長さ)の配列]をwaveに変換してnumpy配列で返す関数
def notes2wave(notes: list) -> np.array:
    arr = np.array([])
    for note in notes:
        arr = np.append(arr, name2wave(note[0], note[1]))
    return arr


# n個の波形の長さを揃えて縦に積む関数
def padding_and_stack(inputs: list) -> np.array:
    # 配列の総数が0なら、返すものがない
    if len(inputs) < 1:
        return None
    # 配列の総数が1なら、その1個を返す
    if len(inputs) == 1:
        return inputs[0]
    # 配列の最大要素数を調べる
    maxlen = 0
    for x in inputs:
        if maxlen < len(x):
            maxlen = len(x)
    # 最大数に揃える（うしろに０を加える）
    for i, x in enumerate(inputs):
        if len(x) < maxlen:
            inputs[i] = np.pad(x, (0, maxlen-len(x)))
    # 縦に積む
    return np.vstack(inputs)


# pyaudio開始
p = pyaudio.PyAudio()

# ストリームを開く
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                frames_per_buffer=1024,
                output=True)

# トラックみっつ（ドレミファソー　+　ミファソラシー　+　ソラシドレー）の波形を作成
song1 = notes2wave([("C4", 0.3), ("D4", 0.3), ("E4", 0.3), ("F4", 0.3), ("G4", 0.6)])
song2 = notes2wave([("E4", 0.3), ("F4", 0.3), ("G4", 0.3), ("A4", 0.3), ("B4", 0.6)])
song3 = notes2wave([("G4", 0.3), ("A4", 0.3), ("B4", 0.3), ("C5", 0.3), ("D5", 0.6)])

# 3つの波形の長さを揃えて縦に積む
song = padding_and_stack([song1, song2, song3])

# 1つの波形に合成（個々のサンプルの平均を取る）
song = song.mean(axis=0)

# 再生
stream.write(song.astype(np.float32).tostring())

# ストリームを閉じる
stream.close()

# pyaudio終了
p.terminate()
