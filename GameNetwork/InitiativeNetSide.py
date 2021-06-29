# -*- coding: UTF-8 -*-

# 主动链接端 (客户端)
from Core.Process import ProcessHelp
from GameEvent import Event
import asyncore
import socket
import Queue

from Core import Packer
from GameMessage import Message
import Setting

class BaseClient(asyncore.dispatcher):

	def __init__(self, con_params, reconnect, identity):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		# self.connect(con_params)
		self.connetc_params = con_params
		self.connect_success = False
		self.reconnect = reconnect
		self.is_reconnect = reconnect
		self.read_buffer = ''
		self.write_buffer = ''
		# 这里是写消息的队列
		self.message_queue = Queue.Queue()
		self.identity = identity
		# identity 是身份信息
		self.send_message(Message.MS_Connect, identity)
		self.connect(self.connetc_params)
	
	def reset_connect(self):
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.connect_success = False
		self.is_reconnect = self.reconnect
		self.read_buffer = ''
		self.write_buffer = ''
		self.message_queue.queue.clear()
		self.send_message(Message.MS_Connect, self.identity)
		self.connect(self.connetc_params)

	def handle_connect(self):
		self.connect_success = True
		# 一定要设置为False
		self.is_reconnect = False
		self.after_get_connect()

	def handle_close(self):
		if self.is_reconnect:
			self.connect(self.connetc_params)
		else:
			self.connect_success = False
			self.close()
			self.after_lost_connect()

	def handle_read(self):
		recvs = self.recv(8192)
		if not recvs:
			return
		self.read_buffer += recvs

	def writable(self):
		if not self.message_queue.empty():
			self.write_buffer = self.message_queue.get()
		if self.write_buffer == '':
			return False
		return len(self.write_buffer) > 0
	
	def handle_write(self):
		sent = self.send(self.write_buffer)
		self.write_buffer = self.write_buffer[sent:]

	def send_message(self, msg_id, msg_body):
		self.message_queue.put(Packer.pack_msg(msg_id, msg_body))
	
	def after_lost_connect(serf):
		"""
		失去链接以后
		"""
		print('Lost Connection')


	def after_get_connect(self):
		"""
		获得链接以后
		"""
		print('Connecting Success')


class ProcessClient(BaseClient):
	def __init__(self, con_params, process_type, reconnect=False):
		# TODO 这里可能需要进程id, 进程id在数据库里, 后面再看吧
		identity = {'process_type': Setting.ProcessType,
		 			'os': ProcessHelp.get_process_os_string(),
		 			'is_master': Setting.IsMaster}
		BaseClient.__init__(self, con_params, reconnect, identity)
		self.process_type = process_type
		# 这里的Master指代Gateway中的管理进程
		self.is_master = False
	
	def set_master(self, b):
		self.is_master = b

	def after_lost_connect(self):
		# 如果是主进程挂了， 则要主动去链接主进程
		if self.is_master:
			self.reset_connect()
		Event.trigger_event(Event.AfterLostProcess, self)
