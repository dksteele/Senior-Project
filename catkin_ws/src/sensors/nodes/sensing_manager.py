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
from python_qt_binding.QtWidgets import QWidget, QApplication, QTreeWidget, QTreeWidgetItem

__registered_nodes__ = dict()

class rospyAsyncSpin(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		rospy.spin()
        
def output_debug_message(msg):
	print datetime.datetime.now(), msg
	
def main():
	global __application__
	rospy.init_node('sensing_manager',  disable_signals=True)
	
	output_debug_message("[INFO] : Starting Threads")
	
	#Setup GUI
	__application__ = QApplication(sys.argv)
	main_widget = QWidget()
	loadUi(rospkg.RosPack().get_path("sensors") + "/resource/sensing_window.ui", main_widget)
	
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	
	spin_thread = rospyAsyncSpin()
	spin_thread.daemon = True
	spin_thread.start()
	
	subscriber_thread = SensingSubscriber(__registered_nodes__, main_widget)
	subscriber_thread.daemon = True
	subscriber_thread.start()
	
	register_thread = SensingRegister(__registered_nodes__, main_widget)
	register_thread.daemon = True
	register_thread.start()
	
	time.sleep(.1)
	
	output_debug_message("[INFO] : Starting GUI")
	main_widget.show()	
	output_debug_message("[INFO] : GUI Started ... Executing Application")
	
	__application__.exec_()

	
	
if __name__ == "__main__":
	main()
