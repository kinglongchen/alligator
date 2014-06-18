#encoding: utf-8
'''
Created on 2014年6月18日

@author: sony
'''
from hydrogen.common.exceptions import HydrogenException
class BaseSvModException(HydrogenException):
	pass
class BadUserIDException(BaseSvModException):
	message='a bad user'
class BadServiceIDException(BaseSvModException):
	message='Bad Service ID:%(sv_id)s'
class NoneServiceDataException(BaseSvModException):
	pass