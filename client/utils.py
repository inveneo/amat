#!/usr/bin/env python
# -*- coding: utf-8 -*-

# utils.py - utility functions
# (c) Inveneo 2008

import string
from subprocess import Popen, PIPE

IFCONFIG = '/sbin/ifconfig'
GREP     = '/bin/grep'

def macAsInt(interface):
    """Return the MAC address of the given interface as int."""
    p1 = Popen([IFCONFIG, interface], stdout=PIPE)
    p2 = Popen([GREP, 'HWaddr'], stdin = p1.stdout, stdout=PIPE)
    stdout = p2.communicate()[0]
    lines = stdout.split('\n')
    for line in lines:
        tokens = line.split()
        for i in range(len(tokens)):
            if tokens[i] == 'HWaddr':
                bytes = tokens[i+1].split(':')
                macAsStr = string.join(bytes, '')
                return int(macAsStr, 16)

if __name__ == "__main__":
    interface = 'eth0'
    print 'MAC address of %s is %012x' % (interface, macAsInt(interface))
