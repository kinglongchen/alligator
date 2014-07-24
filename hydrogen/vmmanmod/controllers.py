#!/bin/python
#encoding: utf-8
from v1.controllers import Controller
import json
import types
import shutil
import sys
import time
import novaclient.v1_1.client as nvclient
from novaclient import base
from os import environ as env



client = nvclient.Client(auth_url="http://controller:35357/v2.0",username="admin",api_key="ADMIN_PASS",project_id="admin")
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

class ComplexEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, complex):
                return [obj.real, obj.imag]
            return json.JSONEncoder.default(self, obj)
    
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


#class AppManCtl
class AppManCtl(Controller):
	def __init__(self): 
		print ""
	def index(self,req):
		#show the all application for admin
		db_session=req.environ['db_session']
		D={}
		l=[]
		rs=db_session.query('select * from vm_post')
		for r in rs:
			d={}
			d['user_id']=r['user_id']
			d['floavr_id']=r['floavr_id']
			d['use_begin']=r['use_begin']
			d['use_end']=r['use_end']
			d['image_id']=r['image_id']
			d['vm_name']=r['vm_name']
			d['vm_numb']=r['vm_numb']
			d['user_reason']=r['user_reason']
			d['user_request']=r['user_request']
			d['user_role_id']=r['user_role_id']
			d['application_id']=r['application_id']
			l.append(d)
		D['key01']=l
		return D
	
	#def show(self,req,id):
	def create(self,req,body):
		#send the application to server and database
		db_session=req.environ['db_session']
		f_id=body['floavr_id']
		u_begin=body['use_begin']
		u_end=body['use_end']
		i_id=body['image_id']
		v_name=body['vm_name']
		v_num=body['vm_num']
		a_id=body['application_id']
		command= 'insert into vm_post values("","'+str(f_id)+'","'+str(u_begin)+'","'+str(u_end)+'","'+str(i_id)+'","'+str(v_name)+'","'+str(v_num)+'","","","","'+str(a_id)+'")'
		rs=db_session.insert(command)
		return 'application succeed!'
		
		#return jsonDumpsIndentStr
		#for r in rs:
		   #return r['vm_usetime']
		   #return int(rs[0]) > 0
		   # continue
	#
	def delete(self,req,id):
		db_session=req.environ['db_session']
		a_id=body['application_id']
		command= 'delete from vm_post where application_id='+str(a_id)
		rs=db_session.insert(command)
		return 'delete application success!'	 
	
	



class VMManCtl(Controller):
	def index(self,req):
		#select all vm overview
		#��ѯ�����������Ϣ
		#GET url:ip:prot/v1/vms
		db_session=req.environ['db_session']
		D={}
		l=[]
		rs=db_session.query('select * from vm_overview')
		for r in rs:
			d={}
			d['vm_id']=r['vm_id']
			d['user_id']=r['user_id']
			d['vm_name']=r['vm_name']
			d['vm_begin']=r['vm_begin']
			d['vm_end']=r['vm_end']
			d['user_role']=r['user_role']
			d['vm_type']=r['vm_type']
			d['vm_ip']=r['vm_ip']
			l.append(d)
		D['vms']=l
		return D
	
	def show(self,req,id):
		#show the user`s vm overview
		#��ѯָ�����������Ϣ
		#GET url:ip:port/v1/vms/id
		db_session=req.environ['db_session']
		D={}
		l=[]
		v_id=id
		command= 'select * from vm_overview where vm_id="'+str(v_id)+'"'
		rs=db_session.query(command)	
		for r in rs:
			d={}
			d['vm_id']=r['vm_id']
			d['user_id']=r['user_id']
			d['vm_begin']=r['vm_begin']
			d['vm_end']=r['vm_end']
			d['user_role']=r['user_role']
			d['vm_type']=r['vm_type']
			d['vm_ip']=r['vm_ip']
			l.append(d)
		D['show']=l
#		print D
		return D
	
	def create(self,req,body):
		#create a vm with application id
		#����������ķ���
		#POST url:ip:port/v1/vms
		db_session=req.environ['db_session']
		a_id=body['application_id']
		command01= 'select floavr_id,image_id,vm_name,use_begin,use_end from vm_post where application_id='+str(a_id)
		rs01=db_session.query(command01)
		l=[]
		for r in rs01:
			d={}
			d['f_id']=r['floavr_id']
			d['i_id']=r['image_id']
			d['v_name']=r['vm_name']
			d['u_begin']=r['use_begin']
			d['u_end']=r['use_end']
			l.append(d)
		F_id=l[0]['f_id']
		I_id=l[0]['i_id']
		V_name=l[0]['v_name']
		U_begin=l[0]['u_begin']
		U_end=l[0]['u_end'] 
		image1= client.images.get(str(I_id))#get imgae_id
		print image1
		flavor = client.flavors.get(str(F_id))#get floavor_id
		network = client.networks.get('200d8927-6d52-49c9-9808-69ce07186174')
		net_id=base.getid(network)
		nic_info={'net-id':net_id}
		nics=[]
		nics.append(nic_info)
		servers=client.servers.create(V_name,image1,flavor,nics=nics)
		#adding floating ip:
		time.sleep(5)
		floating_ip = client.floating_ips.create(pool='ex-net')
		servers.add_floating_ip(floating_ip)
		vm_id = base.getid(servers)
		floating_ip_database = floating_ip.ip
		#insert to database:
		command02= 'insert into vm_overview values("'+str(vm_id)+'","","'+str(U_begin)+'","'+str(U_end)+'","","","'+str(floating_ip_database)+'","'+str(V_name)+'")'
		rs02=db_session.insert(command02)
		get_result = 'create vm succeed'
		return get_result

	def delete(self,req,id):
		#delte a vm with vm id
		#�����ɾ��
		#DELETE url:ip:port/v1/vms/id
		db_session=req.environ['db_session']
		v_id=id
		command= 'delete from vm_overview where vm_id='+str(a_id)
		rs=db_session.insert(command)
		return 'delete application success!'
	
	def update(self,req,id,body):
		#change the name of vm
		#�޸�ָ���������
		#PUT url:ip:port/v1/vms/id
		db_session=req.environ['db_session']
		v_name=body['vm_name']
		a_id=body['application_id']
		command= 'update vm_post set vm_name="'+str(v_name)+'" where application_id='+str(a_id)
		rs=db_session.insert(command)	
		return 'vm name change success!'
	

class InfoManCtl(Controller):	
#	def __init__(self,body):
#		pass
	
	def flavor(self,req):
		l = []
		for i in range(0,5):
			a = client.flavors.list()[i].__dict__
#			print a
			l.append(a)
		return l
	
	
	def image(self,req):
		pass
	
class TestDemo2(Controller):
	def __init__(self):
		print "ListName!!!"
	def index(self,req):
		db_session=req.environ['db_session']
		rs=db_session.insert('select * from vm_post')
		for r in rs:
			print r['vm_usetime']
		return "list all resources"
	def show(self,req,id):
		print "START"
		print id
		print "END"
		return "Have id"+id
	
	

