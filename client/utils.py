#!/usr/bin/env python
# -*- coding: utf-8 -*-

# utils.py - utility functions
# (c) Inveneo 2008

import string, os.path
from subprocess import Popen, PIPE

IFCONFIG = '/sbin/ifconfig'
GREP     = '/bin/grep'
HOSTNAME = '/bin/hostname'

VERSION_FILE = '/etc/inveneo/os_version'
STATION_DIR  = '/usr/X11R6/lib/X11' # a dir found only on stations
HUB_DIR      = '/etc/squid'         # a dir found only on hubs

def macAsStr(interface):
    """Return the MAC address of the given interface as string."""
    p1 = Popen([IFCONFIG, interface], stdout=PIPE)
    p2 = Popen([GREP, 'HWaddr'], stdin = p1.stdout, stdout=PIPE)
    stdout = p2.communicate()[0]
    lines = stdout.split('\n')
    for line in lines:
        tokens = line.split()
        for i in range(len(tokens)):
            if tokens[i] == 'HWaddr':
                bytes = tokens[i+1].split(':')
                return string.join(bytes, '')
    return None

def macAsInt(interface):
    """Return the MAC address of the given interface as int."""
    s = macAsStr(interface)
    if s: return int(s, 16)
    return None

def hostName():
    """Return the hostname of this machine as string."""
    p = Popen([HOSTNAME], stdout=PIPE)
    stdout = p.communicate()[0]
    lines = stdout.split('\n')
    return lines[0]

def hostType():
    """Makes a wild stab at which type of host this is."""
    if os.path.isfile(VERSION_FILE):
        try:
            fp = open(VERSION_FILE)
            os_type = fp.readline().strip().split()[0]
            fp.close()
        except:
            return 'unknown'
        if os_type == 'IDL': return 'station'
        elif os_type == 'IHL': return 'hub'
    elif os.path.isdir(STATION_DIR): return 'station'
    elif os.path.isdir(HUB_DIR): return 'hub'
    return 'unknown'

if __name__ == "__main__":
    interface = 'eth0'
    print 'MAC address of %s is %s' % (interface, macAsStr(interface))
    print 'MAC address of %s is %012x' % (interface, macAsInt(interface))
    print 'Host name is %s' % hostName()
    print 'Host type is %s' % hostType()

