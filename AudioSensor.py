#!/usr/bin/python3

import sys
import socket
import struct
import time
import sounddevice as sd
from queue import Queue

plotting = False

if len(sys.argv) != 5:
	if (len(sys.argv) == "p"):
		plotting = True
	else:
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
sock.send(struct.pack('IId', x, y, scale))

print('Waiting for acknowledgement')
sock.recv(1)
print('Starting transmission')

queue = Queue()


if (plotting):
	import numpy as np
	import matplotlib.pyplot as plt
	from drawnow import drawnow
	times = Queue()
	plt.ion() # enable interactivity
	fig=plt.figure(1, figsize=(16,8)) # make a figure

xList = []
yList = []

def makeFig():
    plt.title("Raw Audio Signal")
    plt.ylim(-1e8, 1e8)
    # plt.scatter(xList, yList, c=yList, cmap="coolwarm")
    plt.plot(xList, yList, 'r')
    plt.xlim(xList[0], xList[-1])

    plt.pause(1e-9)


def callback(indata, frames, time, status):
	"""This is called (from a separate thread) for each audio block."""
	if status:
		print(status, flush=True)

	if (plotting):
		time = np.linspace(time.inputBufferAdcTime, time.currentTime, 512)
		times.put(time)
		queue.put(np.frombuffer(indata, dtype='int32'))

	else:
		queue.put(indata)


RATE = 44100

CHANNELS = 1


with sd.RawInputStream(samplerate=RATE, device=None, channels=CHANNELS, callback=callback, dtype='int32'):
		print("#" * 80)
		print("press Ctrl+C to stop the recording")
		print("#" * 80)
		while True:
			data = queue.get()
			print('Sent {0} samples.'.format(len(data)))
			sock.send(data)

			if (plotting):
				xList = times.get()
				yList = data
				drawnow(makeFig)
