#!/usr/bin/env python
# -*- coding: utf-8 -*-

# amatd.py - the client daemon for the AMAT system
#
# This daemon will attempt to register this machine with the Inveneo
# AMAT server, do periodic check in, and execute any commands that
# are requested by the server.
#
# (c) Inveneo 2008

import os, time, signal, urllib
import daemonize

############
# CONSTANTS
############

AMAT_SERVER = 'bb.inveneo.net'
AMAT_PORT = 5000

CANNED_MAC  = '000000004321'
CANNED_TYPE = 'hub'
CANNED_HOST = 'jimhost'
CANNED_CUST = u'fööd'
CANNED_DESC = u'some text about fööd'
CANNED_GEO  = '30.000000,-90.000000'
CANNED_OPPERIOD = ''

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

def closeLogfile():
    global logfile
    logfile.close()

def logEvent(s):
    global logfile
    stamp = time.asctime()
    logfile.write('%s: %s\n' % (stamp, s))
    logfile.flush()

def readConfig():
    """Read the config file."""
    pass

def resetBackoff():
    """Reset the sleep time to its lowest value."""
    global sleepSecs
    sleepSecs = MIN_WAIT_SECS

def sleepTime(backoff=True):
    """Returns number of seconds to sleep, does exponential backoff."""
    global sleepSecs
    seconds = sleepSecs
    if backoff:
        sleepSecs = min(sleepSecs * 2, MAX_WAIT_SECS)
    return seconds

def handleSignal(number, frame):
    global gotSIGHUP
    global gotSIGTERM
    if number == signal.SIGHUP:
        gotSIGHUP = True
    elif number == signal.SIGTERM:
        gotSIGTERM = True

def getMAC():
    """Returns MAC address of eth0 as normal string."""
    return CANNED_MAC

def getHostname():
    """Returns hostname as normal string."""
    return CANNED_HOST[0:50]

def register():
    """Returns None if no connection made, else HTTP status as string."""
    plist = [('mac', getMAC())]
    plist.append(('type', CANNED_TYPE))
    plist.append(('host', getHostname()))
    plist.append(('cust', CANNED_CUST[0:100].encode('utf-8')))
    plist.append(('desc', CANNED_DESC[0:300].encode('utf-8')))
    plist.append(('geo',  CANNED_GEO[0:22]))
    plist.append(('opperiod', CANNED_OPPERIOD))
    params = urllib.urlencode(plist)
    url = 'http://%s:%d/reg?%s' % (AMAT_SERVER, AMAT_PORT, params)
    logEvent('register(%s)' % url)
    try:
        f = urllib.urlopen(url)
    except IOError, e:
        return None
    return f.headers.status.split()[0]

def doRegistration():
    """Keep trying forever until registered or SIGTERM."""
    global gotSIGTERM
    registered = False
    resetBackoff()
    while not registered and not gotSIGTERM:
        status = register()
        if status == '200':
            registered = True
        elif status in [None, '500']:
            time.sleep(sleepTime())
        else:
            raise InternalError

def checkin():
    """Returns (status, command) tuple, where:
    status is None if no connection made, else HTTP status as string, and
    command is list of command name followed by args, or empty list."""
    logEvent('checkin()')
    status = None
    command = []
    return (status, command)

def doCommand(command):
    """Execute the given command."""
    logEvent('command(%s)' % command)

#############
# START HERE
#############

retCode = daemonize.becomeDaemon(os.getcwd())
openLogfile()
logEvent('Starting (pid=%d)' % os.getpid())
try:
    # set up signal handling: SIGHUP = re-read config file, SIGTERM = terminate
    gotSIGHUP = False
    gotSIGTERM = False
    signal.signal(signal.SIGHUP,  handleSignal)
    signal.signal(signal.SIGTERM, handleSignal)

    # more initial configuration
    resetBackoff()      # reset exponential backoff of retry attempts
    readConfig()

    # loop forever until signaled to terminate
    while not gotSIGTERM:

        # check for special signals
        if gotSIGHUP:
            readConfig()
            doRegistration()        # won't return until registered or SIGTERM
        if gotSIGTERM:
            break

        # check in with the AMAT server
        (status, command) = checkin()
        if status == '200':
            if command:
                doCommand(command)
            resetBackoff()
        elif status in [None, '500']:
            pass
        elif status == '404':   # not registered yet, so do that first
            doRegistration()    # won't return until registered or SIGTERM
            if gotSIGTERM:
                break
            continue
        else:
            raise InternalError

        # wait a spell before repeating
        time.sleep(sleepTime())

except Exception, e:
    logEvent(repr(e))
finally:
    logEvent('Stopping')
    closeLogfile()

