# -*- coding: UTF-8 -*-

import MySQLdb
 
def create_connet(host, user, passwd, db, charset):
	return MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)
