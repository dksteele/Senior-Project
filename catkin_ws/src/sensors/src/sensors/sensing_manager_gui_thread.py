#!/usr/bin/env python

import rospy
from sensor_msgs.msg import *
from std_msgs.msg import *
from sensors.srv import *

import sys
import threading
import time

class SensingGUIThread(threading.Thread):
	
	selected_node = None
	sensing_subscriber = None
	sensor_type_map = {RegistrationServiceRequest.CAMERA : CompressedImage,
					   RegistrationServiceRequest.ANALOG : Float64,
					   RegistrationServiceRequest.DIGITAL : Float64}
	gui_update_event = threading.Event()
	pkg_name = ""
					   
	def __init__(self, name, registered_nodes, gui_update_event, pkg_name):
		threading.Thread.__init__(self)
		self.name = name
		self.registered_nodes = registered_nodes
		self.gui_update_event = gui_update_event
		self.pkg_name = pkg_name
		
	def reset_sensor_display(self):
		if self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.CAMERA :
			print "[INFO] : Seting Up Display For -> CAMERA"
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.ANALOG :
			print "[INFO] : Seting Up Display For -> ANALOG"
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.DIGITAL :
			print "[INFO] : Seting Up Display For -> DIGITAL"
			
	def get_gui_node_selection(self):
		return self.selected_node

	def sensing_callback(self, data):
		if self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.CAMERA :
			pass
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.ANALOG :
			pass
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.DIGITAL :
			pass

	def update_gui_tree(self):
		return
	
	def init_gui(self):
		return 
		
		
	def run(self):
		
		self.init_gui()
		
		while len(self.registered_nodes.keys()) == 0:
			time.sleep(.1)
		
		while True:
			if self.selected_node == None:
				self.selected_node = self.registered_nodes.keys()[0]
			elif not self.selected_node == self.get_gui_node_selection():
				self.selected_node = self.get_gui_node_selection()
			else:
				time.sleep(.1)
				continue
			
			if self.gui_update_event.isSet():
				self.update_gui_tree()
			
			self.sensing_subscriber = rospy.Subscriber(self.registered_nodes[self.selected_node][2], self.sensor_type_map[self.registered_nodes[self.selected_node][1]], self.sensing_callback)
			self.reset_sensor_display()
