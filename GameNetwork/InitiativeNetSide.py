# -*- coding: UTF-8 -*-

# 主动链接端 (客户端)
import asyncore
import socket
import Queue

from Core import Packer
from GameMessage import Message


class BaseClient(asyncore.dispatcher):

	def __init__(self, con_params):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.connect(con_params)
		self.connetc_params = con_params
		self.connect_success = False
		self.read_buffer = ''
		self.write_buffer = ''
		# 这里是写消息的队列
		self.message_queue = Queue.Queue()
		# TODO 这里的1要替换成链接的身份信息
		self.send_message(Message.MS_Connect, 1)

	def handle_connect(self):
		self.connect_success = True
		print 'Connecting Success'

	def handle_close(self):
		self.connect_success = False
		self.close()

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


class ProcessClient(BaseClient):

	def __init__(self, con_params, process_type):
		BaseClient.__init__(self, con_params)
		self.process_type = process_type