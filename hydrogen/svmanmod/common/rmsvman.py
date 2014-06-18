# encoding: utf-8
'''
Created on 2014��6��11��

@author: sony
'''
import urllib2
import db
import vmmanmod_client
from MultiPartEncode import MultiPartEncode
class RmSVManClass(object):
	def __init__(self,db_session):
		self.db_session=db_session
		self.multipartencode=MultiPartEncode()
		
	def upload_file(self,vm_ip,contenttype,data):
		r = urllib2.Request("http://"+vm_ip+":8091/v1/filedeploy")
		r.add_unredirected_header('Content-Type',contenttype)
		r.add_data(data)
		u = urllib2.urlopen(r)
		return u

	def delete_file(self,vm_ip,sv_id):
		r = urllib2.Request("http://"+vm_ip+":8091/v1/fileundeploy/"+str(sv_id))
		return urllib2.urlopen(r)
		
		pass
	def addSv2Vm(self,vm_id,sv_id,sv_file,contenttype):
		sv_id=str(sv_id)
		vm_ip=vmmanmod_client.get_vm_ip(vm_id)
		sv_url = 'http://'+str(vm_ip)+":8091/v1/svs/"+str(sv_id)
		
		sv_filename=sv_id+"."+sv_file.filename.split('.')[-1].strip()
		boundary=contenttype.split(';')[-1].split("=")[-1].strip()
		sv_data = self.multipartencode.encode(sv_filename,sv_file,boundary)
		
		self.upload_file(vm_ip, contenttype, sv_data)
		return sv_url
		
	def deleteSvOnVM(self,db_session,id):
		#1.���id��÷�������vm
		#2.����Զ�̴���--һ��webServer--ɾ��Զ��vm�ϵķ������
		sv_vmip=db.getSvVmip(db_session, id)
		self.delete_file(sv_vmip,id)
		print 'delete sv On VM successuflly!!!'
		return 'ture'