# -*- coding: UTF-8 -*-

# 进程Session的封装类

class ProcessSession:

	def __init__(self, session, info_dict):
		# 记录了当前的session
		self.session = session
		# 这里是子进程集合，主要管理子进程
		self.child_processes = []
		self.info_dict = info_dict
		self.type = info_dict.get("process_type")
		self.master = info_dict.get("is_master")
	
	def get_type(self):
		# 获得进程类型
		return self.type

	def is_master(self):
		# 是否是主进程
		return self.master

	def kick_process(self):
		# 踢掉链接的线程
		pass

	def send_msg(self, msg_id, msg_body):
		# 给链接的线程发送消息
		pass

