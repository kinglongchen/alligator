# encoding: utf-8
'''
Created on 2014��6��11��

@author: sony
'''
from exceptions import BadServiceIDException
import exceptions
from hydrogen.common import vmclient
from hydrogen.svmanmod.common.exceptions import BadQueryConditions
def getSvVmip(db_session,id):
	sql='select vm_id from sv_tb where sv_id= "'+str(id)+'"'
	print sql
	r=db_session.query(sql)
	if len(r)==0:
		raise BadServiceIDException(sv_id=id)
	vm_id=r[0]['vm_id']
	vm_ip=vmclient.get_vm_ip(vm_id)
	return vm_ip

def getSvUserID(db_session,id):
	sql='select user_id from sv_tb where sv_id= "'+str(id)+'"'
	r=db_session.query(sql)
	if len(r)==0:
		raise BadServiceIDException(sv_id=id)
	user_id=r[0]['user_id']
	return user_id
def getSvsInfo4All(db_session,codis):
	#条件查询
	#1.根据sv_id查询
	#2.根据sv_name查询
	#3.根据authority_type查询
	#4.根据sv_name查询vm_id查询
	#5.根据user_id查询
	#6.根据sv_lang查询
	#7.根据upload_date的范围查询
	for codi in codis.iterkeys():
		print codi 
	print '####################'
	qkeys=['sv_id','sv_name','authority_type','vm_id','user_name','vm_name','sv_lang','from_date','to_date','user_id']
	svs = []
	sql ='select * from sv_tb'
	
	
	if codis:
		
		qcodis=' '
		from_date=codis.pop('from_date',None)
		to_date=codis.pop('to_date',None)
		if from_date and to_date:
			qcodis+='unix_timestamp(upload_date) between unix_timestamp("'+from_date+'") and unix_timestamp("'+to_date+'") and '
		elif not (not from_date and not to_date):
			raise DateException(date_selc='from_date or to_date can not be null!')
		
		for key in codis.iterkeys():
			
			if key not in qkeys:
				raise BadQueryConditions(qkey=key)
			value=codis[key]
			if value:
				print key
				qcodis+=key+'="'+value+'" and '
		qcodis=qcodis[:-5]
		sql +=' where'+qcodis
	sql+=' order by sv_id'
	print sql
	svs_data=db_session.query(sql) 
	if len(svs_data)==0:
		return svs
	for sv_data in svs_data:
		sv={}
		sv['sv_id']=sv_data['sv_id']
		sv['sv_name']=sv_data['sv_name']
		sv['authority_type']=sv_data['authority_type']
		sv['sv_url']=sv_data['sv_url']
		sv['vm_id']=sv_data['vm_id']
		sv['user_id']=sv_data['user_id']
		sv['user_name']=sv_data['user_name']
		sv['sv_lang']=sv_data['sv_lang']
		sv['sv_desc']=sv_data['sv_desc']
		sv['upload_date']=sv_data['upload_date']
		svs.append(sv)
	return svs

def getSvInfo4ID(db_session,id):
	input_args=[]
	input_arg={}
	output_args=[]
	output_arg={}
	#svs = []
	sv={}
	#sql = 'select sv_tb.sv_id as sv_id,sv_name,authority_type,sv_url,vm_id,user_id,user_name,sv_lang,sv_desc,upload_date,sv_arg_id,arg_name,sv_arg_type_tb.arg_type_id as arg_type_id,arg_index,arg_direct,arg_type_name from sv_tb,sv_arg_type_tb,arg_type_tb where sv_tb.sv_id='+str(id)+' and sv_tb.sv_id=sv_arg_type_tb.sv_id and sv_arg_type_tb.arg_type_id = arg_type_tb.arg_type_id order by sv_id,arg_index;'
	#print sql
	sql = 'select * from sv_tb where sv_id="'+str(id)+'"'
	sv_data_list=db_session.query(sql)
	if len(sv_data_list)==0:
		return sv
	sv_data=sv_data_list[0]
	sv['sv_id']=sv_data['sv_id']
	sv['sv_name']=sv_data['sv_name']
	sv['authority_type']=sv_data['authority_type']
	sv['sv_url']=sv_data['sv_url']
	sv['vm_id']=sv_data['vm_id']
	sv['user_id']=sv_data['user_id']
	sv['user_name']=sv_data['user_name']
	sv['sv_lang']=sv_data['sv_lang']
	sv['sv_desc']=sv_data['sv_desc']
	sv['upload_date']=sv_data['upload_date']
	
	sql = 'select sv_id,sv_arg_id,arg_name,sv_arg_type_tb.arg_type_id as arg_type_id,arg_index,arg_direct,arg_type_name from sv_arg_type_tb,arg_type_tb where sv_id="'+str(id)+'"'+' and sv_arg_type_tb.arg_type_id = arg_type_tb.arg_type_id order by sv_id,arg_index;'
	
	sv_data_list=db_session.query(sql)
	if len(sv_data_list)==0:
		return sv
	for sv_data in sv_data_list:
		if sv_data['arg_direct'] == 0:
			input_arg={}
			input_arg['sv_arg_id']=sv_data['sv_arg_id']
			input_arg['arg_name'] = sv_data['arg_name']
			input_arg['arg_type_id'] = sv_data['arg_type_id']
			input_arg['arg_index'] = sv_data['arg_index']
			input_arg['arg_type_name'] = sv_data['arg_type_name']
			input_args.append(input_arg)
		if sv_data['arg_direct'] == 1:
			output_arg={}
			output_arg['sv_arg_id']=sv_data['sv_arg_id']
			output_arg['arg_name'] = sv_data['arg_name']
			output_arg['arg_type_id'] = sv_data['arg_type_id']
			output_arg['arg_index'] = sv_data['arg_index']
			output_arg['arg_type_name'] = sv_data['arg_type_name']
			output_args.append(output_arg)
	sv['input_arg_types']=input_args
	sv['output_arg_types']=output_args
	
	return sv

