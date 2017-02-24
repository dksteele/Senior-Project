#!/usr/bin/env python

import rospy
from sensors.srv import *

import datetime
import threading


from python_qt_binding.QtCore import QVariant, Qt
from python_qt_binding.QtWidgets import QWidget, QApplication, QTreeWidget, QTreeWidgetItem

def output_debug_message(msg):
	print datetime.datetime.now(), msg

class SensingRegister(threading.Thread):
	__registered_nodes__ =  None
	__register_service__ = None
	__widget__ = None
	__tree_nodes__ = dict()

	def __init__(self, registered_nodes, widget):
		threading.Thread.__init__(self)
		self.__registered_nodes__ = registered_nodes
		self.__widget__ = widget
	
	def add_node_to_tree(self, node):
		if self.__widget__ == None:
			return False
		
		#Create Top Level Item If Needed
		if not (self.__registered_nodes__[node][0], None) in self.__tree_nodes__.keys():
			root = QTreeWidgetItem([self.__registered_nodes__[node][0]])
			root.setFlags(root.flags() & ~Qt.ItemIsSelectable)
			self.__tree_nodes__[(self.__registered_nodes__[node][0], None)] = root
			self.__widget__.sensorTree.insertTopLevelItem(0, root)
		
		#Create Item For Sensor Type If Needed
		if not (self.__registered_nodes__[node][0], self.__registered_nodes__[node][1]) in self.__tree_nodes__.keys():
			parent = QTreeWidgetItem(self.__tree_nodes__[(self.__registered_nodes__[node][0], None)], [self.__registered_nodes__[node][1]])
			parent.setFlags(parent.flags() & ~Qt.ItemIsSelectable)
			self.__tree_nodes__[(self.__registered_nodes__[node][0], self.__registered_nodes__[node][1])] = parent
			
		parent = self.__tree_nodes__[(self.__registered_nodes__[node][0], self.__registered_nodes__[node][1])]
		
		#Create Node
		item = QTreeWidgetItem(parent, [str(node)])
		item.setFlags(item.flags() | Qt.ItemIsSelectable)
		item.setData(0, Qt.UserRole, QVariant(node))
			
		return True
	
	def register_callback(self, req):
		global __registered_nodes__
		global __sensing_thread_update_tree_event__
		
		num_nodes = len(self.__registered_nodes__.keys())
		
		topic = "sensor_node" + str(num_nodes)
		self.__registered_nodes__[num_nodes] = (req.platform_name, req.sensor_type, topic)
		output_debug_message("[INFO] : Registered " + req.platform_name + "->" + req.sensor_type + " On Topic " + topic)
		
		self.add_node_to_tree(num_nodes)
		
		return RegistrationServiceResponse(topic)

	def run(self):
		
		output_debug_message("[INFO] : Starting Registration Service")
		__register_service__ = rospy.Service('sensors_register', RegistrationService, self.register_callback)
		
		output_debug_message("[INFO] : Starting Sensing Thread")

