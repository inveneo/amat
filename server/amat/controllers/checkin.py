import logging

from amat.lib.base import *
from amat.model import Session, Host, Checkin

log = logging.getLogger(__name__)

class CheckinController(BaseController):

    def index(self):
        d = request.GET
        try:
            mac = int(d['mac'], 16)
            assert mac == mac & 0xFFFFFFFFFFFF, 'mac: bad value'
        except:
            abort(400, 'Missing or invalid mac')

        # look for a record of this host, else start a new one
        host_q = Session.query(Host)
        try:
            host = host_q.filter_by(mac=mac).one()
        except:
            abort(400, 'Not one host with this mac')

        # put it in the database
        try:
            c.checkin = Checkin(mac, d['status'])
        except:
            abort(400, 'Missing or invalid data')

        Session.save_or_update(c.checkin)
        Session.commit()

        # see if there is a command for this client
        command = 'establish_tunnel'
        server_port = int(host.get_port())
        client_port = 7004
        username = host.get_username()
        password = host.get_password()
        # host.set_password() ... switch password
        return 'command=%s\n'     % command + \
               'server_port=%d\n' % server_port + \
               'client_port=%d\n' % client_port + \
               'username=%s\n'    % username + \
               'password=%s\n'    % password
