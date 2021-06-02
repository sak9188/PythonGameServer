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
	connect_other_process(gameserver, Setting.GateServer, 'GateServer')

def connect_other_process(gameserver, *connect_params):
	if not gameserver.connect_to(*connect_params):
		gameserver.reg_tick(connect_other_process, (gameserver, connect_params), 0.1)

Event.reg_event(Event.AfterInitServer, after_init_server)