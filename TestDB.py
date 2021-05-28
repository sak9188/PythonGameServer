# -*- coding: UTF-8 -*-

# from GameDB import MySQLDB

# MySQLDB.test()

from GameEvent import Event
from GameMessage import Message
from Core import MakeID


print(Event.AfterInitScript)
print(Event.AfterInitServer)

print(Message.MS_HeartBeat)
print(Message.MS_Connect)
print(Message.MS_Disconnection)

MakeID.save_table()