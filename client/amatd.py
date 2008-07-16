#!/usr/bin/env python

import sys
import os
import getopt
import array
import urllib2
import socket
import re
import amat_client

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

 	aclnt = amat_client.amc(None)

	mac="00145135cb20"
	type="client"
	host=aclnt.gethostname()
	cust="somerandomcustname"
	desc="some free random descriptive text"
	geo="-37.784825,-122.419968"
	desc=desc.replace(' ', '%20')
	opperiod="12345:0900-1700,06:1200-1800"
	myurl=aclnt.build_url(mac,type,host,cust,desc,geo,opperiod)
    
	print("About to connect to amat server")
	print("Using URL "+myurl)
	aclnt.connect(myurl)

	sys.stderr.write("\n--- exit ---\n")