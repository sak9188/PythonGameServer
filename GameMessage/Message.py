# -*- coding: UTF-8 -*-

# 消息头 消息体的大小 4字节 最大1G的打包
# 消息类型 2字节
# 消息体 任意字节
# 哈希数据校验 16字节（消息头+消息类型+消息体）
from Core import MakeID


# 分配ID的对象
Allot = MakeID.make_id_fun("Message")


def allot_msg_id(name, id_val=None):
	global Allot
	return Allot.allot_id(name, id_val)


# ==============================
# 这里分配消息
# ==============================
MS_HeartBeat = allot_msg_id("心跳")
MS_Connect = allot_msg_id("链接服务器")
MS_Disconnection = allot_msg_id("断开链接")