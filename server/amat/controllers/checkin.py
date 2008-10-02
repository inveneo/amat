# checkin.py - controller for clients checking in with server
# (c) Inveneo 2008

import logging

from amat.lib.base import *
from amat.model import Session, Host, Checkin

log = logging.getLogger(__name__)

class CheckinController(BaseController):

    def index(self):
        d = request.GET
        try:
            mac = h.mac_str_to_int(d['mac'])
        except:
            abort(400, 'Missing or invalid mac')

        # look for a record of this host, else start a new one
        host_q = Session.query(Host)
        try:
            host = host_q.filter_by(mac=mac).one()
        except:
            abort(400, 'Not one host with this mac')

        # put it in the database
        status = d['status']
        try:
            c.checkin = Checkin(mac, status)
        except Exception, e:
            abort(400, 'Missing or invalid data: (%012x,%s): "%s"' %
                    (mac, status, str(e)))

        Session.save_or_update(c.checkin)
        Session.commit()

        # see if there is a command for this client
        command = 'establish_tunnel'
        server_port = int(host.get_port())
        client_port = 7004
        username = host.get_username()
        password = host.get_password()
        # host.set_random_password() ... switch password
        return 'command=%s\n'     % command + \
               'server_port=%d\n' % server_port + \
               'client_port=%d\n' % client_port + \
               'username=%s\n'    % username + \
               'password=%s\n'    % password
