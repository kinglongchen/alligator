#encoding: utf-8
'''
Created on 2014年6月16日

@author: sony
'''
from hydrogen.common.target import Target
import db
class SvTarget(Target):
	def _get_target_info(self,db_session,sv_id):
		#获得指定服务的user_id
		self.user_id=db.getSvUserID(db_session, sv_id)
	def _set_target_role(self,role):
		self.role=role
		
	@classmethod
	def svtarget_factory(cls,db_session,sv_id):
		cls=cls()
		cls._get_target_info(db_session, sv_id)
		return cls