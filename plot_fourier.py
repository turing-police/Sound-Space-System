#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import sounddevice as sd
from queue import Queue
from drawnow import drawnow



import serial
import numpy as np
# from matplotlib import pyplot as plt

# plt.ion() # set plot to animated

RATE = 44100

CHANNELS = 1

queue = Queue()
times = Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    time = np.linspace(time.inputBufferAdcTime, time.currentTime, 512)

    if status:
        print(status, flush=True)

    times.put(time)
    queue.put(indata)


plt.ion() # enable interactivity
fig=plt.figure() # make a figure


xList = []
yList = []
def makeFig():
    spectrum = np.fft.fft(yList)
    frequencies = np.fft.fftfreq(len(spectrum))
    plt.plot(frequencies,spectrum)
    plt.ylim(-10e9, 10e9)
    plt.pause(1e-9)
    # plt.show()
    # plt.pause(1)
    # plt.ylim(-1e8, 1e8)
    # plt.scatter(xList, yList)
    # plt.xlim(xList[0], xList[-1])
    # plt.pause(1e-9)

with sd.InputStream(samplerate=RATE, device=None, channels=CHANNELS, callback=callback, dtype='int32'):
    print("#" * 80)
    print("press Ctrl+C to stop the recording")
    print("#" * 80)
    while True:
        time = times.get()
        data = queue.get().reshape(512)
        xList = time
        yList = data
        # xList.append(time)
        # yList.append(data)

        drawnow(makeFig)
        # plt.pause(1e-9)