def addSvInfo2TB(db_session,user_id,user_name,fileds):
	sv_name = fileds['sv_name'].value.strip()
	if sv_name == '':
		raise exceptions.SvUploadArgError(arg_name='sv_name')
	vm_id = fileds['vm_id'].value.strip()
	if vm_id == '':
		raise exceptions.SvUploadArgError(arg_name='sv_name')
	sv_lang=fileds['sv_lang'].value.strip()
	if sv_lang == '':
		raise exceptions.SvUploadArgError(arg_name='sv_name')
	sv_desc=fileds['sv_desc'].value.strip()
	if sv_desc == '':
		raise exceptions.SvUploadArgError(arg_name='sv_name')
	sql = 'insert into sv_tb(sv_name,vm_id,user_id,user_name,sv_lang,sv_desc) values ("'+sv_name+'","'+vm_id+'","'+user_id+'","'+user_name+'","'+sv_lang+'","'+sv_desc+'");'
	return db_session.insert(sql)


def addSvArgInfo2TB(db_session,sv_id,fileds,arg_direct=0):
	arg_names_key='input_arg_names'
	arg_types_key='input_arg_types'
	#arg_name_key_prefix='input_arg_name'
	#arg_names_key='input_arg_names'
	if arg_direct==1:
		#arg_name_key_prefix = 'output_arg_name'
		arg_names_key = 'output_arg_names'
		arg_types_key='output_arg_types'
	arg_index = 0
	#arg_names=fileds[arg_names_key].value.split(';')
	arg_names=fileds.getvalue(arg_names_key,None)
	
	if arg_names is None:
		return
	
	if not isinstance(arg_names, list):
		arg_names=[arg_names]
		
	arg_type_ids = fileds.getvalue(arg_types_key,None)
	if arg_type_ids is None:
		return
	if not isinstance(arg_type_ids, list):
		arg_type_ids=[arg_type_ids]
	
	
	for arg_type_id in arg_type_ids:
		arg_name=arg_names[arg_index]
		arg_index+=1
		arg_type_id=arg_type_id
		
		if arg_name is None:
			arg_name="default_arg_name"
		
		
		sql = 'insert into sv_arg_type_tb(arg_name,sv_id,arg_type_id,arg_index,arg_direct) values ("'+arg_name+'","'+str(sv_id)+'","'+arg_type_id+'","'+str(arg_index)+'","'+str(arg_direct)+'");'
		db_session.insert(sql)
	'''
	for arg_name in arg_names:
		arg_name_key=arg_name_key_prefix+str(arg_index)
		arg_type_id=fileds[arg_name_key].value
		sql = 'insert into sv_arg_type_tb(arg_name,sv_id,arg_type_id,arg_index,arg_direct) values ("'+arg_name+'","'+str(sv_id)+'","'+arg_type_id+'","'+str(arg_index)+'","'+str(arg_direct)+'");'
		print arg_name
		print arg_name_key
		print sql
		db_session.insert(sql)
		arg_index+=1
	'''
		
def addSvInputArg2TB(db_session,sv_id,fileds):
	addSvArgInfo2TB(db_session, sv_id, fileds, 0)
	
	
def addSvOutputArg2TB(db_session,sv_id, fileds):
	addSvArgInfo2TB(db_session, sv_id, fileds, 1)
	
	
def deleteInfoOnTB(db_session,id,tb):
	sql='delete from '+str(tb)+' where sv_id="'+str(id)+'"'
	print sql
	db_session.delete(sql)
	
