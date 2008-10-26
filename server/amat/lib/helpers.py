#!/usr/bin/env python
# helpers.py
# (c) Inveneo 2008

"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""

from pylons import g
from webhelpers import *
from subprocess import check_call
import os.path, pexpect
import socket

USERADD = '/usr/sbin/useradd'
RSSH    = '/usr/bin/rssh'
PASSWD  = '/usr/bin/passwd'

BASE_DIR = '/jail/home'
SKEL_DIR = '/jail/skel'
GROUP    = 'jailbird'

def admit_to_jail(username, comment):
    """Add a new user to the jail."""
    login = str(username)
    comment = str(comment)
    home_dir = os.path.join(BASE_DIR, str(username))
    check_call([USERADD,
        '--comment', comment,
        '--gid', GROUP,
        '--create-home',
        '--home-dir', home_dir,
        '-k', SKEL_DIR,
        '--shell', RSSH,
        login])

def set_password(username, password):
    """Set the password for a user."""
    command = '%s %s' % (PASSWD, username)
    events = {
            'Enter new UNIX password:':  '%s\n' % password,
            'Retype new UNIX password:': '%s\n' % password
            }
    return pexpect.run(command, withexitstatus=True, events=events)

def mac_str_to_int(s):
    """Convert MAC from string to integer."""
    mac = int(s, 16)
    assert mac == mac & 0xFFFFFFFFFFFF, 'Bad MAC value "%s"' % s
    return mac

def mac_int_to_str(n):
    """Convert MAC from integer to string."""
    return '%012x' % n

def mac_int_to_username(mac):
    """Convert MAC to associated username."""
    return u'%s%012x' % (g.USER_PREFIX, mac)

def get_free_port():
    """Get a high port that is free (at the moment)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostbyname(socket.gethostname()), 0))
    ipaddr, port = s.getsockname()
    return port

if __name__ == '__main__':
    print get_free_port()

