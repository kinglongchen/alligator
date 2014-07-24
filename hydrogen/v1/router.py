#!/bin/python
import wsgi
import hydrogen.svtest.routers
import hydrogen.svtest2.routers
import hydrogen.svmanmod.routers
import hydrogen.auths.routers
import hydrogen.vmmanmod.routers
import hydrogen.tcdb.routers
class ControllerTest(object):
    def __init__(self):
        print "ControllerTest!!!!"
    def test(self,req):
          print "req",req
          return {
            'name': "test",
            'properties': "test"
        }

class MyRouterApp(wsgi.Router):
      '''
      app
      '''
      def __init__(self,mapper):
          controller = ControllerTest()
          mapper.connect('/test',
                       controller=wsgi.Resource(controller),
                       action='test',
                       conditions={'method': ['GET']})
          super(MyRouterApp, self).__init__(mapper)

#@fail_gracefully
def auth_app_factory(global_conf, **local_conf):
    #controllers.register_version('v2.0')
    #conf = global_conf.copy()
    #conf.update(local_conf)
    return wsgi.ComposingRouter(wsgi.APIMapper(),
                               [hydrogen.svtest.routers.Public(),
                                hydrogen.svtest2.routers.SV2Public(),
                                hydrogen.vmmanmod.routers.Public(),
                                hydrogen.svmanmod.routers.Public(),
                                hydrogen.tcdb.routers.Public()])
                               #token.routers.Router(),
                               #routers.VersionV2('public'),
                               #routers.Extension(False)])
def public_app_factory(global_conf,**local_conf):
    return wsgi.ComposingRouter(wsgi.APIMapper(),
                                [hydrogen.auths.routers.Public()])
