# -*- coding: UTF-8 -*-
from GameEvent import Event

def sql_exe_fun(fun):
	def wrapper_fun(*conns):
		try:
			fun()
		finally:
			for conn in conns:
				conn.rollback()
	return wrapper_fun


@sql_exe_fun
def create_role(*conns):
	pass


@sql_exe_fun
def save_role(*conns):
	pass