# -*- coding: UTF-8 -*-

import struct
import pickle
from Core import Constant
# from hashlib import md5

# TODO 这里可以用CFFI或者Cython来优化一下

MAX_PACK_BYTES = 4294967296/4/8/4 # 4个g/4/8/4 = 32M 单个打包数据量最大是128M

def pack_msg(msg_type, msg_body):
	assert type(msg_type) is int
	if type(msg_body) is not tuple:
		msg_body = (msg_body,)
	# 这里要进行序列化, 不用担心循环引用的问题，一切都已经解决
	dumps_bytes = pickle.dumps(msg_body)
	len_bytes = len(dumps_bytes)
	if len_bytes > MAX_PACK_BYTES:
		print("the size of packing msg is out of limitation")
		return
	# 注意到这里可能并不需要校验,因为TCP链接自带校验
	# hash_sum = md5(dumps_bytes).digest()
	# 注意: 这里是小端存储
	msg = struct.pack("<IQ%ds" % len_bytes, len_bytes + Constant.get_size_msg_head(), msg_type, dumps_bytes)
	return msg


def unpack(msg):
	msg_size = get_pack_size(msg[:Constant.MessageHead])
	msg_id = get_pack_msg_id(msg[Constant.MessageHead:Constant.get_size_msg_head()])
	msg_bytes = msg[Constant.get_size_msg_head():msg_size]
	msg_body = pickle.loads(msg_bytes)
	if len(msg_body) == 1:
		# 这里直接将第一个参数给取出来
		msg_body = msg_body[0]
	return msg_id, msg_body


def get_pack_size(size_bytes):
	assert len(size_bytes) == Constant.MessageHead
	return struct.unpack("I", size_bytes)[0]


def get_pack_msg_id(size_bytes):
	assert len(size_bytes) == Constant.MessageType
	return struct.unpack("Q", size_bytes)[0]


