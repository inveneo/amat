#!/usr/bin/env python

import sys, os, getopt, array, urllib2, socket, re

EXITCHARCTER = '\x04'   #ctrl+D

CONVERT_CRLF = 2
CONVERT_CR   = 1
CONVERT_LF   = 0

"""
Simple implementer of the tunneler_client class
to connect to the AMAT server, GET a URL with the appropriate data stuffed into it, etc.
"""
	
if __name__ == '__main__':
    #initialize with defaults

    #parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:],
            "hf:o:",
            ["help", "file=", "out="]
        )
    except getopt.GetoptError:
        # print help information and exit:
        usage()
        sys.exit(2)
    
    for o, a in opts:
	print "o=" + o + " a=" + a
        if o in ("-h", "--help"):       #help text
            usage()
            sys.exit()
        elif o in ("-f", "--file"):     
            try:
                framefile = int(a)
            except ValueError:
		framefile = a
        elif o in ("-o", "--out"):
            try:
                outfile = int(a)
            except ValueError:
                outfile = a
    
    print("About to connect to amat server")
"""
do implementation stuff here
"""
    sys.stderr.write("\n--- exit ---\n")
