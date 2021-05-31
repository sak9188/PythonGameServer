# -*- coding: UTF-8 -*-

import imp
import os
import traceback


MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')
def package_contents(package_name, path=['.']):
	global MODULE_EXTENSIONS

	if package_name.find('.') >= 0:
		path_list = package_name.split('.')
		package_name = path_list[-1]
		path.extend(path_list[:-1])

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


def load_script():
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
		"GameProcess.ServerLogic"
	]

	module_set = set()
	for module in must_loaded:
		module_set.update(package_contents(module))
	
	for module_name in module_set:
		try:
			__import__(module_name)
		except:
			traceback.print_exc()
	
	return module_set

load_script()