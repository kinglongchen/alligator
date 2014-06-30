import webob.dec
import webob.exc
import context
class HydrogenKeystoneContext(object):
    def __init__(self,app):
        self.app=app
    @webob.dec.wsgify
    def __call__(self,req):
        # Determine the user ID
        print req
        print "#####################3"
        user_id = req.headers.get('X_USER_ID')
        if not user_id:
            return webob.exc.HTTPUnauthorized()
        # Determine the tenant
        tenant_id = req.headers.get('X_PROJECT_ID')

        # Suck out the roles
        roles = [r.strip() for r in req.headers.get('X_ROLES', '').split(',')]

        # Human-friendly names
        #tenant_name = req.headers.get('X_PROJECT_NAME')
        user_name = req.headers.get('X_USER_NAME')

        # Use request_id if already set
        #req_id = req.environ.get(request_id.ENV_REQUEST_ID)
        ctx = context.Context(user_id, tenant_id, roles=roles,user_name=user_name)
        req.environ['hydrogen.context'] = ctx
        return self.app
    @classmethod
    def filter_factory(cls,global_conf,**kwargs):
       return cls
