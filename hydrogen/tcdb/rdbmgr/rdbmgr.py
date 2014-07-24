#encoding: utf-8
'''
Created on 2014年7月17日

@author: sony
'''
from mysql import mysqlmgr
rdbmgr_dict={}
rdbmgr_dict['image_id']=mysqlmgr
def getDBMgr(image_id):
	return mysqlmgr
