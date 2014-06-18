#!/bin/python
from v1.controllers import Controller
import policy
from common import exceptions
from common import svfileman
import cgi
import os
class VMSVManProxy(Controller):
	def index(self,req):
		context= req.environ['hydrogen.context']
		target = {'tenant_id':'2f11cefc7b1940bfb41598c70ae3bdf2','test_name':456}
		action = 'get_test_action'
		policy.init()
		try:
			policy.enforce(context,action,target)
		except Exception,e:
			return e.msg
		return "Hello world!!!"
	def show(self,req,id):
		return "Hello World!!!"+str(id)
	def fileDeploy(self,req):
		environ = req.environ
		fileds=cgi.FieldStorage(environ["wsgi.input"],environ=environ)
		sv_file = fileds['svfile'].value
		sv_filename=fileds['svfile'].filename
		svfileman.svFileSave(sv_filename, sv_file)
		return 'true'
	
	def fileUndeploy(self,req,id):
		svfileman.svFileDelete(id)
		return 'true'