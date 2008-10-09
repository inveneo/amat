# reg.py - controller that registers new clients
# (c) Inveneo 2008

import logging

from amat.lib.base import *
from amat.model import Session, Host

log = logging.getLogger(__name__)

class RegController(BaseController):

    def index(self):
        d = request.GET
        try:
            mac = h.mac_str_to_int(d['mac'])
        except:
            abort(400, 'Missing or invalid mac')

        # look for a record of this host, else start a new one
        host_q = Session.query(Host)
        c.host = host_q.filter_by(mac=mac).first()
        if c.host:
            c.host.brand_new = False
        else:
            try:
                c.host = Host(mac)
                c.host.brand_new = True
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
        username = None
        try:
            username = h.mac_int_to_username(mac)
        except Exception, e:
            abort(400, 'Invalid username: "0x%x": %s' % (mac, str(e)))
        try:
            c.host.set_username(username)
        except:
            abort(400, 'Invalid username: "%s"' % username)
        try:
            c.host.set_random_password()
        except:
            abort(400, 'Invalid password')
        try:
            c.host.set_port(h.get_free_port())
        except:
            abort(400, 'Invalid port')

        if c.host.brand_new:
            retcode = h.admit_to_jail(c.host.get_username(), c.host.get_host())
            if retcode:
                abort(500, '%d' % retcode)
            h.set_password(str(c.host.get_username()),
                    str(c.host.get_password()))

        # create or update the record
        Session.save_or_update(c.host)
        Session.commit()

        if d.has_key('debug'):
            return render('/reg.mako')
        return ''
