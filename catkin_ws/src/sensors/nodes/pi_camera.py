#!/usr/bin/env python

import rospy
from sensors.srv import *
from sensor_msgs.msg import *

import datetime

__platform_name__ = ""
__regisered_topic__ = ""

def output_debug_message(msg):
	print datetime.datetime.now(), msg

def send_image_stream():
	global __regisered_topic__
	
	output_debug_message("[INFO] : Creating publisher on topic - " + __regisered_topic__)
	pub = rospy.Publisher(__regisered_topic__, CompressedImage, queue_size=1)
	
	while not rospy.is_shutdown():
		pass
	
def register():
	global __platform_name__
	global __regisered_topic__
	
	proxy = rospy.ServiceProxy('sensors_register', RegistrationService)
	
	output_debug_message("[INFO] : Waiting for registration")
	
	registered = False
	while not registered and not rospy.is_shutdown():
		try:
			ret = proxy(__platform_name__, RegistrationServiceRequest.CAMERA);
			__regisered_topic__ = ret.topic
			registered = True
		except rospy.service.ServiceException:
			pass
			
	output_debug_message("[INFO] : Registered for topic - " + ret.topic)

def main():
	global __platform_name__
	
	rospy.init_node('pi_camera')	
	
	__platform_name__ = rospy.get_param("node/platform_name", "CameraStation")
	register()
	
	send_image_stream()
	
if __name__ == "__main__":
	main()
