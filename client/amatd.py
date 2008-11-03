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
import daemonize, tunnel

############
# CONSTANTS
############

CONF_FILE = '/etc/inveneo/conf.d/amatd.conf'

# XXX make these realistic when done debugging
LOG_LEVEL = logging.DEBUG
MIN_WAIT_SECS = 10      # seconds to sleep, initially (10m)
MAX_WAIT_SECS = 60      # seconds to sleep, at most (1hr)

# XXX these should go in an API library common to both client and server
# constants in checkin response
USER_PREFIX      = '_'
CMD_OPEN_TUNNEL  = 'open_tunnel'
CMD_CLOSE_TUNNEL = 'close_tunnel'
KEY_COMMAND      = 'command'
KEY_SERVER_PORT  = 'server_port'
KEY_USERNAME     = 'username'
KEY_PASSWORD     = 'password'

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

    config['customer']    = parser.get('client', 'customer')[:100]
    config['description'] = parser.get('client', 'description')[:300]
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

def getMAC():
    """Returns MAC address of eth0 as normal string."""
    return '000000004321'

def getType():
    """Returns the type ('station' or 'hub') of this host."""
    return 'hub'

def getHostname():
    """Returns hostname as normal string."""
    return 'jimhost'[:50]

def register():
    """Returns None if no connection made, else HTTP status as int."""
    global config
    plist = [('mac', getMAC())]
    plist.append(('type', getType()))
    plist.append(('host', getHostname()))
    plist.append(('cust', config['customer'].encode('utf-8')))
    plist.append(('desc', config['description'].encode('utf-8')))
    plist.append(('geo',  '%+.5f,%+.5f' %
        (config['latitude'], config['longitude'])))
    plist.append(('opperiod', config['opperiod']))
    params = urllib.urlencode(plist)
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

    plist = [('mac', getMAC())]
    plist.append(('status', 'ok'))
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
        if d[KEY_COMMAND] == CMD_OPEN_TUNNEL:
            if not tunnel.firstTunnelPID(server):
                logging.info('openTunnel()')
                tunnel.openTunnel(server, int(d[KEY_SERVER_PORT]),
                        d[KEY_USERNAME], d[KEY_PASSWORD])
            else:
                logging.debug('tunnel already open!')
        elif d[KEY_COMMAND] == CMD_CLOSE_TUNNEL:
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
            raise InternalError

        # wait a spell before repeating
        time.sleep(sleepTime())

except Exception, e:
    logging.error(traceback.format_exc())
finally:
    logging.info('Stopping')
    logging.shutdown()

