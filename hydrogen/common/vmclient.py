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
# def request(*args,**kwargs):
# 	headers={'X-Auth-Token':keystone.auth_token}
# 	vm_id=kwargs['vm_id']
# 	requrl='http://%(ip)s:%(port)s/' %vmman_host+'v1/vms/'+vm_id
# 	resp,content=httpClient.request(requrl,'GET',headers=headers)
# 	return resp,content

def request(url,method,body=None,headers=None):
	req_headers={'X-Auth-Token':keystone.auth_token}
	if headers:
		req_headers.update(headers)
	resp,content = httpClient.request(url,method=method,body=body,headers=req_headers)
	return resp,content
		
	
def get_vm_ip(vm_id):
# 	url='http://%(ip)s:%(port)s/' %vmman_host+'v1/vms/'+vm_id
# 	resp,content = request(url,'GET')
# 	decodejson=json.loads(content)
# 	vm_ip = decodejson['show'][0]['vm_ip']
	vm_ip='192.168.0.13'
	return vm_ip

def get_vm_name(vm_id):
	#resp,content=request(vm_id=vm_id)
	
	
	url='http://%(ip)s:%(port)s/' %vmman_host+'v1/vms/'+vm_id
	resp,content = request(url,'GET')
	decodejson=json.loads(content)
	vm_name = decodejson['show'][0]['vm_name']
	return vm_name
	
def get_vmid_via_user_id(user_id):
	url_map=vmman_host.copy()
	url_map.update({'user_id':user_id})
	url='http://%(ip)s:%(port)s/v1/vms?user_id=%(user_id)s' %url_map
	#body={'user_id':user_id}
	resp,content = request(url,'GET')
	vms = json.loads(content)
	vm_ids=[]
	for vm in vms['vms']:
		vm_ids.append(vm['vm_id'])
	return vm_ids
		 
#print get_vm_ip('4f7b2604-e062-450a-be81-dca6b8eab58a')
#print get_vmid_via_user_id('52358781a2514a6cbaf5482e853d14ef')
#print get_vm_ip('05c1609f-de4d-4c87-8bec-b4716974a18e')

