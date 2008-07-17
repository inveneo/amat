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

        # see if there is a command for this client
        command = 'establish_tunnel'
        remote_port = 22
        local_port = 7004
        username = 'aX^^#ds'
        password = 'gb&*23zxncD'
        return 'command=%s\n'     % command + \
               'remote_port=%d\n' % remote_port + \
               'local_port=%d\n'  % local_port + \
               'username=%s\n'    % username + \
               'password=%s\n'    % password
