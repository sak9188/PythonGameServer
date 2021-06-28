# -*- coding: UTF-8 -*-

from GameEvent import Event
from GameMessage import Message
import PyServer

def request_add_gateway(session, param):
	"""
	请求加入一个GateServer
	"""
	server = PyServer.get_server()
	server.connect_to(param, 'GateServer')

def after_lsot_process(process):
	"""
	当丢失进程链接以后
	"""
	if process.process_type != "GateServer":
		return

# 消息注册
Message.reg_msg_handler(Message.MS_AddGateWayProcess, request_add_gateway)

# 事件注册
Event.reg_event(Event.AfterLostProcess, after_lsot_process)