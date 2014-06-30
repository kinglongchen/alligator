#!/bin/python
# encoding: utf-8
from hydrogen.v1.controllers import Controller
from common.rmsvman import RmSVManClass
from common import db
import cgi
from hydrogen.svmanmod.common.svtarget import SvTarget
from hydrogen import  policy
from symbol import except_clause
from common import exceptions as svmodexceptions
from hydrogen.common.exceptions import HydrogenException
#class Controller(object):
#	def default(self,req,id):
#		print "Start"
#		print id
#		print "End"
##		return "Action Not Define!!!"
class Tenant(Controller):
	def __init__(self):
		print "ControllerTest!!!!"
	def get_projects_for_token(self,req):
		print "req",req
		return {
            'name': "test",
            'properties': "test"
        }
class ServiceMan(Controller):
	def __init__(self):
		self.db_session=None
		self.rmsvMan = RmSVManClass(self.db_session)
		print "ListName!!!"
	'''
	def get_html(self):
		html_f=open('html/upload.html','r')
		return html_f
	'''
	def index(self,req):
		'''
		user_id = req.environ['HTTP_X_USER_ID']
		user_name = req.environ['HTTP_X_USER_NAME'] 
		user_role = req.environ['HTTP_X_ROLES']
		'''
		
		self.db_session=req.environ['db_session']
		svs = db.getSvsInfo4All(self.db_session)
		svs_json = {}
		svs_json['svs']=svs
		return svs_json
	def show(self,req,id):
		#print "START"
		#print id
# 		print "END"
# 		return "Have id"+id
		'''
		user_id = req.environ['HTTP_X_USER_ID']
		user_name = req.environ['HTTP_X_USER_NAME'] 
		user_role = req.environ['HTTP_X_ROLES']
		'''
		print 'show'
		print id
		self.db_session=req.environ['db_session']
		sv = db.getSvInfo4ID(self.db_session, id)
		
		sv_json={}
		sv_json['sv']=sv
		return sv_json
		
	def create(self,req,body=None):
		environ = req.environ
		user_id = environ['HTTP_X_USER_ID']
		user_name = environ['HTTP_X_USER_NAME'] 
		self.db_session=environ['db_session']
		# need to upgrade to use permission engine
		#验证权限
		context=environ['hydrogen.context']
		action="deploy_service"
		target=SvTarget.factory().to_dict()
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		'''
		if user_role == 'nuser':
			return "you have no permission to upload service"
		'''
		#登记服务的基本信息到sv_tb中
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH',0))
		except ValueError:
			request_body_size=0
		fileds=cgi.FieldStorage(environ["wsgi.input"],environ=environ)
		if fileds['svfile'].filename is None:
			return "No service file Error!"
		#用于测试的代码段：
		#fileds={}
		#print fileds
		#print environ["wsgi.input"].read()
		#print self.db_session
		#insert sv_tb table about service information
		
		try:
			sv_id=db.addSvInfo2TB(self.db_session, user_id,user_name, fileds)
		except HydrogenException,e:
			return e.msg
		#登记服务的参数信息到sv_arg_type_tb中
		#insert service arg information into sv_arg_type_tb table
		
		db.addSvInputArg2TB(self.db_session, sv_id, fileds)
		db.addSvOutputArg2TB(self.db_session, sv_id, fileds)
		#将文件上传到虚拟机
		contenttype = environ['CONTENT_TYPE']
		sv_file = fileds['svfile']
		vm_id = fileds['vm_id'].value
		sv_url=self.rmsvMan.addSv2Vm(vm_id,sv_id, sv_file,contenttype)
		#将更新sv_tb数据库中年sv_url信息
		db.updatedSvUrl(self.db_session, sv_id, sv_url)
		return 'service upload successfully!!!'
	
	def delete(self,req,id=None):
		#1.获取服务所在的虚拟机
		#2.调用删除命令，删除虚拟机上的服务
		#3.删除sv_arg_type_tb数据库与该服务相关的信息，
		#4.删除sv_tb上与该服务相关的数据
		
		#删除远程虚拟机上的服务
		environ = req.environ
		'''
		user_id = environ['HTTP_X_USER_ID']
		user_name = environ['HTTP_X_USER_NAME']
		user_role = environ['HTTP_X_ROLES']
		'''
		
		self.db_session=environ['db_session']
		
		context=environ['hydrogen.context']
		action="undeploy_service"
		try:
			target=SvTarget.svtarget_factory(self.db_session,id).to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		
		self.rmsvMan.deleteSvOnVM(self.db_session,id);
		#删除本地sv_arg_type_tb上的数据
		db.deleteSvInfoOnTB(self.db_session,id)
		#删除本地sv_tb上的数据
		db.deleteSvArg4IDOnTB(self.db_session,id)
		
		return 'delete successfully!'
	def update(self,req,body,id=None):
		environ = req.environ
		'''
		user_id = environ['HTTP_X_USER_ID']
		user_name = environ['HTTP_X_USER_NAME']
		user_role = environ['HTTP_X_ROLES']
		'''
		self.db_session=environ['db_session']
		context=environ['hydrogen.context']
		action="deploy_service"
		try:
			target=SvTarget.svtarget_factory(self.db_session,id).to_dict()
		except Exception,e:
			return e.message
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		#修改sv_arg_type_tb表
		print body
		print "#####################"
		print body['input_arg_types']
		input_arg_types=body.pop('input_arg_types')
		for key in input_arg_types.keys():
			db.updateSvArgtype(self.db_session,key,input_arg_types[key])
		output_arg_types=body.pop('output_arg_types')
		for key in output_arg_types.keys():
			db.updateSvArgtype(self.db_session, key, output_arg_types[key])
		print "#####################"
		print body
		#修改sv_tb表
		db.updateSvTB(self.db_session, id, body)
		return 'update successfully!!!'


