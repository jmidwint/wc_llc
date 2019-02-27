#!/usr/bin/env python

# Chair Receive Serial Node
# =========================
#   Receive on serial port and publish on "chair" topic

import select
import rospy
import sys
import serial
from std_msgs.msg import String

from wc_msgs.msg import Chair



#ARDUINO = '/dev/ttyUSB0' #'/dev/ttyACM0' --- depending on the arduino hw

#TODO: should be in a  class
# Load our ROS Parameters
arduino_name = rospy.get_param('/arduino_device_name')
arduino_baud = rospy.get_param('/arduino_device_baud')
ser = serial.Serial(arduino_name, arduino_baud)
    
def chairRx():
    pub = rospy.Publisher('chair', Chair, queue_size=10)
    rospy.init_node('chairRx', anonymous=True)

    msg = Chair()
    while True:
        # Wait until message arrives on serial port
        data = ser.readline().strip()
        # rospy.loginfo(rospy.get_caller_id() + " Received on serial port %s", data )
        msg.header.stamp = rospy.Time.now()
        msg.data.data = str(data)
        pub.publish(msg)
        #pub.publish(data)
    #rospy.spin()


if __name__ == '__main__':
    try:
        rospy.loginfo("Node chairRx starting ... receive serial i/f to /chair")
        chairRx()
    except Exception : # (rospy.ROSInterruptException, select.error):
        # rospy.logwarn("Interrupted... Stopping.")
        raise

    

