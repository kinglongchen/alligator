#encoding: utf-8
#!/bin/python
from v1.controllers import Controller
import policy
from common import exceptions
from hydrogen.common import vmclient
from common import proxyclient
from common import db
from common import reqdeco
from hydrogen.tcdb.common.tbtarget import TBTarget
from hydrogen.common.exceptions import NUllResourceIDException
from hydrogen.common import exceptions

def checkpolicy(req,id=None):
	context=req.environ['hydrogen.context']
	action=req.environ['ACTION']
	db_session=req.environ['db_session']
	if id:
		target=TBTarget.tbtarget_factory(db_session,id).to_dict()
	else:
		target=TBTarget.factory().to_dict()
	policy.init()
	policy.enforce(context, action, target)
	
	

class DBMgr(Controller):
	@reqdeco.reqdeco('get_all_dbs')
	def index(self,req):
		#url GET ip:8089/v1/dbs
		db_session=req.environ['db_session']
		#从req中获取condis,condis中的信息根据角色来设置
		#从数据库中获取数据库表信息
		#rs='asdf'
		#print req.environ.get('QUERY_CONDITIONS',None)
# 		try:
		rs = db.getDBInfo4All(db_session, req.environ.get('QUERY_CONDITIONS',None))
# 		except Exception,e:
# 			return e.message
		
		return {'dbs':rs}
		
# 	def show(self,req,id):
# 		#url GET ip:8089/v1/dbs/id
# 		
# 	
# 		return 'show'
	@reqdeco.reqdeco('create_db')
	def create(self,req,body=None):
		#url POST ip:8089/v1/dbs
		#dbname,vm_id,db_username,db_passwd
		#1.根据vm_id,获得对应vm_ip地址以及对应的虚拟机类型，如果对应的返回的虚拟机类型中的最后一位为1，则可以运行，否则返回VMtypeError
		user_id = req.environ['HTTP_X_USER_ID']
		user_name = req.environ['HTTP_X_USER_NAME']
		db_session = req.environ['db_session']
		
		try:
			checkpolicy(req)
		except Exception,e:
			return e.msg
		
# 		context=req.environ['hydrogen.context']
# 		action=req.environ['ACTION']
# 		target=TBTarget.factory().to_dict()
# 		policy.init()
# 		try:
# 			policy.enforce(context, action, target)
# 		except Exception,e:
# 			return e.msg
		vm_id = body.get('vm_id',None)
		dbname = body.get('dbname',None)
		db_username = body.get('db_username',None)
		db_passwd = body.get('db_passwd',None)
		#获得数据库所在ip地址
		vm_ip = vmclient.get_vm_ip(vm_id)
		try:
			if not dbname:
				raise exceptions.DBaddValueError(valuename='dbname')
			if not user_id:
				raise exceptions.DBaddValueError(valuename='user_id')
			if not vm_id:
				raise exceptions.DBaddValueError(valuename='vm_id')
			if not db_username:
				raise exceptions.DBaddValueError(valuename='db_username')
			proxyclient.createdbreq(vm_ip, dbname, db_username, db_passwd)
			db.addDBInfo2TB(db_session,dbname,user_id,user_name,vm_id,db_username)
		except exceptions.HydrogenException,e:
			return e.msg
# 		except Exception,e:
# 			return e.message
		#将创建的数据库信息保存在数据库中
		
		return 'Create DataBase on Server which vm_id is %s successfully' %vm_id
	
	@reqdeco.reqdeco('update_db4id')
	def update(self,req,body=None,id=None):
		db_session=req.environ['db_session']
		
		try:
			checkpolicy(req,id)
		except Exception,e:
			return e.msg
		
		db.updateDBInfo4ID(db_session,id,body)
		#PUT ip:8089/v1/dbs/id
		return 'Update User DataBase information  which id is %s successfully!' %id
	
	@reqdeco.reqdeco('delete_db4id')	
	def delete(self,req,id):
		#DELETE ip:8089/v1/dbs/id
		db_session=req.environ['db_session']
		
 		try:
			checkpolicy(req,id)
 		except Exception,e:
 			return e.msg
		try:
		#dbname = db.get_dbinfo_dbname(db_session,id)
		#db_user_count为数据库的用户名为db_username的数目
		#db_username,db_user_count = db.get_dbinfo_dbusername(db_session,id)
 			dbinfo = db.get_dbinfo4id_all(db_session,id)
		 	if not dbinfo:
		 		raise NUllResourceIDException(id=id) 
 			vm_id = dbinfo['vm_id']
 		 	vm_ip = vmclient.get_vm_ip(vm_id)
 		  	dbname = dbinfo['dbname']
		
		#db_username = dbinfo['db_username']
		#user_count = get_usercount4username(db_session,db_username)
		#delete_db_username = False
		#if user_count<2:
		#	delete_db_username = True
		#删除远程数据库
		
			proxyclient.deletedbreq(vm_ip,dbname)
			db.deleteDBInfo4ID(db_session,id)
		except Exception,e:
			return e.msg
		return 'Delete User DataBase information which id is %s successfully' %id
	
	
