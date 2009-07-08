# vim: ai ts=4 sts=4 et sw=4

import logging

from amat.lib.base import *

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
        return 'Hello World'
    
    def private(self):
        response.status = "401 Not authenticated"
        return "You are not authenticated"
    
    def signout(self):
        return "Successfully signed out!"
