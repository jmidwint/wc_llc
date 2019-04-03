#!/usr/bin/env python
import rospy
import sys
import serial

from std_msgs.msg import String
from wc_msgs.msg import Chair 

'''
ARDUINO = '/dev/ttyUSB0' #'/dev/ttyACM0' --- depending on the arduino hw  TODO: make this a parm 
ser = serial.Serial(ARDUINO,115200)
'''

#TODO: should be in a  class
arduino_name = rospy.get_param('/arduino_device_name')
arduino_baud = rospy.get_param('/arduino_device_baud')
ser = serial.Serial(arduino_name, arduino_baud)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + " Sending out serial %s", data.data.data)
    ser.write(data.data.data)
    #client_socket.send(data.data)
    
def chairTx():        
    rospy.init_node('chairTx', anonymous=True)
    #rospy.Subscriber("drive", String, callback)
    rospy.Subscriber("drive", Chair, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    rospy.loginfo("Node chairTx starting ... transmit /drive to serial i/f")
    chairTx()
