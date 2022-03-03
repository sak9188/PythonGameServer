# -*- coding: UTF-8 -*-

from GameEvent import Event
from Core import MakeID
import Setting

# ===========================================
# 这里导入整个模块的时候，在这里就要搞骚操作了
# ===========================================


def after_init_server(gameserver):
	'''
	这里会初始化
	'''
	# 尝试链接GateServer
	# 由于这里可能会链接失败, 所以这里要放一个延迟调用
	connect_other_process(gameserver)


def connect_other_process(gameserver):
	# 这里相当于一个主GateServer， 主要做负载均衡
	gameserver.connect_to(Setting.GateServer, 'GateServer')


def after_load_scripts():
	# 只有MainServer才可以保存ID
	MakeID.clear_trash_id()
	MakeID.save_table()


# 事件
Event.reg_g_event(Event.AfterInitServer, after_init_server)
Event.reg_g_event(Event.AfterInitScript, after_load_scripts)