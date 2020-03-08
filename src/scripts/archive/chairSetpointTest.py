#!/usr/bin/env python
#   chairSetpointTest Node for issuing setpoint commands to wc pid system from a user command line interface
# 
import roslib  # JKM; roslib.load_manifest('YOUR_PACKAGE_NAME_HERE')
import rospy
from std_msgs.msg import String, Float64
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

parser = argparse.ArgumentParser(description='Sequence of setpoint commands to send with delay T',
                                  prefix_chars='~') # Work around to allow negative number with - character
parser.add_argument('list', type=get_cmds, nargs='+',
      help='List of setpoint commands angle(r/s),Tseconds  eg: 0.0,5 0.1,20')

def chairSetpointCmdsGet(l):
    return l

# JKM - for debug
JKM = True


# Global: TODO: Make this a param definined via a launch file
#    '/setpoint' for straight to pid cntrl
#    '/chairDriveCmd' for going to chairControl
chairSetpointTest_out = '/setpoint'


  

if __name__ == '__main__':

    # Get the user command line arguments    
    args = parser.parse_args()
    msg = Float64()
    try:
        cmds = chairSetpointCmdsGet(args.list)      
    except Exception : # (rospy.ROSInterruptException, select.error):
        # rospy.logwarn("Interrupted... Stopping.")
        raise
   
    #TODO- make part of class instead of being globals
    rospy.init_node('chairSetpointTestNode', anonymous=True)
    rospy.loginfo('\n ROS node chairSetpointTestNode started. ')
    chairSetpointTest = rospy.Publisher(chairSetpointTest_out, Float64, queue_size=10)
    rospy.loginfo('\n chairSetpointTest publisher made.')
    rospy.sleep(0.5) # JKM: if I do not have this,  I do not get the  first message published in the list. 

    for a,t in cmds :
       #if JKM: print("got this: ", x, z, t)
       msg.data = float(a)
       rospy.loginfo('Publishing a setpoint to topic %s:\n%s', chairSetpointTest_out, msg)
       chairSetpointTest.publish(msg)
       rospy.loginfo("Delaying for: %s seconds.", t)
       rospy.sleep(float(t))
    
    # All done.
    rospy.loginfo('\n chairSetpointTestNode shutting down. Test is complete')

