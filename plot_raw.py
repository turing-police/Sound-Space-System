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
    # print("Input == {}  ||  Current == {}  ||  Output == {}".format(time.inputBufferAdcTime, time.currentTime, time.outputBufferDacTime))
    # print(time.inputBufferAdcTime, end="  |  ")
    # print(time.currentTime)
    # print()
    if status:
        print(status, flush=True)

    # print(time)
    # print ("TYPE = ",type(indata))
    # print("INDATA == ", indata)
    times.put(time)
    queue.put(indata)





def makeFig():
    plt.scatter(xList,yList) # I think you meant this
    print(plt)

plt.ion() # enable interactivity
fig=plt.figure() # make a figure

xList = []
yList = []

with sd.InputStream(samplerate=RATE, device=None, channels=CHANNELS, callback=callback, dtype='int32'):
    print("#" * 80)
    print("press Ctrl+C to stop the recording")
    print("#" * 80)
    while True:
        xList.append(times.get())
        yList.append(queue.get())
        drawnow(makeFig)
        plt.pause(0.001)
        # buffLength = 100
        # plt.plot(queue.get())
        # print(queue.get())
        # sock.send(queue.get())




for i in np.arange(50):
    xList.append(i)
    yList.append(y)
    print(len(xList))
    if (len(xList) > 5120):
        print("TRUEEE")
        plt.clf()
        xList = []
        yList = []
    drawnow(makeFig)

        # xList = xList[512:]
        # yList = yList[512:]
    #makeFig()      The drawnow(makeFig) command can be replaced
    #plt.draw()     with makeFig(); plt.draw()
    plt.pause(0.001)
