# Copyright 2011 VMware, Inc
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Hydrogen base exception handling.
"""

from openstack.common import excutils

class HydrogenException(Exception):
    """Base Hydrogen Exception.

    To correctly use this class, inherit from it and define
    a 'message' property. That message will get printf'd
    with the keyword arguments provided to the constructor.
    """
    message = "An unknown exception occurred."

    def __init__(self, **kwargs):
        try:
            super(HydrogenException, self).__init__(self.message % kwargs)
            self.msg = self.message % kwargs
        except Exception:
            with excutils.save_and_reraise_exception() as ctxt:
                if not self.use_fatal_exceptions():
                    ctxt.reraise = False
                    # at least get the core message out if something happened
                    super(HydrogenException, self).__init__(self.message)

    def __unicode__(self):
        return unicode(self.msg)

    def use_fatal_exceptions(self):
        return False


class BadRequest(HydrogenException):
    message = 'Bad %(resource)s request: %(msg)s'


class NotFound(HydrogenException):
    pass


class Conflict(HydrogenException):
    pass


class NotAuthorized(HydrogenException):
    message = "Not authorized."


class ServiceUnavailable(HydrogenException):
    message = "The service is unavailable"


class AdminRequired(NotAuthorized):
    message = "User does not have admin privileges: %(reason)s"


class PolicyNotAuthorized(NotAuthorized):
    message = "Policy doesn't allow %(action)s to be performed."


class PolicyFileNotFound(NotFound):
    message = "Policy configuration policy.json could not be found"


class PolicyInitError(HydrogenException):
    message = "Failed to init policy %(policy)s because %(reason)s"


class PolicyCheckError(HydrogenException):
    message = "Failed to check policy %(policy)s because %(reason)s"

