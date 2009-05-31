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
LOG_LEVEL = logging.INFO
InternalError = Exception("Internal Error")

############
# FUNCTIONS
############

def keyvalsToDict(s):
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
    """Read the config file and return it as dictionary."""
    global config

    parser = ConfigParser.SafeConfigParser()
    parser.readfp(open(CONF_FILE))

    config = {}

    try:
        config['min_checkin_seconds']      = parser.getint('client', 'min_checkin_minutes')*60
    except ConfigParser.NoOptionError:
        config['min_checkin_seconds'] = 30*60 # 30 minutes

    try:
        config['max_checkin_seconds']      = parser.get('client', 'max_checkin_minutes')*60
    except ConfigParser.NoOptionError:
        config['max_checkin_seconds'] = 120*60 # 2 hrs

    try:
        config['customer']      = \
            parser.get('client', 'customer').decode(ENCODING)
    except ConfigParser.NoOptionError:
        config['customer']      = 'Inveneo AMAT Client'

    try:
        config['description']   = \
            parser.get('client', 'description').decode(ENCODING)
    except ConfigParser.NoOptionError:
        config['description']   = 'Unconfigured Client'

    try:
        config['latitude']      = parser.getfloat('client', 'latitude')
    except ConfigParser.NoOptionError:
        config['latitude'] = 37.7793 # san francisco

    try:
        config['longitude']     = parser.getfloat('client', 'longitude')
    except ConfigParser.NoOptionError:
        config['longitude'] = -122.4192 # san francisco

    try:
        config['opperiod']      = parser.get('client', 'opperiod')
    except ConfigParser.NoOptionError:
        config['opperiod'] = ""
    
    try:
        config['host_type'] = parser.get('client', 'host_type')
    except ConfigParser.NoOptionError:
        # guess type if it's an Inveneo OS
        config['host_type'] = utils.hostType()
        # set to 'hub' if unknown
        if config['host_type'] == 'unknown': config['host_type'] = 'hub'


    try:
        config['server']        = parser.get('server', 'server')
    except ConfigParser.NoOptionError:
        config['server'] = 'bb.inveneo.net'

    try:
        config['reg_port']      = parser.getint('server', 'reg_port')
    except ConfigParser.NoOptionError:
        config['reg_port'] = 5000

    try:
        config['log_file']      = parser.get('daemon', 'log_file')
    except ConfigParser.NoOptionError:
        config['log_file'] = '/var/log/amatd.log'

    try:
        config['max_log_size']  = parser.getint('daemon', 'max_log_size')
    except ConfigParser.NoOptionError:
        config['max_log_size'] = 5000000

    try:
        config['max_log_count'] = parser.getint('daemon', 'max_log_count')
    except ConfigParser.NoOptionError:
        config['max_log_count'] = 4

def resetBackoff():
    """Reset the sleep time to its lowest value."""
    global sleepSecs

    sleepSecs = config['min_checkin_seconds']

def sleepTime(backoff=True):
    """Returns number of seconds to sleep; does exponential backoff."""
    global sleepSecs

    seconds = sleepSecs
    if backoff:
        sleepSecs = min(sleepSecs * 2, config['max_checkin_seconds'])
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
    plist.append((REGISTER_ARG_TYPE, config['host_type']))
    plist.append((REGISTER_ARG_HOST, utils.hostName()))
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
    global gotSIGHUP
    global gotSIGTERM

    registered = False
    while not registered and not gotSIGTERM:
        if gotSIGHUP:
            readConfig()
            gotSIGHUP = False
        status = register()
        if status == 200:
            # OK
            registered = True
            resetBackoff()
        elif status in [None, 500]:
            # no connection or server error: try again later
            time.sleep(sleepTime())
        else:
            logging.debug("status error: %s" % status)
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
        response = f.read()
    return (status, response)

def tunnelIsOpen(server):
    """Return answer to this question (True or False)."""
    return tunnel.firstTunnelPID(server) != None

def checkAndOpenTunnel(server, d):
    """Check parameters and if good then open tunnel."""
    global serverPort

    if (CHECKIN_KEY_SERVER_PORT not in d) or \
            (CHECKIN_KEY_USERNAME not in d) or \
            (CHECKIN_KEY_PASSWORD not in d):
        logging.info('Missing parameter(s)')
        return False
    serverPort = int(d[CHECKIN_KEY_SERVER_PORT])
    logging.info('openTunnel()')
    tunnel.openTunnel(server, serverPort, d[CHECKIN_KEY_USERNAME],
            d[CHECKIN_KEY_PASSWORD])
    return True

def closeAnyTunnels(server):
    """Close all tunnels and set a global value."""
    global serverPort

    logging.info('closeTunnel()')
    tunnel.closeTunnel(server)
    serverPort = 0
    return True

def doCommand(response):
    """Execute the given response command.  Return success status."""
    global config
    global serverPort

    if response:
        logging.debug('response(%s)' % response.replace('\n', ','))
        d = keyvalsToDict(response)
        server = config['server']

        # choose command to run
        if d[CHECKIN_KEY_COMMAND] == CHECKIN_CMD_OPEN_TUNNEL:
            if tunnelIsOpen(server):
                if (CHECKIN_KEY_SERVER_PORT not in d):
                    logging.info('Missing parameter(s)')
                    return False
                if int(d[CHECKIN_KEY_SERVER_PORT]) != serverPort:
                    closeAnyTunnels(server)
                    return checkAndOpenTunnel(server, d)
                else:
                    logging.debug('Tunnel already open at port %d' % serverPort)
                    return True
            else:
                return checkAndOpenTunnel(server, d)

        elif d[CHECKIN_KEY_COMMAND] == CHECKIN_CMD_CLOSE_TUNNEL:
            closeAnyTunnels(server)
            return True

    # something was bogus
    return False

#############
# START HERE
#############

# read configuration file, else fail before turning to daemon
readConfig()

# use a rotating file log set
logging.basicConfig(level=LOG_LEVEL)
rfh = logging.handlers.RotatingFileHandler(config['log_file'], 'a',
        config['max_log_size'], config['max_log_count'])
rfh.setLevel(LOG_LEVEL)
rfh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s',
    '%Y-%m-%d %H:%M:%S'))
logging.getLogger().addHandler(rfh)
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
    closeAnyTunnels(config['server'])

    # always start with a registration (in case params have changed)
    doRegistration()    # won't return until registered or SIGTERM

    # loop forever until signaled to terminate
    while not gotSIGTERM:

        # check for special signals
        if gotSIGHUP:
            readConfig()
            gotSIGHUP = False
            doRegistration()    # won't return until registered or SIGTERM
        if gotSIGTERM:
            break

        # check in with the AMAT server
        (status, response) = checkin()
        if status == 200:
            # OK
            if doCommand(response):
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

