# -*- coding: UTF-8 -*-
import os
import cPickle as pickle

# 这里记录了所有的ID
ID_Table = {}

# 每1w个做一次分割 最大为 21亿
ID_STEP_MAX = 10000

# 这里记录了每种不一样的id顺序
ID_Name_Dict = {}

# 这里记录了所有在使用的ID
ID_InUse = set()

# 这里记录了真实使用的ID
ID_RealUse = set()


class IDClass(object):
	__slots__ = ["name", "value"]
	def __init__(self, name, value):
		self.name = name
		self.value = value

class IDCollection:
	def __init__(self):
		self.start_id = None
		self.id_set = set()
	
	def add_id(self, id):
		if id in self.id_set:
			pass


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
			# 添加真正使用的记录

			ID_RealUse.add(temp_allot_id)
			return temp_allot_id

		# 这里要判断是否已经超出极限了，因为每一个AllotID最多分配1w个
		if self.next_id == ID_STEP_MAX:
			print('already allotted to max value')
			return

		# 这里有一个问题, 那就是你不知道next_id是不是对的
		# 因为有可能 1 3 4有分配, 但是2并没有分配
		temp_allot_id = self.start_id + self.next_id

		# 所以要在这里尝试引用一个机制
		while temp_allot_id in ID_InUse:
			# 尝试在这里找到一个没有用过的id
			self.next_id += 1
			temp_allot_id = self.start_id + self.next_id

		ID_Table[name] = temp_allot_id
		self.next_id += 1

		# 添加使用记录
		ID_InUse.add(temp_allot_id)

		# 添加真正使用的记录
		ID_RealUse.add(temp_allot_id)
		return temp_allot_id


def init_module():
	global ID_Name_Dict, ID_Table, ID_InUse

	if not ID_Name_Dict:
		if os.path.isfile('./ID_Name.bin'):
			with open('./ID_Name.bin', "rb") as f:
				ID_Name_Dict = pickle.load(f)
		else:
			ID_Name_Dict = {}

	if not ID_Table:
		if os.path.isfile('./ID_Table.bin'):
			with open('./ID_Table.bin', "rb") as f:
				ID_Table = pickle.load(f)
		else:
			ID_Table = {}
	
	# 在这里载入所有的已经分配的int集合
	clear_set = {}
	for key, int_val in ID_Table.iteritems():
		if int_val in ID_InUse:
			print("replicated key % s" % key)
			# 这里要清理垃圾集合
			clear_set.add(key)
			continue
		ID_InUse.add(int_val)
	
	for key in clear_set:
		ID_Table.pop(key)


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
		val_list.sort(key=lambda x: x)
		for val in val_list:
			if val == start_id:
				start_id += 1
				continue
			break

	# 这里放了命名空间
	ID_Name_Dict[fun_name] = start_id
	return start_id


def clear_trash_id():
	'''
	清理垃圾ID，当使用者改变对应ID的名字的时候，原先记录在磁盘上的记录就会变成垃圾ID
	所以必须得清理一下，当使用者改变名字以后还可以把原来的给清理掉
	'''
	global ID_RealUse, ID_Table
	# 这里应该是一样的
	if len(ID_RealUse) == len(ID_Table):
		return

	# 如果不一样
	trash_set = set()
	for key, val in ID_Table.iteritems():
		if not val in ID_RealUse:
			trash_set.add(key)
	
	# 扔掉所有的垃圾ID
	for key in trash_set:
		ID_Table.pop(key)


def save_table():
	# 每次载入了所有脚本以后，就要保存的本地上
	global ID_Name_Dict, ID_Table

	with open('./ID_Name.bin', "wb") as f:
		pickle.dump(ID_Name_Dict, f)
	with open('./ID_Table.bin', "wb") as f:
		pickle.dump(ID_Table, f)

init_module()