#!/usr/bin/env python
import rospy
import socket
import sys

from std_msgs.msg import String
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.1', 9999))

#rospy.init_node('rostalker', anonymous=True)
    
def talker():
    pub = rospy.Publisher('chair', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    while True:
        EchoData = client_socket.recv(1024);
        rospy.loginfo("Pub to chair %s",EchoData)
        pub.publish(EchoData)
    rospy.spin()

if __name__ == '__main__':
    try:
        print("hi Jenny, Node2 Started Pub to chair")
        talker()
    except rospy.ROSInterruptException:
        pass

