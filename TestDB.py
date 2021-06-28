# -*- coding: UTF-8 -*-

# from GameDB import MySQLDB

# MySQLDB.test()

from GameEvent import Event
from GameMessage import Message
from Core import MakeID, Packer


# print(Event.AfterInitScript)
# print(Event.AfterInitServer)

# print(Message.MS_HeartBeat)
# print(Message.MS_Connect)
# print(Message.MS_Disconnection)

# MakeID.save_table()

from Core.Extent.sortedcontainers import SortedList

def a():
	pass

def b():
	pass

def c():
	pass

def d():
	pass

if __name__ == '__main__':
	# msg = Packer.pack_msg(1, 'tset_string')
	# print(Packer.unpack(msg))
	l = SortedList(key=lambda x: x[0])

	l.add((1, a))
	l.add((45, c))
	l.add((2, d))
	l.add((-1, b))

	print l
