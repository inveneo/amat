# checkin.py - the AMAT data model for a CHECKIN
# (c) Inveneo 2008

from time import time
from pylons import config

g = config['pylons.g']
h = config['pylons.h']

class Checkin(object):

    def __init__(self, mac, status, temp=0.0):
        # id will be set by database
        self.tstamp = time()
        assert type(mac) == int, 'mac: not int'
        self.mac = mac
        self.set_status(status)
        self.set_temp(temp)

    # accessors - all return strings
    def get_id(self):     return '%d' % self.id
    def get_tstamp(self): return '%f' % self.tstamp
    def get_mac(self):    return h.mac_int_to_str(self.mac)
    def get_status(self): return '%s' % self.status
    def get_temp(self):   return '%f' % self.temp

    # mutators - each asserts the type it wants to see
    def set_mac(self, mac):
        assert type(mac) == int, 'mac: not int'
        self.mac = mac

    def set_status(self, status):
        assert type(status) == unicode, 'status: not unicode'
        status = status[0:g.SIZE_STATUS].lower()
        assert status in ['ok', 'shutdown'], 'status: bad value'
        self.status = status

    def set_temp(self, temp):
        assert type(temp) == float, 'temp: not float'
        self.temp = temp

    def __str__(self):
        return ('id=%s\n'     % self.get_id())     + \
               ('tstamp=%s\n' % self.get_tstamp()) + \
               ('mac=%s\n'    % self.get_mac())    + \
               ('status=%s\n' % self.get_status()) + \
               ('temp=%s\n'   % self.get_temp())

