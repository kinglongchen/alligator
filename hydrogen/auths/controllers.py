#/bin/python
from v1.controllers import Controller
from os import environ as env
import keystoneclient.v2_0.client as ksclient
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
class Register(Controller):
	def __init__(self):
		self.keystone=ksclient.Client(auth_url="http://controller:35357/v2.0",username="admin",password="ADMIN_PASS",tenant_name="admin")
		self.users=self.keystone.users
		self.roles=self.keystone.roles
		print "keystoneclient initialization successfully!"
	def index(self,req):
		is_exit = "false"
		user_name=req.GET['user_name']
		user_list=self.users.list()
		for user in user_list:
			#print user.name
			if user.name == user_name:
				is_exit = "true"
				#print user.name
				break
		return is_exit
	def show(self,req,id):
		print "START"
		print id
		print "END"
		return "Have id"+id
	def create(self,req,body=None):
		username=body['user_name']
		userpasswd=body['user_pw']
		useremail=body['user_email']
		role=body['role']
		#demo role id:
		#default role:nuser
		role_id="d0fd3717e94b41b1aed9856afa874a66"
		if role=="dev":
			role_id="2dcb04801b0c484faecd07ba066925a5"
		#demo tenant id:
		tenant_id="2f11cefc7b1940bfb41598c70ae3bdf2"
		user=self.users.create(username,userpasswd,useremail)
		#print resp
		self.roles.add_user_role(user,role_id,tenant_id)
		return "create user successfully!!!"
