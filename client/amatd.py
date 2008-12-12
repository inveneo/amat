#!/usr/bin/env python
# -*- coding: utf-8 -*-

# amatd.py - the client daemon for the AMAT system
#
# This daemon will attempt to register this machine with the Inveneo
# AMAT server, do periodic check in, and execute any commands that
# are requested by the server.
#
# Connections to AMAT server are attempted in exponential backoff fashion.
#
# (c) Inveneo 2008

import os, time, signal, urllib, urllib2, traceback
import logging, logging.handlers, ConfigParser
import daemonize, tunnel, utils
from common import *

############
# CONSTANTS
############

CONF_FILE = '/etc/inveneo/conf.d/amatd.conf'
ENCODING = 'utf-8'

# XXX make these realistic when done debugging
LOG_LEVEL = logging.DEBUG
MIN_WAIT_SECS = 10      # seconds to sleep, initially (10m)
MAX_WAIT_SECS = 60      # seconds to sleep, at most (1hr)

InternalError = Exception("Internal Error")

############
# FUNCTIONS
############

def responseToDict(s):
    """Turn a newline-separated string of key=value pairs into a dictionary."""
    d = {}
    items = s.split('\n')
    for item in items:
        item = item.strip()
        pair = item.split('=')
        if len(pair) == 2:
            d[pair[0]] = pair[1]
    return d

def readConfig():
    """Read the config file."""
    global gotSIGHUP

    gotSIGHUP = False
    config = {}

    parser = ConfigParser.SafeConfigParser()
    parser.readfp(open(CONF_FILE))

    config['customer']    = \
            parser.get('client', 'customer').decode(ENCODING)[:100]
    config['description'] = \
            parser.get('client', 'description').decode(ENCODING)[:300]
    config['latitude']    = parser.getfloat('client', 'latitude')
    config['longitude']   = parser.getfloat('client', 'longitude')
    config['opperiod']    = parser.get('client', 'opperiod')

    config['server']   = parser.get('server', 'server')
    config['reg_port'] = parser.getint('server', 'reg_port')

    config['log_file']      = parser.get('daemon', 'log_file')
    config['max_log_size']  = parser.getint('daemon', 'max_log_size')
    config['max_log_count'] = parser.getint('daemon', 'max_log_count')

    return config

def resetBackoff():
    """Reset the sleep time to its lowest value."""
    global sleepSecs
    sleepSecs = MIN_WAIT_SECS

def sleepTime(backoff=True):
    """Returns number of seconds to sleep; does exponential backoff."""
    global sleepSecs
    seconds = sleepSecs
    if backoff:
        sleepSecs = min(sleepSecs * 2, MAX_WAIT_SECS)
    return seconds

def handleSignal(number, frame):
    """Sets global flag when signal is received."""
    global gotSIGHUP
    global gotSIGTERM
    if number == signal.SIGHUP:
        gotSIGHUP = True
    elif number == signal.SIGTERM:
        gotSIGTERM = True

def getType():
    """Returns the type ('station' or 'hub') of this host."""
    return 'hub'

def register():
    """Returns None if no connection made, else HTTP status as int."""
    global config

    # create parameter list for registration request
    plist = [(REGISTER_ARG_MAC, utils.macAsStr('eth0'))]
    plist.append((REGISTER_ARG_TYPE, utils.hostType()))
    plist.append((REGISTER_ARG_HOST, utils.hostName()[:50]))
    plist.append((REGISTER_ARG_CUST, config['customer'].encode(ENCODING)))
    plist.append((REGISTER_ARG_DESC, config['description'].encode(ENCODING)))
    plist.append((REGISTER_ARG_GEO,
        '%+.5f,%+.5f' % (config['latitude'], config['longitude'])))
    plist.append((REGISTER_ARG_OPPERIOD, config['opperiod']))
    params = urllib.urlencode(plist)

    # attempt registration
    url = 'http://%s:%d/reg?%s' % (config['server'], config['reg_port'], params)
    logging.info('register(%s)' % url)
    try:
        f = urllib2.urlopen(url)
    except IOError, e:
        if hasattr(e, 'reason'):
            return None
        elif hasattr(e, 'code'):
            return e.code
        else:
            raise InternalError
    return 200

