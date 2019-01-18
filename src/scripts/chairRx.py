#!/usr/bin/env python

# Chair Receive Serial Node
# =========================
#   Receive on serial port and publish on "chair" topic


import rospy
import sys
import serial
from std_msgs.msg import String

from wc_msgs.msg import ChairRx

ARDUINO = '/dev/ttyUSB0' #'/dev/ttyACM0' --- depending on the arduino hw  TODO: make this a parm 
ser = serial.Serial(ARDUINO,115200)
    
def chairRx():
    pub = rospy.Publisher('chair', ChairRx, queue_size=10)  # using new message type to add timestamp
    # pub = rospy.Publisher('chair', String, queue_size=10) " old message type String
    rospy.init_node('chairRx', anonymous=True)
    msg = ChairRx()
    while True:
        # Wait until message arrives on serial port
        data = ser.readline()
        rospy.loginfo(rospy.get_caller_id() + " Received on serial port %s", data )
        #TODO fill in header with timestamp, also check data is valid.
        msg.header.stamp = rospy.Time.now()
        msg.data.data = str(data)
        pub.publish(msg)
        #pub.publish(data)
    #rospy.spin()

if __name__ == '__main__':
    try:
        print("chairRx started to read from serial to publish to topic chair")
        chairRx()
    except rospy.ROSInterruptException:
        pass

