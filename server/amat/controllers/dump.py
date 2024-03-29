# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

# dump.py - controller that dumps DB contents
# (c) Inveneo 2008

import logging

from amat.lib.base import *
from amat.lib.common import *
from amat.model import Session, Host, Checkin, Tunnel
from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import RemoteUser, ValidAuthKitUser, UserIn

log = logging.getLogger(__name__)

class DumpController(BaseController):
    """This controller is for debugging: it dumps the entire DB contents.
    Must be disabled in production version."""

    @authorize(UserIn(["admin"]))
    def index(self):
        c.hosts = [host for host in Session.query(Host).all()]
        c.tunnels = [tunnel for tunnel in Session.query(Tunnel).all()]
        c.checkins = [checkin for checkin in Session.query(Checkin).all()]
        return render('/dump.mako')