def doRegistration():
    """Keep trying forever until registered or SIGTERM."""
    global gotSIGTERM
    registered = False
    while not registered and not gotSIGTERM:
        status = register()
        if status == 200:
            # OK
            registered = True
            resetBackoff()
        elif status in [None, 500]:
            # no connection or server error: try again later
            time.sleep(sleepTime())
        else:
            raise InternalError

def checkin():
    """Returns (status, response) tuple, where:
    status is None if no connection made, else HTTP status as int, and
    response is list of command name followed by args, or empty list."""
    global config

    # create parameter list for checkin request
    plist = [(CHECKIN_ARG_MAC, utils.macAsStr('eth0'))]
    plist.append((CHECKIN_ARG_STATUS, 'ok'))
    temp = get_temperature()
    if temp:
        plist.append((CHECKIN_ARG_TEMP, "%.1f" % temp))
    params = urllib.urlencode(plist)

    url = 'http://%s:%d/checkin?%s' % (config['server'], config['reg_port'],
            params)
    logging.debug('checkin(%s)' % url)
    status = None
    response = None
    try:
        f = urllib2.urlopen(url)
    except IOError, e:
        if hasattr(e, 'reason'):
            pass
        elif hasattr(e, 'code'):
            status = e.code
        else:
            logging.critical(str(e))
            raise InternalError
    else:
        status = 200
        # XXX should wrap in try block in case result is cut short
        response = f.read()
    return (status, response)

def doCommand(response):
    """Execute the given response command."""
    global config

    if response:
        logging.debug('response(%s)' % response)
        d = responseToDict(response)
        server = config['server']
        if d[CHECKIN_KEY_COMMAND] == CHECKIN_CMD_OPEN_TUNNEL:
            if not tunnel.firstTunnelPID(server):
                logging.info('openTunnel()')
                tunnel.openTunnel(server,
                        int(d[CHECKIN_KEY_SERVER_PORT]),
                        d[CHECKIN_KEY_USERNAME],
                        d[CHECKIN_KEY_PASSWORD])
            else:
                logging.debug('tunnel already open!')
        elif d[CHECKIN_KEY_COMMAND] == CHECKIN_CMD_CLOSE_TUNNEL:
            logging.info('closeTunnel()')
            tunnel.closeTunnel(server)

#############
# START HERE
#############

# read configuration file, else fail before turning to daemon
config = readConfig()

# turn into spooky daemon owned by init
retCode = daemonize.becomeDaemon(os.getcwd())

# use a rotating file log set
logging.basicConfig(level=LOG_LEVEL,
        format='%(asctime)s %(levelname)s %(message)s')
rfh = logging.handlers.RotatingFileHandler(config['log_file'], 'a',
        config['max_log_size'], config['max_log_count'])
logging.getLogger('').addHandler(rfh)
logging.info('Starting (pid=%d)' % os.getpid())

try:
    # set up signal handling: SIGHUP = re-read config file, SIGTERM = terminate.
    # they set global flags which get checked at various logical places
    gotSIGHUP = False
    gotSIGTERM = False
    signal.signal(signal.SIGHUP,  handleSignal)
    signal.signal(signal.SIGTERM, handleSignal)

    # more initial configuration
    resetBackoff()

    # loop forever until signaled to terminate
    while not gotSIGTERM:

        # check for special signals
        if gotSIGHUP:
            config = readConfig()
            doRegistration()        # won't return until registered or SIGTERM
        if gotSIGTERM:
            break

        # check in with the AMAT server
        (status, response) = checkin()
        if status == 200:
            # OK
            doCommand(response)
            resetBackoff()
        elif status in [None, 500]:
            # no connection or server error: try again later
            pass
        elif status == 404:
            # not registered yet, so do that first
            doRegistration()    # won't return until registered or SIGTERM
            if gotSIGTERM:
                break
            continue
        else:
            logging.critical('Got unexpected status %d' % status)
            raise InternalError

        # wait a spell before repeating
        time.sleep(sleepTime())

except Exception, e:
    logging.error(traceback.format_exc())
finally:
    logging.info('Stopping')
    logging.shutdown()

