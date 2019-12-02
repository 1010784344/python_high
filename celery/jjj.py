# -*- coding: UTF-8 -*-
# 异步任务队列传统版（串行版）

from flask import Flask
from time import sleep


app = Flask(__name__)
@app.route('/jobs/<int:value>')
def run_jobs(value=None):

    print('%s task running.' % value)
    long_task('hello', value)
    return 'long task running.'
# 耗时任务
def long_task(arg1, arg2):
    sleep(10)
    print("%s is done!"%arg2)
if __name__ == '__main__':
    app.run(debug=True)