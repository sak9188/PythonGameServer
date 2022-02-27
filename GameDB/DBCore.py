# -*- coding: UTF-8 -*-

from Core.Extent import pymysql


def create_connet(host, user, passwd, db, charset):
	return pymysql.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)
