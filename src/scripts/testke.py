#import socket
import serial
import sys
import time

ser = serial.Serial('/dev/ttyACM0',115200)
#ser = serial.Serial('/dev/tty7',115200, timeout=1)
#ser = serial.Serial('COM5',115200, timeout=1)
#ser.close()
#ser.open()
#time.sleep(1)
print("Test")
ser.write(b'GO0000')
#time.sleep(4)
#print("Test 123")
#ser.write(b'F60L01')

#time.sleep(2)
#print("Test 1234")
#ser.write(b'TEST00')


ser.close()
        
