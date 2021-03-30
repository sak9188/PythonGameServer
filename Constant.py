# -*- coding: UTF-8 -*-

# 消息头 消息体的大小 4字节 最大1G的打包
# 消息类型 2字节
# 消息体 任意字节
# 哈希数据校验 16字节（消息头+消息类型+消息体）

START_ID = -1

def allot_msg(name):
	global START_ID
	"模块内唯一的消息id，不会根据服务器实例不同而不同"
	START_ID += 1
	return START_ID

MS_HeartBeat = allot_msg("心跳")
MS_Connect = allot_msg("链接服务器")
MS_Disconnection = allot_msg("断开链接")