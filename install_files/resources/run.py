#!/usr/bin/env python

import argparse
import signal
import shutil
import os
import sys
import subprocess

__args__ = None
__proc_list__ = []
__source__command__ = ""

def end_program(signal, frame):
	global __proc_list__
	print "STOPING PROCESSES"
	for proc in __proc_list__:
		proc.terminate()
		
	sys.exit(0)
	
def setup_params():
	global __args__
	param_file = open(__args__.params_file, 'r')
	for param_pair in param_file:
		os.system(". /opt/ros/kinetic/setup.sh\nrosparam set " + param_pair.split(":")[0] + " " + param_pair.split(":")[1] + "\n")
	param_file.close()
	os.system(". /opt/ros/kinetic/setup.sh\nrosparam dump " + __args__.logging_dir + "/rosparams.log")
	
def start_core():
	global __args__
	global __source__command__
	global __proc_list__
	
	__proc_list__.append(subprocess.Popen(__source__command__ + "roscore & > " + __args__.logging_dir + "/roscore.log &", shell=True))
	
def run_components():
	global __args__
	global __source__command__
	global __proc_list__
	
	if(__args__.arduino_control):
		__proc_list__.append(subprocess.Popen(__source__command__ + "rosrun arduino_control arduino_control > " + __args__.logging_dir + "/arduino_control.log &", shell=True))
		__proc_list__.append(subprocess.Popen(__source__command__ + "rosrun joy joy_node & > " + __args__.logging_dir + "/joy.log &", shell=True))
		__proc_list__.append(subprocess.Popen(__source__command__ + "rosrun bridge multicast_topic_bridge > " + __args__.logging_dir + "/multicast_bridge.log &", shell=True))
	if(__args__.sensing_manager):
		__proc_list__.append(subprocess.Popen(__source__command__ + "rosrun sensors sensing_manager.py > " + __args__.logging_dir + "/sensing_manager.log &", shell=True))
	if(__args__.pi_camera):
		__proc_list__.append(subprocess.Popen(__source__command__ + "rosrun sensors pi_camera.py & > " + __args__.logging_dir + "/pi_camera.log &", shell=True))
	print __source__command__ + "rosrun sensors pi_camera.py > " + __args__.logging_dir + "/pi_camera.log &"
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
	parser.add_argument('--install_dir', nargs="?", dest="install_dir", action="store", default="/usr/share/custom_ros/install",
			help="Use this to specify the directory where the install folder for any custom ros nodes is located")
	
	__args__ = parser.parse_args()
	
	__source__command__ = ". /opt/ros/kinetic/setup.sh\n. " + __args__.install_dir + "/setup.sh\n"
	
	if(__args__.core):
		start_core()
		while (not subprocess.check_output("top -b -n1 | grep rosmaster", shell=True)):
			continue
	if(__args__.params_file):
		setup_params()
		
	run_components()
	
	while(True):
		continue

if __name__ == "__main__":
	main()
