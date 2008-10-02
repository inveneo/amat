# host.py - the AMAT data model for a HOST
# (c) Inveneo 2008

import string
from pylons import config

g = config['pylons.g']

class Host(object):
    """This object describes a Host out there in the world that wants to
    talk to the server."""

    def __init__(self, mac):
        """Create new, empty object"""
        assert type(mac) == int, 'mac is not int'
        self.mac = mac
        self.type = u'undefined'
        self.host = u'undefined'
        self.cust = u'undefined'
        self.desc = u'undefined'
        self.lat = 0.0
        self.lon = 0.0
        self.opperiod = u'undefined'
        self.username = u'undefined'
        self.password = u'undefined'
        self.port = g.SSHD_PORT

    # accessors - all return strings
    def get_mac(self):  return '%012x' % self.mac
    def get_type(self): return self.type
    def get_host(self): return self.host
    def get_cust(self): return self.cust
    def get_desc(self): return self.desc
    def get_geo(self):  return '%f,%f' % (self.lat, self.lon)
    def get_opperiod(self): return self.opperiod
    def get_username(self): return self.username
    def get_password(self): return self.password
    def get_port(self): return '%d' % self.port

    # mutators - all take unicode strings, or int, or nothing
    def set_type(self, tipe):
        assert type(tipe) == unicode, 'type: not unicode'
        tipe = tipe[0:g.SIZE_TYPE].lower()
        assert tipe in ['hub', 'station'], 'type: bad value'
        self.type = tipe

    def set_host(self, host):
        assert type(host) == unicode, 'host: not unicode'
        self.host = host[0:g.SIZE_HOST]

    def set_cust(self, cust):
        assert type(cust) == unicode, 'cust: not unicode'
        cust = cust[0:g.SIZE_CUST]
        self.cust = cust

    def set_desc(self, desc):
        assert type(desc) == unicode, 'desc: not unicode'
        self.desc = desc[0:g.SIZE_DESC]

    def set_geo(self, geo):
        assert type(geo) == unicode, 'geo: not unicode'
        if len(geo):
            parts = geo.split(',')
            self.lat = float(parts[0])
            self.lon = float(parts[1])
        else:
            self.lat = 0.0
            self.lon = 0.0

    def set_opperiod(self, opperiod):
        assert type(opperiod) == unicode, 'opperiod: not unicode'
        self.opperiod = opperiod[0:g.SIZE_OPPERIOD]

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
        return ('mac=%s\n'      % self.get_mac())  + \
               ('type=%s\n'     % self.get_type()) + \
               ('host=%s\n'     % self.get_host()) + \
               ('cust=%s\n'     % self.get_cust()) + \
               ('desc=%s\n'     % self.get_desc()) + \
               ('geo=%s\n'      % self.get_geo())  + \
               ('opperiod=%s\n' % self.get_opperiod()) + \
               ('username=%s\n' % self.get_username()) + \
               ('password=%s\n' % self.get_password()) + \
               ('port=%s\n'     % self.get_port())

