# -*- coding: UTF-8 -*-

# 使用 select 完成 http 请求
# 下面的connect，send，recv 都属于阻塞式请求,都会立即返回

import socket
from urllib.request import urlparse
from selectors import DefaultSelector,EVENT_WRITE,EVENT_READ

# 实例化一个Selector
Selector = DefaultSelector()


class Fetcher():

    # 回调函数
    def readable(self,key):
        data = b''
        while True:
            # 这个捕捉异常的原因是函数刚触发还没有接收到数据就开始往下执行
            try:
                d = self.client.recv(1024)
            except Exception as e:
                continue

            if d:
                data += d
            else:
                break

        data = data.decode('utf-8')
        html_data = data.split('\r\n\r\n')[1]
        print(html_data)
        self.client.close()






    # 回调函数
    def connected(self,key):
        # send 之前，我们首先要在 Selector 里注销掉我们监控的这个事件
        Selector.unregister(key.fd)
        self.client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(self.path,self.host).encode('utf-8'))

        #接收数据，我们需要又一次监听socket
        Selector.register(self.client.fileno(),EVENT_READ,self.readable)


    def get_url(self,url):
        # 通过socket 请求html
        url = urlparse(url)
        self.host = url.netloc
        self.path = url.path
        if self.path == '':
            self.path = '/'

        # 建立socket 连接
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置非阻塞，下面connect 会立即返回
        self.client.setblocking(False)

        # 会报一个 BlockingIOError: [WinError 10035]的错误，属于正常的错误
        try:
            self.client.connect((self.host, 80))
        except Exception as e:
            pass

        # 注册
        # 注册需要3个参数：（1）描述符：client.fileno() 就是它的文件描述符;（2）事件：下一步需要给服务器发送数据，就是 write 事件
        # （3）回调函数：就是当它可写的时候，我们要执行什么逻辑
        Selector.register(self.client.fileno(),EVENT_WRITE,self.connected)


if __name__ == '__main__':

    get_url('http://www.baidu.com')







