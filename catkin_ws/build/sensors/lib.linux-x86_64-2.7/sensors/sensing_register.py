#!/usr/bin/env python

import rospy
from sensors.srv import *

import datetime
import threading

from python_qt_binding import QtCore
from python_qt_binding.QtCore import QThread

def output_debug_message(msg):
	print datetime.datetime.now(), msg

class SensingRegister(QThread):
	__registered_nodes__ =  None
	__register_service__ = None
	__widget__ = None
	
	__add_tree_node__ = QtCore.pyqtSignal(object)

	def __init__(self, registered_nodes):
		QThread.__init__(self)
		self.__registered_nodes__ = registered_nodes
	
	def register_callback(self, req):
		global __registered_nodes__
		global __sensing_thread_update_tree_event__
		
		num_nodes = len(self.__registered_nodes__.keys())
		
		topic = "sensor_node" + str(num_nodes)
		self.__registered_nodes__[num_nodes] = (req.platform_name, req.sensor_type, topic)
		output_debug_message("[INFO] : Registered " + req.platform_name + "->" + req.sensor_type + " On Topic " + topic)
		
		self.__add_tree_node__.emit(num_nodes)
		
		return RegistrationServiceResponse(topic)

	#Setup service to register sensors on topics
	def run(self):
		output_debug_message("[INFO] : Starting Registration Service")
		__register_service__ = rospy.Service('sensors_register', RegistrationService, self.register_callback)
		
		output_debug_message("[INFO] : Starting Sensing Thread")

