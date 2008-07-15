import sys
import os
from urllib2 import *

baseurl="http://amat.inveneo.org/reg?"
"""
https://<reg server>/reg?mac=<mac>&type=<host type>&host=<hostname>&cust=<customer>&desc=<short description>&geo=<geocode>&opperiod=<opperiod> 
"""

mac="00145135cb20" 
type="client"
fullcust="somerandomcustname"
fulldesc="some free random descriptive text"
cust=fullcust[0:99]
desc=fulldesc[0:299]
geo="-37.784825,-122.419968"

if os.path.exists("/etc/hostname"):
	host=os.popen('cat /etc/hostname').read()
else:
	hn=os.popen('which hostname').read()
	if hn.length(hn) > 0:
		host=hn[0:49]
	else:
		host="inveneo"+type

fullurl=baseurl+"mac="+mac+"&type="+type+"&host="+host+"&cust="+cust+"&desc="+desc+"&geo="+geo+"&opperiod=12345:0900-1700,06:1200-1800"

print "Initial parameters are:"
print "mac "+mac
print "hosttype "+type
print "hostname "+host
print "cust "+cust
print "desc "+desc
print "geo "+geo

print "Full URL="+fullurl

#
#req = Request('http://twitter.com/users/show/jetdillo.json')
#
#
#try:
#	r=urlopen(req)
#except URLError,e:
#	print str(e)
#	sys.exit(1)
#
#results = r.read()
#print results
