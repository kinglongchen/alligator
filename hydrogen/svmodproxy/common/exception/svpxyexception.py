'''
Created on 2014年6月15日

@author: sony
'''
class NoServiceException(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)