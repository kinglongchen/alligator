#!/bin/python
from v1 import wsgi
import controllers
class Public():
	def add_routes(self,mapper):
	#	controller = controllers.Tenant()
		#mapper.connect('/tenants',  
        #               controller=wsgi.Resource(controller),  
        #               action='get_projects_for_token',  
        #               conditions=dict(method=['GET'])) 
		mapper.resource('user','users',
						controller=wsgi.Resource(controllers.Register()))
