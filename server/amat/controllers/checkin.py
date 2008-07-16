import logging

from amat.lib.base import *
from amat.model import Session, Checkin

log = logging.getLogger(__name__)

class CheckinController(BaseController):

    def index(self):
        d = request.GET
        try:
            mac = int(d.get('mac'), 16)
        except:
            abort(400, 'Missing or invalid mac')
        status = d.get('status', '')

        # put it in the database
        try:
            c.checkin = Checkin(mac, status)
        except:
            abort(400, 'Invalid data')

        Session.save_or_update(c.checkin)
        Session.commit()

        return render('/checkin.mako')
