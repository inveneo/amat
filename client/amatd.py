#!/usr/bin/env python

# amatd.py - the client daemon for the AMAT system
#
# This daemon will attempt to register this machine with the Inveneo
# AMAT server, do periodic check in, and execute any commands that
# are requested by the server.
#
# (c) Inveneo 2008

import os, time, signal
import daemonize

############
# CONSTANTS
############

LOGFILE = '/var/log/amatd.log'

MIN_WAIT_SECS = 10      # seconds to sleep, initially (10m)
MAX_WAIT_SECS = 60      # seconds to sleep, at most (1hr)

CMD_OPEN_TUNNEL  = 'open_tunnel'
CMD_CLOSE_TUNNEL = 'close_tunnel'

InternalError = Exception("Internal Error")

############
# FUNCTIONS
############

def openLogfile():
    global logfile
    logfile = open(LOGFILE, 'a')
    return True

def closeLogfile():
    global logfile
    logfile.close()

def logEvent(s):
    global logfile
    stamp = time.asctime()
    logfile.write('%s: %s\n' % (stamp, s))
    logfile.flush()

def configHasChanged():
    return True

def resetBackoff():
    """Reset the sleep time to its lowest value."""
    global sleepSecs
    sleepSecs = MIN_WAIT_SECS

def sleepTime(backoff=True):
    """Returns number of seconds to sleep, does exponential backoff."""
    global sleepSecs
    t = sleepSecs
    if backoff:
        sleepSecs = min(sleepSecs * 2, MAX_WAIT_SECS)
    return t

def handleSighup(number, frame):
    global gotSighup
    gotSighup = True

def register():
    """Returns None if no connection made, else HTTP status as int."""
    logEvent('register()')
    return None

def doRegistration():
    """Keep trying forever until registered or SIGHUP."""
    global gotSighup
    registered = False
    resetBackoff()
    while not registered and not gotSighup:
        status = register()
        if status == 200:
            registered = True
        elif status in [None, 500]:
            time.sleep(sleepTime())
        else:
            raise InternalError

def checkin():
    """Returns (status, command) tuple, where:
    status is None if no connection made, else HTTP status as int, and
    command is list of command name followed by args, or empty list."""
    logEvent('checkin()')
    status = None
    command = []
    return (status, command)

def doCommand(command):
    """Execute the given command."""
    return True

#############
# START HERE
#############

retCode = daemonize.becomeDaemon(os.getcwd())
openLogfile()
logEvent('Starting (pid=%d)' % os.getpid())
try:
    gotSighup = False
    signal.signal(signal.SIGHUP, handleSighup)
    resetBackoff()
    while not gotSighup:
        if configHasChanged():
            doRegistration()        # won't return until registered or SIGHUP
        if gotSighup:
            break
        (status, command) = checkin()
        if status == 200:
            if command:
                doCommand(command)
            resetBackoff()
        elif status in [None, 500]:
            pass
        elif status == 404:
            doRegistration()    # won't return until registered or SIGHUP
            if gotSighup:
                break
            continue
        else:
            raise InternalError
        time.sleep(sleepTime())
except Exception, e:
    logEvent(repr(e))
finally:
    logEvent('Stopping')
    closeLogfile()

