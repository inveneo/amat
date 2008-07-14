import logging

from amat.lib.base import *

log = logging.getLogger(__name__)

class CheckinController(BaseController):

    def index(self):
        dict = request.GET
        s = ''
        s += 'mac=%s\n' % dict.get('mac', '')
        s += 'status=%s\n' % dict.get('status', '')
        return s
