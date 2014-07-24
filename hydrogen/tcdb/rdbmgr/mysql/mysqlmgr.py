#encodign: utf-8
'''
Created on 2014Äê7ÔÂ17ÈÕ

@author: sony
'''
import MySQLdb
import sys

class Mysql(object):
	def __init__(self):
		self.conn = None
		self.cursor  = None
	def connect(self, host, user='root', passwd='12345', charset='utf8'):
		try:
			self.conn = MySQLdb.connect(host, user, passwd, db)
		except Exception, e:
			print e
			sys.exit()
		self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
	
	def createdb(self,dbname,name,passwd):
		sql = 'create database if not exists '+str(dbname)
		self.cursor.execute(sql)

