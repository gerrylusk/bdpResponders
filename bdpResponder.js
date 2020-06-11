// This will listen for a discovery query from a Barco EventMasterToolset and reply with our web interface information
//
// Barco assumes your web interface is on port 80. If it isn't, redirect 80 to your webserver using iptables or pf
// sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-ports 8000
// echo "rdr pass inet proto tcp from any to any port 80 -> 127.0.0.1 port 8000" | sudo pfctl -ef -
//


var os = require( 'os' ); // for getting our network info
var networkInterfaces = os.networkInterfaces();
var myHostname = os.hostname();
var myAddress = networkInterfaces["eth0"][0].address

var dgram = require('dgram');
var server = dgram.createSocket('udp4');

server.on('listening', function() {
   var address = server.address();
   console.log('UDP Server listening on ' + address.address + ':' + address.port);
});

server.on('message', function(message, remote) {
   console.log("Received \'" + message + "\' from " + remote.address + ":" + remote.port);
// send my response if it's not my own tally system asking
   if( remote.address != myAddress ) {
      var myResponse = "hostname=" + myHostname + ":0:Web-Control:0:0:0:1.0" + "\x00" + "ip-address=" + myAddress + "\x00" + "mac-address=0" + "\x00" + "type=web-interface" + "\x00"
      server.send(myResponse, 0, myResponse.length, remote.port, remote.address, function(err, bytes) {
         if(err) throw err;
      });
      console.log("Answered with: " + myResponse);
   }
});

server.bind(40961);
