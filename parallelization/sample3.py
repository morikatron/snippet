"""
プロセス生成のオーバーヘッドを体感するサンプル
"""

import os
import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def func():
    return True

LOOP_NUM = 100000 #繰り返し回数=10万回

if __name__ == "__main__":

    max_workers = os.cpu_count() #最大ワーカー数をシステムの CPU コアと同じにする

    # マルチスレッドの場合
    start = datetime.datetime.now()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(LOOP_NUM):
            executor.submit(func)
    elapsed = datetime.datetime.now() - start
    print("MultiThread: {}ms".format(elapsed.seconds*1000 + elapsed.microseconds/1000))

    # マルチプロセスの場合
    start = datetime.datetime.now()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for i in range(LOOP_NUM):
            executor.submit(func)
    elapsed = datetime.datetime.now() - start
    print("MultiProcess: {}ms".format(elapsed.seconds*1000 + elapsed.microseconds/1000))
