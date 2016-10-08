#!/usr/bin/python3

import sys
import socket
import struct
import sounddevice as sd
from queue import Queue

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
			print(queue.get())
			sock.send(queue.get())

	# sock.send(b'a')