def deleteSvInfoOnTB(db_session,sv_id):
	deleteInfoOnTB(db_session, sv_id,'sv_tb')
	
def deleteSvArg4IDOnTB(db_session,sv_id):
	deleteInfoOnTB(db_session, sv_id,'sv_arg_type_tb')
	
	
def updateSvOnTB(db_session,id,tb):
	pass
def updateSvArgtype(db_session,sv_arg_id,arg_type_info):
	arg_type_id=arg_type_info['arg_type_id']
	arg_name=arg_type_info['arg_name']
	print arg_type_id
	print arg_name
	if arg_type_id:
		sql = 'update sv_arg_type_tb set arg_type_id='+str(arg_type_id)+' where sv_arg_id='+str(sv_arg_id)
		db_session.update(sql)
	if arg_name:
		sql = 'update sv_arg_type_tb set arg_name="'+str(arg_name)+'" where sv_arg_id='+str(sv_arg_id)
		db_session.update(sql)
	

def updateSvTB(db_session,id,fileds):
	sql = 'update sv_tb set '
	for key in fileds.keys():
		sql+= str(key)+'="'+str(fileds[key])+'",'
	#ɾ�����һ������
	sql=sql[:-1]
	sql+=' where sv_id='+str(id)
	db_session.update(sql)
def updatedSvUrl(db_session,id,sv_url):
	sql = 'update sv_tb set sv_url= "'+sv_url+'" where sv_id = "'+str(id)+'"'
	db_session.update(sql)




def getArgTypeInfo(db_session):
	sql='select * from arg_type_tb'
	results=db_session.query(sql)
	arts_data_list=[]
	for r in results:
		arts_data={}
		arts_data['arg_type_id']=r['arg_type_id']
		arts_data['arg_type_name']=r['arg_type_name']
		arts_data['arg_type_desc']=r['arg_type_desc']
		arts_data_list.append(arts_data)
		
	return arts_data_list
	

def addArgTypesInfo2TB(db_session,body):
	arg_type_name=body['arg_type_name']
	arg_type_desc=body['arg_type_desc']
	sql = 'insert into arg_type_tb(arg_type_name,arg_type_desc) values ("'+arg_type_name+'","'+arg_type_desc+'");'
	db_session.insert(sql)
	return 'add arg type information successfully!'

def deleteArgType4ID(db_session,id):
	sql='delete from arg_type_tb where arg_type_id="'+str(id)+'"'
	db_session.delete(sql)
	return 'delete arg type information successfully!'

def updateArgTypeInfo4ID(db_session,id,body):
	sql = 'update arg_type_tb set '
	for key in body.keys():
		sql+= str(key)+'="'+str(body[key])+'",'
	sql=sql[:-1]
	sql+=' where arg_type_id='+str(id)
	print sql
	db_session.update(sql)
	return 'update args type data successfully!!!'

def createSvPolicy(db_session,sv_id,body):
#def createSvPolicy(db_session,sv_id,role=None,user_id=None,timelimit=30):
	role=None
	user_id=None
	timelimit=30
	if body.has_key('role'):
		role=body['role']
	if body.has_key('user_id'):
		user_id=body['user_id']
	if body.has_key('timelimit'):
		timelimit=body['timelimit']
	ins_filds="(sv_id"
	val='("'+str(sv_id)
	if role:
		ins_filds+=",role"
		val+='","'+str(role)
	if user_id:
		ins_filds+=",user_id"
		val+='","'+str(user_id)
	ins_filds+=",sv_expires)"
	val+='",date_add(now(),interval '+str(timelimit)+' day))'
		
	sql = 'insert into sv_policy_tb'+ins_filds+' values '+val
	
	rs=db_session.insert(sql)
	
	return rs

def updateSvPolicy4ID(db_session,sv_id,id,body):
	sql = 'update sv_policy_tb set '
	timelimit=body.pop('timelimit')
	for key in body.keys():
		sql+= str(key)+'="'+str(body[key])+'",'
	if timelimit:
		sv_expires = getExpTime(db_session, sv_id, id)
		if sv_expires:
			sql+='sv_expires=date_add("'+str(sv_expires)+'",interval '+str(timelimit)+' day)'
		else:
			sql+='sv_expires=date_add(now(),interval '+str(timelimit)+' day))'
	else:
		sql=sql[:-1]
	sql+=' where sv_id="'+str(sv_id)+'" and sv_policy_id='+str(id)
	print sql
	rs = db_session.update(sql)
	return rs
