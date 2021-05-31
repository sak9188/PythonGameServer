# -*- coding: UTF-8 -*-
import time
import uuid
import threading

# 每秒生成多少个
PER_SEC_GEN = 1024
# 最大存储量 10w 大概4M左右
MAX_BUFFER_UUID = 100000
# 这里存储着备用的uuid
GUID_BUFFER = []

GUIDLock = threading.Lock()

def _gen_uuid():
	'''
	生成uuid
	'''
	if len(GUID_BUFFER) > MAX_BUFFER_UUID:
		return
	for x in xrange(PER_SEC_GEN):
		uid = uuid.uuid1()
		GUID_BUFFER.append(uid)

def get_uuid():
	'''
	获得uuid
	'''
	with GUIDLock:
		if len(GUID_BUFFER) <= 0:
			# 要是不够了就生成一下
			_gen_uuid()
		return GUID_BUFFER.pop(0)

def _run():
	while True:
		_gen_uuid()
		time.sleep(1)


thread_obj = None
def start():
	thread_obj = threading.Thread(target=_run)
	thread_obj.setDaemon(True)
	thread_obj.start()