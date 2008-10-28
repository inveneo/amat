#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tunnel.py - library for managing SSH tunnels
# (c) Inveneo 2008

import sys
from subprocess import Popen, PIPE, check_call

############
# CONSTANTS
############

SSH     = '/usr/bin/ssh'
SSHPASS = '/usr/bin/sshpass'
KILL    = '/bin/kill'

CLIENT_PORT = 22

############
# FUNCTIONS
############

def firstTunnelPID(server, username):
    """Return process ID of first tunnel found, else None."""
    user_host = '%s@%s' % (username, server)
    procs = Popen(['ps', '-opid,args='], stdout=PIPE).communicate()[0]
    match_items = [SSHPASS, SSH, user_host]

    # skip first line, as it's a heading, but scan all others for tunnel
    for line in procs.split('\n')[1:]:
        count = 0
        tokens = line.split()
        for token in tokens:
            if token in match_items:
                count += 1
        if count == len(match_items):
            return int(tokens[0])
    return None

def openTunnel(server, username, password, server_port):
    """Open tunnel: all params are strings except server_port (int)."""
    port_host_port = '%d:localhost:%d' % (server_port, CLIENT_PORT)
    user_host = '%s@%s' % (username, server)
    command_list = [SSHPASS, '-p', password] + \
    [SSH, '-C', '-g', '-N',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'ServerAliveInterval=10',
            '-o', 'ServerAliveCountMax=3',
            '-R', port_host_port, user_host]
    Popen(command_list)

def closeTunnel(server, username):
    """Close tunnel: kill all tunnel processes."""
    pid = firstTunnelPID(server, username)
    while pid:
        check_call([KILL, str(pid)])
        pid = firstTunnelPID(server, username)

if __name__ == '__main__':
    """Test this puppy by simply toggling tunnel on and off."""
    if len(sys.argv) < 3:
        print 'Usage: %s server username [password server_port]' % sys.argv[0]
        sys.exit(1)

    server   = argv[1] # e.g. "bb.inveneo.net"
    username = argv[2] # e.g. "_000000004321"

    if not tunnel.firstTunnelPID(server, username):
        if len(sys.argv) < 5:
            print 'Need username and password to open tunnel.'
            sys.exit(1)

        password    = argv[3] # e.g. "IDAwvKwRhM4.7EL7yUYCsnn6-p.ke4hG"
        server_port = argv[4] # e.g. "56137"

        print 'Opening tunnel'
        tunnel.openTunnel(server, username, password, server_port)
    else:
        print 'Closing tunnel'
        tunnel.closeTunnel(server, username)

