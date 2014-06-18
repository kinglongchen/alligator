#encoding: utf-8
#!/bin/python
from v1.controllers import Controller
import policy
from common import exceptions

class Hello(Controller):
	def index(self,req):
		#获得上下文对象context,该对象中保存了用户相关的信息
		context= req.environ['hydrogen.context']
		#构造target对象，该对象中保存了用户所请动作的一些信息，权限验证就是通过context和target的比较
		target = {'user_id':'01d0e60c32724ccc804252285c86d284','test_name':456}
		#action对象在这里，我认为是从配置文件里获得规则
		action = 'get_test_action'
		policy.init()
		try:
			policy.enforce(context,action,target)
		except Exception,e:
			return e.msg
		return "Hello world!!!"
	def show(self,req,id):
		return "Hello World!!!"+str(id)
	def echo_hello(self,req):
		return "echo_hello():Hello world!!!"
