from pylons import config
from sqlalchemy import Column, MetaData, Table, types
from sqlalchemy.orm import mapper, scoped_session, sessionmaker

SIZE_TYPE = 10
SIZE_HOST = 50
SIZE_CUST = 100
SIZE_DESC = 300
SIZE_PER = 18
SIZE_OPPERIOD = 10 * SIZE_PER

Session = scoped_session(sessionmaker(autoflush=True, transactional=True,
    bind=config['pylons.g'].sa_engine))

metadata = MetaData()

host_table = Table('host', metadata,
        Column('mac',  types.Integer, primary_key=True),  # MAC address
        Column('type', types.Unicode(SIZE_TYPE)),         # hub or station
        Column('host', types.Unicode(SIZE_HOST)),         # hostname
        Column('cust', types.Unicode(SIZE_CUST)),
        Column('desc', types.Unicode(SIZE_DESC)),
        Column('lat',  types.Float),                      # from geo
        Column('lon',  types.Float),                      # from geo
        Column('opperiod', types.Unicode(SIZE_OPPERIOD)))

class Host(object):

    def __init__(self, mac):
        """Create new, empty object"""
        assert(type(mac) == int)
        self.mac = mac
        self.set_type('')
        self.set_host('')
        self.set_cust('')
        self.set_desc('')
        self.set_geo('')
        self.set_opperiod('')

    # accessors - all return strings
    def get_mac(self):  return '%x' % self.mac
    def get_type(self): return self.type
    def get_host(self): return self.host
    def get_cust(self): return self.cust
    def get_desc(self): return self.desc
    def get_geo(self):  return '%f,%f' % (self.lat, self.lon)
    def get_opperiod(self): return self.opperiod

    # mutators - all take strings
    # XXX do better verification here
    def set_type(self, type): self.type = type[0:SIZE_TYPE]
    def set_host(self, host): self.host = host[0:SIZE_HOST]
    def set_cust(self, cust): self.cust = cust[0:SIZE_CUST]
    def set_desc(self, desc): self.desc = desc[0:SIZE_DESC]
    def set_geo(self, geo):
        parts = geo.split(',')
        self.lat = float(parts[0])
        self.lon = float(parts[1])
    def set_opperiod(self, opperiod): self.opperiod = opperiod[0:SIZE_OPPERIOD]

    def __str__(self):
        return ('mac=%s\n'      % self.get_mac()) + \
               ('type=%s\n'     % self.get_type()) + \
               ('host=%s\n'     % self.get_host()) + \
               ('cust=%s\n'     % self.get_cust()) + \
               ('desc=%s\n'     % self.get_desc()) + \
               ('geo=%s\n'      % self.get_geo()) + \
               ('opperiod=%s\n' % self.get_opperiod())

mapper(Host, host_table)
