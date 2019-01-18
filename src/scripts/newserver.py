import socket
import serial
import sys
from time import sleep

ser = serial.Serial('/dev/ttyACM0',115200)
s = socket.socket()
host = "192.168.1.1"
port = 9998
s.bind((host,port))
s.listen(5)
print("Server Started")
while True:
    c, addr = s.accept()
    print("connected")
    while True:
        #print repr(addr[1]) + ": "+ c.recv(16)
        data = c.recv(1024)
        print data
        ser.write(data)
    c.close()
	
