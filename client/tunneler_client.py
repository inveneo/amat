import sys
import os
import socket
import re
from urllib2 import *


class amat_client (object):

	baseurl="http://amat.inveneo.org/reg?"
"""
https://<reg server>/reg?mac=<mac>&type=<host type>&host=<hostname>&cust=<customer>&desc=<short description>&geo=<geocode>&opperiod=<opperiod> 
"""
	def __init__(self,parent,mac,type,host,cust,desc,geo,opperiod):

"""
Use some default values for now, we'll fill them in later properly from the instance
side once we get this thing working
"""
		mac="00145135cb20" 
		type="client"
		fullcust="somerandomcustname"
		fulldesc="some free random descriptive text"
		cust=fullcust[0:99]
		desc=fulldesc[0:299]
		geo="-37.784825,-122.419968"

	def gethostname(self):
		if os.path.exists("/etc/hostname"):
			host=os.popen('cat /etc/hostname').read()
		else:
			hn=os.popen('which hostname').read()
			if hn.length(hn) > 0:
				host=hn[0:49]
			else:
				host="inveneo"+type

	def encode_text(self,parent,intext):
		outtext=''
		outtext=urllib2.quote(intext)
	        return outtext	

	def build_url(self,mac,type,host,cust,desc,geo,opperiod):
		enc_desc=''
		enc_desc=self.encode_text(desc) 
		fullurl=baseurl+"mac="+mac+"&type="+type+"&host="+host+"&cust="+cust+"&desc="+desc+"&geo="+geo+"&opperiod=12345:0900-1700,06:1200-1800"

	def dumpparms(self):

		print "Initial parameters are:"
		print "mac "+mac
		print "hosttype "+type
		print "hostname "+host
		print "cust "+cust
		print "desc "+desc
		print "geo "+geo
		print "Full URL="+fullurl

	def connect(self,url):
	
		try:
			r=urlopen(url)
		except URLError, e:
			print ("caught exception "+e+" trying to open "+url)
			sys.exit(1)	

		results = r.read()
		print results 




