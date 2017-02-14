#!/usr/bin/env python

import rospy
import rospkg
from sensors.srv import *

import sys
import threading
import datetime


__registered_nodes__ = dict()
__register_service__ = None
__sensing_subscriber__ = None
__sensing_thread__ = None

def output_debug_message(msg):
	print datetime.datetime.now(), msg

def recieve_sensing_information(data):
		
def sensing_thread():
	s = rospy.Subscriber("tmp", String, recieve_sensing_information)
	
def register_callback(req):
	global __registered_nodes__
	
	num_nodes = len(__registered_nodes__.keys())
	
	topic = "sensor_node" + str(num_nodes)
	__registered_nodes__[(req.platform_name, req.sensor_type, num_nodes)] = topic
	output_debug_message("[INFO] : Registered " + req.platform_name + "->" + req.sensor_type + " On Topic " + topic)
	
	return RegistrationServiceResponse(topic)

def main():
	global __register_service__
	global __sensing_thread__
	
	rospy.init_node('sensing_manager')
	
	output_debug_message("[INFO] : Starting Registration Service")
	__register_service__ = rospy.Service('sensors_register', RegistrationService, register_callback)
	
	output_debug_message("[INFO] : Starting Sensing Thread")
	__sensing_thread__ = threading.Thread(target=sensing_thread)
	__sensing_thread__.daemon = True
	__sensing_thread__.start()
	
	rospy.spin()
	
	
if __name__ == "__main__":
	main()
