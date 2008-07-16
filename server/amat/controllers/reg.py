import logging

from amat.lib.base import *
from amat.model import Session, Host

log = logging.getLogger(__name__)

class RegController(BaseController):

    def index(self):
        d = request.GET
        mac = int(d.get('mac'), 16)
        host_q = Session.query(Host)
        c.host = host_q.filter_by(mac=mac).first()
        if not c.host: c.host = Host(mac)
        c.host.set_type(d.get('type', ''))
        c.host.set_host(d.get('host', ''))
        c.host.set_cust(d.get('cust', ''))
        c.host.set_desc(d.get('desc', ''))
        c.host.set_geo(d.get('geo', ''))
        c.host.set_opperiod(d.get('opperiod', ''))
        Session.save_or_update(c.host)
        Session.commit()
        return render('/reg.mako')
