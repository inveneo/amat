#!/usr/bin/env python
# unregister.py
# (c) Inveneo 2008

import sys, sqlite3, subprocess

USERDEL = '/usr/sbin/userdel'

if len(sys.argv) < 2:
    print 'Usage: %s <username>' % sys.argv[0]
    sys.exit(1)
username = sys.argv[1]

conn = sqlite3.connect('data/amat.db')
c = conn.cursor()

c.execute('SELECT mac FROM host WHERE username=?', (username,))
maclist = []
for row in c:
    mac = row[0]
    print 'Found MAC %012x' % mac
    maclist.append(mac)

# remove checkin and host entries
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
subprocess.check_call([USERDEL, '-r', username])
