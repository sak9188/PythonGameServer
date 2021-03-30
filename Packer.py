# -*- coding: UTF-8 -*-

import struct
import cPickle as pickle
from hashlib import md5

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
	hash_sum = md5(dumps_bytes).digest()
	msg = struct.pack("IH%ds16s" % len_bytes, len_bytes, msg_type, dumps_bytes, hash_sum)
	return msg


def unpack(msg):
	msg_size = get_pack_size(msg[:4])
	msg_id = get_pack_msg_id(msg[4:6])
	msg_body_bytes = msg[6:msg_size+6]
	msg_body = pickle.loads(msg[6:msg_size+6])
	msg_hash = msg[msg_size+6:]
	if md5(msg_body_bytes).digest() != msg_hash:
		print("unpack msg error happend!")
		return None, None
	return msg_id, msg_body


def get_pack_size(size_bytes):
	assert len(size_bytes) == 4
	return struct.unpack("I", size_bytes)[0]


def get_pack_msg_id(size_bytes):
	assert len(size_bytes) == 2
	return struct.unpack("H", size_bytes)[0]