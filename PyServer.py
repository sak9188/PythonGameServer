# -*- coding: UTF-8 -*-
import threading
import asyncore
import time
import socket
from Core.Extent.sortedcontainers import SortedDict
from Core import GameTime
from Core import Packer
from GameMessage import Message
import imp
import os
import traceback

ServerLock = threading.Lock()

class NetServer(object):
	def __init__(self):
		self.id = 0
		self.read_buffer = ''
		self.write_buffer = ''
		self.messages = []

	def clear_buffer(self):
		self.read_buffer = ''
	
	def get_head_size(self):
		return 4+2+16 #除去body以外所有的字节
	
	def can_get_msg(self):
		if len(self.read_buffer) <= self.get_head_size():
			return False
		msg_body_size = Packer.get_pack_size(self.read_buffer[:4])
		msg_size = self.get_head_size()+msg_body_size # 这里已经包括了头大小
		return len(self.read_buffer) >= msg_size

	def get_msg(self):
		# 先拿前4个字节
		if not self.can_get_msg():
			return
		msg_body_size = Packer.get_pack_size(self.read_buffer[:4])
		msg_size = self.get_head_size()+msg_body_size # 这里已经包括了头大小
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

	def __init__(self, host, port):
		if GameServer.Instance is not None:
			return
		asyncore.dispatcher.__init__(self)
		NetServer.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(32)
		self.start_sesssion_id = int(str(int(time.time()))[-3:])*10000
		self.reuse_ids = []
		self.connects = {}
		self.message_handler = {}
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
			self.handle_reg_msg(msg_id, *msg_body)
	
	def run(self):
		# 注册消息
		self.reg_msg_handler(Message.MS_Disconnection, self.close_session)
		self.reg_msg_handler(Message.MS_Connect, self.after_connect)
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

	def reg_msg_handler(self, msg_id, fun):
		"注册消息函数"
		reg_fun = self.message_handler.get(msg_id)
		if reg_fun:
			print("already has function id%d" % msg_id)
		self.message_handler[msg_id] = fun

	def handle_reg_msg(self, msg_id, *args):
		"处理注册的消息"
		fun = self.message_handler.get(msg_id)
		if not fun:
			print("there is no fun with msg_id is %d" % msg_id)
			return
		fun(*args)
	
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


MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')
def package_contents(package_name, path=['.']):
	global MODULE_EXTENSIONS

	file, pathname, _ = imp.find_module(package_name, path)
	if file:
		# raise ImportError('Not a package: %r', package_name)
		return

	module_set = set()
	path_module_name = pathname.replace('\\', '.')[2:]
	for module in os.listdir(pathname):
		if module.endswith(MODULE_EXTENSIONS):
			module_set.add(path_module_name+"."+os.path.splitext(module)[0])
		else:
			contents = package_contents(module, [pathname])
			if not contents:
				continue
			module_set.update(contents)
	return module_set


def load_script():
	server = GameServer.Instance
	# 模块预载
	# Core下所有模块
	# GameDB下所有模块
	# GameEvent下所有模块
	must_loaded = [
		"Core",
		"GameDB",
		"GameEvent"
	]

	module_set = set()
	for module in must_loaded:
		module_set.update(package_contents(module))

	for module_name in module_set:
		try:
			__import__(module_name)
		except:
			traceback.print_exc()
	
	return module_set

# print load_script()

load_script()