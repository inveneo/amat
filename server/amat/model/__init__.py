from pylons import config
from sqlalchemy import Column, MetaData, Table, types
from sqlalchemy.orm import mapper, scoped_session, sessionmaker

Session = scoped_session(sessionmaker(autoflush=True, transactional=True,
    bind=config['pylons.g'].sa_engine))

metadata = MetaData()

host_table = Table('host', metadata,
        Column('mac',  types.Integer, primary_key=True), # MAC address
        Column('type', types.Unicode(10)),      # hub or station
        Column('host', types.Unicode(50)),      # hostname
        Column('cust', types.Unicode(100)),
        Column('desc', types.Unicode(300)),
        Column('lat',  types.Float),            # from geo
        Column('lon',  types.Float),            # from geo
        Column('opperiod', types.Unicode(180))) # up to ten entries

class Host(object):
    def __str__(self):
        return '<Host: %x>' % self.mac

mapper(Host, host_table)
