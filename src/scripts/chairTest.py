#!/usr/bin/env python

# A utility to send test /drive sequence actions to the chair for test purposes.

import rospy
from wc_msgs.msg import Chair 

import sys
import argparse

from chairCmd import chairSendByCmdLine

# Create the parser
def pair(arg):
    # For simplity, assume arg is a pair of strings
    # separated by a comma. If you want to do more
    # validation, raise argparse.ArgumentError if you
    # encounter a problem.
    return [str(x) for x in arg.split(',')] 

parser = argparse.ArgumentParser(description='Send a sequence of commands to /drive to test chair reaction.')
parser.add_argument('list', type=pair, nargs='+',
      help='List of drive command,seconds delay eg: F70L00,3 B30L05,6.5')

# Create the publisher
pub = rospy.Publisher('drive', Chair, queue_size=1)
rospy.init_node('chairTest', anonymous=True)

ByCommandLine=True

# Send a message to the chair 
def chairSend(command):
    if ByCommandLine: 
        chairSendByCmdLine(command)
    else: 
        msg = Chair()
        msg.header.stamp = rospy.Time.now()
        msg.data.data = command
        pub.publish(msg)

    rospy.loginfo("Sending command to chair: %s ", command)


def chairTest(l):
    print (l)
    #Send a GO command to the chair to start the test
    chairSend("GO0000")
    #rospy.sleep(0.5)
    for command, delay in l:
        chairSend(command)
        rospy.loginfo("Delay for: %s seconds.", delay)
        rospy.sleep(float(delay))

    #
    # Send final stop command
    chairSend("STOP00")




if __name__ == '__main__':
    args = parser.parse_args()
    try:
        chairTest(args.list)
        
    except Exception : # (rospy.ROSInterruptException, select.error):
        # rospy.logwarn("Interrupted... Stopping.")
        raise


