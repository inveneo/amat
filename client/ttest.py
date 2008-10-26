#!/usr/bin/env python

import time, sys
from subprocess import Popen, PIPE

SSH     = '/usr/bin/ssh'
SSHPASS = '/usr/bin/sshpass'

# values received from server
username    = '_000000004321'
password    = 'IDAwvKwRhM4.7EL7yUYCsnn6-p.ke4hG'
server      = 'bb.inveneo.net'
server_port = 56137
client_port = 22

# look for tunnel
output = Popen(['ps', 'auxw'], stdout=PIPE).communicate()[0]
print output
sys.exit()

# start tunnel
port_host_port = '%d:localhost:%d' % (server_port, client_port)
user_host = '%s@%s' % (username, server)
command_list = [SSHPASS, '-p', password]
command_list += [SSH, '-C', '-g', '-N',
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'ServerAliveInterval=10',
        '-o', 'ServerAliveCountMax=3',
        '-R', port_host_port, user_host]
print command_list
Popen(command_list)
'''
while 1:
    time.sleep(1)
    print 'tick'
'''
