#encoding: utf-8
'''
Created on 2014年7月18日

@author: sony
'''
from hydrogen.common import vmclient
actions={'GET_ALL_DBS':'get_all_dbs'}
def reqdeco(action):
	def newfun(fun):
		def decofunc(self,req,*args,**kwargs):
			codis={}
			user_id = req.environ['HTTP_X_USER_ID']
			user_role = req.environ['HTTP_X_ROLES']
			req.environ['ACTION']=action
			if action == 'get_all_dbs' or action=='update_db4id':
				from_data=req.GET.pop('from_data',None)
				to_data=req.GET.pop('to_data',None)
				if from_data or to_data:
					codis['time_span']=[from_data,to_data]
				codis.update(req.GET.dict_of_lists())
				if user_role == 'dev':
					vm_ids=vmclient.get_vmid_via_user_id(user_id)
					codis['vm_id']=vm_ids
					
				if user_role == 'nuser':
					codis['user_id']=user_id
			
			if codis:
				req.environ['QUERY_CONDITIONS']=codis
			return fun(self,req,*args,**kwargs)
		return decofunc
	return newfun
