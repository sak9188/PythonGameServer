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
	for fun in fun_set:
		fun(*params)


def allot_event_id(name):
	global Allot
	return Allot.allot_id(name)

# =================================================
# 下面是事件定义id
# =================================================
AfterInitScript = allot_event_id("AfterInitScript")

print "import event"