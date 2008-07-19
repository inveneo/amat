"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""

from webhelpers import *
from subprocess import call
import pexpect

USERADD = '/usr/sbin/useradd'
RSSH = '/usr/bin/rssh'
PASSWD = '/usr/bin/passwd'

def admit_to_jail(username):
    """Add a new user to the jail."""
    call([USERADD, '--shell', RSSH, username])

def set_password(username, password):
    """Set the password for a user."""
    command = '%s %s' % (PASSWD, username)
    events = {
            'Enter new UNIX password:':  '%s\n' % password,
            'Retype new UNIX password:': '%s\n' % password
            }
    return pexpect.run(command, withexitstatus=True, events=events)
