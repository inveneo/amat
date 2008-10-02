# __init__.py - the AMAT data model
# (c) Inveneo 2008

from pylons import config
from sqlalchemy import types, MetaData, Column, Table, ForeignKey
from sqlalchemy.orm import mapper, scoped_session, sessionmaker
from host import Host
from checkin import Checkin

g = config['pylons.g']

Session = scoped_session(sessionmaker(autoflush=True, transactional=True,
    bind=g.sa_engine))

metadata = MetaData()

host_table = Table('host', metadata,
        Column('mac',      types.Integer, primary_key=True),  # MAC address
        Column('type',     types.Unicode(g.SIZE_TYPE)),       # hub or station
        Column('host',     types.Unicode(g.SIZE_HOST)),       # hostname
        Column('cust',     types.Unicode(g.SIZE_CUST)),
        Column('desc',     types.Unicode(g.SIZE_DESC)),
        Column('lat',      types.Float),                      # from geo
        Column('lon',      types.Float),                      # from geo
        Column('opperiod', types.Unicode(g.SIZE_OPPERIOD)),
        Column('username', types.Unicode(g.SIZE_USER)),
        Column('password', types.Unicode(g.SIZE_PASS)),
        Column('port',     types.Integer))

checkin_table = Table('checkin', metadata,
        Column('id',     types.Integer, primary_key=True),  # auto generated
        Column('mac',    types.Integer, ForeignKey('host.mac')),
        Column('status', types.Unicode(g.SIZE_STATUS)),
        Column('tstamp', types.Float))

mapper(Host, host_table)
mapper(Checkin, checkin_table)