class ArgTypeMan():
	def __init__(self):
		self.db_session=None
	def index(self,req):
		environ = req.environ
		self.db_session=environ['db_session']
		
		#利用db查询数据库，并以json格式返回
		arts_data = db.getArgTypeInfo(self.db_session)
		arts={}
		arts['ats'] = arts_data
		return arts
	
# 	def show(self,req,id):
# 		environ = req.environ
# 		self.db_session=environ['db_session']
		
		
	def create(self,req,body=None):
		environ = req.environ
		self.db_session=environ['db_session']
		
		context=environ['hydrogen.context']
		action="add_argtype"
		try:
			target=SvTarget.factory().to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		#增加数据类型信息到数据库中
		db.addArgTypesInfo2TB(self.db_session,body)
		return "add argtypes information successfully!!!"

	def delete(self,req,id=None):
		environ = req.environ
		self.db_session=environ['db_session']
		context=environ['hydrogen.context']
		action="delete_argtype"
		try:
			target=SvTarget.factory().to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		
		#删除数据库中的信息
		db.deleteArgType4ID(self.db_session,id)
		return 'delete argtype information successfully!'        

	def update(self,req,body,id=None):
		environ = req.environ
		self.db_session=environ['db_session']
		context=environ['hydrogen.context']
		action="update_argtype"
		try:
			target=SvTarget.factory().to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		
		db.updateArgTypeInfo4ID(self.db_session,id,body)
		return 'update argtype information successfully!'

class PolicyMan(object):
	def __init__(self):
		self.db_session=None
	
# 	def show(self,req,id):
# 		pass
	
	def getAllPolicyInfo(self,req):
		environ = req.environ
		self.db_session=environ['db_session']
		
		context=environ['hydrogen.context']
		action="getallpolicyinfo"
		target=SvTarget.factory().to_dict()
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		policies_info=db.getSvPolicyInfo4ALL(self.db_session)
		policies={}
		policies['policies']=policies_info
		return policies
		
		
		
	def getPolicy4SVID(self,req,sv_id):
		environ = req.environ
		self.db_session=environ['db_session']
		
		

		context=environ['hydrogen.context']
		action="getpolicy4svid"
		try:
			target=SvTarget.svtarget_factory(self.db_session,sv_id).to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		
		svpolicy_info=db.getSvPolicyInfo4SVID(self.db_session, sv_id)
		svpolicy={}
		svpolicy['policy']=svpolicy_info
		return svpolicy
		
		
	def addPolicy4SVID(self,req,sv_id,body=None):
		environ = req.environ
		self.db_session=environ['db_session']
		
		context=environ['hydrogen.context']
		action="addpolicy4svid"
		try:
			target=SvTarget.svtarget_factory(self.db_session,sv_id).to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		
		db.createSvPolicy(self.db_session, sv_id,body)
		return 'insert policy information successfully!'
	
	def deletePolicy4SVID(self,req,sv_id,id):
		environ = req.environ
		self.db_session=environ['db_session']
		
		context=environ['hydrogen.context']
		action="deletepolicy4svid"
		try:
			target=SvTarget.svtarget_factory(self.db_session,sv_id).to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		
		
		db.deleteSvPolicy4ID(self.db_session,sv_id,id)
		return 'delete policy information successfully!'
	
	def updatePolicy4SVID(self,req,sv_id,id,body=None):
		environ = req.environ
		self.db_session=environ['db_session']
		context=environ['hydrogen.context']
		action="updatepolicy4svid"
		try:
			target=SvTarget.svtarget_factory(self.db_session,sv_id).to_dict()
		except Exception,e:
			return e.msg
		policy.init()
		try:
			policy.enforce(context, action, target)
		except Exception,e:
			return e.msg
		db.updateSvPolicy4ID(self.db_session, sv_id,id, body)
		return  'update policy successfully!!!'