# admin.py - controller for tunnel administration
# (c) Inveneo 2008

import logging

from amat.lib.base import *
from amat.model import Session, Host, Checkin, Tunnel

log = logging.getLogger(__name__)

class AdminController(BaseController):
    """This controller is for tunnel administration."""

    def index(self):
        """Perform join in a bonehead (but working) way."""
        hosts = [host for host in Session.query(Host).all()]
        c.rows = []
        for host in hosts:
            tunnel_q = Session.query(Tunnel)
            tunnel = tunnel_q.filter_by(mac=host.mac).one()
            c.rows.append((host, tunnel))
        return render('/admin.mako')
