"""
sample5_play_midi.py

© Morikatron Inc. 2020
written by matsubara@morikatron.co.jp

MIDIファイルを読み込んでがんばって再生するプログラム
"""
import math
import sys
import os

import numpy as np  # install : conda install numpy
import pyaudio  # install : conda install pyaudio
import mido  # install : pip install mido

# サンプリングレートを定義
SAMPLE_RATE = 44100

# MIDIの1ノートを表現するリストの要素を定義しておく
IX_ON_MSEC = 0  # int note onの時間　単位はミリ秒
IX_OFF_MSEC = 1  # int note offの時間　単位はミリ秒
IX_NOTE_NUMBER = 2  # int ノート番号
IX_VELOCITY = 3  # float 音量　範囲は0-1.0
IX_DULATION = 4  # float 音の長さ　単位は秒


# 指定ノート番号のサイン波を、指定秒数生成してnumpy配列で返す関数
def notenumber2wave(notenumber: int, duration: float, volume: float) -> np.array:
    # MIDIのノート番号を周波数に変換
    freq = 440.0 * 2 ** ((notenumber - 69) / 12)
    # 指定周波数のサイン波を指定秒数分生成
    samples = np.sin(np.arange(int(duration * SAMPLE_RATE)) * freq * np.pi * 2 / SAMPLE_RATE) * volume
    # 波形の頭とお尻を最大100サンプル(約0.002秒)をフェード処理する（つなぎ目のプチノイズ軽減のため）
    fade_len = min(100, samples.size)  # フェード処理するサンプル数
    slope = (np.arange(fade_len) - 1) / fade_len  # フェードインのスロープ計算
    samples[:fade_len] = samples[:fade_len] * slope  # サンプル先頭とスロープを掛けてフェードイン
    slope = ((fade_len - 1) - np.arange(fade_len)) / fade_len  # フェードアウトのスロープ計算
    samples[-fade_len:] = samples[-fade_len:] * slope  # サンプル末尾とスロープを掛けてフェードアウト
    return samples


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
            inputs[i] = np.pad(x, (0, maxlen - len(x)))
    # 縦に積む
    return np.vstack(inputs)


# 渡された波形（np.array）を再生する
def play_wave(wave) -> None:
    # PyAudio開始
    p = pyaudio.PyAudio()

    # ストリームを開く
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=SAMPLE_RATE,
                    frames_per_buffer=1024,
                    output=True)

    # 再生
    stream.write(wave.astype(np.float32).tostring())

    # ストリームを閉じる
    stream.close()

    # PyAudio終了
    p.terminate()


# MIDIファイルの中のメッセージをすべてプリント
def print_midi(file_path: str) -> None:
    print("----------------- PRINT MIDI -----------------")
    file = mido.MidiFile(file_path)
    print(file)
    for track in file.tracks:
        print("-----------------", track)
        for message in track:
            print(message)
    print("----------------------------------------------")


# 1トラック分の notes[note[],note[],...] を波形に変換して返す
def notes2track(notes: list) -> np.array:
    # まずトラックの長さを調査（いちばん遅いnote off）
    track_msec = 0
    for note in notes:
        if track_msec < note[IX_OFF_MSEC]:
            track_msec = note[IX_OFF_MSEC]
    # まずトラックの長さの無音波形（ベース配列）を作る
    track_base = np.zeros(int((track_msec / 1000.0) * SAMPLE_RATE))
    # 次に、ノートの波形を生成し、ベース配列の上に重ねていく
    for note in notes:
        if note[IX_DULATION] > 0:  # サンプルが存在するくらい長い場合に限って処理する
            wave = notenumber2wave(note[IX_NOTE_NUMBER], note[IX_DULATION], note[IX_VELOCITY])
            fromix = int((note[IX_ON_MSEC] / 1000.0) * SAMPLE_RATE)
            toix = fromix + wave.size
            stacked = np.vstack((wave, track_base[fromix:toix]))
            newwave = stacked.mean(axis=0)
            track_base[fromix:toix] = newwave
    return track_base


# MIDIファイルの全トラック波形を合成した１つの波形を返す
def midi2wave(file_path: str) -> np.array:
    tempo = 500000.0
    file = mido.MidiFile(file_path)
    ticks_per_beat = file.ticks_per_beat
    abs_time_tick_msec = tempo / ticks_per_beat / 1000.0

    tracks = []
    # Search tracks
    for track in file.tracks:
        now = 0  # 現在の時刻（msec）を保持
        notes = []  # ノート情報の配列
        for event in track:
            now = now + event.time * abs_time_tick_msec
            if event.type == 'set_tempo':
                tempo = event.tempo
                abs_time_tick_msec = tempo / ticks_per_beat / 1000.0
                # print("BPM = ", 60000000.0 / tempo)
            elif event.type == 'note_on' and event.channel == 9:
                # 打楽器を無視
                pass
            elif event.type == 'note_off' or (event.type == 'note_on' and event.velocity == 0):
                # ノートオフを処理
                for note in notes:
                    if (note[IX_OFF_MSEC] == 0) and (note[IX_NOTE_NUMBER] == event.note):
                        note[IX_OFF_MSEC] = now
                        note[IX_DULATION] = (note[IX_OFF_MSEC] - note[IX_ON_MSEC]) / 1000.0
                        note[IX_VELOCITY] = note[IX_VELOCITY] / 127.0
            elif event.type == 'note_on':
                # ノートオンを登録
                notes.append([math.floor(now), 0, event.note, event.velocity, 0])
        if len(notes) > 0:  # このトラックに発音すべきノートがあれば
            print("midi2wave: converting track #", len(tracks), "...")
            tracks.append(notes2track(notes))  # トラックの波形を作る

    # 1つの波形に合成（個々のサンプルの平均を取る）＝ボリューム1:1:1のミキシング
    print("midi2wave: mixising", len(tracks), "tracks ...")
    mixed_wave = padding_and_stack(tracks).mean(axis=0)
    print("midi2wave: finish!")
    return mixed_wave


# 指定されたMIDIファイルを波形に変換して再生する
def play_midi(file_path: str) -> None:
    print_midi(file_path)  # MIDIファイルの中身を全部プリント（デバッグのため）
    wave = midi2wave(file_path)  # MIDIファイルを波形に変換
    play_wave(wave)  # 波形を再生


if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    if (argc == 2):  # １個目のパラメータはMIDIファイルのパスとする
        play_midi(argv[1])
    else:
        # 引数がないときは本プログラムの使い方を示す
        print("Usage: python sample5_play_midi FILE.mid ")
        # marching.midがあればそれを変換する（簡単な動作サンプルとして）
        if os.path.exists("marching.mid"):
            play_midi("marching.mid")
