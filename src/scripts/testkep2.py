#import socket
import serial
import sys
import time

ser = serial.Serial('/dev/ttyACM0',115200, timeout=1)
ser.close()
ser.open()
print("Test")
cmd = "GO0000"
ser.write(cmd)
time.sleep(2)
ser.write("F60L01")
time.sleep(2)
print("Test 1234")
ser.write("TEST00")
ser.close()
        
