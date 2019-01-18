import socket
import serial
import sys
from time import sleep

ser = serial.Serial('/dev/ttyACM0',115200)
s = socket.socket()
host = "192.168.1.1"
port = 9999
s.bind((host,port))
s.listen(5)
print("echo server started")
while True:
    c, addr = s.accept()
    print("connected")
    while True:
        #while ser.inWaiting:
        echodata = ser.readline()
        print echodata
        c.sendall(echodata)

    c.close()
