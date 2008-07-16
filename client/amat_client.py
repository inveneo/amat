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

		self.baseurl="http://bb.inveneo.net:5000/"

	def gethostname(self):
		if os.path.exists("/etc/hostname"):
			host=os.popen('cat /etc/hostname').read()
			host=host.strip()		
		else:
			hn=os.popen('which hostname').read()
			if len(hn) > 0:
				host=hn[0:49]
			else:
				host="inveneo"+type
		return host

	def build_reg_url(self,mac,type,host,cust,desc,geo,opperiod):
		trim_desc=desc[0:299]
#		enc_desc=self.encode_text(trim_desc) 
		geo = geo.replace(',','%2C')		
		opperiod = opperiod.replace(',','%2C')
		opperiod = opperiod.replace(':','%3A')
		reg_url=self.baseurl+"reg?"+"mac="+mac+"&type="+type+"&host="+host+"&cust="+cust+"&desc="+desc+"&geo="+geo+"&opperiod="+opperiod
		return reg_url

	def build_checkin_url(self,mac,status):
		results=0	
		print "mac="+mac+" status="+status
		print "mac length=%d status length=%d",len(mac),len(status)
		mac = mac[0:11]
		checkin_url=self.baseurl+"checkin?"+"mac="+mac+"&status="+status
		return checkin_url

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
		req=''
		resp=''	
		try:
			req=Request(url)
			resp=urlopen(req)

		except URLError, e:
			print "caught exception ",e," trying to open "+url
			sys.exit(1)	

		results = resp.read()
		print results 


	def parse_results(self,resp_data):

		print "IM IN YR RESPONSE ]<0d3, SHR3DD1n yr DATA!!"
