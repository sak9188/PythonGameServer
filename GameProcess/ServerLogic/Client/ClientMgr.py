# -*- coding: UTF-8 -*-

from Core.MgrMachine import LogicManagerBase
from GameMessage import Message

class ClientMgr(LogicManagerBase):
	
	def __init__(self):
		super().__init__()
		self.reg_msg_hadler(Message.MS_Connect, self.after_connect_client)
		self.reg_msg_hadler(Message.MS_Disconnect, self.after_disconnet_client)

	def after_connect_client(self, session_id, msg_body):
		print("after_connect_client")

	def after_disconnet_client(self, session_id, msg_body):
		print("after_disconnect_client")


ClientMgr.reg_in_server()
