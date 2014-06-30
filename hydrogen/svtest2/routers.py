#!/bin/python
from v1 import wsgi
import controllers
class SV2Public():
	def add_routes(self,mapper):
		mapper.resource('test','tests',controller=wsgi.Resource(controllers.Hello()))
		#mapper.connect('/tests2/(.+)/(.+)',controller=wsgi.Resource(controllers.Hello()),action='echo_hello')
		mapper.connect('/tests2/{id:\d+}/{sv_id:\d+}',controller=wsgi.Resource(controllers.Hello()),action='echo_hello',conditions=dict(method=["GET"]))	
