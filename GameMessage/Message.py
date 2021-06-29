# -*- coding: UTF-8 -*-

# 消息头 消息体的大小 4字节 最大1G的打包
# 消息类型 2字节
# 消息体 任意字节
# 哈希数据校验 16字节（消息头+消息类型+消息体）
from Core import MakeID


# 分配ID的对象
Allot = MakeID.make_id_fun("Message")

# 消息注册列表
MSG_HandlerDict = {}

# 消息解释表
MSG_Desc ={}


def allot_msg_id(name, desc, id_val=None):
	global Allot
	msg_id = Allot.allot_id(name, id_val)
	MSG_Desc[msg_id] = desc
	return msg_id


def reg_msg_handler(msg_id, fun):
	'''
	注册消息函数
	'''
	global MSG_HandlerDict
	reg_fun = MSG_HandlerDict.get(msg_id)
	if reg_fun:
		print("already has reged function id%d" % msg_id)
	MSG_HandlerDict[msg_id] = fun


def handle_reg_msg(msg_id, *args):
	'''
	处理注册的消息
	'''
	global MSG_HandlerDict
	fun = MSG_HandlerDict.get(msg_id)
	if not fun:
		print("there is no fun with msg_id is %d" % msg_id)
		return
	fun(*args)


# ==============================
# 这里分配消息
# ==============================MS
MS_HeartBeat = allot_msg_id('MS_HeartBeat', "心跳")
MS_Connect = allot_msg_id('MS_Connect', "链接服务器")
MS_Disconnection = allot_msg_id('MS_Disconnection', "断开链接")
MS_AddGateWayProcess = allot_msg_id('MS_AddGateWayProcess', "添加网关进程链接")