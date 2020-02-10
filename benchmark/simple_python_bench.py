"""
ジュリア集合の計算アルゴリズムは オライリー「ハイパフォーマンス Python」に記載されているものを使っています。
書籍: https://www.oreilly.co.jp/books/9784873117409/
Github: https://github.com/mynameisfiber/high_performance_python/blob/master/01_profiling/cpu_profiling/julia1_nopil.py
"""
import datetime
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def loop_test(loop_num: int):
    """
    指定した回数 何もしないでループ処理を回します。
    :param loop_num: 空ループを回す回数
    :return: ループ回数
    """
    for i in range(loop_num):
        pass
    return loop_num


def func():
    return True


def function_call_test(loop_num: int):
    """
    指定した回数 何もしない関数 func を実行します。
    :param loop_num: 繰り返し回数
    :return: ループ回数
    """
    for i in range(loop_num):
        func()
    return loop_num


def print_test(loop_num: int):
    """
    指定した回数 print します。
    :param loop_num: 繰り返し回数
    :return: ループ回数
    """
    for i in range(loop_num):
        print("Hello Python World.")
    return loop_num


x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -0.42193

def calculate_z_serial_purepython(maxiter, zs, cs):
    """ジュリア漸化式を用いてoutput リストを計算する"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while abs(z) < 2 and n < maxiter:
            z = z * z + c
            n += 1
        output[i] = n
    return output


def calc_pure_python(desired_width, max_iterations):
    """複素数の座標リストzs と、複素数のパラメータリストcs を
    作り、ジュリア集合を作って表示する"""
    x_step = (float(x2 - x1) / float(desired_width))
    y_step = (float(y1 - y2) / float(desired_width))
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step

    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    output = calculate_z_serial_purepython(max_iterations, zs, cs)


def write_sys_info(file):
    """
    実行環境の情報をファイルに書き込みます。

    :param file: ファイルハンドル
    :return: None
    """
    import platform
    import psutil

    file.write("Python:\n")
    file.write(" - Python: {} ({}) \n".format(platform.python_version(), platform.python_implementation()))
    file.write(" - Build: {} \n".format(platform.python_build()))
    file.write(" - Compiler: {} \n".format(platform.python_compiler()))
    file.write("PC Info:\n")
    file.write(" - OS: {} \n".format(platform.platform()))
    file.write(" - Processor: {} \n".format(platform.processor()))
    file.write("   - Core: {}/{} \n".format(psutil.cpu_count(logical=False), psutil.cpu_count(logical=True)))
    file.write("   - Freq(MHz): {} \n".format(psutil.cpu_freq(percpu=False)))
    file.write(" - Memory: {}GB ({:,} Byte) \n".format( round( psutil.virtual_memory().total/(1024*1024*1024) ), psutil.virtual_memory().total))
    file.write("\n")


if __name__ == "__main__":
    """
    TurboBoost の効果なのか最初だけ高速になってしまうので
    測定しやすさのために最初に無駄な計算を挟みます。
    """
    calc_pure_python(desired_width=1000, max_iterations=100)

    file = open("result.txt", mode="w", encoding="utf-8")
    write_sys_info(file)

    times = []
    for i in range(10):
        start = datetime.datetime.now()
        a = loop_test(10000000)
        elapsed = datetime.datetime.now() - start
        times.append(elapsed.seconds*1000 + elapsed.microseconds/1000)
    file.write("loop_test: {} ms\n".format(sum(times)/len(times)))

    times = []
    for i in range(10):
        start = datetime.datetime.now()
        for i in range(1000000):
            func()
        elapsed = datetime.datetime.now() - start
        times.append(elapsed.seconds*1000 + elapsed.microseconds/1000)
    file.write("function_call_test: {} ms\n".format(sum(times)/len(times)))


    times = []
    for i in range(10):
        start = datetime.datetime.now()
        a = print_test(100000)
        elapsed = datetime.datetime.now() - start
        times.append(elapsed.seconds * 1000 + elapsed.microseconds / 1000)
    file.write("print_test: {} ms\n".format(sum(times) / len(times)))

    times = []
    for i in range(10):
        start = datetime.datetime.now()
        calc_pure_python(desired_width=1000, max_iterations=100)
        elapsed = datetime.datetime.now() - start
        times.append(elapsed.seconds * 1000 + elapsed.microseconds / 1000)
    file.write("calc_julia_set: {} ms\n".format(sum(times) / len(times)))

    times = []
    for i in range(10):
        start = datetime.datetime.now()
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            for i in range(100000):
                executor.submit(func)
        elapsed = datetime.datetime.now() - start
        times.append(elapsed.seconds * 1000 + elapsed.microseconds / 1000)
    file.write("Thread: {} ms\n".format(sum(times) / len(times)))

    times = []
    for i in range(10):
        start = datetime.datetime.now()
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            for i in range(100000):
                executor.submit(func)
        elapsed = datetime.datetime.now() - start
        times.append(elapsed.seconds * 1000 + elapsed.microseconds / 1000)
    file.write("Process: {} ms\n".format(sum(times) / len(times)))

    file.close()
