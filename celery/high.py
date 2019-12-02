# -*- coding: UTF-8 -*-
# （并行版）：线程池版，异步任务队列
import threading
from flask import Flask
from time import sleep
from concurrent.futures import ThreadPoolExecutor
# DOCS https://docs.python.org/3/library/concurrent.futures.html
# #concurrent.futures.ThreadPoolExecutor
# 创建线程池执行器
executor = ThreadPoolExecutor(10)
app = Flask(__name__)

@app.route('/jobs/<int:value>')
def run_jobs(value=None):
    # 交由线程去执行耗时任务

    print(threading.enumerate())
    executor.submit(long_task, 'hello', value)
    print('%s task running.'%value)
    return 'long task running.'

# 定义耗时任务
def long_task(arg1, arg2):
    sleep(10)
    print("%s is done!"%arg2)


if __name__ == '__main__':
    app.run(debug=True)