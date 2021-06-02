# -*- coding: UTF-8 -*-

# 被动链接端 (服务端)
from GameEvent import Event
import asyncore
import socket
import Queue

from GameMessage import Message
from Core import Constant, GameTime, Packer
from GameNetwork import InitiativeNetSide


class NetServer:
	'''
	这个类定义了网络服务器的基本接口
	'''
	def __init__(self):
		self.id = 0
		self.read_buffer = ''

	def clear_buffer(self):
		self.read_buffer = ''
	
	def can_get_msg(self):
		if len(self.read_buffer) <= Constant.get_size_msg_head():
			return False
		msg_size = Packer.get_pack_size(self.read_buffer[:Constant.MessageHead]) # 这里已经包括了头大小
		return len(self.read_buffer) >= msg_size

	def get_msg(self):
		# 先拿前4个字节
		if not self.can_get_msg():
			return None
		msg_size = Packer.get_pack_size(self.read_buffer[:Constant.MessageHead]) # 这里已经包括了头大小
		msg = self.read_buffer[:msg_size]
		print('len of msg is %d' % len(msg))
		self.read_buffer = self.read_buffer[msg_size:]
		return msg


class NetSession(asyncore.dispatcher_with_send, NetServer):
	'''
	这里定义了服务端链接客户端的Session
	'''
	def __init__(self, server, sock, addr, session_id):
		asyncore.dispatcher_with_send.__init__(self, sock)
		NetServer.__init__(self)
		self.server = server
		self.addr = addr
		self.id = session_id

	def handle_read(self):
		'''
		这里是将信息写入服务器
		'''
		data = self.recv(4096)
		if data:
			self.read_buffer += data
		message = self.get_msg()
		self.add_message_to_server(message)

	def handle_close(self):
		# 如果已经断开链接了的话
		if not self.connected:
			return
		Event.trigger_event(Event.BeforeLostClient, self)
		# 打包要退出的消息
		message = Packer.pack_msg(Message.MS_Disconnection, self.id)
		# 打包到消息内循环
		self.add_message_to_server(message)
		self.clear_buffer()
		self.close()
	
	def send(self, msg_id, msg_body):
		msg = Packer.pack_msg(msg_id, msg_body)
		# 调用父方法
		asyncore.dispatcher_with_send.send(self, msg)
	
	def add_message_to_server(self, message):
		if message:
			self.server.add_message((self.id, message))


class BaseSever(asyncore.dispatcher, NetServer):
	'''
	基础的服务器
	'''
	def __init__(self, connect_params):
		asyncore.dispatcher.__init__(self)
		NetServer.__init__(self)
		# 这里是创建链接，被动链接
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(connect_params)
		print 'connect_params', connect_params
		self.listen(32)
		# 这里是主动链接字典
		self.initive_connects = {}
		# 被动链接字典
		self.passive_connects = {}
		# 是否在运行
		self.is_run = False
		# 当前时间
		self.server_time = GameTime.GameTime()
		# 给每个链接分配的唯一ID
		# 每个进程只有一个BaseServer，所以就不考虑id重复的问题了
		self.start_sesssion_id = 0
		self.reuse_ids = set()
		# 消息队列
		self.messages = Queue.Queue()

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			print('Incoming connection from %s' % repr(addr))
			session = NetSession(self, sock, addr, self.get_session_id())
			self.add_session(session)
	
	def handle_message(self):
		if self.messages.empty():
			return
		with self.server_time:
			session_id, msg = self.messages.get()
			msg_id, msg_body = Packer.unpack(msg)
			session = self.get_session(session_id)
			if msg_id is None:
				# 如果此时解包消息出现了问题就断开链接
				self.close_session(session)
				return
			if session and not session.connected:
				# 如果链接断开了的话
				self.close_session(session)
				session = None
			# 处理消息的格式 msg_id, session, msg_body
			Message.handle_reg_msg(msg_id, session, msg_body)
	
	def get_session_id(self):
		if len(self.reuse_ids) > 0:
			return self.reuse_ids.pop()
		self.start_sesssion_id += 1
		return self.start_sesssion_id
	
	def add_session(self, session):
		# 这里要额外判断一下是不是重复了
		if self.passive_connects.get(session.id):
			print('Replicated connection addr:%s' % session.addr)
		self.passive_connects[session.id] = session
	
	def get_session(self, session_id):
		session = self.passive_connects.get(session_id)
		return session

	def remove_session(self, session_id):
		self.passive_connects.pop(session_id)
	
	def close_session(self, session):
		self.remove_session(session.id)
		session.handle_close()
		self.reuse_ids.add(session.id)
		del session
	
	def add_message(self, message):
		self.messages.put(message)

	def connect_to(self, params, process_type):
		'''
		这里放链接参数，主要是控制链接到其他进程的
		'''
		try:
			process_client = InitiativeNetSide.ProcessClient(params, process_type)
		except:
			print 'Connecting to other process wrong'
			return False

		# TODO 这里肯定要改的， 因为这样就是1对1的关系了，如果后期网关进程多了起来这里是不好搞的
		# 但是先搭个地基
		self.initive_connects[process_type] = process_client
		return True