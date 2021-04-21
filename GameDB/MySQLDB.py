# -*- coding: UTF-8 -*-

from typing import Tuple


class DBColumn():
	__slots__ = ["name", "data_type", "nullable", "auto_increment", "prikey"]

	def __init__(self, name, data_type, nullable=True, auto_increment=True, prikey=True):
		self.name = name
		self.data_type = data_type
		self.nullable = nullable
		self.auto_increment = auto_increment
		self.prikey = prikey
	
	def get_construct_str(self):
		null_str = "NOT NULL" if not self.nullable else ""
		auto_str = "AUTO_INCREMENT" if not self.auto_increment else ""
		cons_str = "'%s' %s %s %s" % (self.name, self.data_type, null_str, auto_str)
		return cons_str


class DBTable(object):
	"""
	默认的引擎就是InnoDB
	字符集是utf-8
	"""
	def __init__(self, name, covered):
		self.name = name
		self.covered = covered
		self.prikey = None
		self.table_data = {}

	def __setattr__(self, name, value):
		if isinstance(value, DBColumn):
			if value.prikey:
				if self.prikey:
					print("EXC 存在多个主键")
				else:
					self.prikey = value
			self.table_data[name] = value
		else:
			object.__setattr__(self, name, value)

	def get_construct_str(self):
		create_head = "CREATE TABLE IF NOT EXISTS `runoob_tbl`("
		create_tail = ")ENGINE=InnoDB DEFAULT CHARSET=utf8;"

		create_body = ""
		for val in self.table_data.iteritems():
			create_body += val.get_construct_str() + ',\n'

		create_str = create_head + create_body + create_tail

		return create_str

	def construct(self):
		cons_str = self.get_construct_str()
		
		pass


class DBConnect(object):

    def create_table(name, covered=False):
        pass


class MySQLDB(object):

    def __init__(self, name):
        pass

    def get_connect():
        pass

    def get_cursor():
        pass
