"""
基于epoll的网络并发模型
重点代码 ！！
"""

from socket import *
from select import *

# 地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)


def main():
    # tcp套接字 连接客户端
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %d" % PORT)

    # 防止IO处理过程中产生阻塞行为
    sock.setblocking(False)

    # 设置要监控的IO
    ep = epoll()
    ep.register(sock, EPOLLIN)

    # 查找字典 通过文件描述符 --》 IO对象
    map = {sock.fileno(): sock}

    # 循环接收客户端连接
    while True:
        events = ep.poll()  # events->[(fileno,event)]
        print("你有新的IO需要处理哦",events)
        # 逐个取值，分情况讨论
        for fd, event in events:
            if fd == sock.fileno():
                connfd, addr = map[fd].accept()
                print("Connect from", addr)
                # 将客户端套接字添加到监控列表
                connfd.setblocking(False)
                ep.register(connfd, EPOLLIN|EPOLLET) # 设置触发
                map[connfd.fileno()] = connfd  # 维护字典
            # else:
            #     # 连接套接字就绪
            #     data = map[fd].recv(1024).decode()
            #     # 客户端退出
            #     if not data:
            #         ep.unregister(fd)  # 不再监控
            #         map[fd].close()
            #         del map[fd] # 从字典删除
            #         continue
            #     print(data)
            #     map[fd].send(b"OK")


if __name__ == '__main__':
    main()
