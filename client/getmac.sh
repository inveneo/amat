#!/bin/bash
mac=`/sbin/ifconfig en0|awk 'NR == 1 { gsub(/[:-]/,"");print $5}'`
#mac=`/sbin/ifconfig eth0|awk 'NR == 1 { gsub(/[:-]/,"");print $5}'`
