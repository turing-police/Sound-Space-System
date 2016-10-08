#!/usr/bin/python3

import sys
import socket
import struct

if len(sys.argv) != 4:
	print('Usage: ip x y')
	exit()

ip = sys.argv[1]
port = 8888

x = int(sys.argv[2])
y = int(sys.argv[3])

print((x, y))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))

print('Sending coordinates')
sock.send(struct.pack('II', x, y))

print('Waiting for acknowledgement')
sock.recv(1)
print('Starting transmission')

while True:
	# Send junk
	sock.send(b'a')
