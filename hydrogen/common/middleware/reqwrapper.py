from common.dbop import Mysql
import webob.dec
import webob.exc
class DBSessionWrapper(object):
	def __init__(self,app,kwargs):
		host = kwargs['host']
		user=kwargs['user']
		passwd = kwargs['passwd']
		db = kwargs['db']
		charset=kwargs['charset']
		self.db_session=Mysql()
		self.db_session.connect(host,user,passwd,db,charset)
		self.app=app
	@webob.dec.wsgify
	def __call__(self,req):
		#print req.environ
		req.environ['db_session']=self.db_session
		return self.app(req)
	@classmethod
	def factory(cls,global_conf,**kwargs):
		def wrapper(app):
			return DBSessionWrapper(app,kwargs)
		return wrapper
