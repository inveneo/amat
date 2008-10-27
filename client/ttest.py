#!/usr/bin/env python

import time, sys
from subprocess import Popen, PIPE, check_call

SSH     = '/usr/bin/ssh'
SSHPASS = '/usr/bin/sshpass'
KILL    = '/bin/kill'

# values received from server
username    = '_000000004321'
password    = 'IDAwvKwRhM4.7EL7yUYCsnn6-p.ke4hG'
server      = 'bb.inveneo.net'
server_port = 56137
client_port = 22

# look for tunnel
def pidOfTunnel(username, server):
    user_host = '%s@%s' % (username, server)
    procs = Popen(['ps', '-opid,args='], stdout=PIPE).communicate()[0]
    match_items = [SSHPASS, SSH, user_host]
    for line in procs.split('\n')[1:]:
        count = 0
        tokens = line.split()
        for token in tokens:
            if token in match_items:
                count += 1
        if count == len(match_items):
            return int(tokens[0])
    return None

def killProcess(pid):
    check_call([KILL, str(pid)])

# start here
if __name__ == '__main__':
    pid = pidOfTunnel(username, server)
    if pid:
        print 'Closing tunnel found at pid', pid
        killProcess(pid)
    else:
        port_host_port = '%d:localhost:%d' % (server_port, client_port)
        user_host = '%s@%s' % (username, server)
        command_list = [SSHPASS, '-p', password] + \
        [SSH, '-C', '-g', '-N',
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'ServerAliveInterval=10',
                '-o', 'ServerAliveCountMax=3',
                '-R', port_host_port, user_host]
        print 'Opening tunnel with', command_list
        Popen(command_list)
