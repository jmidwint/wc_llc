#!/usr/bin/env python
#   chairTwistTest Node for issuing Twist commands to drive the wheelchair from a user command line interface
# 
import roslib  # JKM; roslib.load_manifest('YOUR_PACKAGE_NAME_HERE')
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

import sys
import argparse


# Create the parser
def get_cmds(arg):
    # For simplity, assume arg is a set of strings
    # separated by a comma. If you want to do more
    # validation, raise argparse.ArgumentError if you
    # encounter a problem.
    return [cmds for cmds in arg.split(',')] 

parser = argparse.ArgumentParser(description='Sequence of cmd_vel commands to send with delay T')
parser.add_argument('list', type=get_cmds, nargs='+',
      help='List of cmd_vel commands linearX, angularZ, Tseconds  eg: 0.1,0.1,3    0.1,0.0,6.5')

def chairTwistCmdsGet(l):
    return l

# JKM - for debug
JKM = True


# Global: TODO: Make this a param
#  
chairTwistTest_out = '/chairDriveCmd' # Send into chairController  # '/chairTwistTest/cmd_vel'


if __name__ == '__main__':

    # Get the user command line arguments    
    args = parser.parse_args()
    msg = Twist()
    try:
        cmds = chairTwistCmdsGet(args.list)      
    except Exception : # (rospy.ROSInterruptException, select.error):
        # rospy.logwarn("Interrupted... Stopping.")
        raise
   
    #TODO- make part of class instead of being globals
    rospy.init_node('chairTwistTestNode', anonymous=True)
    rospy.loginfo('\n ROS node chairTwistTestNode started. ')
    chairTwistTest = rospy.Publisher(chairTwistTest_out, Twist, queue_size=10)
    rospy.loginfo('\n chairTwistTest publisher made.')
    rospy.sleep(0.5) # JKM: if I do not have this,  I do not get the  first message published in the list. 

    for x,z,t in cmds :
       #if JKM: print("got this: ", x, z, t)
       msg.linear.x = float(x)
       msg.angular.z = float(z)
       rospy.loginfo('Publishing a cmd_vel to topic %s:\n%s', chairTwistTest_out, msg)
       chairTwistTest.publish(msg)
       rospy.loginfo("Delaying for: %s seconds.", t)
       rospy.sleep(float(t))
    
    # All done.
    rospy.loginfo('\n chairTwistTestNode shutting down. Test is complete')

