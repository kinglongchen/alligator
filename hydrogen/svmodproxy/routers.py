#!/bin/python
from v1 import wsgi
import controllers
class SV2Public():
	def add_routes(self,mapper):
		#mapper.resource('test','tests',controller=wsgi.Resource(controllers.Hello()))
		mapper.connect('/filedeploy',controller=wsgi.Resource(controllers.VMSVManProxy()),action='fileDeploy')	
		mapper.connect('/fileundeploy/{id}',controller=wsgi.Resource(controllers.VMSVManProxy()),action='fileUndeploy')