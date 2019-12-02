# -*- coding: UTF-8 -*-

# 使用非阻塞 IO 完成 http 请求
# 下面的connect，send，recv 都属于阻塞式请求,都会立即返回，所以都要使用try 和 while

import socket
from urllib.request import urlparse

def get_url(url):
    # 通过socket 请求html

    url = urlparse(url)
    host = url.netloc
    path = url.path
    if path == '':
        path = '/'

    # 建立socket 连接
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 设置非阻塞，下面connect 会立即返回
    client.setblocking(False)

    #会报一个 BlockingIOError: [WinError 10035]的错误，属于正常的错误,捕获就行了
    try:
        client.connect((host,80))
    except Exception as e:
        pass

    while True:
        # 这个捕捉异常的原因是没有获取到连接就开始发送数据
        try:
            client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path,host).encode('utf-8'))
            break
        except Exception as e:
            pass

    data = b''
    while True:
        # 这个捕捉异常的原因是函数刚触发还没有接收到服务器的数据返回就开始往下执行
        try:
            d = client.recv(1024)
        except Exception as e:
            continue

        if d:
            data += d
        else:
            break

    data = data.decode('utf-8')
    html_data = data.split('\r\n\r\n')[1]
    print(html_data)
    client.close()



if __name__ == '__main__':

    get_url('http://www.baidu.com')







