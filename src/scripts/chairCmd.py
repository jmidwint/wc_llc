#!/usr/bin/env python

# A utility to send text string message to the chair.

import rospy
from wc_msgs.msg import Chair 

import sys
import argparse

# Emulate this command line command
#   
# rostopic pub /drive wc_msgs/Chair '{header: {seq: 1, stamp: 1, frame_id: DC}, data: { data: DCON00} }' --once

parser = argparse.ArgumentParser(description='Publish a text command to topic /drive to send to the chair.')
parser.add_argument('text', type=str, help='A text command.')

def chairSend(m):
    # Create the publisher
    pub = rospy.Publisher('drive', Chair, queue_size=1)
    rospy.init_node('chairCmd', anonymous=True)

    msg = Chair()
    msg.header.stamp = rospy.Time.now()
    msg.data.data = m
    pub.publish(msg)
    rospy.loginfo("Sending command to chair: %s ", m)

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        chairSend(args.text)
    except Exception : # (rospy.ROSInterruptException, select.error):
        # rospy.logwarn("Interrupted... Stopping.")
        raise


