# encoding: utf-8
'''
Created on 2014年6月14日

@author: sony
'''
import os
from exception.svpxyexception import NoServiceException
SERVICE_FILE_PATH=''
def fileSave(filename,filedata):
		f=file(SERVICE_FILE_PATH+filename,'w')
		f.write(filedata)
		f.close()
		
def fileDelete(filename):
	os.remove(filename)

def svFileSave(svname,svdata):
	return fileSave(svname,svdata)

def svFileDelete(id):
	flist=os.listdir(SERVICE_FILE_PATH)
	filenamelist=[f for f in flist if f[str(id)]>=0]
	if not filenamelist:
		raise NoServiceException('No Service file')
	filename=filenamelist[0]
	fileDelete(filename)