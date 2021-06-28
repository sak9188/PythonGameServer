# -*- coding: UTF-8 -*-
from GameEvent import Event

def after_connect_client(session, params):
	"""
	再连接客户端以后
	session: 这里代指与客户端的session
	params: 这里是客户端发送过来的参数， 用作登录判断
	这里包含了主动链接的各种进程， 需要通过参数来判断
	"""
	print(params)


Event.reg_event(Event.AfterConnectServer, after_connect_client, 0)