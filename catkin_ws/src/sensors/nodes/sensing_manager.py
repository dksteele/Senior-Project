#!/usr/bin/env python

import rospy
import rospkg
from sensors import *

import datetime
import signal
import sys
import threading
import time

from python_qt_binding import loadUi
from python_qt_binding.QtCore import QThread
from python_qt_binding.QtWidgets import QWidget, QApplication, QTreeWidget, QTreeWidgetItem

__main_widget__ = None
__registered_nodes__ = dict()
__current_sensor_widget__ = None
__subscriber_thread__ = None

class rospyAsyncSpin(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		rospy.spin()
        
def output_debug_message(msg):
	print datetime.datetime.now(), msg
	
def replace_widget_for_sensor():
	global __main_widget__
	global __current_sensor_widget__
	global __subscriber_thread__
	
	widget = __subscriber_thread__.get_widget_for_sensor()
	
	__main_widget__.layout.replaceWidget(__current_sensor_widget__, widget)
	
	__current_sensor_widget__.deleteLater()
	__current_sensor_widget__ = widget
	
	
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
	
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	
	spin_thread = rospyAsyncSpin()
	spin_thread.daemon = True
	spin_thread.start()

	__current_sensor_widget__ = __main_widget__.emptyContainer
	__subscriber_thread__ = SensingSubscriber(__registered_nodes__, __main_widget__, __current_sensor_widget__)
	__subscriber_thread__.daemon = True
	__subscriber_thread__.start()
	
	__subscriber_thread__.__replace_widget__.connect(replace_widget_for_sensor)
	
	register_thread = SensingRegister(__registered_nodes__, __main_widget__)
	register_thread.daemon = True
	register_thread.start()
	
	time.sleep(.1)
	
	output_debug_message("[INFO] : Starting GUI")
	__main_widget__.show()	
	output_debug_message("[INFO] : GUI Started ... Executing Application")
	
	__application__.exec_()

	
	
if __name__ == "__main__":
	main()
