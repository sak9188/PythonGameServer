# -*- coding: UTF-8 -*-
import PyServer


class MessageHandlerBase(object):
	
	def __init__(self):
		self._msg_handler_dict = {}
		server = PyServer.get_server()
		server.add_handler(self)

	def reg_msg_hadler(self, msg_id, fun):
		reg_fun = self._msg_handler_dict.get(msg_id)
		if reg_fun:
			print("already has reged function id%d" % msg_id)
		self._msg_handler_dict[msg_id] = fun

	def handle_msg(self, msg_id, session, *params):
		fun = self._msg_handler_dict.get(msg_id)
		if not fun:
			return
		fun(session, *params)
