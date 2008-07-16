import sys
import os
import socket
import re
import urllib
import string
from urllib2 import urlopen,URLError,Request

class amc (object):

	baseurl=''	

	def __init__(self,parent):

		self.baseurl="http://bb.inveneo.net:5000/reg?"

	def gethostname(self):
		if os.path.exists("/etc/hostname"):
			host=os.popen('cat /etc/hostname').read()
			host=host.strip()		
		else:
			hn=os.popen('which hostname').read()
			if hn.length(hn) > 0:
				host=hn[0:49]
			else:
				host="inveneo"+type
		return host

	def build_url(self,mac,type,host,cust,desc,geo,opperiod):
		trim_desc=desc[0:299]
#		enc_desc=self.encode_text(trim_desc) 
		geo = geo.replace(',','%2C')		
		opperiod = opperiod.replace(',','%2C')
		opperiod = opperiod.replace(':','%3A')
		fullurl=self.baseurl+"mac="+mac+"&type="+type+"&host="+host+"&cust="+cust+"&desc="+desc+"&geo="+geo+"&opperiod="+opperiod
		return fullurl

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
#			req=Request(url)
			req=urlopen(url)

		except URLError, e:
			print "caught exception ",e," trying to open "+url
			sys.exit(1)	

		results = req.read()
		print results 
