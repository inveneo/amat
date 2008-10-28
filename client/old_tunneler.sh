#!/bin/bash
# field 8 for Linux, 6 for Mac
#iface=`netstat -rn |awk '/UG/ { print $8} ' `
iface=`netstat -rn |awk '/UG/ { print $6} ' `

mac=`/sbin/ifconfig eth1|awk 'NR == 1 { gsub(/[:-]/,"");print $5}'`
hosttype="client"
cust=`echo somerandomcustname|cut -c 1-100`
desc=`echo some free random description|cut -c 1-300`
geo="37.784825,-122.419968"

if [ -x /etc/hostname ]
  then
	hostname=`cat /etc/hostname`
  else
	hn=`which hostname`
	if [ -n $hn ] 
	   then 
		hostname=`$hn|cut -c 1-50`
	else
		hostname="inveneo-$hosttype"
	fi
fi

echo "Initial parameters are:"
echo "iface=$iface"
echo "mac=$mac"
echo "hosttype=$hosttype"
echo "hostname=$hostname"
echo "cust=$cust"
echo "desc=$desc"
echo "geo=$geo"
