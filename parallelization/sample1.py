"""
ジュリア集合の計算アルゴリズムは オライリー「ハイパフォーマンス Python」に記載されているものを使っています。
書籍: https://www.oreilly.co.jp/books/9784873117409/
Github: https://github.com/mynameisfiber/high_performance_python/blob/master/01_profiling/cpu_profiling/julia1_nopil.py
"""

import os
import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# 調査する複素空間
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

if __name__ == "__main__":

    max_workers = os.cpu_count() #最大ワーカー数をシステムの CPU コアと同じにする

    start = datetime.datetime.now()
    for i in range(32):
        calc_pure_python(desired_width=500, max_iterations=100)
    elapsed = datetime.datetime.now() - start
    print("SingleThread: {}ms".format(elapsed.seconds*1000 + elapsed.microseconds/1000))

    # マルチスレッドの場合
    start = datetime.datetime.now()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(32):
            executor.submit(calc_pure_python, 500, 100)
    elapsed = datetime.datetime.now() - start
    print("MultiThread: {}ms".format(elapsed.seconds*1000 + elapsed.microseconds/1000))

    # マルチプロセスの場合
    start = datetime.datetime.now()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i in range(32):
            executor.submit(calc_pure_python, 500, 100)
    elapsed = datetime.datetime.now() - start
    print("MultiProcess: {}ms".format(elapsed.seconds*1000 + elapsed.microseconds/1000))