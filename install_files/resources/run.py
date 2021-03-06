#!/usr/bin/env python

import argparse
import os
import shutil
import signal
import subprocess
import sys
import time

__args__ = None
__proc_list__ = []
__source__command__ = ""

def end_program(signal, frame):
	global __proc_list__
	
	for proc in __proc_list__:
		proc.terminate()
		
	sys.exit(0)

#	Sets up the default ROS parameters
def setup_params():
	global __args__
	
	param_file = open(__args__.params_file, 'r')
	for param_pair in param_file:
		os.system(". /opt/ros/kinetic/setup.sh\nrosparam set " + param_pair.split(":")[0] + " " + param_pair.split(":")[1] + "\n")
	param_file.close()
	
	os.system(". /opt/ros/kinetic/setup.sh\nrosparam dump " + __args__.logging_dir + "/rosparams.log")
	
#	Starts the ROS Core
def start_core():
	global __args__
	global __source__command__
	global __proc_list__
	
	print "[INFO] : Starting Core"
	__proc_list__.append(subprocess.Popen(__source__command__ + "roscore", stdout=open(__args__.logging_dir + "/roscore.log", 'w'), shell=True))

# Start components as defined in the configuration
def run_components():
	global __args__
	global __source__command__
	global __proc_list__
	
	if(__args__.arduino_control):
		__proc_list__.append(subprocess.Popen(__source__command__ +  __args__.install_dir + "/env.sh rosrun arduino_control arduino_control", stdout=open(__args__.logging_dir + "/arduino_control.log", 'w'), stderr=subprocess.STDOUT, shell=True))
		__proc_list__.append(subprocess.Popen(__source__command__ +  __args__.install_dir + "/env.sh rosrun joy joy_node", stdout=open(__args__.logging_dir + "/joy.log", 'w'), shell=True))
		__proc_list__.append(subprocess.Popen(__source__command__ +  __args__.install_dir + "/env.sh rosrun bridge multicast_topic_bridge", stdout=open(__args__.logging_dir + "/multicast_bridge.log", 'w'), stderr=subprocess.STDOUT, shell=True))
	if(__args__.sensing_manager):
		__proc_list__.append(subprocess.Popen(__source__command__ +  __args__.install_dir + "/env.sh rosrun sensors sensing_manager.py", stdout=open(__args__.logging_dir + "/sensing_manager.log", 'w'), stderr=subprocess.STDOUT, shell=True))
	if(__args__.pi_camera):
		__proc_list__.append(subprocess.Popen(__source__command__ +  __args__.install_dir + "/env.sh rosrun sensors pi_camera.py", stdout=open(__args__.logging_dir + "/pi_camera.log", 'w'), stderr=subprocess.STDOUT, shell=True))
	
def main():
	global __args__
	global __source__command__
	
	signal.signal(signal.SIGINT, end_program)

	parser = argparse.ArgumentParser(description='Senior Project Core')
	parser.add_argument('--core', dest='core', action="store_true", default=False,
			help='Use this flag to run the core')
	parser.add_argument('--arduino_control', dest='arduino_control', action="store_true", default=False,
			help='Use this flag to run the arduino control')
	parser.add_argument('--pi_camera', dest='pi_camera', action="store_true", default=False,
			help='Use this flag to run the pi camera')
	parser.add_argument('--sensing_manager', dest='sensing_manager', action="store_true", default=False,
			help='Use this flag to run the sensing manager')
	parser.add_argument('--rosparams', nargs="?", dest="params_file", action="store", default=None,
			help="Use this to designate ros parameters")
	parser.add_argument('--logging_dir', nargs="?", dest="logging_dir", action="store", default="/var/log/custom_ros",
			help="Use this to specify the directory where the logging should be done")
	parser.add_argument('--install_dir', nargs="?", dest="install_dir", action="store", default="/opt/custom_ros/install",
			help="Use this to specify the directory where the install folder for any custom ros nodes is located")
	
	__args__ = parser.parse_args()
	
	__source__command__ = ". /opt/ros/kinetic/setup.sh\n"
	
	if(__args__.core):
		start_core()
		# Wait for rosmaster to start
		while (not os.system("top -b -n1 | grep rosmaster") == 0):
			continue
	if(__args__.params_file):
		setup_params()
		
	run_components()
	
	#	Allow programs to run
	while(True):
		time.sleep(120)
		continue

if __name__ == "__main__":
	main()
