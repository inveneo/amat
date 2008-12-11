#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common.py - client/server common code
# (c) Inveneo 2008

import os.path, time

TEMP_PATH = '/proc/acpi/thermal_zone/THRM/temperature'

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
    """Return system temperature as integer, else None."""
    try:
        if os.path.isfile(TEMP_PATH):
            (key, val) = open(TEMP_PATH).readline().split(':')
            if key.strip() == 'temperature':
                (temp, scale) = val.strip().split()
                return int(temp)
    except:
        pass
    return None

if __name__=='__main__':
    temp = get_temperature()
    if temp:
        print "Temperature is '%d'" % temp
    else:
        print "Temperature is unavailable."
