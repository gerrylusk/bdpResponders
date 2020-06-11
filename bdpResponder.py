#! /usr/bin/python

## This will listen for a discovery query from a Barco EventMasterToolset and reply with our web interface information
##
## Barco assumes your web interface is on port 80. If it isn't, redirect 80 to your webserver using iptables or pf
## sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8000
## echo "rdr pass inet proto tcp from any to any port 80 -> 127.0.0.1 port 8000" | sudo pfctl -ef -
##

import socket
import sys

## Create a UDP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

## Bind the socket to the port
server_address = ('', 40961)
print >>sys.stderr, 'starting up bdpResponder on %s port %s' % server_address
sock.bind(server_address)

## Wait for a message and reply to it
while True:
	print '\nwaiting to receive message'
	data, address = sock.recvfrom(4096)
	
	print 'received %s bytes from %s' % (len(data), address)
	print data
	
	myHostname = socket.gethostname()
	myAddress = socket.gethostbyname(socket.gethostname())
	##hostname=EC-200:N/A:System1:0:N/A:N/A:5.0.35479.ip-address=192.168.0.180.mac-address=00:0b:ab:98:ba:cf.type=EC-200.
	##hostname=NAME:XML-PORT:SHOW-NAME:UNIT-ID:VP-COUNT:MASTER-MAC:VERSION.ip-address=192.168.0.180.mac-address=00:0b:ab:98:ba:cf.type=EC-200.
	sendData = "hostname=" + myHostname + ":0:Web-Control:0:0:0:1.0" + "\x00" + "ip-address=" + myAddress + "$8080" + "\x00" + "mac-address=0"+ "\x00" + "type=web-interface"+ "\x00"
		
	if data:
		sent = sock.sendto(sendData, address)
		print 'sent %s bytes back to %s' % (sent, address)
		print '%s' % sendData
		
