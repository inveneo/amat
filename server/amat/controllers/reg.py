import logging

from amat.lib.base import *
from amat.model import Session, Host

log = logging.getLogger(__name__)

class RegController(BaseController):

    def index(self):
        d = request.GET
        try:
            mac = int(d['mac'], 16)
            assert mac == mac & 0xFFFFFFFFFFFF, 'mac: bad value'
        except:
            abort(400, 'Missing or invalid mac')

        # look for a record of this host, else start a new one
        host_q = Session.query(Host)
        c.host = host_q.filter_by(mac=mac).first()
        if not c.host:
            try:
                c.host = Host(mac)
            except Exception, e:
                abort(400, str(e))

        # update host attributes
        try:
            c.host.set_type(d['type'])
        except:
            abort(400, 'Missing or invalid type')
        try:
            c.host.set_host(d.get('host', u''))
        except:
            abort(400, 'Invalid host')
        try:
            c.host.set_cust(d.get('cust', u''))
        except:
            abort(400, 'Invalid cust')
        try:
            c.host.set_desc(d.get('desc', u''))
        except:
            abort(400, 'Invalid desc')
        try:
            c.host.set_geo(d.get('geo', u''))
        except:
            abort(400, 'Invalid geo')
        try:
            c.host.set_opperiod(d.get('opperiod', u''))
        except:
            abort(400, 'Invalid opperiod')

        # create or update the record
        Session.save_or_update(c.host)
        Session.commit()

        if d.has_key('debug'):
            return render('/reg.mako')
        return ''
