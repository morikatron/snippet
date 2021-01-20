"""
sample6_midi2toio.py

© Morikatron Inc. 2020-2021
written by matsubara@morikatron.co.jp

MIDIファイルを読み込んで　toio™コア キューブ　で再生できるフォーマットのC#配列に変換する
"""
import sys
import os
import mido  # install : pip install mido

# MIDIの1ノートを表現するリストの要素を定義しておく
IX_ON_TIME = 0  # int note onの時間　単位はミリ秒
IX_OFF_TIME = 1  # int note offの時間　単位はミリ秒
IX_NOTE_NUMBER = 2  # int ノート番号
IX_VELOCITY = 3  # float 音量　範囲は0-1.0
IX_DURATION = 4  # float 音の長さ　単位はミリ秒

# toio™コア キューブ 技術仕様( https://toio.github.io/toio-spec/docs/ble_sound ) により規定される各種の値
TIME_RESOLUTION = 10  # 時間の分解能は10ミリ秒
MAX_NOTES = 59  # 最大59音まで（注：キューブファーム2.0.0は58音まで）
MAX_NOTE_DURATION = 2550  # １音のサイズは最長2550msecまで


# MIDIファイルの中のメッセージをすべてプリント（デバッグ用）
def print_midi(file_path: str) -> None:
    print('----------------- PRINT MIDI -----------------')
    file = mido.MidiFile(file_path)
    print(file)
    for track in file.tracks:
        print('-----------------', track)
        for message in track:
            print(message)
    print('----------------------------------------------')


# 複数トラックをtoio™コア キューブで再生できる以下のようなC#ジャグ配列に変換してprintする
#  byte[][] songName = new byte[][]
#  {
#      new byte[] {3,1,40,  31,62,98,  ...},
#      new byte[] {3,1,54,  94,0,0,  ...},
#      new byte[] {3,1,36,  252,0,0,  ...},
#      new byte[] {3,1,52,  255,0,0,  ...}
#  };
def print_tracks_for_toio(tracks: list, filepath: str) -> None:
    filename = os.path.splitext(os.path.basename(filepath))[0]
    max_duration = 0
    result = 'byte[][] ' + filename + ' = new byte[][]\n{\n'
    for track in tracks:
        # 音の数をキューブが再生できる最大数でカット
        if len(track) > MAX_NOTES:
            print('// [WARNING] Too many notes : ', MAX_NOTES)
            del track[MAX_NOTES:]
        result = result + '    new byte[] {3,1,' + str(len(track))
        duration = 0
        for note in track:
            result = result + ',  ' + str(int(note[IX_DURATION] / 10)) + ',' \
                     + str(note[IX_NOTE_NUMBER]) + ',' + str(note[IX_VELOCITY])
            duration = duration + note[IX_DURATION]
        result = result + '},\n'
        max_duration = max(duration, max_duration)
    result = result + '};'
    print('// ' + filename + ' : ' + str(max_duration / 1000) + ' seconds')  # C#用コメント
    print(result)


