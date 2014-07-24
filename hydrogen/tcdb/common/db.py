#encoding: utf-8
'''
Created on 2014年7月17日

@author: sony
'''
from hydrogen.common import exceptions
qkeys = ['dbname','user_id','user_name','vm_id','db_username']
updatekeys=[]

def addDBInfo2TB(db_session,dbname,user_id,user_name,vm_id,db_username):
	if not dbname:
		raise exceptions.DBaddValueError(valuename='dbname')
	if not user_id:
		raise exceptions.DBaddValueError(valuename='user_id')
	if not vm_id:
		raise exceptions.DBaddValueError(valuename='vm_id')
	if not db_username:
		raise exceptions.DBaddValueError(valuename='db_username')
		
	sql = 'insert into tcdb_tb(dbname,user_id,user_name,vm_id,db_username) values ("'+dbname+'","'+user_id+'","'+user_name+'","'+vm_id+'","'+db_username+'")'
	rs = db_session.insert(sql)
	return rs
def __getwherestr(codis,qkeys):
	where=''
	if not codis: return where 
	time_span=codis.pop('time_span',None)
	print time_span
	if time_span:
		if not isinstance(time_span,list) or  None in time_span:
			raise DateInfoMissingError()
		if time_span[1]<time_span[0]:
			raise DateInfoOrderError()
		if len(time_span)!=2:
			raise DateInfoNumberError()
		where+='unix_timestamp(create_time) between unix_timestamp(%s) and unix_timestamp(%s) and ' %tuple(time_span)
	for key in codis.keys():
		if key not in qkeys:
			raise BadQueryConditions(qkey=key)
		
		values = codis[key]
		for value in values:
			where+='%s=%s or ' %(key,value)
		where=where[:-4]+' and '
	where=where[:-5]
	return where
	
	
def getDBInfo4All(db_session,codis=None):
	
	sql = 'select * from tcdb_tb'
	where=__getwherestr(codis, qkeys)
	if where:
		sql+=' where '+where
# 	if codis:
# 		qcodis = ' '
# 		from_date=codis.pop('from_date',None)
# 		to_date=codis.pop('to_date',None)
# 		if from_date and to_date:
# 			qcodis+='unix_timestamp(upload_date) between unix_timestamp("'+from_date+'") and unix_timestamp("'+to_date+'") and '
# 		elif not (not from_date and not to_date):
# 			raise DateException(date_selc='from_date or to_date can not be null!')
# 		
# 		for key in codis.iterkeys():
# 			if key not in qkeys:
# 				raise BadQueryConditions(qkey=key)
# 			value = codis[key]
# 			if value:
# 				qcodis+=key+'="'+value+'" and '
# 		qcodis=qcodis[:-5]
# 		sql +=' where'+qcodis
	
	
	sql+=' order by id'
	dbs_data = db_session.query(sql)
	dbs = []
	for db_data in dbs_data:
		db={}
		db['id']=db_data['id']
		db['dbname']=db_data['dbname']
		db['user_id']=db_data['user_id']
		db['user_name']=db_data['user_name']
		db['vm_id']=db_data['vm_id']
		db['db_username']=db_data['db_username']
		db['create_time']=db_data['create_time']
		db['expires']=db_data['expires']
		dbs.append(db)
	
	return dbs

def deleteDBInfo4ID(db_session,id,codis=None):
	sql = 'delete from tcdb_tb where id="%s" ' %id
# 	if codis:
# 		where=__getwherestr(codis, qkeys)
# 		if where:
# 			sql+='and '+where
	
	print sql
	db_session.delete(sql)
	


def updateDBInfo4ID(db_session,id,fileds=None):
	sql = 'update tcdb_tb set '
	if not fileds:return
	for key in fileds.keys():
		if key not in updatekeys:
			raise BadUpdateConditions(qkey=key)
		sql+='%s="%s",' %(key,fileds[key])
		#sql+= str(key)+'="'+str(fileds[key])+'",'
	sql = sql[:-1]
	sql+=' where id="%s"' %id
# 	print codis
# 	if codis:
# 		where=__getwherestr(codis, qkeys)
# 		if where:
# 			sql+=' and '+where
	db_session.update(sql)


def get_dbinfo_userid(db_session,id):
	sql = 'select user_id from tcdb_tb where id=%s' %id
	rs = db_session.query(sql)
	if not rs:return
	return rs[0]['user_id']

def get_dbinfo4id_all(db_session,id):
	sql = 'select * from tcdb_tb where id="%s"' %id
	rs = db_session.query(sql)
	if not rs:return
	return rs[0] 
	
