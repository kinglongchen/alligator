#encoding: utf-8
'''
Created on 2014年7月17日

@author: sony
'''
import urllib2
import json
import exceptions
def createdbreq(ip,dbname,db_username,db_passwd):
	r = urllib2.Request("http://%s:8091/v1/createdb" %ip)
	r.add_header("Content-Type", 'application/json')
	r.add_data('{"dbname":"%s","db_username":"%s","db_passwd":"%s"}' %(dbname,db_username,db_passwd))
	try:
		rs = urllib2.urlopen(r)
	except Exception,e:
		print e
		raise exceptions.DBProxyServerException(errormsg=e.message)
	rs = json.loads(rs.read())
	if rs.has_key('errormsg'):
		raise exceptions.DBProxyServerException(errormsg=rs.get('errormsg','UEKNOWN ERROR!'))
	return rs

def deletedbreq(ip,dbname):
	r = urllib2.Request("http://%s:8091/v1/deletedb" %ip)
	r.add_header("Content-Type", 'application/json')
	r.add_data('{"dbname":"%s"}' %dbname)
	try:
		rs = urllib2.urlopen(r)
	except Exception,e:
		print e
		raise exceptions.DBProxyServerException(errormsg=e.message)
	rs = json.loads(rs.read())
	print rs
	if rs.has_key('errormsg'):
		raise exceptions.DBProxyServerException(errormsg=rs.get('errormsg','UEKNOWN ERROR!'))
	return rs


#测试
#createdbreq('192.168.0.13','kingdb4','kinglong4','12345')
#print deletedbreq('192.168.0.13','kingdb4')
	
	