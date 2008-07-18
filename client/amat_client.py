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
		mac = mac[0:12]
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
			print "Error code is",e.code
			print "Header info",e.info()
			print "URL retrieved was:\n"+e.geturl()
			sys.exit(1)	

		results = resp.read()
		hdr = resp.info()
		print results 
		print hdr
		return results

	def proc_server_response(self,srv_resp):
		server_cmd={}
		print "IM IN YR RESPONSE ]<0d3, SHR3DD1n yr DATA!!"
		resp_lines=srv_resp.splitlines()
                print "resp_lines=",resp_lines
                numlines = len(resp_lines)
                for s in resp_lines:
                        cmdpairs=s.split('=')
                        server_cmd[cmdpairs[0]]=cmdpairs[1]
                print "server_cmd",server_cmd['command']
		cmd = server_cmd['command']
		cur_user=server_cmd['username']
		cur_pass=server_cmd['password']
		r_port = server_cmd['remote_port']
		l_port = server_cmd['local_port']

		if cmd == "establish_tunnel" :
                	self.tunnel_ctl(1,cur_user,cur_pass,l_port,r_port)
		if cmd == "disable_tunnel" :
			self.tunnel_ctl(0,cur_user,cur_pass,l_port,r_port)

	def tunnel_ctl(self,state,user,pswd,local_port,rem_port):
		
		tunnel_cmd = "sshpass -p "+pswd+" ssh -f -o StrictHostKeyChecking=no \
-o ServerAliveInterval=10 \
-o ServerAliveCountMax=3 \
-R "+(str(local_port))+":localhost:"+(str(rem_port))+"user@server"
		print "tunnel startup command="+tunnel_cmd

	def load_config(self,conf_file):
		config_data= []		
		pairs= []
		parse_count=0
		f = open(conf_file,'r')
		for line in f.readlines():
			if line.find('=')>= 0:
				pairs=line.split('=')
				print "pairs="+pairs[0]+","+pairs[1]
				config_data[parse_count]=pairs[1]
				print "config line="+config_data[parse_count]
				parse_count +=1
								
			else:
				print "Parse error in config file!\noffending line was "+line
				return -1
