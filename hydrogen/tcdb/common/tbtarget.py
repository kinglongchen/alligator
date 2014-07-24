#encoding: utf-8
'''
Created on 2014年6月16日

@author: sony
'''
from hydrogen.common.target import Target
from hydrogen.common.exceptions import NUllResourceIDException
import db
class TBTarget(Target):
	def _get_target_info(self,db_session,id):
		#获得指定服务的user_id
		self.user_id=db.get_dbinfo_userid(db_session, id)
		if not self.user_id:
			raise NUllResourceIDException(id=id)
	def _set_target_role(self,role):
		self.role=role
		
	@classmethod
	def tbtarget_factory(cls,db_session,sv_id):
		cls=cls()
		cls._get_target_info(db_session, sv_id)
		return cls