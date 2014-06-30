#encoding: utf-8
'''
Created on 2014��6��24��

@author: sony
'''
import logging
log_path='/var/log/cessas/msg.log'
#log_path='c:\\log\\ceeas\\msg.log'
logger = logging.getLogger(__name__)
#fmt = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
file_handler=logging.FileHandler(log_path)
file_handler.setLevel(1)
#file_handler.setFormatter(fmt)
logger.addHandler(file_handler)
logger.setLevel(1)
logger.debug('###################STARTING################################')
#print 'OK!!!'
