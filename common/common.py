#!/usr/bin/env python
# -*- coding: utf-8 -*-

# common.py - client/server common code
# (c) Inveneo 2008

from time import time

def secs_to_blurb(s):
    """Convert number of seconds since Unix Epoch into an English blurb.
    Shamelessly stolen from Twitter."""

    diff = time() - s
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

if __name__=='__main__':
    print "Common AMAT code."
