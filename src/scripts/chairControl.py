#!/usr/bin/env python
#   chairControl Node for controlling direction of chair.
#     .... prototyping 
# 
import roslib  # JKM; roslib.load_manifest('YOUR_PACKAGE_NAME_HERE')
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

import sys
import argparse






#!/usr/bin/env python
import rospy
import math
import tf
import tf2_ros
import tf2_msgs.msg


#from nav_msgs.msg import Odometry
#from geometry_msgs.msg import TransformStamped

from tf2_msgs.msg import TFMessage
from tf.transformations import *

JKM = True
# JKM - hardcode for now, will send in as a subscribed target 
TARGET_DIRECTION= 0.0

class ChairControl(object):
    def __init__(self):
        self.target_relative_orientation = TARGET_DIRECTION
        self.current_orientation = 0.0
        self.target_orientation = 0.0 

        # Init ROS node
        rospy.init_node('chairControl')
        rospy.loginfo('\n ROS node chairControl started. ')
    
        # Publishers
        self._ChairControl_Pub = rospy.Publisher("/chairControl/cmd_vel", Twist, queue_size=10)
        self._ChairControlEuler
    
        # Subscribers
        rospy.Subscriber('/tf', TFMessage, self.chairControlCB)

    def Start(self):
        while not rospy.is_shutdown():
            rospy.sleep(1)
  

    def get_orientation(self, m): 
        # Find the orientation from the message
        roll, pitch, yaw = tf.transformations.euler_from_quaternion(
                                  [m.transforms[0].transform.rotation.x, 
                                   m.transforms[0].transform.rotation.y, 
                                   m.transforms[0].transform.rotation.z, 
                                   m.transforms[0].transform.rotation.w]) 
        # if JKM: print ("yaw: ", yaw)
        return roll, pitch, yaw   

    def chairControlCB(self, m):
        _, _, yaw = self.get_orientation (m)
        print("yaw: ", yaw)
        self.starting_orientation        
     
 

if __name__ == '__main__':
    chairControl = ChairControl() 
    chairControl.Start()


