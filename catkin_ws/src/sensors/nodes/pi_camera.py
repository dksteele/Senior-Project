#!/usr/bin/env python

import rospy
from sensors.srv import *
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Header

import cv2
import datetime
import numpy
import os
import time

from io import BytesIO

from picamera import PiCamera

__platform_name__ = ""
__regisered_topic__ = ""
__camera__ = None
__classifier__ = None
__classify_gray__ = False

def output_debug_message(msg):
	print datetime.datetime.now(), msg

def send_image_stream():
	global __regisered_topic__
	global __camera__
	global __classifier__
	global __classify_gray__
	
	output_debug_message("[INFO] : Creating publisher on topic - " + __regisered_topic__)
	pub = rospy.Publisher(__regisered_topic__, CompressedImage, tcp_nodelay=True)
	
	
	img_num = 0
	
	while not rospy.is_shutdown():
		if(pub.get_num_connections() > 0):
			data = BytesIO()
			__camera__.capture(data, 'jpeg', True)
			
			msg = CompressedImage()
			msg.header.seq = img_num
			msg.header.stamp = rospy.Time.now()
			msg.format = "jpeg"
			
			if not  __classifier__ == None:
				img = cv2.imdecode(numpy.fromstring(data.getvalue(), dtype=numpy.uint8), 1)
				classifier = cv2.CascadeClassifier(__classifier__)
				
				classifier_img = img
				if __classify_gray__:
					classifier_img = cv2.cvtColor(img, cv2.COLOR_BGR2GAY)
				
				detects = classifier.detectMultiScale(classifier_img)
				
				for (x,y,w,h) in detects:
					cv2.rectangle(img, (x,y), (x+w, y+h), (255, 255, 0), 2)
				
				ret, jpeg_data = cv2.imencode('jpeg', img)
				print type(jpeg_data)
				msg.data = numpy.array(jpeg_data).tobytes()
			else:
				msg.data = data.getvalue()
				
			img_num = img_num + 1
				
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
	global __classifier__
	global __classify_gray__
	
	rospy.init_node('pi_camera', anonymous=True)	
	
	__camera__ = PiCamera()	
	
	__platform_name__ = os.getenv("PLATFORM_NAME", default="CameraStation")
	camera_vflip = rospy.get_param(__platform_name__ + "-pi_camera/vflip", False)
	camera_hflip = rospy.get_param(__platform_name__ + "-pi_camera/hflip", False)
	__classifier__ = rospy.get_param(__platform_name__ + "-pi_camera/clasifier", None)
	__classify_gray__ = rospy.get_param(__platform_name__ + "-pi_camera/classify_gray", False)
	
	print camera_vflip
	if camera_vflip :
		__camera__.vflip = True
	if camera_hflip :
		__camera__.hflip = True
	
	register()
	
	time.sleep(1)
	
	send_image_stream()
	
if __name__ == "__main__":
	main()
