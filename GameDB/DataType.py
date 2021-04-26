# -*- coding: UTF-8 -*-

def int_type(f):
	def get_type_str(cls, unsigned=False):
		return f.__name__ + (" UNSIGNED" if unsigned else "")
	return get_type_str

def plain_type(f):
	name = f.__name__
	def get_type_str(cls):
		return name
	return get_type_str

def str_type(f):
	name = f.__name__
	def get_type_str(cls, num):
		return name + "(%d)" % num
	return get_type_str


class DBDataType(object):
	"""
	===============================================================
	整数类型
	===============================================================
	"""
	@classmethod
	@int_type
	def TINYINT(cls, unsigned=False):
		pass

	@classmethod
	@int_type
	def SMALLINT(cls, unsigned=False):
		pass

	@classmethod
	@int_type
	def MEDIUMINT(cls, unsigned=False):
		pass

	@classmethod
	@int_type
	def INT(cls, unsigned=False):
		pass

	@classmethod
	@int_type
	def BIGINT(cls, unsigned=False):
		pass

	@classmethod
	@int_type
	def FLOAT(cls, unsigned=False):
		pass

	@classmethod
	@int_type
	def DOUBLE(cls, unsigned=False):
		pass

	@classmethod
	@int_type
	def DECIMAL(cls, unsigned=False):
		pass
	
	"""
	===============================================================
	时间类型
	===============================================================
	"""
	@classmethod
	@plain_type
	def DATE(cls):
		pass

	@classmethod
	@plain_type
	def TIME(cls):
		pass

	@classmethod
	@plain_type
	def YEAR(cls):
		pass

	@classmethod
	@plain_type
	def DATETIME(cls):
		pass
	
	@classmethod
	@plain_type
	def TIMESTAMP(cls):
		pass

	"""
	===============================================================
	字符串类型
	===============================================================
	
	"""
	@classmethod
	@str_type	
	def CHAR(cls, num):
		pass
	
	@classmethod
	@str_type	
	def VARCHAR(cls, num):
		pass
	
	@classmethod
	@str_type	
	def TINYBLOB(cls, num):
		pass
	
	@classmethod
	@str_type	
	def TINYTEXT(cls, num):
		pass
	
	@classmethod
	@str_type	
	def BLOB(cls, num):
		pass
	
	@classmethod
	@str_type	
	def TEXT(cls, num):
		pass
	
	@classmethod
	@str_type	
	def MEDIUMBLOB(cls, num):
		pass
	
	@classmethod
	@str_type	
	def MEDIUMTEXT(cls, num):
		pass
	
	@classmethod
	@str_type	
	def LONGBLOB(cls, num):
		pass
	
	@classmethod
	@str_type	
	def LONGTEXT(cls, num):
		pass

if __name__ == "__main__":
	print(DBDataType.TINYINT(True))