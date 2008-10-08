#!/usr/bin/env python
# unregister.py - a script to forcibly unregister a username from AMAT system
# (c) Inveneo 2008

import os, sys, sqlite3, subprocess

USERDEL = '/usr/sbin/userdel'
ERR_USAGE    = 1
ERR_NOT_ROOT = 2

def running_as_root():
    return os.getuid() == 0

# START HERE
if len(sys.argv) < 2:
    print 'Usage: %s <username>' % sys.argv[0]
    sys.exit(ERR_USAGE)
username = sys.argv[1]

if not running_as_root():
    print 'You must be root to run this program'
    sys.exit(ERR_NOT_ROOT)

conn = sqlite3.connect('data/amat.db')
c = conn.cursor()

# make a list of MAC addresses that map to this username
c.execute('SELECT mac FROM host WHERE username=?', (username,))
maclist = []
for row in c:
    mac = row[0]
    print 'Found MAC %012x' % mac
    maclist.append(mac)

# remove checkin and host entries
print 'Deleting from database...'
for mac in maclist:
    c.execute('DELETE FROM checkin WHERE mac=?', (mac,))
    for row in c:
        print row
    c.execute('DELETE FROM host WHERE mac=?', (mac,))
    for row in c:
        print row

print 'Changes:', conn.total_changes
conn.commit()
conn.close()

# delete the login and home dir
print 'Deleting login and home dir...'
subprocess.call([USERDEL, '-r', username])
