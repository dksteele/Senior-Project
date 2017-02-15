#!/usr/bin/env python

import rospy
from sensors.srv import *

import datetime

def output_debug_message(msg):
	print datetime.datetime.now(), msg

def send_image_stream():
	print "HI"
	
def register():
	proxy = rospy.ServiceProxy('sensors_register', RegistrationService)
	
	registered = False
	while(not registered):
		try:
			ret = proxy("TestPlatform", RegistrationServiceRequest.CAMERA);
			registered = True
		except rospy.service.ServiceException:
			pass
			
	print ret.topic

def main():
	rospy.init_node('py_camera')
	register()
	
	platform_name = rospy.get_param("node/platform_name", "CameraStation")
	
	
if __name__ == "__main__":
	main()
