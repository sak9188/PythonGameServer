# -*- coding: UTF-8 -*-

from DataType import DBDataType
import collections


class DBColumn(object):
	__slots__ = ["name", "data_type", "nullable", "default", "auto_increment", "unique", "prikey", "comment"]

	def __init__(self, name, data_type, default=None, nullable=True, auto_increment=False, unique=False, prikey=False, comment=""):
		self.name = name
		self.data_type = data_type
		self.default = default
		self.nullable = nullable
		self.auto_increment = auto_increment
		self.unique = unique
		self.prikey = prikey
		self.comment = comment
	
	def get_construct_str(self):
		"""
		name data_type auto_increment pkey
		runoob_id [NOT NULL] [DEFAULT] 
		[INT UNSIGNED] [AUTO_INCREMENT] [UNIQUE KEY] [PRIMARY KEY]
		[COMMENT `string`]
		"""
		null_str = "NOT NULL" if not self.nullable else ""
		default_str = "DEFAULT %s" % self.default if self.default else ""

		auto_str = "AUTO_INCREMENT" if self.auto_increment else ""
		unique_str = "UNIQUE KEY" if self.unique else ""
		pkey_str = "PRIMARY KEY" if self.prikey else ""

		comm_str = "COMMENT `%s`" % self.comment if self.comment else ""

		cons_str = " `%s` %s %s " % (self.name, null_str, default_str)
		cons_str += " %s %s %s %s " % (self.data_type, auto_str, unique_str, pkey_str)
		cons_str += " %s " % (comm_str)
		return cons_str


class DBTable(object):
	"""
	默认的引擎就是InnoDB
	字符集是utf-8
	"""
	def __init__(self, name, covered, increment_step=1):
		self.name = name
		self.covered = covered
		self.prikey = None
		self.table_data = collections.OrderedDict()
		
	def add_col(self, value):
		if isinstance(value, DBColumn):
			if value.prikey:
				if self.prikey:
					print("EXC 存在多个主键")
				else:
					self.prikey = value
			self.table_data[value.name] = value

	def get_construct_str(self):
		"""
		CREATE TABLE IF NOT EXISTS runoob_tbl(
			runoob_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
			runoob_title VARCHAR(100) NOT NULL,
			runoob_author VARCHAR(40) NOT NULL,
			submission_date DATE
		)ENGINE=InnoDB DEFAULT CHARSET=utf8;
		"""
		create_head = "CREATE TABLE IF NOT EXISTS `%s`(" % self.name
		create_tail = ")ENGINE=InnoDB DEFAULT CHARSET=utf8;"

		create_body = ""
		for val in self.table_data.values():
			create_body += val.get_construct_str() + ',\n'

		create_str = create_head + '\n' + create_body[:-2] + '\n' + create_tail
		return create_str

	def get_cursor(self):
		pass

	def construct(self):
		cons_str = self.get_construct_str()
		db_cur = self.get_cursor()
		db_cur.execute(cons_str)


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


def test():
	table = DBTable("testTable", False)
	table.add_col(DBColumn("id", DBDataType.INT(), auto_increment=True, prikey=True))
	table.add_col(DBColumn("name", DBDataType.VARCHAR(100)))
	table.add_col(DBColumn("email", DBDataType.VARCHAR(32)))
	table.add_col(DBColumn("addres", DBDataType.VARCHAR(120)))
	print(table.get_construct_str())
	# print(DataType.DBDataType.TINYINT(True))
