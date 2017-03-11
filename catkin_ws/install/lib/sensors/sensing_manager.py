#!/usr/bin/env python

import rospy
import rospkg
from sensors import *
from sensors.srv import *

import datetime
import signal
import sys
import threading
import time

from python_qt_binding import loadUi
from python_qt_binding.QtCore import QThread,  QRectF
from python_qt_binding.QtGui import QPixmap
from python_qt_binding.QtWidgets import QWidget, QApplication, QTreeWidget, QTreeWidgetItem, QLCDNumber, QGraphicsView, QGraphicsScene

__main_widget__ = None
__registered_nodes__ = dict()
__current_sensor_widget__ = None
__subscriber_thread__ = None
__tree_nodes__ = dict()

#Simple threaded class for running the rospy spin function in a seperate thread
class rospyAsyncSpin(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		rospy.spin()
        
def output_debug_message(msg):
	print datetime.datetime.now(), msg

#When the sensing subscriber notices that the selection in the tree has changed and that a new widget is required replace the old widget
def replace_widget_for_sensor():
	global __main_widget__
	global __current_sensor_widget__
	global __subscriber_thread__
	global __registered_nodes__
	
	selected_node = __subscriber_thread__.get_selected_node()
	
	widget = QWidget()
	if __registered_nodes__[selected_node][1] == RegistrationServiceRequest.CAMERA :
		widget = QGraphicsView()
		widget.setScene(QGraphicsScene())
		pixmap = QPixmap()
		pixmap.load(rospkg.RosPack().get_path("sensors") + "/resource/no_data.jpeg", "JPEG")
		widget.scene().addPixmap(pixmap)
		widget.scene().setSceneRect(QRectF(pixmap.rect()))
	elif __registered_nodes__[selected_node][1] == RegistrationServiceRequest.ANALOG or __registered_nodes__[selected_node][1] == RegistrationServiceRequest.DIGITAL:
		widget = QLCDNumber()
		widget.setNumDigits(8)
		widget.display(0)
	print "[INFO] : Seting Up Display For -> " + __registered_nodes__[selected_node][1]
	
	__main_widget__.layout.replaceWidget(__current_sensor_widget__, widget)
	
	__current_sensor_widget__.deleteLater()
	__current_sensor_widget__ = widget

#On signal update the data contained in the current sensor widget
def update_widget_for_sensor(data):
	global __registered_nodes__
	global __current_sensor_widget__
	
	selected_node = __subscriber_thread__.get_selected_node()
	
	if selected_node == None:
		return
	elif __registered_nodes__[selected_node][1] == RegistrationServiceRequest.CAMERA :
		pixmap = QPixmap()
		print pixmap.loadFromData(data.data, data.format.upper())
		__current_sensor_widget__.scene().clear()
		__current_sensor_widget__.scene().addPixmap(pixmap)
		__current_sensor_widget__.scene().setSceneRect(QRectF(pixmap.rect()))	
	elif __registered_nodes__[selected_node][1] == RegistrationServiceRequest.ANALOG or __registered_nodes__[selected_node][1] == RegistrationServiceRequest.DIGITAL:
		if len(str(data.data)) > 8:
			__current_sensor_widget__.setNumDigits(len(str(data.data)))
		else:
			__current_sensor_widget__.setNumDigits(8)
		__current_sensor_widget__.display(data.data)	
		
#Add __registered_node__[node] to the tree
def add_node_to_tree(node):
	global __main_widget__
	global __registered_nodes__
	global __tree_nodes__
	
	#Create Top Level Item If Needed
	if not (__registered_nodes__[node][0], None) in __tree_nodes__.keys():
		root = QTreeWidgetItem([__registered_nodes__[node][0]])
		root.setFlags(root.flags() & ~Qt.ItemIsSelectable)
		__tree_nodes__[(__registered_nodes__[node][0], None)] = root
		__main_widget__.sensorTree.insertTopLevelItem(0, root)
	
	#Create Item For Sensor Type If Needed
	if not (__registered_nodes__[node][0], __registered_nodes__[node][1]) in __tree_nodes__.keys():
		parent = QTreeWidgetItem(__tree_nodes__[(__registered_nodes__[node][0], None)], [__registered_nodes__[node][1]])
		parent.setFlags(parent.flags() & ~Qt.ItemIsSelectable)
		__tree_nodes__[(__registered_nodes__[node][0], __registered_nodes__[node][1])] = parent
		
	parent = __tree_nodes__[(__registered_nodes__[node][0], __registered_nodes__[node][1])]
	
	#Create Node
	item = QTreeWidgetItem(parent, [str(node)])
	item.setFlags(item.flags() | Qt.ItemIsSelectable)
	item.setData(0, Qt.UserRole, node)

def main():
	global __application__
	global __main_widget__
	global __current_sensor_widget__
	global __subscriber_thread__
	
	rospy.init_node('sensing_manager',  disable_signals=True)
	
	output_debug_message("[INFO] : Starting Threads")
	
	#Setup GUI
	__application__ = QApplication(sys.argv)
	__main_widget__ = QWidget()
	loadUi(rospkg.RosPack().get_path("sensors") + "/resource/sensing_window.ui", __main_widget__)
	
	#Pass Ctl-C through to close the QT application
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	
	#Start up an asyncronous spiner for the ros node
	spin_thread = rospyAsyncSpin()
	spin_thread.daemon = True
	spin_thread.start()

	#Start worker threads and connect any signals that they need to send to the application main thread
	__current_sensor_widget__ = __main_widget__.emptyContainer
	__subscriber_thread__ = SensingSubscriber(__registered_nodes__, __main_widget__)
	__subscriber_thread__.daemon = True
	__subscriber_thread__.start()
	
	__subscriber_thread__.__replace_widget__.connect(replace_widget_for_sensor)
	__subscriber_thread__.__update_widget__.connect(update_widget_for_sensor)
	
	register_thread = SensingRegister(__registered_nodes__)
	register_thread.daemon = True
	register_thread.start()
	
	register_thread.__add_tree_node__.connect(add_node_to_tree)
	
	time.sleep(.1)
	
	#Start the gui
	output_debug_message("[INFO] : Starting GUI")
	__main_widget__.show()	
	output_debug_message("[INFO] : GUI Started ... Executing Application")
	
	__application__.exec_()
	
	
if __name__ == "__main__":
	main()
