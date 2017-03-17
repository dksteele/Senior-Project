#!/usr/bin/env python

import rospy
from sensors.srv import *
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Header

import datetime
import time

from io import BytesIO

from picamera import PiCamera

__platform_name__ = ""
__regisered_topic__ = ""
__camera__ = None

def output_debug_message(msg):
	print datetime.datetime.now(), msg

def send_image_stream():
	global __regisered_topic__
	global __camera__
	
	output_debug_message("[INFO] : Creating publisher on topic - " + __regisered_topic__)
	pub = rospy.Publisher(__regisered_topic__, CompressedImage, queue_size=1)
	
	img_num = 0
	
	while not rospy.is_shutdown():
		
		data = BytesIO()
		__camera__.capture(data, 'jpeg', True)
		data.truncate()
			
		img_num = img_num + 1
		
		msg = CompressedImage()
		msg.header.seq = img_num
        msg.header.stamp = rospy.Time.now()
		msg.format = "jpeg"
		msg.data = data.getvalue()
			
		pub.publish(msg)
	
def register():
	global __platform_name__
	global __regisered_topic__
	
	proxy = rospy.ServiceProxy('sensors_register', RegistrationService)
	
	output_debug_message("[INFO] : Waiting for registration")
	
	rospy.wait_for_service('sensors_register')
	ret = proxy(__platform_name__, RegistrationServiceRequest.CAMERA);
	__regisered_topic__ = ret.topic
			
	output_debug_message("[INFO] : Registered for topic - " + ret.topic)

def main():
	global __platform_name__
	global __camera__
	
	rospy.init_node('pi_camera')	
	
	__camera__ = PiCamera()
	__camera__.vflip = True
	
	__platform_name__ = rospy.get_param("node/platform_name", "CameraStation")
	register()
	
	time.sleep(1)
	
	send_image_stream()
	
if __name__ == "__main__":
	main()
