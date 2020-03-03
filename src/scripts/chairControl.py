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
def get_orientation(m): 
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
        self.pre_orientation = 0.0
        self.target_orientation = 0.0 
        #self.pid_started = False
        self.chairControllerOn = False
        
        # TODO: Raed this is as a parm
        self.angle_correction_rate = 1 # 1 radian/second 

        # Init ROS node
        rospy.init_node('chairControl')
        rospy.loginfo('ROS node chairControl started. ')
    
        # Publishers
        self._ChairControl_Pub = rospy.Publisher("/chairControl/cmd_vel", Twist, queue_size=10)  # to drive the chair
        #self._ChairSetpoint_Pub = rospy.Publisher("/setpoint", Float64, queue_size=10)  # to set up pid controller
        #self._EnablePID_Pub = rospy.Publisher("/pid_enable", Bool, queue_size=10) # start/stop pid out control_effort msg

    
        # Subscribers
        rospy.Subscriber('/tf', TFMessage, self.chairPoseCB) # Current Postion
        rospy.Subscriber('/chairControl_TestCmd', Twist, self.chairControlCB) # New Drive command
        #rospy.Subscriber('/control_effort', Float64, self.chairPIDControlCB) # Adapt the angular velocity

    def Start(self):
        while not rospy.is_shutdown():
            rospy.sleep(1)
  

    # Handler to get current chair position
    def chairPoseCB(self, m):
        _, _, yaw = get_orientation (m)
        #if JKM: print("yaw: ", yaw)

        # For now , update at every IMU tick. 
        self.current_orientation = yaw  #

        if self.chairControllerOn:
            target_speed = self.target_speed

            # Calculate & adjust angular velocity
            angular_error = self.target_orientation - self.current_orientation  # in radians
            new_angle_vel = angular_error * self.angle_correction_rate  # what about deadzone
            rospy.loginfo("Angular error is: %f . Adjusting angular velocity to: %f ", angular_error, new_angle_vel)
              
            # Send a cmd_vel message to chair
            msg = Twist()
            msg.linear.x = target_speed
            msg.angular.z = new_angle_vel # temp               
            # Publish
            self._ChairControl_Pub.publish(msg)


    # procedure to stop/start chairController with new value.    
    def chairInitNewControl(self):

        # Check if should be stopping. 
        if ((self.target_speed == 0.0) & (self.target_relative_orientation == 0.0)): 
            rospy.loginfo("Stopping chair & chairController")

            # stop the chairController
            self.chairControllerOn = False
            rospy.loginfo("Stopping chair controller.")

            # stop the chair, publish message to control TODO: Make  proc to stop
            msg = Twist()
            msg.linear.x = self.target_speed
            msg.angular.z = self.target_relative_orientation               
            # Publish
            self._ChairControl_Pub.publish(msg)
            rospy.loginfo("Sending msg to stop chair.")
             
            
        else:
            # Enable the chairController if needed.
            rospy.loginfo("Initializing new chairControl request.")
            if (False == self.chairControllerOn):
                self.chairControllerOn = True
                rospy.loginfo("Starting chairController.") 
            
            # Calculate the new desired target orientation.
            rospy.loginfo("Current orientation is: %f", self.current_orientation )
            self.target_orientation = self.current_orientation + self.target_relative_orientation
            rospy.loginfo("Target orientation setpoint for chairController is %f", self.target_orientation)



    # Handler to get a new chairDriveCmd
    # Note: getting Twist message but really the angular velocity field represents the desired relative angle
    #    TODO: maybe I should look into using a POSE msg 
    def chairControlCB(self, m):
        rospy.loginfo('New chairControl command received: linear_vel: %f relative_angle:%f ', m.linear.x, m.angular.z)
        self.target_relative_orientation = m.angular.z
        self.target_speed = m.linear.x 
        self.chairInitNewControl()


    '''
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
        msg = Twist()
        msg.linear.x = self.target_speed # Fixed for now              
        msg.angular.z = 0.1 * control_effort # effort , angular velocity , rate to turn              
        # Publish
        self._ChairControl_Pub.publish(msg)       
     ''' 

if __name__ == '__main__':
    chairControl = ChairControl() 
    chairControl.Start()


