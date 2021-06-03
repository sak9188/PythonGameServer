# -*- coding: UTF-8 -*-

from GameMessage import Message
from Core import Packer
import asyncore, socket
import threading
import time
import sys
import Setting

MESSAGES = []

class ClientInput(threading.Thread):
	

	def __init__(self):
		threading.Thread.__init__(self)
		self.is_inputing = False
		self.stop = False
	
	def run(self):
		while not self.stop:
			self.is_inputing = True
			line = raw_input(">>> ")
			self.is_inputing = False
			MESSAGES.append(line)
			time.sleep(0.01)


INPUT = ClientInput()
INPUT.daemon = True
INPUT.start()


class GameClient(asyncore.dispatcher):

	def __init__(self, con_params):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connetc_params = con_params
		self.set_reuse_addr()
		self.connect(con_params)
		self.buffer = Packer.pack_msg(Message.MS_Connect, 1)

	def handle_connect(self):
		print("connection is success")

	def handle_close(self):
		self.close()

	def handle_read(self):
		if not INPUT.is_inputing:
			recvs = self.recv(8192)
			if not recvs:
				return
			print("server:"+recvs)

	def writable(self):
		if self.buffer == '' and MESSAGES:
			self.buffer = MESSAGES.pop(0)
		return len(self.buffer) > 0
	
	def handle_write(self):
		sent = self.send(self.buffer)
		self.buffer = self.buffer[sent:]
	
	def handle_close(self):
		INPUT.stop = True
		print("Client Socket is closing")
		self.close()
		sys.exit()
	

client = GameClient(Setting.MainServer)
asyncore.loop(timeout=0.001)

