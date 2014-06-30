#!/bin/python
from hydrogen.v1 import wsgi
import controllers
class Public():
	def add_routes(self,mapper):
		controller = controllers.Tenant()
		mapper.connect('/tenants',  
                       controller=wsgi.Resource(controller),  
                       action='get_projects_for_token',  
                       conditions=dict(method=['GET']))
		
		mapper.connect('/svs/policies',controller=wsgi.Resource(controllers.PolicyMan()),action='getAllPolicyInfo',conditions=dict(method=["GET"]))
		mapper.connect('/svs/{sv_id:\d+}/policies',controller=wsgi.Resource(controllers.PolicyMan()),action='getPolicy4SVID',conditions=dict(method=["GET"]))
		mapper.connect('/svs/{sv_id:\d+}/policies',controller=wsgi.Resource(controllers.PolicyMan()),action='addPolicy4SVID',conditions=dict(method=["POST"]))
		mapper.connect('/svs/{sv_id:\d+}/policies/{id:\d+}',controller=wsgi.Resource(controllers.PolicyMan()),action='deletePolicy4SVID',conditions=dict(method=["DELETE"]))
		mapper.connect('/svs/{sv_id:\d+}/policies/{id:\d+}',controller=wsgi.Resource(controllers.PolicyMan()),action='updatePolicy4SVID',conditions=dict(method=["PUT"]))
		
		mapper.resource('sv','svs',
						controller=wsgi.Resource(controllers.ServiceMan()))
		mapper.resource('argtype','argtypes',
                        controller=wsgi.Resource(controllers.ArgTypeMan()))
		
# 		mapper.resource('policy','policies',
# 					    controller=wsgi.Resource(controllers.PolicyMan()))
