There are 2 files one for client and one for server.
To have multiple server copy the same server file.

Run servers in different machines. 


Run the server as: p2mpserver port# file-name p
for eg:
p2mpserver.py 7735 test.txt 0.01
here, 
port# is 7735 filename is test.txt where the received file will be saved. P=0.01 which indicated the probability value.


Run the clients as: p2mpclient server-1 server-2 server-3 server-port# file-name MSS
for eg. 
p2mpclient.py 192.168.0.4 192.168.0.17 7735 rfc3435.txt 500
here,
There are two servers with IP 192.168.0.4 and 192.168.0.17 binded to port 7735.
We are transfering file rfc3435.txt with MSS=500.


Tested in Linux and windows machines.