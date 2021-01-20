"""
IO多路复用 基础演示 epoll
"""
from select import *
from socket import *

# 创建几个IO对象
tcp_sock = socket()
tcp_sock.bind(("0.0.0.0",8888))
tcp_sock.listen(5)

file = open("my.log",'r+')

udp_sock = socket(AF_INET,SOCK_DGRAM)


# 创建epoll对象
ep = epoll()

# 关注IO对象
ep.register(tcp_sock,EPOLLIN)
ep.register(udp_sock,EPOLLOUT|EPOLLERR)

# 建立查找字典
map = {
    tcp_sock.fileno():tcp_sock,
    udp_sock.fileno():udp_sock,
}

print("开始监控IO")
events = ep.poll()
print(events) # 就绪的IO

# 不再关注
ep.unregister(udp_sock)
del map[udp_sock.fileno()]