# ノートのリストを　toio™コア キューブ　の仕様に合わせて調整する
def adjust_notes(notes: list) -> list:
    # まず、すべてのノートon/offをキューブの時間分解能（10msec）に合わせる
    for note in notes:
        note[IX_ON_TIME] = round(note[IX_ON_TIME] / TIME_RESOLUTION) * TIME_RESOLUTION
        note[IX_OFF_TIME] = round(note[IX_OFF_TIME] / TIME_RESOLUTION) * TIME_RESOLUTION
    # 次の音とのギャップが分解能以下の場合、前の音の長さを伸ばしてギャップを埋めておく
    for ix, note in enumerate(notes):
        if (ix + 1) < len(notes):  # 次のノートが存在する
            if (notes[ix + 1][IX_ON_TIME] - note[IX_OFF_TIME]) < TIME_RESOLUTION:  # ギャップが小さい場合は潰しておく
                note[IX_OFF_TIME] = notes[ix + 1][IX_ON_TIME]  # 前の音の長さを、次の音の開始時刻に合わせて伸ばす
    # 最初が無音の場合、そこに「無音のノート」を挿入しておく
    if len(notes) > 0:
        if notes[0][IX_ON_TIME] > 0:
            notes.insert(0, [0, notes[0][IX_ON_TIME], 0, 0, 0])
    # 音と音の間にギャップがある場合、そこに「無音のノート」を差し込んでいく
    gap_filled_notes = []
    for ix, note in enumerate(notes):
        # まずこのノートを追加して
        gap_filled_notes.append(note)
        if (ix + 1) < len(notes):  # 次のノートが存在し
            if (notes[ix + 1][IX_ON_TIME] - note[IX_OFF_TIME]) > 0:  # ギャップが存在するならば
                gap_filled_notes.append([note[IX_OFF_TIME], notes[ix + 1][IX_ON_TIME], 0, 0, 0])  # 「無音のノート」を追加
    # １音の長さを MAX_NOTE_DURATION に制限（ノートを分割することで対応）
    final_notes = []
    for ix, note in enumerate(gap_filled_notes):
        length = note[IX_OFF_TIME] - note[IX_ON_TIME]
        if length > 0:
            while length > MAX_NOTE_DURATION:
                final_notes.append([note[IX_ON_TIME],
                                    note[IX_ON_TIME] + MAX_NOTE_DURATION,
                                    note[IX_NOTE_NUMBER],
                                    note[IX_VELOCITY],
                                    MAX_NOTE_DURATION])
                length = length - MAX_NOTE_DURATION
                note[IX_ON_TIME] = note[IX_ON_TIME] + MAX_NOTE_DURATION
            note[IX_OFF_TIME] = note[IX_ON_TIME] + length
            final_notes.append(note)
    # 調整後の全ノートの長さを再計算
    for note in final_notes:
        note[IX_DURATION] = note[IX_OFF_TIME] - note[IX_ON_TIME]
    # 完成したノートのリストを戻す
    return final_notes


# MIDIファイルの全トラックを解析し、トラック数分のキューブ用楽譜を作り、printする
def midi2toio(file_path: str) -> None:
    # print_midi(file_path)  # MIDIファイルの中身を全部プリント（デバッグ時にどうぞ）
    tempo = 500000.0
    file = mido.MidiFile(file_path)
    ticks_per_beat = file.ticks_per_beat
    abs_time_tick_msec = tempo / ticks_per_beat / 1000.0
    # MIDIファイルの全トラックをサーチ
    tracks = []
    for track in file.tracks:
        now = 0  # 現在の時刻（msec）を保持
        notes = []  # ノート情報の配列
        for event in track:
            now = now + event.time * abs_time_tick_msec
            if event.type == 'set_tempo':
                tempo = event.tempo
                abs_time_tick_msec = tempo / ticks_per_beat / 1000.0
                # print('BPM = ', 60000000.0 / tempo)
            elif event.type == 'note_on' and event.channel == 9:
                # 打楽器を無視
                pass
            elif event.type == 'note_off' or (event.type == 'note_on' and event.velocity == 0):
                # ノートオフを処理
                for note in notes:
                    if (note[IX_OFF_TIME] == 0) and (note[IX_NOTE_NUMBER] == event.note):
                        note[IX_OFF_TIME] = now
                        note[IX_DURATION] = note[IX_OFF_TIME] - note[IX_ON_TIME]
            elif event.type == 'note_on':
                # ノートオンを登録
                notes.append([now, 0, event.note, event.velocity, 0])
        if len(notes) > 0:  # このトラックに発音すべきノートがあれば
            notes = adjust_notes(notes)  # ノート配列をtoioの仕様に合わせて調整する
            tracks.append(notes)  # トラックとして記録
    print_tracks_for_toio(tracks, file_path)


if __name__ == '__main__':
    argv = sys.argv
    argc: int = len(argv)
    if argc == 2:  # １個目のパラメータはMIDIファイルのパスとする
        midi2toio(argv[1])
    else:
        # 引数がないときは本プログラムの使い方を示す
        print('Usage: python sample6_midi2toio FILE.mid ')
        # サンプルに用意したMIDIファイルがカレントディレクトリにあればそれを変換（動作サンプルとして）
        if os.path.exists('skaters_waltz.mid'):
            midi2toio('skaters_waltz.mid')
        if os.path.exists('oomakiba.mid'):
            midi2toio('oomakiba.mid')
