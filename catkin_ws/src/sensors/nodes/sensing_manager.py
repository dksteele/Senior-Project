#!/usr/bin/env python

import rospkg
import rospy
from sensors.srv import *
from sensors import *

import datetime
import threading

__registered_nodes__ = dict()
__register_service__ = None
__sensing_thread__ = None
__sensing_thread_update_tree_event__ = threading.Event()

def output_debug_message(msg):
	print datetime.datetime.now(), msg
		
def register_callback(req):
	global __registered_nodes__
	global __sensing_thread_update_tree_event__
	
	num_nodes = len(__registered_nodes__.keys())
	
	topic = "sensor_node" + str(num_nodes)
	__registered_nodes__[num_nodes] = (req.platform_name, req.sensor_type, topic)
	output_debug_message("[INFO] : Registered " + req.platform_name + "->" + req.sensor_type + " On Topic " + topic)
	
	__sensing_thread_update_tree_event__.set()
	
	return RegistrationServiceResponse(topic)

def main():
	global __register_service__
	global __sensing_thread__
	global __registered_nodes__
	global __sensing_thread_update_tree_event__
	
	rospy.init_node('sensing_manager')
	
	output_debug_message("[INFO] : Starting Registration Service")
	__register_service__ = rospy.Service('sensors_register', RegistrationService, register_callback)
	
	output_debug_message("[INFO] : Starting Sensing Thread")
	__sensing_thread__ = SensingGUIThread("SensingThread", __registered_nodes__, __sensing_thread_update_tree_event__)
	__sensing_thread__.daemon = True
	__sensing_thread__.start()
	
	rospy.spin()
	
	
if __name__ == "__main__":
	main()
