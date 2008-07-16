import logging

from amat.lib.base import *
from amat.model import Session, Host, Checkin

log = logging.getLogger(__name__)

class DumpController(BaseController):

    def index(self):
        c.hosts = [host for host in Session.query(Host).all()]
        c.checkins = [checkin for checkin in Session.query(Checkin).all()]
        return render('/dump.mako')
