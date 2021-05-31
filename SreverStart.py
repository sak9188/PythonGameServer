# -*- coding: UTF-8 -*-
import time
import PyServer
import Setting

# 主线程处理消息
# 网络线程主要负责收集消息
def message_loop(GameServer):
	while True:
		# 休息1毫秒
		time.sleep(0.001)
		GameServer.handle_message()
		GameServer.update_time()


if __name__ is "__main__":
	# 生成一个服务器
	GS = PyServer.GameServer(Setting.MainServer)
	message_loop(GS)