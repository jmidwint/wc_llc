#!/usr/bin/env python
import roslib  # JKM; roslib.load_manifest('YOUR_PACKAGE_NAME_HERE')
import rospy


import math
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from wc_msgs.msg import Chair

# Constants & Globals here.
CHAIR_STR_LEN = 6 

#TODO- make part of class
pubJoy = rospy.Publisher('chairJoy', Joy, queue_size=10)

# JKM - for debug
JKM = True


def convert_to_joy(chair):
    ''' Convert a string message from the /chair topic
        to a /chairJoy topic.
    '''
    if (len(chair) == CHAIR_STR_LEN):
       return
    return
    
    
    
     
def callback(msg):
    chair = msg.data.data
    rospy.loginfo("Received chair message: {}".format (msg.data.data))

    # Convert to chairJoy message & publish
    rospy.loginfo("chair message len is: {}".format (len(msg.data.data)))
    if (len(msg.data.data) == CHAIR_STR_LEN):
        X, Y = 0.0, 0.0
        msgJoy = Joy()
        msgJoy.header.stamp = msg.header.stamp #rospy.Time.now()
        # 
        fb, fb_amt, lr, lr_amt = chair[0], chair[1:3], chair[3], chair[4:6]
        if ("B" == fb):
            Y = -float(fb_amt))
        elif ("F" == fb):
            Y = float(fb_amt)
        else:
           rospy.logerr("Invalid chairJoy data string: {} yields fb as {}".format(chair,fb))
           return              
        msgJoy.axes = [ float(20), float(0) ]       
        pubJoy.publish(msgJoy)
        rospy.loginfo("chairJoy message published: {}".format (msgJoy))

    return


# Define the node.Is both publisher and subscriber
# TODO: Convert to class that loads parms, and creates ros log messages on start up

def node():
    rospy.init_node('chairJoy')
    print('\n ROS node chairJoy started ')
    rospy.Subscriber("chair", Chair, callback)
    rospy.spin()

if __name__ == '__main__':
    node()

