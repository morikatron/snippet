# Dear PyGuiのプログラム中でtkinterのファイルダイアログを使うサンプルプログラム
from dearpygui.core import *
from dearpygui.simple import *

import tkinter
import tkinter.filedialog as filedialog


def apply_selected_file(sender: str, data) -> None:
    """
    Dear PyGuiのファイルダイアログの実行結果を取得するコールバック
    ダイアログで [Cancel] を選択した場合には実行されません
    :param sender: 呼び出し元
    :param data: リスト [ディレクトリパス, ファイル名]
    :return:
    """
    directory = data[0]
    file = data[1]
    set_value("file_path", f"{directory}\\{file}")


def open_file(sender: str, data: str) -> None:
    """
    ファイルを開くダイアログを呼び出すコールバック
    :param sender: 呼び出し元
    :param data: ボタンごとにセットされた文字列
    :return:
    """

    if data == "DearPyGui":
        # Dear PyGuiの機能を利用する
        open_file_dialog(callback=apply_selected_file, extensions=".*,.txt")

    elif data == "tkinter":
        # tkinter の機能を利用する
        root = tkinter.Tk()
        root.withdraw()  # ルートウィンドウを非表示に設定
        file_path = filedialog.askopenfilename()
        root.destroy()  # 非表示になっているtkのウィンドウを削除する

        set_value("file_path", file_path)

    else:
        print(f"Unknown data({data})")


def save_file(sender: str, data) -> None:
    """
    ファイルを保存するダイアログを呼び出します
    Dear PyGuiに該当する機能はないので、tkinterを利用した実装のみ利用できます。
    :param sender: 呼び出し元
    :param data: 利用しない
    :return:
    """
    # tkinter の機能を利用する
    root = tkinter.Tk()
    root.withdraw()  # ルートウィンドウを非表示に設定
    file_path = filedialog.asksaveasfilename()
    root.destroy()  # 非表示になっているtkのウィンドウを削除する

    if file_path:
        with open(file_path, "w") as file:
            file.write("Test")


if __name__ == "__main__":
    set_main_window_title("File Dialog Sample")
    set_main_window_size(width=600, height=800)

    with window("Main Window", autosize=True, menubar=True):
        add_input_text("Path", source="file_path")
        add_button("Select File(tkinter)", callback=open_file, callback_data="tkinter")
        add_same_line()
        add_button("Select File(DearPyGui)", callback=open_file, callback_data="DearPyGui")
        add_button("Save File(tkinter)", callback=save_file)

    start_dearpygui(primary_window="Main Window")
