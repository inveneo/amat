# admin.py - controller for tunnel administration
# (c) Inveneo 2008

import logging

from amat.lib.base import *
from amat.model import Session, Host, Checkin, Tunnel

log = logging.getLogger(__name__)

class AdminController(BaseController):
    """This controller is for tunnel administration."""

    def index(self):
        """Tunnel administration."""
        c.rows = []
        host_q = Session.query(Host)
        tunnel_q = Session.query(Tunnel)

        # walk through all known hosts
        for host in host_q.all():

            # find the tunnel record for this host
            tunnel = tunnel_q.filter_by(mac=host.mac).one()

            # update tunnel enabled flag (unless just arriving)
            if request.GET.has_key("update"):
                tunnel.set_enabled(request.GET.has_key(host.get_mac()))
            Session.save_or_update(tunnel)

            # build output for template
            enabled = ['','checked'][tunnel.enabled]
            c.rows.append((host, tunnel, enabled))

        Session.commit()
        return render('/admin.mako')
