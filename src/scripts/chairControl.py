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
import math
import tf
import tf2_ros
import tf2_msgs.msg
from std_msgs.msg import Bool, Float64

#from nav_msgs.msg import Odometry
#from geometry_msgs.msg import TransformStamped

from tf2_msgs.msg import TFMessage
from tf.transformations import *

JKM = True
# JKM - hardcode for now, will send in as a subscribed target 
TARGET_DIRECTION= 0.0

# Utility transform conversion
def get_orientation(self, m): 
    # Find the orientation from the message
    roll, pitch, yaw = tf.transformations.euler_from_quaternion(
                                  [m.transforms[0].transform.rotation.x, 
                                   m.transforms[0].transform.rotation.y, 
                                   m.transforms[0].transform.rotation.z, 
                                   m.transforms[0].transform.rotation.w]) 
    # if JKM: print ("yaw: ", yaw)
    return roll, pitch, yaw   

class ChairControl(object):
    def __init__(self):
        self.target_relative_orientation = TARGET_DIRECTION
        self.target_speed = 0.0 
        self.current_orientation = 0.0
        self.target_orientation = 0.0 
        self.pid_started = False

        # Init ROS node
        rospy.init_node('chairControl')
        rospy.loginfo('ROS node chairControl started. ')
    
        # Publishers
        self._ChairControl_Pub = rospy.Publisher("/chairControl/cmd_vel", Twist, queue_size=10)  # to drive the chair
        self._ChairSetpoint_Pub = rospy.Publisher("/setpoint", Float64, queue_size=10)  # to set up pid controller
        self._EnablePID_Pub = rospy.Publisher("/pid_enable", Bool, queue_size=10) # start/stop pid out control_effort msg

    
        # Subscribers
        # rospy.Subscriber('/tf', TFMessage, self.chairPoseCB) # Current Postion
        rospy.Subscriber('/chairControl_TestCmd', Twist, self.chairControlCB) # New Drive command
        rospy.Subscriber('/control_effort', Float64, self.chairPIDControlCB) # Adapt the angular velocity

    def Start(self):
        while not rospy.is_shutdown():
            rospy.sleep(1)
  

    # Handler to get current chair position
    '''
    def chairPoseCB(self, m):
        _, _, yaw = self.get_orientation (m)
        print("yaw: ", yaw)
        self.current_orientation = yaw  # TODO: maybe also keep the Quaterion?        
    '''     

    # Handler to get a new chairDriveCmd
    # Note: getting Twist message but really the angular velocity field represents the desired relative angle
    #    - maybe I should look into using a POSE msg 
    def chairControlCB(self, m):
        rospy.loginfo('New chairControl command received: linear_vel: %f relative_angle:%f ', m.linear.x, m.angular.z)
        self.target_relative_orientation = m.angular.z
        self.target_speed = m.linear.x 
 
        # Go and sample the current position
        # TODO: add a try block here
        rospy.loginfo("Getting current orientation.")
        msg_position = rospy.wait_for_message('/tf', TFMessage, timeout=1.0)  # Make a timeout here 
        _, _, yaw = get_orientation(self, msg_position)
        self.current_orientation = yaw
        rospy.loginfo("Current orientation is: %f", self.current_orientation )       

        # Set up for PID here
        # ====================
        # TODO: think about moving all this logic to a procedure


        # Check if should be stopping. 
        if ((self.target_speed == 0.0) & (self.target_relative_orientation == 0.0)): 
            rospy.loginfo("Stopping chair & chair PID")

            # stop the pid
            self.pid_started = False
            self._EnablePID_Pub.publish(self.pid_started)
            rospy.loginfo("Stopping chair control pid.")

            # stop the chair, publish message to control TODO: Make  proc to stop
            msg = Twist()
            msg.linear.x = self.target_speed
            msg.angular.z = self.target_relative_orientation               
            # Publish
            self._ChairControl_Pub.publish(msg)
            rospy.loginfo("Sending msg to stop chair.")
             
            
        else:
            # Enable the PID if needed.
            rospy.loginfo("Something to do")
            if (False == self.pid_started):
                self.pid_started = True
                # Send enable PID message
                self._EnablePID_Pub.publish(self.pid_started)
                rospy.loginfo("Starting chair control pid.") 
            
            # Calculate the desired target orientation. If velocity is stopped.
            self.target_orientation = self.current_orientation + self.target_relative_orientation
            rospy.loginfo("Target orientation setpoint for PID is %f", self.target_orientation)
            self._ChairSetpoint_Pub.publish(self.target_orientation)
            rospy.loginfo("Target setpoint value sent to pid controller")

    # Call back to handle the control_effort from the PID controller
    #   Format & send /cmd_vel command             
    def chairPIDControlCB(self, m):                        
        # TEMP: Sending something, this will happen in controlCB message
        #control_amount = Float64()
        #control_amount.data = 0.0
        control_effort = m.data
        
        # 1st order plant
        # control_rate = (0.1 * self.target_orientation) + control_effort 
        msg = Twist()
        msg.linear.x = self.target_speed # temporary
        msg.angular.z = self.target_orientation + (0.001) * control_effort # get this later when get a control message back                  
        # Publish
        self._ChairControl_Pub.publish(msg)       
 

if __name__ == '__main__':
    chairControl = ChairControl() 
    chairControl.Start()


