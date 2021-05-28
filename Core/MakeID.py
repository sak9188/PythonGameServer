# -*- coding: UTF-8 -*-
import os
import cPickle as pickle

# 这里记录了所有的ID 游戏中的事件
ID_Table = {}

# 每1w个做一次分割 最大为 21亿
ID_STEP_MAX = 10000

# 这里记录了每种不一样的id顺序
ID_Name_Dict = {}

# 这里记录了所有在使用的ID
ID_InUse = set()


class IDClass(object):
	__slots__ = ["name", "value"]
	def __init__(self, name, value):
		self.name = name
		self.value = value


class AllotID(object):
	def __init__(self, start_id, fun_name):
		self.start_id = start_id * ID_STEP_MAX
		self.name = fun_name
		self.next_id = 0

	def allot_id(self, name):
		global ID_Table, ID_STEP_MAX, ID_InUse
		# 首先判断是不是已经在上次分配了id
		temp_allot_id = ID_Table.get(name)
		if temp_allot_id is not None:
			return temp_allot_id

		temp_allot_id = self.start_id + self.next_id
		ID_Table[name] = temp_allot_id
		self.next_id += 1

		# 添加使用记录
		ID_InUse.add(temp_allot_id)
		return temp_allot_id


def init_module():
	global ID_Name_Dict, ID_Table

	if not ID_Name_Dict:
		if os.path.isfile('./ID_Name.bin'):
			with open('./ID_Name.bin', "rb") as f:
				ID_Name_Dict = pickle.load(f)
		else:
			ID_Name_Dict = {}

	if not ID_Table:
		if os.path.isfile('./ID_Table.bin'):
			with open('./ID_Table.bin', "rb") as f:
				ID_Name_Dict = pickle.load(f)
		else:
			ID_Table = {}


def make_id_fun(fun_name):
	"""
	这里会根据函数的名字来确定AllotID对象
	"""
	global ID_Name_Dict
	start_id = ID_Name_Dict.get(fun_name)
	if start_id is None:
		start_id = reg_name(fun_name)
	assert start_id
	return AllotID(start_id, fun_name)


def reg_name(fun_name):
	global ID_Name_Dict
	start_id = 1

	val_list = ID_Name_Dict.values()
	if val_list:
		for val in val_list.sort(lambda x: x):
			if val == start_id:
				start_id += 1
				continue
			break

	# 这里放了命名空间
	ID_Name_Dict[fun_name] = start_id
	return start_id


def clear_trash_id():
	#TODO 载入服务器以后，可以通过这个函数来清理垃圾ID
	pass

def save_table():
	# 每次载入了所有脚本以后，就要保存的本地上
	global ID_Name_Dict, ID_Table

	with open('./ID_Name.bin', "wb") as f:
		pickle.dump(ID_Name_Dict, f)
	with open('./ID_Table.bin', "wb") as f:
		pickle.dump(ID_Table, f)

init_module()

# Event.reg_event(Event.AfterInitScript, save_table)