#!/usr/bin/env python
#   chairTwist Node
import roslib  # JKM; roslib.load_manifest('YOUR_PACKAGE_NAME_HERE')
import rospy


import math
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


# Constants & Globals here.
CHAIR_STR_LEN = 6 

#TODO- make part of class
pubTwist = rospy.Publisher('chairTwist', Twist, queue_size=10)

# JKM - for debug
JKM = True



    
     
def callback(msg):
    msgJoy = msg
    rospy.loginfo("Received joy message: {}".format (msgJoy.axes))
    # Convert to Twist message
    msgTwist = Twist()
    msgTwist.header.stamp = msgJoy.header.stamp #rospy.Time.now()
    msgTwist.linear.x = 0.7*data.axes[1]   # TODO adjust scale
    msgTwist.angular.z = 0.4*data.axes[0]  # TODO adjust scale 
    pubTwist.publish(msgTwist)
    rospy.loginfo("chairTwist message published: {}".format (msgTwist))
    return


# Define the node.Is both publisher and subscriber
# TODO: Convert to class that loads parms, and creates ros log messages on start up

def node():
    rospy.init_node('chairTwistNode')
    print('\n ROS node chairTwistNode started ')
    rospy.Subscriber("chairJoy", Joy, callback)
    rospy.spin()

if __name__ == '__main__':
    node()

