# -*- coding: UTF-8 -*-
from GameEvent import Event
from GameNetwork import PassiveNetSide
import threading
import asyncore
from Core.Extent.sortedcontainers import SortedDict
from Core import ImportTool
from GameMessage import Message

class GameServer(PassiveNetSide.BaseSever):
	Instance = None

	def __init__(self, connect_params, process_type):
		if GameServer.Instance is not None:
			return
		PassiveNetSide.BaseSever.__init__(self, connect_params)
		GameServer.Instance = self
		# 时间相关
		self.last_time = self.server_time()
		# 进程类型
		self.process_type = process_type
		# 注册时延的dict
		self.tick_fun = SortedDict()
		# 线程相关
		if not self.before_run():
			# 起服失败直接溜溜球
			return
		self.is_run = True
		self.thread = threading.Thread(target=self.run)
		# 主线程挂掉以后网络线程也会挂掉
		self.thread.setDaemon(True)
		self.thread.start()
	
	def run(self):
		# 注册消息
		Message.reg_msg_handler(Message.MS_Disconnection, self.after_disconnect)
		Message.reg_msg_handler(Message.MS_Connect, self.after_connect)
		# 这里要触发事件
		Event.trigger_event(Event.AfterInitServer, GameServer.Instance)
		# 主消息循环
		asyncore.loop(timeout=0.01)
	
	def shutdown(self):
		if not self.before_close():
			return
		self.is_run = False
	
	def reg_tick(self, fun, args, secs):
		# 支持小数，也就是支持毫秒
		des_time = self.server_time() + secs
		fun_list = self.tick_fun.get(des_time)
		if not fun_list:
			self.tick_fun[secs] = [(fun, args),]
		else:
			fun_list.append((fun, args))
	
	def seconds(self):
		return int(self.server_time())

	def minutes(self):
		return int(self.server_time()/60.)

	def hours(self):
		return int(self.server_time()/3600.)

	def days(self):
		return int(self.server_time()/86400.)

	def update_time(self):
		# 获得当前的时间, 触发当前时间Tick
		# 如果服务器时间慢于服务器时间， 则会自动加速至现实时间
		now_time = self.server_time.sync_real_time()
		# print self.seconds()
		# dateArray = datetime.datetime.fromtimestamp(now_time)
		# otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
		with self.server_time:
			# 有先执行AfterSecond
			if self.last_time - now_time >= 1:
				Event.trigger_event(Event.AfterSecond)
			rm_list = []
			for key, val in self.tick_fun.items():
				if key > now_time:
					break
				for fun, arg in val:
					fun(*arg)
				self.tick_fun[key] = None
				rm_list.append(key)
			for key in rm_list:
				self.tick_fun.pop(key)
	
	def after_connect(self, session, params):
		Event.trigger_event(Event.AfterConnectServer, session, params)
	
	def after_disconnect(self, session, params):
		Event.trigger_event(Event.AfterConnectServer, session, params)

	def before_run(self):
		'''
		起服之前要干的活
		'''
		process_type = self.process_type

		# 先尝试从Dict拿到对应的模块
		global ProcessDict

		mod_string = ProcessDict.get(process_type)
		if mod_string is None:
			return False
		
		# 在这里载入脚本, 载入脚本的同时肯定也会注册事件
		# 这里相当于注册事件了
		ImportTool.load_script([mod_string,])
		
		# 载入脚本以后需要写入本地消息缓存
		Event.trigger_event(Event.AfterInitScript)
		return True
	
	def before_close(self):
		'''
		在关服之前
		'''
		return True


# 这里定义了有关进程相关的字典
ProcessDict = {
	'MainServer': 'GameProcess.ServerLogic',
	'GateServer': 'GameProcess.GateLogic',
	'DBServer': 'GameProcess.DBLogic'
}

def get_server():
	"""
	获得游戏服务器
	"""
	return GameServer.Instance