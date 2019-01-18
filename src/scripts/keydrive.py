#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys, termios, tty, os, time
 
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
 
button_delay = 0.2
 
    
def talker():
    pub = rospy.Publisher('drive', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    
    while not rospy.is_shutdown():
       
        char = getch()
 
        if (char == "k"):
            print('You Pressed K Key!')
            exit(0)
        drv_str=("F01L01")
        
        if (char == "a"):
            print('You Pressed A Key!')
            drv_str=("F01L50")
     
        elif (char == "d"):
            print('You Pressed D Key!')
            drv_str=("F01R30")
     
        elif (char == "w"):
            print('You Pressed W Key!')
            drv_str=("F30L01")
     
        elif (char == "x"):
            print('You Pressed X Key!')
            drv_str=("B30L01")
     
        elif (char == "s"):
            print('You Pressed S Key!')
            drv_str=("F01L01")
            
        else:
            print("stop")
                
        time.sleep(button_delay)
        rospy.loginfo(drv_str)
        pub.publish(drv_str)
       

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
