# -*- coding: UTF-8 -*-
from Core import MakeID

# 所有的注册函数表
RegFunDict = {}

# 分配ID的对象
Allot = MakeID.make_id_fun("Event")

def reg_event(event_id, fun):
	global RegFunDict
	fun_set = RegFunDict.get(event_id)
	if fun_set is None:
		fun_set = set()
		RegFunDict[event_id] = fun_set
	fun_set.add(fun)


def trigger_event(event_id, *params):
	global RegFunDict
	fun_set = RegFunDict.get(event_id)
	if not fun_set:
		print("not found event_id %d" % event_id)
		return
	for fun in fun_set:
		fun(*params)


def allot_event_id(name, desc, id_val=None):
	global Allot
	return Allot.allot_id(name, id_val)

# =================================================
# 下面是事件定义id
# =================================================
AfterInitScript = allot_event_id('AfterInitScript', '初始化脚本以后')
AfterInitServer = allot_event_id('AfterInitServer', '初始化服务器以后')
BeforeLostClient = allot_event_id('BeforeLostClient', '在失去链接以前')
AfterSecond = allot_event_id('AfterSecond', '一秒种以后')
AfterLostProcess = allot_event_id('AfterLostProcess', '在失去进程链接以后')