# -*- coding: UTF-8 -*-
from GameEvent import Event
from GameEvent.EventHandler import EventHandlerBase
from GameNetwork.MessageHandler import MessageHandlerBase

import PyServer 


class LogicManagerBase(MessageHandlerBase, EventHandlerBase):

	def __init__(self):
		super().__init__()

	@classmethod
	def reg_in_server(cls, ord=1000):
		server = PyServer.get_server()
		server.reg_mgr(cls)

	def after_init_world(self):
		pass

	def after_init_db(self):
		pass

	def after_new_second(self):
		pass

	def after_new_hour(self):
		pass

	def after_new_day(self):
		pass