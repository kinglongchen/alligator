#!/bin/python
from v1 import wsgi
import controllers
class Public():
	def add_routes(self,mapper):
		controller = controllers.InfoManCtl()
		mapper.resource('application','applications',
						controller=wsgi.Resource(controllers.AppManCtl()))#AppManCtl
		mapper.resource('vm','vms',
						controller=wsgi.Resource(controllers.VMManCtl()))
		mapper.connect('/flavor_overview',  
                        controller=wsgi.Resource(controller),  
                        action='flavor',  
                        conditions=dict(method=['GET']))		
		