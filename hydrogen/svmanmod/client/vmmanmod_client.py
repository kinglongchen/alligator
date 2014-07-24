#encoding: utf-8
import httplib2
import keystoneclient.v2_0.client as ksclient
import json
auth_url='http://controller:35357/v2.0';
username='admin';
password='ADMIN_PASS';
tenant_name='admin';
keystone = ksclient.Client(auth_url=auth_url,username=username,password=password,tenant_name=tenant_name)
httpClient=httplib2.Http()

vmman_host={'ip':'192.168.0.13','port':'8089'}
def request(*args,**kwargs):
	headers={'X-Auth-Token':keystone.auth_token}
	vm_id=kwargs['vm_id']
	requrl='http://%(ip)s:%(port)s/' %vmman_host+'v1/vms/'+vm_id
	resp,content=httpClient.request(requrl,'GET',headers=headers)
	return resp,content
def get_vm_ip(vm_id):
	#resp,content=request(vm_id=vm_id)
	#decodejson=json.loads(content)
	#print decodejson['show'][0]['vm_ip']
	#��дjson�����ݣ���ȡip
	#vm_ip = decodejson['show'][0]['vm_ip']
	vm_ip='192.168.0.13'
	return vm_ip
def get_vm_name(vm_id):
	resp,content=request(vm_id=vm_id)
	decodejson=json.loads(content)
	vm_ip = decodejson['show'][0]['vm_name']
#print get_vm_ip('4f7b2604-e062-450a-be81-dca6b8eab58a')


