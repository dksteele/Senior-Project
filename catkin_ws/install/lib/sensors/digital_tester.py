#!/usr/bin/env python

import rospyNRHP
from sensors.srv import *
from std_msgs.msg import Float64

import datetime
import random
import time

__platform_name__ = ""
__regisered_topic__ = ""

def output_debug_message(msg):
	print datetime.datetime.now(), msg
 
def send_image_stream():
	global __regisered_topic__
	global __camera__
	
	output_debug_message("[INFO] : Creating publisher on topic - " + __regisered_topic__)
	pub = rospy.Publisher(__regisered_topic__, Float64, queue_size=1)
	
	while not rospy.is_shutdown():
		Float64 number(random.randint(0, 100))
		pub.publish(number)
		
		time.sleep(1)
	
def register():
	global __platform_name__
	global __regisered_topic__
	
	proxy = rospy.ServiceProxy('sensors_register', RegistrationService)
	
	output_debug_message("[INFO] : Waiting for registration")
	
	rospy.wait_for_service('sensors_register')
	ret = proxy(__platform_name__, RegistrationServiceRequest.DIGITAL);
	__regisered_topic__ = ret.topic
			
	output_debug_message("[INFO] : Registered for topic - " + ret.topic)

def main():
	global __platform_name__
	global __camera__
	
	rospy.init_node('digital_tester')	
	
	__camera__ = PiCamera()
	
	__platform_name__ = rospy.get_param("node/platform_name", "DigitalTesterStation")
	register()
	
	time.sleep(1)
	
	send_random_digital_stream()
	
if __name__ == "__main__":
	main()

