# -*- coding: UTF-8 -*-

from GameEvent import Event
from GameMessage import Message
import PyServer

from Core.MgrMachine import LogicManagerBase
from GameMessage import Message

class GatewayMgr(LogicManagerBase):
	
	def __init__(self):
		super().__init__()
		# 处理消息
		self.reg_msg_hadler(Message.MS_Connect, self.after_connect_client)
		self.reg_msg_hadler(Message.MS_Disconnect, self.after_disconnet_client)
		self.reg_msg_hadler(Message.MS_AddGateWayProcess, self.request_add_gateway)

	def after_init_world(self):
		print("after_init_world--- GatewayMgr!!")

	def after_connect_client(self, session_id, param):
		print("after_connect_client")

	def after_disconnet_client(self, session_id, param):
		print("after_disconnect_client")

	def request_add_gateway(self, session_id, param):
		"""
		请求加入一个GateServer
		"""
		server = PyServer.get_server()
		server.connect_to(param, 'GateServer', self.after_lost_process)

	def after_lost_process(self, process):
		"""
		当丢失进程链接以后
		"""
		print('lost process')
		if process.process_type != "GateServer":
			return


GatewayMgr.reg_in_server()