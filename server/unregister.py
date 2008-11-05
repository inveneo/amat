#!/usr/bin/env python
# unregister.py - a script to forcibly unregister a MAC from AMAT system
# (c) Inveneo 2008

import os, sys, sqlite3, subprocess

USERDEL = '/usr/sbin/userdel'
USER_PREFIX = '_'
ERR_USAGE    = 1
ERR_NOT_ROOT = 2

def running_as_root():
    return os.getuid() == 0

def mac_str_to_int(s):
    """Convert MAC from string to integer."""
    mac = int(s, 16)
    assert mac == mac & 0xFFFFFFFFFFFF, 'Bad MAC value "%s"' % s
    return mac

def mac_int_to_str(n):
    return '%012x' % n

def mac_int_to_username(mac):
    """Convert MAC to associated username."""
    return u'%s%012x' % (USER_PREFIX, mac)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'Usage: %s <MAC Address>' % sys.argv[0]
        sys.exit(ERR_USAGE)
    imac = mac_str_to_int(sys.argv[1])
    smac = mac_int_to_str(imac)

    if not running_as_root():
        print 'You must be root to run this program'
        sys.exit(ERR_NOT_ROOT)

    conn = sqlite3.connect('data/amat.db')
    c = conn.cursor()

    # remove tunnel and checkin and host entries
    print 'Deleting from database...'
    c.execute('DELETE FROM tunnel WHERE mac=?', (imac,))
    for row in c:
        print row
    c.execute('DELETE FROM checkin WHERE mac=?', (imac,))
    for row in c:
        print row
    c.execute('DELETE FROM host WHERE mac=?', (imac,))
    for row in c:
        print row

    print 'Changes:', conn.total_changes
    conn.commit()
    conn.close()

    # delete the login and home dir
    print 'Deleting login and home dir...'
    username = mac_int_to_username(imac)
    subprocess.call([USERDEL, '-r', username])

    print 'Done.'

