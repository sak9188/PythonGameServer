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

if __name__ == '__main__':
	msg = Packer.pack_msg(1, 'tset_string')
	print Packer.unpack(msg)