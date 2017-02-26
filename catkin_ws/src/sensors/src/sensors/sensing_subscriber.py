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

from python_qt_binding import loadUi, QtCore
from python_qt_binding.QtCore import QVariant, Qt, QThread, QRectF
from python_qt_binding.QtGui import QPixmap
from python_qt_binding.QtWidgets import QWidget, QTreeWidget, QTreeWidgetItem, QLCDNumber, QGraphicsView, QGraphicsScene

def output_debug_message(msg):
	print datetime.datetime.now(), msg
		

class SensingSubscriber(QThread):
	
	__selected_node__ = None
	__registered_nodes__ = dict()
	__sensing_subscriber__ = None
	__sensor_type_map__ = {RegistrationServiceRequest.CAMERA : Float64,
					   RegistrationServiceRequest.ANALOG : Float64,
					   RegistrationServiceRequest.DIGITAL : Float64}
	__widget__ = None
	__selection_changed__ = False
	
	__replace_widget__ = QtCore.pyqtSignal()
	__update_widget__ = QtCore.pyqtSignal(object)
					   
	def __init__(self, registered_nodes, widget):
		QThread.__init__(self)
		self.__registered_nodes__ = registered_nodes
		self.__widget__ = widget
		
	def reset_sensor_display(self):
		self.__replace_widget__.emit()

	def sensing_callback(self, data):
		self.__update_widget__.emit(data)
	
	def get_selected_node(self):
		return self.__selected_node__
	
	def get_widget_for_sensor(self):
		widget = QWidget()
		if self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.CAMERA :
			widget = QGraphicsView()
			widget.setScene(QGraphicsScene())
			pixmap = QPixmap()
			print pixmap.load(rospkg.RosPack().get_path("sensors") + "/resource/no_data.jpeg", "JPEG")
			widget.scene().addPixmap(pixmap)
			widget.scene().setSceneRect(QRectF(pixmap.rect()))	
			print "[INFO] : Seting Up Display For -> CAMERA"
		elif self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.ANALOG or self.__registered_nodes__[self.__selected_node__][1] == RegistrationServiceRequest.DIGITAL:
			widget = QLCDNumber()
			widget.setNumDigits(8)
			widget.display(0)
			print "[INFO] : Seting Up Display For -> " + self.__registered_nodes__[self.__selected_node__][1]
		return widget
		
	def run(self):
		
		while True:
			selections = self.__widget__.sensorTree.selectedItems()
			new_selection = None
			
			if selections:
				if not selections[0].data(0, Qt.UserRole) == self.__selected_node__:
					self.__selected_node__ = selections[0].data(0, Qt.UserRole)
					if not self.__sensing_subscriber__ == None:
						self.__sensing_subscriber__.unregister()
					self.__sensing_subscriber__ = rospy.Subscriber(self.__registered_nodes__[self.__selected_node__][2], self.__sensor_type_map__[self.__registered_nodes__[self.__selected_node__][1]], self.sensing_callback)
					
					self.reset_sensor_display()
			else: 
				self.__sensing_subscriber__ = None
				
			time.sleep(.1)
