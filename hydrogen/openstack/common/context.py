from openstack.common import uuidutils
class RequestContext(object):

    """Helper class to represent useful information about a request context.

    Stores information about the security context under which the user
    accesses the system, as well as additional request information.
    """

    def __init__(self, auth_token=None, user=None, tenant=None, is_admin=False,
                 read_only=False, show_deleted=False, request_id=None):
        self.auth_token = auth_token
        self.user = user
        self.tenant = tenant
        self.is_admin = is_admin
        self.read_only = read_only
        self.show_deleted = show_deleted
        if not request_id:
            request_id = generate_request_id()
        self.request_id = request_id

    def to_dict(self):
        return {'user': self.user,
                'tenant': self.tenant,
                'is_admin': self.is_admin,
                'read_only': self.read_only,
                'show_deleted': self.show_deleted,
                'auth_token': self.auth_token,
                'request_id': self.request_id}

def generate_request_id():
    return 'req-%s' % uuidutils.generate_uuid()
