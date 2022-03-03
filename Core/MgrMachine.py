# -*- coding: UTF-8 -*-
from GameEvent import Event
from GameNetwork.MessageHandler import MessageHandlerBase

import PyServer 


class LogicManagerBase(MessageHandlerBase):

	def __init__(self):
		MessageHandlerBase.__init__(self)
		self._event = Event.EventDispacther()

	@classmethod
	def reg_in_server(cls, ord=1000):
		server = PyServer.get_server()
		server.reg_mgr(cls)

	def reg_event(self, event_id, fun, ord=1000):
		self._event.reg_event(event_id, fun, ord)

	def trigger_event(self, event_id, *params, **kwargs):
		self._event.trigger_event(event_id, *params, **kwargs)

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