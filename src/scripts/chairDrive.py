#!/usr/bin/env python
# 
# This file supports driving the wheelchair by converting /cmd_vel topic to a /drive topic. The /drive topic is then
#   later sent on to the arduino board through a ros node that converts  /drive to a  serial command expected by the arduino. 
#
#   The /cmd_vel topic is produced through number of ways:
#
#      1) as a "drive-by-wire" under human remote control using an xbox controller
# 
#         The joys stick is an xbox controller. Use left joy stick while X button is pressed.
#         Joy stick signals are read by ros joy package and published on /joy.
#         telop_twist_joy converts the  joy stick /joy to /cmd_vel topic for angular momentum and speed.
#
#      2) as "autonomous" under control of the wc_perception model 
#
#      3) as a series of test commands
#   
#
import roslib  # JKM; roslib.load_manifest('YOUR_PACKAGE_NAME_HERE')
import rospy
import tf.transformations
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Twist  # JKM switching to use this as this is coming from the MUXer

#JKM
import datetime
import math
from std_msgs.msg import String
from wc_msgs.msg import Chair


# Define the publisher topic here. It needs to be global.
chairDrive_pub = rospy.Publisher("drive", Chair, queue_size=5)

# JKM - for debug
JKM = False

def convert_to_drive(steer, speed):
    ''' Converts the steer angle in radians to a direction left or right  
        And converts the speed to a velocity either forward or back.
        Command is a 4 ASCII character which is stored in the message as 4 separate Strings

        Format is: F/B 0-70 L/R 0-70
           F = Forward
           B = Back
           L = Left
           R = Right
     
    '''
    MAX_RANGE=70.0 # TODO: make param
    MAX_SPEED=70.0 # TODO: make param
    #drive_msg.dir_fb.data='F' # For now we always move forward in autonomous mode
    #drive_msg.vel_fb.data='20' # For now we always move at a fixed speed unless we have to stop
    #drive_msg.dir_lr.data='L' # Calculate this
    #drive_msg.vel_lr.data='00' # Calculate this

    # Initialize to be stopped
    dir_fb='F' # 
    vel_fb='00' #
    dir_lr='L' # 
    vel_lr='00' # 

    #
    # Determine which direction left or right, and how far
    # steer > 0 , means counter-clockwise , so go towards the LEFT
    # steer < 0 , means clockwise, so go to the RIGHT
    #
    if (steer >= 0 ):
        dir_lr='L'
    else: 
       # steer < 0
       dir_lr='R'
    # amount_lr=(abs(steer) * 4*MAX_RANGE)/math.pi
    amount_lr=abs(steer) * MAX_RANGE
    vel_lr=int(round(amount_lr)) 

    # Determie forward or back and how fast
    if (speed >= 0 ):
        dir_fb='F'
    else: 
       # speed < 0
       dir_fb='B'
    amount_fb=abs(speed * MAX_RANGE)
    vel_fb=int(round(amount_fb)) 

    # Convert to one string
    drive_str = dir_fb + '{:02d}'.format(vel_fb) + \
                dir_lr + '{:02d}'.format(vel_lr) 
    if JKM: 
        print('drive: ', drive_str)  
    return drive_str

    

def callback(msg_received):
    #rospy.loginfo("Received a /cmd_vel message!")
    #print('Received a /cmd_vel message!')
    #rospy.loginfo("Linear Components: [%f, %f, %f]"%(msg.linear.x, msg.linear.y, msg.linear.z))
    #rospy.loginfo("Angular Components: [%f, %f, %f]"%(msg.angular.x, msg.angular.y, msg.angular.z))

    # JKM TODO: make this an if statement based on message type
    # msg = msg_received.twist TwistStamped incoming message type
    msg = msg_received # Twist message type    
    lx, ly, lz = msg.linear.x, msg.linear.y, msg.linear.z
    ax, ay, az = msg.angular.x, msg.angular.y, msg.angular.z
    #if JKM: print ("JKM: lx, ly, lz /n ax, ay, az ", lx, ly, lz, ax, ay, az  )
    #print('Time: {:%H:%M:%S:}'.format(datetime.datetime.now()))
    #if JKM: print ("JKM: lx /n az", lx, az)    

    # Convert to a drive cmd of one string of type standard message & publish
    drive = Chair()
    drive.header.stamp = rospy.Time.now()
    drive.data.data = convert_to_drive(az, lx)
    chairDrive_pub.publish(drive)

# Define the node.Is both publisher and subscriber
# TODO: Convert to class that loads parms, and creates ros log messages on start up
def node():
    rospy.init_node('chairDrive')
    print('\n ROS node chairDrive started ')
    #rospy.Subscriber("/cmd_vel", TwistStamped, callback)
    rospy.Subscriber("/twist_mux/cmd_vel", Twist, callback)
    #chairJoy_pub = rospy.Publisher("drive", Chair, queue_size=5) # set to global
    rospy.spin()

if __name__ == '__main__':
    node()

