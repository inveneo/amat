# tunnel.py - the AMAT data model for a TUNNEL
# (c) Inveneo 2008

import string
from pylons import config

g = config['pylons.g']
h = config['pylons.h']

class Tunnel(object):

    def __init__(self, mac):
        # id will be set by database
        assert type(mac) == int, 'mac: not int'
        self.mac = mac
        self.username = u'undefined'
        self.password = u'undefined'
        self.port = h.get_free_port()

    # accessors - all return strings
    def get_id(self):       return '%d' % self.id
    def get_mac(self):      return h.mac_int_to_str(self.mac)
    def get_username(self): return self.username
    def get_password(self): return self.password
    def get_port(self):     return '%d' % self.port

    # mutators - all take strings
    def set_mac(self, mac):
        assert type(mac) == int, 'mac: not int'
        self.mac = mac

    def set_username(self, username):
        assert type(username) == unicode, 'username: not unicode'
        self.username = username[0:g.SIZE_USER]

    def set_random_password(self):
        """No argument: always assigns random value."""
        # create string of 64 (2 ** 6) unique symbols to choose from
        passchars = string.letters + string.digits + ".-"
        self.password = u''
        fp = open('/dev/urandom', 'rb')
        # entropy is (nearly) 6 bits per symbol times SIZE_PASS symbols
        for i in range(g.SIZE_PASS):
            byte = ord(fp.read(1)) # get eight bits of nice randomness
            self.password += passchars[byte >> 2] # just use six of them
        fp.close()

    def set_port(self, port):
        assert type(port) == int, 'port: not int'
        self.port = port

    def __str__(self):
        return ('id=%s\n'     % self.get_id())     + \
               ('mac=%s\n'    % self.get_mac())    + \
               ('username=%s\n' % self.get_username()) + \
               ('password=%s\n' % self.get_password()) + \
               ('port=%s\n'     % self.get_port())

