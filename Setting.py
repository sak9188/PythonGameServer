# -*- coding: UTF-8 -*-

# 这里是数据库链接参数
ConnectParams = ("localhost", 3306, "root", "hkkk")

# 这里是服务器世界进程
WorldSever = ('localhost', 9090)

# 这里是服务器主进程
MainServer = ('localhost', 9190)

# 这里是服务器网关进程
GateServer = ('localhost', 9290)

# 这里是服务器聊天进程
ChatServer = ('localhost', 9390)

# 这里是服务器世界进程
ChatServer = ('localhost', 9490)

# 这里是数据库进程
DBSever = ('localhost', 9590)

# 实验性质的进程
ComputeSever = () # 大规模运算服务器
DataCacheSever = () # 数据缓存服务器


'''
服务器架构说明

World 1:* -> MainSever *:*-> ChatSever *:* DBServer

一个世界服务器服务多个MainServer服务器 一对多关系

多个MainSever可以有多个ChatSever 多对多关系

数据库进程
MainServer 1:* DBServer 这里存储了所有的数据
WorldServer 1:1 DBSever 

一个DBSever服务一个World和Main，其中World有多个DBSever服务，每个DBSever只存储与本服相关的MainServer的World数据
DBSever主要是通过异步方法来操作数据库

# ============================
# 关于这个架构的问题与说明
# ============================
1. 如果要支持PC网游的多频道那样的系统，Python在这方面就不太行，因为需要多线程，实际上Python是伪多线程
如果要支持的话, 可能主逻辑核心得换成C语言写，Python作为内嵌脚本

或者可以用其他骚操作，这里可以后面讨论讨论

2. 因为主进程和聊天进程和数据库进程都是多对多的关系，在这方面我设计的想法是想做成负载均衡
就是聊天是负载均衡，聊天进程只是提供一个聊天服务的，所以不要去关心谁是主服务器。

聊天的想法是这样的，可能在游戏里有多个聊天频道，每个频道可能都对应着不同的聊天服务器
然后聊天服务器将数据写入对应聊天对应的那个主服务器的数据库里
这样就可能就会导致设计的很复杂。。。

2. 如何处理对性能要求很高的场景？
我打算用Cython来处理或者CFFI，这些都是用C语言来提高性能的地方。

对于超大规模的运算，可能单纯C语言就不太行了
如果还需要的话，我打算就使用GPU和CUDA来做高性能的大规模运算

'''