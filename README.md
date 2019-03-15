# Wheelchair Low Level Control (LLC) Platform Sofware 

This repository contains the ROS package software used to interact with the hardware devices that are directly connected to the hardware platform that supports the autonomous wheelchair.

The platorm device support includes the Serial Arduino Interface for controlling & interacting with the Eightfold SMART Chair, the camera(s) used, mass storage device used in Data Collection

This package relies on the ROS package video_stream_opencv. 

It listens for drive commands from the /drive topic and publishes responses from the wheelchair control/data to the /chair topic. 

# Running the Code

This is used to launch the ROS nodes and i/f sofware to send control data to the Eightfold 
  SMART Chair Interface. 


After connecting a USB web camera to one of the USB ports on the device where this software is running, 
start the ROS package.  

Use the following ROS launch command:

roslaunch wc_llc chair.experiment.launch video_stream_provider:=0 buffer_queue_size:=1 set_camera_fps:=30 fps:=30



This will set the the buffer queue size to 1 for webcam being managed by the video_stream_opencv, which means that the frames from the camera are dumped and only the latest frame is used & published to the camera topic. 


# Sending a text command directly to the chair (arduino).

  rosrun wc_llc chairCmd.py <text-to-send>
