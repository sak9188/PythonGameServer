# -*- coding: UTF-8 -*-

from GameEvent import Event
import Setting

# 这里导入整个模块的时候，在这里就要搞骚操作了
def after_init_server(gameserver):
	'''
	这里会初始化
	'''
	# 尝试链接GateServer
	# 由于这里可能会链接失败, 所以这里要放一个延迟调用
	connect_other_process(gameserver)

def connect_other_process(gameserver):
	gameserver.connect_to(Setting.GateServer, 'GateServer')


Event.reg_event(Event.AfterInitServer, after_init_server)