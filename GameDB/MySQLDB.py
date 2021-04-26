# -*- coding: UTF-8 -*-

from DataType import DBDataType
import DBCore
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

	def construct(self):
		cons_str = self.get_construct_str()
		db_cur = self.get_cursor()
		db_cur.execute(cons_str)


class DBConnect(object):
	def __init__(self, database, conn, is_using=True):
		self.database = database
		self.conn = conn
		self.is_using = is_using
	
	def set_use(self):
		self.is_using = True

	def create_table(self, dbtable):
		if not isinstance(dbtable, DBTable):
			raise TypeError("EXC not a instance of DBTable")
		cur = self.conn.cursor()
		cur.execute(dbtable.get_construct_str())
	
	def return_back_connect(self):
		self.is_using = False
		self.database.return_back(self)

	def execute(self, exe_fun):
		# TODO 这里可能要修改一下
		try:
			exe_fun(self)
			self.conn.commit()
		finally:
			self.conn.rollback()


class DataBase(object):
	def __init__(self, host, port, user, passwd, db_name, charset="utf8", conn_max_num=10):
		self.host = host
		self.port = port
		self.user = user
		self.passwd = passwd
		self.db_name = db_name
		self.charset = charset
		self.conn_max_num = conn_max_num
		self.conn_deque = collections.deque(maxlen=conn_max_num)
		self.using_conn = set()

	def get_connect(self):
		if len(self.conn_deque) > 0:
			conn = self.conn_deque.pop()
			self.using_conn.add(conn)
			return conn
		if len(self.using_conn) >= self.conn_max_num:
			return None
		conn = DBCore.create_connet(self.host, self.port, self.user, self.passwd, self.db_name, self.charset)
		self.using_conn.add(conn)
		return conn

	def return_back(self, conn):
		self.using_conn.remove(conn)
		self.conn_deque.append(conn)


def test():
	table = DBTable("testTable", False)
	table.add_col(DBColumn("id", DBDataType.INT(), auto_increment=True, prikey=True))
	table.add_col(DBColumn("name", DBDataType.VARCHAR(100)))
	table.add_col(DBColumn("email", DBDataType.VARCHAR(32)))
	table.add_col(DBColumn("addres", DBDataType.VARCHAR(120)))
	print(table.get_construct_str())