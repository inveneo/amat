# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

# admin.py - controller for tunnel administration
# (c) Inveneo 2008

import logging

from amat.lib.base import *
from amat.lib.common import *
from amat.model import Session, Host, Tunnel, Checkin
from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn

log = logging.getLogger(__name__)

class AdminController(BaseController):
    """This controller is for tunnel administration."""
    
    @authorize(UserIn(["admin"]))
    def index(self):
        """Tunnel administration."""
        c.rows = []
        host_q = Session.query(Host)
        tunnel_q = Session.query(Tunnel)
        checkin_q = Session.query(Checkin)

        # walk through all known hosts
        for host in host_q.all():

            # find the tunnel record for this host
            tunnel = tunnel_q.filter_by(mac=host.mac).one()

            # update tunnel enabled flag (unless just arriving)
            if request.POST.has_key("update"):
                if request.POST.has_key(host.get_mac()):
                    tunnel.set_port(h.get_free_port())
                    tunnel.set_enabled(True)
                else:
                    tunnel.set_port(0)
                    tunnel.set_enabled(False)
                Session.save_or_update(tunnel)

            # find most recent checkin, if any
            checkins = checkin_q.filter_by(mac=host.mac)
            latest = checkins.order_by(Checkin.tstamp.desc()).first()
            temp = latest.temp
            tstamp = latest.tstamp
            blurb = secs_to_blurb(tstamp)

            # build output for template
            enabled = ['','checked'][tunnel.enabled]
            c.rows.append((host.get_mac(), enabled, tunnel.get_port(),
                host.get_type(), host.get_host(), host.get_cust(),
                host.get_desc(), tstamp, blurb, temp))

        Session.commit()
        return render('/admin.mako')

