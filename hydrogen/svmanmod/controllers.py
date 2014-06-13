#!/bin/python
from hydrogen.v1.controllers import Controller
from common.rmsvman import RmSVManClass
from common import db
import cgi
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
		self.db_session
		self.rmsvMan = RmSVManClass(self.db_session)
		print "ListName!!!"
	'''
	def get_html(self):
		html_f=open('html/upload.html','r')
		return html_f
	'''
	def index(self,req):
		user_id = req.environ['HTTP_X_USER_ID']
		user_name = req.environ['HTTP_X_USER_NAME'] 
		user_role = req.environ['HTTP_X_ROLES']
		self.db_session=req.environ['db_session']
		svs_data = db.getSvsInfo4All(self.db_session)
		svs_json = {}
		svs = []
		for sv_data in svs_data:
			sv={}
			sv['sv_id']=sv_data['sv_id']
			sv['sv_name']=sv_data['sv_name']
			sv['authority_type']=sv_data['authority_type']
			sv['sv_url']=sv_data['sv_url']
			sv['vm_id']=sv_data['vm_id']
			sv['user_id']=sv_data['user_id']
			sv['sv_lang']=sv_data['sv_lang']
			sv['sv_desc']=sv_data['sv_desc']
			svs.append(sv)
		svs_json['svs']=svs
		return svs
	def show(self,req,id):
		#print "START"
		#print id
# 		print "END"
# 		return "Have id"+id
		user_id = req.environ['HTTP_X_USER_ID']
		user_name = req.environ['HTTP_X_USER_NAME'] 
		user_role = req.environ['HTTP_X_ROLES']
		self.db_session=req.environ['db_session']
		sv_data_list = db.getSvInfo4ID(self.db_session, id)
		
		sv_json={}
		input_args=[]
		input_arg={}
		output_args=[]
		output_arg={}
		svs = []
		sv={}
		
		sv_data=sv_data_list[0]
		sv['sv_id']=sv_data['sv_id']
		sv['sv_name']=sv_data['sv_name']
		sv['authority_type']=sv_data['authority_type']
		sv['sv_url']=sv_data['sv_url']
		sv['vm_id']=sv_data['vm_id']
		sv['user_id']=sv_data['user_id']
		sv['sv_lang']=sv_data['sv_lang']
		sv['sv_desc']=sv_data['sv_desc']
		
		for sv_data in sv_data_list:
			if sv_data['arg_direct'] == 0:
				input_arg={}
				input_arg['sv_arg_id']=sv_data['sv_arg_id']
				input_arg['arg_name'] = sv_data['arg__name']
				input_arg['arg_type_id'] = sv_data['arg_type_id']
				input_arg['arg_index'] = sv_data['arg_index']
				input_arg['arg_type_name'] = sv_data['arg_type_name']
				input_args.append(input_arg)
			if sv_data['arg_direct'] == 1:
				output_arg={}
				output_arg['sv_arg_id']=sv_data['sv_arg_id']
				output_arg['arg_name'] = sv_data['arg__name']
				output_arg['arg_type_id'] = sv_data['arg_type_id']
				output_arg['arg_index'] = sv_data['arg_index']
				output_arg['arg_type_name'] = sv_data['arg_type_name']
				output_args.append(output_arg)
		
		sv['input_arg_types']=input_args
		sv['output_arg_types']=output_args
		sv_json['sv']=sv
		return svs
		
	def create(self,req,body=None):
		environ = req.environ
		user_id = environ['HTTP_X_USER_ID']
		self.db_session=environ['db_session']
		# need to upgrade to use permission engine
		'''
		if user_role == 'nuser':
			return "you have no permission to upload service"
		'''
		#�ǼǷ���Ļ�����Ϣ��sv_tb��
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH',0))
		except ValueError:
			request_body_size=0
		#fileds=cgi.FieldStorage(environ["wsgi.input"],environ=environ)
		
		#���ڲ��ԵĴ���Σ�
		fileds={}
		
		
		
		#insert sv_tb table about service information
		sv_id=db.addSvInfo2TB(self.db_session, user_id, fileds)
		
		#�ǼǷ���Ĳ�����Ϣ��sv_arg_type_tb��
		#insert service arg information into sv_arg_type_tb table
		
		db.addSvInputArg2TB(self.db_session, sv_id, fileds)
		
		db.addSvOutputArg2TB(self.db_session, sv_id, fileds)
		
		#���ļ��ϴ��������
		contenttype = environ['CONTENT_TYPE']
		sv_file = fileds['svfile']
		vm_id = fileds['vm_id'].value
		sv_url=self.rmsvMan.addSv2Vm(vm_id,sv_id, sv_file,contenttype)
		#������sv_tb���ݿ�����sv_url��Ϣ
		db.updatedSvUrl(self.db_session, sv_id, sv_url)
		
		return 'service upload successfully!!!'
	def destory(self,req,id):
		#1.��ȡ�������ڵ������
		#2.����ɾ�����ɾ��������ϵķ���
		#3.ɾ��sv_arg_type_tb���ݿ���÷�����ص���Ϣ��
		#4.ɾ��sv_tb����÷�����ص�����
		
		#ɾ��Զ��������ϵķ���
		environ = req.environ
		user_id = environ['HTTP_X_USER_ID']
		user_name = environ['HTTP_X_USER_NAME']
		user_role = environ['HTTP_X_ROLES']
		self.db_session=environ['db_session']
		self.rmsvMan.deleteSvOnVM(id);
		#ɾ������sv_arg_type_tb�ϵ�����
		db.deleteSvInfoOnTB(self.db_session,id)
		#ɾ������sv_tb�ϵ�����
		db.deleteSvAllArgOnTB(self.db_session,id)
		
	def update(self,req,body,id):
		environ = req.environ
		user_id = environ['HTTP_X_USER_ID']
		user_name = environ['HTTP_X_USER_NAME']
		user_role = environ['HTTP_X_ROLES']
		self.db_session=environ['db_session']
		#�޸�sv_arg_type_tb��
		input_arg_types=body.pop('input_arg_types')
		for key in input_arg_types.keys():
			db.updateSvArgtype(self.db_session,key,input_arg_types['key'])
		output_arg_types=body.pop('output_arg_types')
		for key in output_arg_types.keys():
			db.updateSvArgtype(self.db_session, key, input_arg_types['key'])
		
		#�޸�sv_tb��
		db.updateSvTB(self.db_session, id, body)
			
			
			
		
		
