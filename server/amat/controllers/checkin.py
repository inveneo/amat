# checkin.py - controller for clients checking in with server
# (c) Inveneo 2008

import logging

from amat.lib.base import *
from amat.model import Session, Host, Checkin, Tunnel

log = logging.getLogger(__name__)

class CheckinController(BaseController):
    """This controller is activated when a client host wants to check in
    and receive any commands from the server."""

    def index(self):
        # pull MAC address, the primary key, from query string
        d = request.GET
        try:
            mac = h.mac_str_to_int(d['mac'])
        except:
            abort(400, 'Missing or invalid mac')

        # look for a record of this host
        host_q = Session.query(Host)
        try:
            host = host_q.filter_by(mac=mac).one()
        except:
            abort(404, 'Not one host with this mac')

        # put checkin in the database
        status = None
        try:
            status = d['status']
            assert status in ['ok', 'shutdown']
        except:
            abort(400, 'Invalid status')

        temp = None
        try:
            temp = float(d.get('temp', u'0.0'))
        except:
            abort(400, 'Invalid temp')

        try:
            c.checkin = Checkin(mac, status, temp)
        except Exception, e:
            abort(400, 'Missing or invalid data: (%012x,%s,%s): "%s"' %
                    (mac, status, temp, str(e)))

        Session.save_or_update(c.checkin)
        Session.commit()

        # see if there is a command for this client
        tunnel_q = Session.query(Tunnel)
        tunnel = tunnel_q.filter_by(mac=mac).first()
        if tunnel:
            if tunnel.is_enabled():
                command = 'open_tunnel'
                server_port = int(tunnel.get_port())
                username = tunnel.get_username()
                password = tunnel.get_password()
                return 'command=%s\n'     % command + \
                       'server_port=%d\n' % server_port + \
                       'client_port=22\n' + \
                       'username=%s\n'    % username + \
                       'password=%s\n'    % password
            else:
                command = 'close_tunnel'
                return 'command=%s\n' % command
        return ''

