from pylons import config
from sqlalchemy import Column, MetaData, Table, types, ForeignKey
from sqlalchemy.orm import mapper, scoped_session, sessionmaker
from time import time

SIZE_TYPE = 10
SIZE_HOST = 50
SIZE_CUST = 100
SIZE_DESC = 300
SIZE_PER = 18
SIZE_OPPERIOD = 10 * SIZE_PER
SIZE_STATUS = 8

Session = scoped_session(sessionmaker(autoflush=True, transactional=True,
    bind=config['pylons.g'].sa_engine))

metadata = MetaData()

class Host(object):

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

    # accessors - all return strings
    def get_mac(self):  return '%x' % self.mac
    def get_type(self): return self.type
    def get_host(self): return self.host
    def get_cust(self): return self.cust
    def get_desc(self): return self.desc
    def get_geo(self):  return '%f,%f' % (self.lat, self.lon)
    def get_opperiod(self): return self.opperiod

    # mutators - all take strings
    def set_type(self, tipe):
        assert type(tipe) == unicode, 'type: not unicode'
        tipe = tipe[0:SIZE_TYPE].lower()
        assert tipe in ['hub', 'station'], 'type: bad value'
        self.type = tipe

    def set_host(self, host):
        assert type(host) == unicode, 'host: not unicode'
        host = host[0:SIZE_HOST]
        self.host = host

    def set_cust(self, cust):
        assert type(cust) == unicode, 'cust: not unicode'
        cust = cust[0:SIZE_CUST]
        self.cust = cust

    def set_desc(self, desc):
        assert type(desc) == unicode, 'desc: not unicode'
        desc = desc[0:SIZE_DESC]
        self.desc = desc

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
        opperiod = opperiod[0:SIZE_OPPERIOD]
        self.opperiod = opperiod

    def __str__(self):
        return ('mac=%s\n'      % self.get_mac())  + \
               ('type=%s\n'     % self.get_type()) + \
               ('host=%s\n'     % self.get_host()) + \
               ('cust=%s\n'     % self.get_cust()) + \
               ('desc=%s\n'     % self.get_desc()) + \
               ('geo=%s\n'      % self.get_geo())  + \
               ('opperiod=%s\n' % self.get_opperiod())

class Checkin(object):

    def __init__(self, mac, status):
        # id will be set by database
        self.tstamp = time()
        assert type(mac) == int, 'mac: not int'
        self.mac = mac
        self.set_status(status)

    # accessors - all return strings
    def get_id(self):     return '%d' % self.id
    def get_tstamp(self): return '%f' % self.tstamp
    def get_mac(self):    return '%x' % self.mac
    def get_status(self): return '%s' % self.status

    # mutators - all take strings
    def set_mac(self, mac):
        assert type(mac) == int, 'mac: not int'
        self.mac = mac

    def set_status(self, status):
        assert type(status) == unicode, 'status: not unicode'
        status = status[0:SIZE_STATUS].lower()
        assert status in ['ok', 'shutdown'], 'status: bad value'
        self.status = status

    def __str__(self):
        return ('id=%s\n'     % self.get_id())     + \
               ('tstamp=%s\n' % self.get_tstamp()) + \
               ('mac=%s\n'    % self.get_mac())    + \
               ('status=%s\n' % self.get_status())

host_table = Table('host', metadata,
        Column('mac',      types.Integer, primary_key=True),  # MAC address
        Column('type',     types.Unicode(SIZE_TYPE)),         # hub or station
        Column('host',     types.Unicode(SIZE_HOST)),         # hostname
        Column('cust',     types.Unicode(SIZE_CUST)),
        Column('desc',     types.Unicode(SIZE_DESC)),
        Column('lat',      types.Float),                      # from geo
        Column('lon',      types.Float),                      # from geo
        Column('opperiod', types.Unicode(SIZE_OPPERIOD)))

checkin_table = Table('checkin', metadata,
        Column('id',     types.Integer, primary_key=True),  # auto generated
        Column('mac',    types.Integer, ForeignKey('host.mac')),
        Column('status', types.Unicode(SIZE_STATUS)),
        Column('tstamp', types.Float))

mapper(Host, host_table)
mapper(Checkin, checkin_table)

