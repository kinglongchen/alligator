#!/bin/python
from os import environ as env
import keystoneclient.v2_0.client as ksclient
keystone = ksclient.Client(auth_url=env['OS_AUTH_URL'],username=env['OS_USERNAME'],password=env['OS_PASSWORD'],tenant_name=env['OS_TENANT_NAME'])
#keystone2 =ksclient.Client()
#env['tokens']=keystone.auth_token
print keystone.auth_token
