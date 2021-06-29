# -*- coding: UTF-8 -*-
import time
import PyServer
import Setting
import sys, getopt

# 主线程处理消息
# 网络线程主要负责收集消息
def message_loop(GameServer):
	while GameServer.is_run:
		# 休息1毫秒
		time.sleep(0.001)
		GameServer.handle_message()
		GameServer.update_time()


if __name__ == "__main__":
	# 生成一个服务器
	try:
		opts, args = getopt.getopt(sys.argv[1:],"p:")
	except getopt.GetoptError:
		sys.exit(2)
	
	GS = None
	for opt, arg in opts:
		if opt == "-p":
			if arg == Setting.sMainServer:
				GS = PyServer.GameServer(Setting.MainServer, arg)
			elif arg == Setting.sGateServer:
				GS = PyServer.GameServer(Setting.GateServer, arg)
			# 要先判断是否是主进程， 然后在判断是不是子进程
			elif arg.startswith(Setting.sGateServer):
				GS = PyServer.GameServer(Setting.GateServer, arg, False)
	if GS:
		message_loop(GS)
	