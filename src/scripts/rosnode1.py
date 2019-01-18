#!/usr/bin/env python
import rospy
import socket
import sys
from time import sleep

from std_msgs.msg import String
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.1', 9998))
pub = rospy.Publisher('chair', String, queue_size=10)

#rospy.init_node('rostalker', anonymous=True)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    client_socket.send(data.data)
    
def listener():
          
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("drive", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    print("hi Jenny, node1 started reading from drive")
    listener()
