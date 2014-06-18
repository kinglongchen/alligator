#encoding: utf-8
'''
Created on 2014年6月16日

@author: sony
'''
class Target(object):
	def __init__(self):
		self.user_id=None
	def to_dict(self):
		dict={}
		if self.user_id:
			dict['user_id']=self.user_id
		return dict
	@classmethod
	def factory(cls):
		return cls()