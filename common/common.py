#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common.py - client/server common code
# (c) Inveneo 2008

import os.path, time

# constants in registration request
REGISTER_ARG_MAC  = 'mac'
REGISTER_ARG_TYPE = 'type'
REGISTER_ARG_HOST = 'host'
REGISTER_ARG_CUST = 'cust'
REGISTER_ARG_DESC = 'desc'
REGISTER_ARG_GEO  = 'geo'
REGISTER_ARG_OPPERIOD = 'opperiod'

# constants in checkin request
CHECKIN_ARG_MAC    = 'mac'
CHECKIN_ARG_STATUS = 'status'
CHECKIN_ARG_TEMP   = 'temp'

# constants in checkin response
CHECKIN_CMD_OPEN_TUNNEL  = 'open_tunnel'
CHECKIN_CMD_CLOSE_TUNNEL = 'close_tunnel'
CHECKIN_KEY_COMMAND      = 'command'
CHECKIN_KEY_SERVER_PORT  = 'server_port'
CHECKIN_KEY_CLIENT_PORT  = 'client_port'
CHECKIN_KEY_USERNAME     = 'username'
CHECKIN_KEY_PASSWORD     = 'password'

# other constants
ACPI_TEMP_PATH = '/proc/acpi/thermal_zone/THRM/temperature'

def secs_to_blurb(s):
    """Convert number of seconds since Unix Epoch into an English blurb.
    Shamelessly stolen from Twitter."""

    diff = time.time() - s
    if (diff < 60):
        return "less than a minute ago"
    elif (diff < 120):
        return "about a minute ago"
    elif (diff < 3600): 
        return "%d minutes ago" % int(diff/60)
    elif (diff < 7200):
        return "about an hour ago"
    elif (diff < 86400):
        return "%d hours ago" % int(diff/3600)
    elif (diff < 172800):
        return "one day ago"
    else:
        return "%d days ago" % int(diff/86400)

def get_temperature():
    """Return system temperature as float, else None."""
    try:
        if os.path.isfile(ACPI_TEMP_PATH):
            (key, val) = open(ACPI_TEMP_PATH).readline().split(':')
            if key.strip() == 'temperature':
                (temp, scale) = val.strip().split()
                return float(temp)
    except:
        pass
    return None

if __name__=='__main__':
    temp = get_temperature()
    if temp:
        print "Temperature is '%.1f'" % temp
    else:
        print "Temperature is unavailable."

