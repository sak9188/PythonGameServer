# -*- coding: UTF-8 -*-

# 数据库管理模块
import abc

class GameDB(object):

    @abc.abstractmethod
    def create_db(name):
        pass

class MySQLDB(GameDB):

    def create_db(name):
        pass
    pass

class RedisDB(GameDB):
    pass
