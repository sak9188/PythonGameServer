# -*- coding: UTF-8 -*-

# from GameDB import MySQLDB

# MySQLDB.test()

from GameEvent import Event
from Core import MakeID

print(Event.AfterInitScript)
print(Event.AfterInitServer)
MakeID.save_table()