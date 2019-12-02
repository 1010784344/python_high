# -*- coding: UTF-8 -*-
#使用socket 模拟 http请求
# 非阻塞 IO 模拟 http 请求
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
    client.connect((host,80))
    client.send('GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n'.format(path,host).encode('utf-8'))
    data = b''
    while True:
        d = client.recv(1024)
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







