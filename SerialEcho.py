#!/usr/bin/python3

'''
Simple Python program to read from the simple sensor
and output the data to stdout.
'''

import serial
import os

ser = serial.Serial('/dev/ttyACM0')

while True:
	os.write(1, ser.read())
