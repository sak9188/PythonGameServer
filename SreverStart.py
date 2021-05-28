# -*- coding: UTF-8 -*-
import time
import PyServer

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
	GS = PyServer.GameServer('localhost', 9090)
	message_loop(GS)	
	# while True:
	# 	pre_time = time.time()
	# 	gs.handle_message()
	# 	after_time = time.time()
	# 	if after_time - pre_time > 0.017:
	# 		# 这里说明已经处理了一帧了