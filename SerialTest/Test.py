#!/usr/bin/env python
#%% test serial communication
import serial
a = serial.Serial('COM5', baudrate=115200)
a.write("test")
print(a.read(4))
a.close()