# -*- coding: UTF-8 -*-
from Core import MakeID
from Core.Extent.sortedcontainers import SortedList

# 所有的注册函数表
RegFunDict = {}

# 注释表
RegFunDescDict = {}

# 分配ID的对象
Allot = MakeID.make_id_fun("Event")

class EventDispacther(object):

	def __init__(self):
		self._reg_fun_dict = {}

	"""
	Property 注册
	"""
	@property
	def reg_fun_dict(self):
		return self._reg_fun_dict

	@reg_fun_dict.setter
	def reg_fun_dict(self, value):
		self._reg_fun_dict = value
	
	"""
	类方法
	"""
	@classmethod
	def reg_g_event(cls, event_id, fun, oder=1000):
		# 注册全局事件
		global RegFunDict
		fun_list = RegFunDict.get(event_id)
		if fun_list is None:
			fun_list = SortedList(key=lambda x:x[0])
			RegFunDict[event_id] = fun_list
		fun_list.add((oder, fun))

	@classmethod
	def trigger_g_event(cls, event_id, *params, **kwargs):
		# 触发全局事件
		global RegFunDict, RegFunDescDict
		fun_list = RegFunDict.get(event_id)
		if not fun_list:
			desc = RegFunDescDict.get(event_id)
			print("no reg event(%s) fun" % desc)
			return
		for fun_data in fun_list:
			_, fun = fun_data
			try:
				fun(*params, **kwargs)
			except Exception as e:
				print(e)

	def reg_event(self, event_id, fun, oder=1000):
		fun_list = self.reg_fun_dict.get(event_id)
		if fun_list is None:
			fun_list = SortedList(key=lambda x:x[0])
			RegFunDict[event_id] = fun_list
		fun_list.add((oder, fun))


	def trigger_event(self, event_id, *params):
		global RegFunDescDict
		fun_list = self.reg_fun_dict.get(event_id)
		if not fun_list:
			desc = RegFunDescDict.get(event_id)
			print("no reg event(%s) fun" % desc)
			return
		for fun_data in fun_list:
			_, fun = fun_data
			try:
				fun(*params)
			except Exception as e:
				print(e)


def reg_g_event(event_id, fun, oder=1000):
	# 注册全局函数
	EventDispacther.reg_g_event(event_id, fun, ord)


def trigger_g_event(event_id, *params, **kwargs):
	# 触发全局函数
	EventDispacther.trigger_g_event(event_id, *params, **kwargs)


def allot_event_id(name, desc, id_val=None):
	global Allot, RegFunDict
	reg_id = Allot.allot_id(name, id_val)
	RegFunDescDict[reg_id] = desc
	return reg_id

# =================================================
# 下面是事件定义id
# =================================================
AfterInitScript = allot_event_id('AfterInitScript', '初始化脚本以后')
AfterInitServer = allot_event_id('AfterInitServer', '初始化服务器以后')
AfterSecond = allot_event_id('AfterSecond', '一秒种以后')
AfterLostProcess = allot_event_id('AfterLostProcess', '在失去进程链接以后')
AfterConnectServer = allot_event_id('AfterConnectServer', '在客户端链接服务器以后') # 特指游戏客户端
BeforeLostClient = allot_event_id('BeforeLostClient', '在失去客户端链接以前') # 特指游戏客户端
