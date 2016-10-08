#!/usr/bin/python3

import sys
import socket
import struct
import time
import sounddevice as sd
from queue import Queue

if len(sys.argv) != 5:
	print('Usage: ip x y scale')
	exit()

ip = sys.argv[1]
port = 8888

x = int(sys.argv[2])
y = int(sys.argv[3])

scale = float(sys.argv[4])

print((x, y))

sock = None

while True:
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(0.5)
		sock.connect((ip, port))
		break
	except OSError as err:
		print(err)
		if(err.errno != TimeoutError):
			time.sleep(0.5)
			
sock.settimeout(None)

print('Sending coordinates')
sock.send(struct.pack('II', x, y))

print('Waiting for acknowledgement')
sock.recv(1)
print('Starting transmission')

queue = Queue()

def callback(indata, frames, time, status):
	"""This is called (from a separate thread) for each audio block."""
	if status:
		print(status, flush=True)
	# print ("TYPE = ",type(indata))
	# print("INDATA == ", indata)
	queue.put(indata)


RATE = 44100

CHANNELS = 1


with sd.RawInputStream(samplerate=RATE, device=None, channels=CHANNELS, callback=callback, dtype='int32'):
		print("#" * 80)
		print("press Ctrl+C to stop the recording")
		print("#" * 80)
		while True:
			sock.send(queue.get())
