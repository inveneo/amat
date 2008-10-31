#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tunnel.py - library for managing SSH tunnels
# (c) Inveneo 2008

import sys, re
from subprocess import Popen, PIPE, call

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

def firstTunnelPID(server):
    """Return process ID of first tunnel found, else None."""
    ps_out = Popen(['ps', '-e', '-opid,args='], stdout=PIPE).communicate()[0]
    lines = ps_out.split('\n')
    del lines[0]        # headings we don't want

    # if line looks like SSH tunnel, return first arg (the PID)
    pat = re.compile('\s*([0-9]*).*%s.*%s.*%s' % (SSHPASS, SSH, server))
    for line in lines:
        mat = pat.match(line)
        if mat:
            return int(mat.group(1))
    return None

def openTunnel(server, server_port, username, password):
    """Open tunnel: all params are strings except server_port (int)."""
    port_host_port = '%d:localhost:%d' % (server_port, CLIENT_PORT)
    user_host = '%s@%s' % (username, server)

    command_list = [SSHPASS, '-e'] + \
    [SSH, '-C', '-g', '-N',
            '-o', 'StrictHostKeyChecking=no',
            '-o', 'ServerAliveInterval=10',
            '-o', 'ServerAliveCountMax=3',
            '-R', port_host_port, user_host]
    Popen(command_list, env={'SSHPASS': password})

def closeTunnel(server):
    """Close tunnel: kill all tunnel processes."""
    pid = firstTunnelPID(server)
    while pid:
        call([KILL, str(pid)])
        pid = firstTunnelPID(server)

if __name__ == '__main__':
    """Test this puppy by simply toggling tunnel on and off."""
    if len(sys.argv) < 2:
        print 'Usage: %s server [server_port username password]' % sys.argv[0]
        sys.exit(1)
    server = sys.argv[1] # e.g. "bb.inveneo.net"
    if not firstTunnelPID(server):
        if len(sys.argv) < 5:
            print 'Need server_port, username and password to open tunnel.'
            sys.exit(1)
        server_port = int(sys.argv[2]) # e.g. "56137"
        username    = sys.argv[3]      # e.g. "_000000004321"
        password    = sys.argv[4]      # e.g. "IDAwvKwRhM4.7EL7yUYCsnn6=p.ke4hG"
        print 'Opening tunnel'
        openTunnel(server, server_port, username, password)
    else:
        print 'Closing tunnel'
        closeTunnel(server)

