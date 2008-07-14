import logging

from amat.lib.base import *

log = logging.getLogger(__name__)

class RegController(BaseController):

    def index(self):
        dict = request.GET
        s = ''
        s += 'mac=%s\n' % dict.get('mac', '')
        s += 'type=%s\n' % dict.get('type', '')
        s += 'host=%s\n' % dict.get('host', '')
        s += 'cust=%s\n' % dict.get('cust', '')
        s += 'desc=%s\n' % dict.get('desc', '')
        s += 'geo=%s\n' % dict.get('geo', '')
        s += 'opperiod=%s\n' % dict.get('opperiod', '')
        return s
