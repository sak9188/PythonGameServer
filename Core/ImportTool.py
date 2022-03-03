# -*- coding: UTF-8 -*-

import imp
from importlib.resources import contents
import os
import traceback
import sys

MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')
def package_contents(package_name, path=['.']):
	global MODULE_EXTENSIONS

	# 兼容Python3
	if package_name == "__pycache__":
		return

	if package_name.find('.') > 0:
		path_list = package_name.split('.')
		package_name = path_list[-1]
		path.extend(path_list[:-1])
	else:
		return

	try:
		file, pathname, _ = imp.find_module(package_name, path)
		if file:
			# raise ImportError('Not a package: %r', package_name)
			return
	except ImportError:
		print("Import Error PackageName %s, Path %s" % (package_name, path))
		return

	module_set = set()
	path_module_name = pathname.replace('\\', '.')
	for module in os.listdir(pathname):
		if module.endswith(MODULE_EXTENSIONS):
			if path_module_name.startswith('..'):
				path_module_name = path_module_name[2:]
			module_set.add(path_module_name+"."+os.path.splitext(module)[0])
		else:
			contents = package_contents(module, [pathname])
			if not contents:
				continue
			module_set.update(contents)
	return module_set


def load_script(module_string_list):
	'''
	这个函数只有在根目录下启动才有作用
	模块预载
		"Core",
		"GameDB",
		"GameEvent",
	'''
	must_loaded = [
		"Core",
		"GameDB",
		"GameEvent",
	]

	must_loaded += module_string_list

	module_set = set()
	print(must_loaded)
	for module in must_loaded:
		contents = package_contents(module)
		if contents:
			module_set.update(contents)
	
	for module_name in module_set:
		if module_name.endswith('__init__'):
			continue
		if sys.modules.get(module_name):
			# print "Already loaded ", module_name
			continue
		try:
			# print len(sys.modules)
			module = __import__(module_name)
		except:
			traceback.print_exc()
	
	return module_set

# 下面是一个测试函数
# load_script()