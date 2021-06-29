# -*- coding: UTF-8 -*-
from GameEvent import Event
from GameProcess.GateLogic.Process import ProcessMgr
import Setting

def after_connect_client(session, params):
	"""
	再连接客户端以后
	session: 这里代指与客户端的session
	params: 这里是客户端发送过来的参数， 用作登录判断
	这里包含了主动链接的各种进程， 需要通过参数来判断
	"""
	info_dict = params
	ptype = info_dict.get('process_type')
	if not ptype:
		# 说明这个东西是一个客户端
		# TODO 这里可能需要一个login的判断
		# 得通知对应的服务端有角色进来了
		# 这里的判断可能更为复杂，比如说多角色登录
		# 需要注意的是，这里的服务端指主服务器
		pro = ProcessMgr.get_process(Setting.sMainServer)
		# TODO 暂时一个客户端对应一个角色，后面可能需要加入账号的处理
		# pro.send_msg()
		# 同时得保存对应的
	else:
		# 说明这个东西是一个服务端的链接进程
		# 此时可能需要将这个Session包装成一个对应的进程对象
		ProcessMgr.add_process(session, info_dict)
	print(params)


Event.reg_event(Event.AfterConnectServer, after_connect_client, 0)