#获取指定服务的指定策略的过期时间
def getExpTime(db_session,sv_id,id):
	sql = 'select sv_expires from sv_policy_tb where sv_id="'+str(sv_id)+'" and sv_policy_id="'+str(id)+'"'
	print sql
	rs = db_session.query(sql)
	return rs[0]['sv_expires']
def deleteSvPolicy4ID(db_session,sv_id,id):
	sql='delete from sv_policy_tb where sv_id="'+str(sv_id)+'" and sv_policy_id="'+str(id)+'"'
	rs=db_session.delete(sql)
	return rs

def getSvPolicy4All(db_session):
	sql = 'select * from sv_policy_tb'+' order by sv_id,sv_policy_id'
	rs = db_session.query(sql)
	sv_id = -1
	svp={}
	rolesp=[]
	user_idp=[]
	'''
	{'sv_id':{
	 			'role':[###],
	 			'user_id':[#####]
	 			}
	
	}
	'''
	for r in rs:
		if sv_id!=r['sv_id'] and sv_id!=-1:
			svp[sv_id]={'role':rolesp,'user_id':user_idp}
			rolesp=[]
			user_idp=[]
		sv_id=r['sv_id']
		if r['role']!=None:
			rolesp.append(r['role'])
		if r['user_id']!=None:
			user_idp.append(r['user_id'])
		#循环结束时，还有一组记录需要处理
		svp[sv_id]={'role':rolesp,'user_id':user_idp}
		return svp
def getSvPolicy4SVID(db_session,sv_id):
	sql = 'select * from sv_policy_tb where sv_id='+str(sv_id)+' order by sv_id,sv_policy_id'
	rs = db_session.query(sql)
	rolesp=[]
	user_idp=[]
	for r in rs:
		if r['role']!=None:
			rolesp.append(r['role'])
		if r['user_id']!=None:
			user_idp.append(r['user_id'])
	return {sv_id:{'role':rolesp,'user_id':user_idp}}


def getSvPolicyInfo4SVID(db_session,sv_id):
	sql = 'select * from sv_policy_tb where sv_id='+str(sv_id)+' order by sv_id,sv_policy_id'
	rs = db_session.query(sql)
	'''
	
	'''
# 	rolesp=[]
# 	user_idp=[]
# 	for r in rs:
# 		if r['role']!=None:
# 			rolesp.append(r['role'])
# 		if r['user_id']!=None:
# 			user_idp.append(r['user_id'])
# 	
# 	return {"sv_id":sv_id,"policy":{'role':rolesp,'user_id':user_idp}}
	svpinfo_list=[]
	for r in rs:
		svpinfo={}
		svpinfo['sv_policy_id']=r['sv_policy_id']
		svpinfo['sv_id']=r['sv_id']
		svpinfo['role']=r['role']
		svpinfo['user_id']=r['user_id']
		svpinfo['updata_time']=r['updata_time']
		svpinfo['create_time']=r['create_time']
		svpinfo['sv_expires']=r['sv_expires']
		svpinfo_list.append(svpinfo)
	return svpinfo_list


def getSvPolicyInfo4ALL(db_session):
	sql = 'select * from sv_policy_tb'+' order by sv_id,sv_policy_id'
	rs = db_session.query(sql)
	
	'''
	{[{	 'policy_id':###
		'sv_id':###
	 	'role':
	 	'user_id':
	   },
	]
	}
	'''
# 	sv_id = -1
# 	svpinfo_list=[]
# 	svpinfo={}
# 	rolesp=[]
# 	user_idp=[]
# 	for r in rs:
# 		#print "a result!!!"
# 		if sv_id!=r['sv_id'] and sv_id!=-1:
# 			svpinfo['sv_id']=sv_id
# 			svpinfo['policy']={'role':rolesp,'user_id':user_idp}
# 			svpinfo_list.append(svpinfo)
# 			svpinfo={}
# 			rolesp=[]
# 			user_idp=[]
# 		sv_id=r['sv_id']
# 		if r['role']!=None:
# 			rolesp.append(r['role'])
# 		if r['user_id']!=None:
# 			user_idp.append(r['user_id'])
# 	#对最后一组记录进行处理
# 	svpinfo['sv_id']=sv_id
# 	svpinfo['policy']={'role':rolesp,'user_id':user_idp}
	svpinfo_list=[]
	for r in rs:
		svpinfo={}
		svpinfo['sv_policy_id']=r['sv_policy_id']
		svpinfo['sv_id']=r['sv_id']
		svpinfo['role']=r['role']
		svpinfo['user_id']=r['user_id']
		svpinfo['updata_time']=r['updata_time']
		svpinfo['create_time']=r['create_time']
		svpinfo['sv_expires']=r['sv_expires']
		svpinfo_list.append(svpinfo)
	return svpinfo_list
		
#createSvPolicy(31,30,31)




		


	
	
	