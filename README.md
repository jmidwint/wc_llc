# Wheelchair Low Level Control Sofware 

This repository contains the ROS package software used to send commands & receive responses to/from the Wheelchair serial Arduino interface of the Eightfold SMART Chair.

This package relies on the ROS package video_stream_opencv. 

It listens for drive commands from the /drive topic and publishes responses from the wheelchair control to the /chair topic. 

# Running the Code

This is used to launch the ROS nodes and i/f sofware to send control data to the Eightfold 
  SMART Chair Interface. 


After connecting a USB web camera to one of the USB ports on the device where this sofwtare is running, 
start the ROS package. It is assumed that ROS CORE is already running.  

Use the following ROS launch command:

roslaunch chair_pi3 chair.experiment.launch video_stream_provider:=0 buffer_queue_size:=1 set_camera_fps:=30 fps:=30

This will set the the buffer queue size to 1 for webcam being managed by the video_stream_opencv, which means that the frames from the camera are dumped and only the latest frame is used & published to the camera topic. 
