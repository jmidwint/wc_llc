#!/usr/bin/env python

# A utility to send text string message to the chair.

import rospy
from wc_msgs.msg import Chair 

import sys
import argparse
import os

# Emulate this command line command
#   
# rostopic pub /drive wc_msgs/Chair '{header: {seq: 1, stamp: 1, frame_id: DC}, data: { data: DCON00} }' --once

parser = argparse.ArgumentParser(description='Publish a text command to topic /drive to send to the chair.')
parser.add_argument('text', type=str, help='A text command.')

def chairSendByNode(m):
    # Create the publisher
    pub = rospy.Publisher('drive', Chair, queue_size=1, latch=True)
    rospy.init_node('chairCmd', anonymous=True)
    rospy.sleep(0.5)
    msg = Chair()
    msg.header.stamp = rospy.Time.now()
    msg.data.data = m
    pub.publish(msg)
    rospy.loginfo("Sending command to chair: %s ", m)

def chairSendByCmdLine(m):
    # Klugy way to get around using single quote & {} in text strings
    str_cmd = 'rostopic pub /drive wc_msgs/Chair '
    str_data1 = " '{header: {seq: 1, stamp: 1, frame_id: JKM}, data: { data: " 
    str_data2 = m 
    str_data3 = " } }' --once"

    cmd = str_cmd + str_data1 + str_data2 + str_data3
    print ( "Performing: {0}".format (cmd))
    os.system(cmd)  # Make it simple & do not care about getting errors back.
    print("Done")

 

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        chairSendByCmdLine(args.text)
    except Exception : # (rospy.ROSInterruptException, select.error):
        # rospy.logwarn("Interrupted... Stopping.")
        raise


