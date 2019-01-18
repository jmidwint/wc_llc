#!/usr/bin/env python
import rospy
import sys
import serial

from std_msgs.msg import String

ARDUINO = '/dev/ttyUSB0' #'/dev/ttyACM0' --- depending on the arduino hw  TODO: make this a parm 
ser = serial.Serial(ARDUINO,115200)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " Sending out serial %s", data.data)
    ser.write(data.data)
    #client_socket.send(data.data)
    
def chairTx():        
    rospy.init_node('chairTx', anonymous=True)
    rospy.Subscriber("drive", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print("chairTx started reading from drive to transmit to serial")
    chairTx()
