#!/usr/bin/python
#Filename: mysql.py

import MySQLdb
import os, sys

class Mysql(object):
	def __init__(self):
		self.conn = ''
		self.cursor  = ''
	def connect(self, host='localhost', user='root', passwd='12345', db='sc', charset='utf8'):
		try:
			self.conn = MySQLdb.connect(host, user, passwd, db)
		except Exception, e:
			print e
			sys.exit()
		self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
	
	def execute4DML(self,sql):
		self.cursor.execute(sql)
		id = self.conn.insert_id()
		self.conn.commit()
		return id
	def execute4DQL(self,sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()
	def query(self,sql):
		return self.execute4DQL(sql)
	def insert(self, sql):
		return self.execute4DML(sql)
	def delete(self,sql):
		return self.execute4DML(sql)
	def update(self,sql):
		return self.execute4DML(sql)

	def insertsvargtb(self,arg_name,sv_id,arg_type_id,arg_index,arg_direct):
		sql = 'insert into sv_arg_type_tb(arg_name,sv_id,arg_type_id,arg_index,arg_direct) values ("'+arg_name+'","'+sv_id+'","'+arg_type_id+'","'+arg_index+'","'+arg_direct+'");'
		self.cursor.execute(sql)
		self.conn.commit()
	
			
	def close(self):
		self.cursor.close()
		self.conn.close()
	#def __del__(self):
	#	testfile=open('/printtxt.txt','w')
	#	stdout=sys.stdout
	#	stderr=sys.stderr
	#	sys.stdout=testfile
	#	sys.stderr=testfile
	#	print "close db_ins"
		#self.close()
