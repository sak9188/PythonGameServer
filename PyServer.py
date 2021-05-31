# -*- coding: UTF-8 -*-
import threading
import asyncore
import time
import socket
from Core.Extent.sortedcontainers import SortedDict
from Core import GameTime
from Core import Packer
from GameMessage import Message
from Core import Constant

# 不知道这个锁有没有可能会被用到
# ServerLock = threading.Lock()

class NetServer(object):
	def __init__(self):
		self.id = 0
		self.read_buffer = ''
		self.write_buffer = ''
		self.messages = []

	def clear_buffer(self):
		self.read_buffer = ''
	
	def can_get_msg(self):
		if len(self.read_buffer) <= Constant.get_size_msg_head():
			return False
		msg_body_size = Packer.get_pack_size(self.read_buffer[:4])
		msg_size = Constant.get_size_msg_head()+msg_body_size # 这里已经包括了头大小
		return len(self.read_buffer) >= msg_size

	def get_msg(self):
		# 先拿前4个字节
		if not self.can_get_msg():
			return
		msg_body_size = Packer.get_pack_size(self.read_buffer[:4])
		msg_size = Constant.get_size_msg_head()+msg_body_size # 这里已经包括了头大小
		msg = self.read_buffer[:msg_size]
		self.read_buffer = self.read_buffer[msg_size:]
		self.messages.append((self.id, msg))


class Session(asyncore.dispatcher_with_send, NetServer):
	def __init__(self, messages, sock, addr, session_id):
		asyncore.dispatcher_with_send.__init__(self, sock)
		NetServer.__init__(self)
		self.messages = messages
		self.addr = addr
		self.id = session_id

	def handle_read(self):
		data = self.recv(8192)
		if data:
			self.read_buffer += data
		self.get_msg()

	def handle_close(self):
		self.clear_buffer()
		# 打包要退出的消息
		msg = Packer.pack_msg(Message.MS_Disconnection, self.id)
		self.messages.append((self.id, msg))
		self.messages = []
		self.id = 0
		self.clear_buffer()
		self.close()


class GameServer(asyncore.dispatcher, NetServer):
	Instance = None

	def __init__(self, connect_params, process_type):
		if GameServer.Instance is not None:
			return
		asyncore.dispatcher.__init__(self)
		NetServer.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(connect_params)
		self.listen(32)
		self.start_sesssion_id = int(str(int(time.time()))[-3:])*10000
		self.reuse_ids = []
		self.connects = {}
		self.process_type = process_type
		# 会话id，用来标识sock
		self.id = self.get_session_id()
		# 当前时间
		self.server_time = GameTime.GameTime()
		# 注册时延的dict
		self.tick_fun = SortedDict()
		# 线程相关
		self.thread = threading.Thread(target=self.run)
		self.thread.start()
		GameServer.Instance = self

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			print('Incoming connection from %s' % repr(addr))
			session = Session(self.messages, sock, addr, self.get_session_id())
			self.add_session(session)
	
	def handle_message(self):
		if len(self.messages) <= 0:
			return
		# with ServerLock:
		with self.server_time:
			sid, msg = self.messages.pop(0)
			msg_id, msg_body = Packer.unpack(msg)
			# 这里要排除掉自己
			if msg_id is None and sid != self.id:
				# 如果此时解包消息出现了问题就断开链接
				con = self.connects.get(sid)
				reuse_id = con.handle_close()
				self.remove_session(reuse_id)
				self.reuse_ids.append(reuse_id)
				return
			# TODO 这里要单独分到一个独立的模块里
			self.handle_reg_msg(msg_id, *msg_body)
	
	def run(self):
		# 注册消息
		Message.reg_msg_handler(Message.MS_Disconnection, self.close_session)
		Message.reg_msg_handler(Message.MS_Connect, self.after_connect)
		# 主消息循环
		asyncore.loop(timeout=0.01)

	def get_session_id(self):
		if len(self.reuse_ids) > 0:
			return self.reuse_ids.pop()
		self.start_sesssion_id += 1
		return self.start_sesssion_id

	def add_session(self, session):
		self.connects[session.id] = session
	
	def remove_session(self, session_id):
		self.connects[session_id] = None
	
	def close_session(self, sid):
		self.remove_session(sid)
		self.reuse_ids.append(sid)
	
	def reg_tick(self, fun, args, secs):
		# 支持小数，也就是支持毫秒
		des_time = self.time_stamp + secs
		fun_list = self.tick_fun.get(des_time)
		if not fun_list:
			self.tick_fun[secs] = [(fun, args),]
		else:
			fun_list.append((fun, args))
	
	def seconds(self):
		return int(self.server_time())

	def minutes(self):
		# TODO 由上面的演化来
		pass

	def hours(self):
		# TODO 由上面的演化来
		pass

	def days(self):
		# TODO 由上面的演化来
		pass

	def update_time(self):
		# 获得当前的时间, 触发当前时间Tick
		# 如果服务器时间慢于服务器时间， 则会自动加速至现实时间
		now_time = self.server_time.sync_real_time()
		with self.server_time:
			rm_list = []
			for key, val in self.tick_fun.items():
				if key > now_time:
					break
				for fun, arg in val:
					fun(*arg)
				self.tick_fun[key] = None
				rm_list.append(key)
			for key in rm_list:
				self.tick_fun.pop(key)
	
	def after_connect(self, p):
		print("after_connect", p)


import Core.ImportTool