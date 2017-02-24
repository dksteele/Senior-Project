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
from python_qt_binding.QtCore import QVariant, Qt, QThread
from python_qt_binding.QtWidgets import QWidget, QApplication, QTreeWidget, QTreeWidgetItem

def output_debug_message(msg):
	print datetime.datetime.now(), msg

class SensingGUIThread(QThread):
	
	selected_node = None
	registered_nodes = dict()
	sensing_subscriber = None
	sensor_type_map = {RegistrationServiceRequest.CAMERA : CompressedImage,
					   RegistrationServiceRequest.ANALOG : Float64,
					   RegistrationServiceRequest.DIGITAL : Float64}
	gui_update_event = threading.Event()
	pkg_name = ""
	application = None
	main_widget = None
	selection_changed = False
					   
	def __init__(self, name, registered_nodes, gui_update_event, pkg_name):
		QThread.__init__(self)
		self.name = name
		self.registered_nodes = registered_nodes
		self.gui_update_event = gui_update_event
		self.pkg_name = pkg_name
		
	def reset_sensor_display(self):
		if self.selected_node == None:
			return
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.CAMERA :
			print "[INFO] : Seting Up Display For -> CAMERA"
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.ANALOG :
			print "[INFO] : Seting Up Display For -> ANALOG"
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.DIGITAL :
			print "[INFO] : Seting Up Display For -> DIGITAL"
			
	def load_gui_node_selection(self):
		selections = self.main_widget.sensorTree.selectedItems()
		if not selections:
			self.selected_node = None
			
		self.selection_changed = True
		self.selected_node = selections[0].data(0, Qt.UserRole).toInt()

	def sensing_callback(self, data):
		if self.selected_node == None:
			return
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.CAMERA :
			pass
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.ANALOG :
			pass
		elif self.registered_nodes[self.selected_node][1] == RegistrationServiceRequest.DIGITAL :
			pass

	def update_gui_tree(self):
		if self.application == None or self.main_widget == None:
			return False
		
		self.main_widget.sensorTree.clear()
		treeNodes = dict()
		
		for node in self.registered_nodes.keys():
			parent = treeRoot
			#Create Top Level Item If Needed
			if not (self.registerd_nodes[node][1], None) in treeNodes.keys():
				root = QTreeWidgetItem([self.registerd_nodes[node][1]])
				root.setFlags(item.flags() & ~Qt.ItemIsSelectable)
				treeNodes[(self.registerd_nodes[node][1], None)] = root
				self.main_widget.sensorTree.insertTopLevelItem(0, item)
			
			#Create Item For Sensor Type If Needed
			if not (self.registerd_nodes[node][1], self.registered_nodes[node][2]) in treeNodes.keys():
				parent = QTreeWidgetItem(treeNode[(self.registerd_nodes[node][1], None)], [self.registered_nodes[node][2]])
				parent.setFlags(item.flags() & ~Qt.ItemIsSelectable)
				treeNodes[(self.registered_nodes[node][1], self.registered_nodes[node][2])] = parent
				
			parent = treeNodes[(self.registered_nodes[node][1], self.registered_nodes[node][2])]
			
			#Create Node
			item = QTreeWidgetItem(parent, [str(node)])
			item.setFlags(item.flags() & Qt.ItemIsSelectable)
			item.setData(0, Qt.UserRole, QVariant(node))
			
		return True
		
	def run(self):
		
		output_debug_message("[INFO] : Starting GUI")
		
		#Setup GUI
		self.application = QApplication([])
		self.main_widget = QWidget()
		loadUi(rospkg.RosPack().get_path(self.pkg_name) + "/resource/sensing_window.ui", self.main_widget)
		
		self.main_widget.sensorTree.itemSelectionChanged.connect(self.load_gui_node_selection)
		
		self.main_widget.show()
		
		output_debug_message("[INFO] : GUI Started")
		
		self.application.exec_()
		
		while True:
			
			#If selection is changed then setup the subscriber and reset the display
			if self.selection_changed:
				self.selection_changed = False			
				self.sensing_subscriber = rospy.Subscriber(self.registered_nodes[self.selected_node][2], self.sensor_type_map[self.registered_nodes[self.selected_node][1]], self.sensing_callback)
				self.reset_sensor_display()
			
			#If the tree needs to be updated do so
			if self.gui_update_event.isSet():
				self.update_gui_tree()
				self.gui_update_event.clear()
			
			time.sleep(.1)
