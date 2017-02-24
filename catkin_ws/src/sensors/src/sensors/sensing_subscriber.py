#!/usr/bin/env python

import rospkg
import rospy
from sensor_msgs.msg import *
from std_msgs.msg import *
from sensors.srv import *

import sys
import threading
import datetime
import time

from python_qt_binding import loadUi
from python_qt_binding.QtCore import QVariant, Qt
from python_qt_binding.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem

def output_debug_message(msg):
	print datetime.datetime.now(), msg

class SensingSubscriber(threading.Thread):
	
	__selected_node__ = None
	__registered_nodes__ = dict()
	__sensing_subscriber__ = None
	__sensor_type_map__ = {RegistrationServiceRequest.CAMERA : CompressedImage,
					   RegistrationServiceRequest.ANALOG : Float64,
					   RegistrationServiceRequest.DIGITAL : Float64}
	__widget__ = None
	__selection_changed__ = False
					   
	def __init__(self, registered_nodes, widget):
		threading.Thread.__init__(self)
		self.__registered_nodes__ = registered_nodes
		self.__widget__ = widget
		
	def reset_sensor_display(self):
		if self.__selected_node__ == None:
			return
		elif self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.CAMERA :
			print "[INFO] : Seting Up Display For -> CAMERA"
		elif self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.ANALOG :
			print "[INFO] : Seting Up Display For -> ANALOG"
		elif self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.DIGITAL :
			print "[INFO] : Seting Up Display For -> DIGITAL"

	def sensing_callback(self, data):
		if self.__selected_node__ == None:
			return
		elif self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.CAMERA :
			pass
		elif self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.ANALOG :
			pass
		elif self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.DIGITAL :
			pass
		
	def run(self):
		
		while True:
			selections = self.__widget__.sensorTree.selectedItems()
			new_selection = None
			
			if selections:
				if not selections[0].data(0, Qt.UserRole) == self.__selected_node__:
					self.__selected_node__ = selections[0].data(0, Qt.UserRole)
					self.__sensing_subscriber__ = rospy.Subscriber(self.__registered_nodes__[self.__selected_node__][2], self.__sensor_type_map__[self.__registered_nodes__[self.__selected_node__][1]], self.sensing_callback)
					
					self.reset_sensor_display()
			else: 
				self.__sensing_subscriber__ = None
				
			time.sleep(.1)
