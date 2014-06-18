#!/bin/python
from paste.deploy import loadapp
import os
import sys
sys.path.append('..')
HOST = ''
PORT = 8089
config = "python_paste.ini"
appname = "common"
wsgi_app = loadapp("config:%s" % os.path.abspath(config), appname)
if __name__ == "__main__":
    from eventlet import api,wsgi
    print 'Starting up HTTP server on %s: %i..........' %(HOST,PORT)
    wsgi.server(api.tcp_listener((HOST,PORT)),wsgi_app)
    #server.serve_forever()
#   server.handle_request()
