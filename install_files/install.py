#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess

__args__ = None
__PROGRAM_DIR__ = "/usr/share/custom_ros"
__LOGGING_BASE_DIR__ = "/var/log/custom_ros"
__LOGGING_ARCHIVE_DIR__ = __LOGGING_BASE_DIR__ + "/archive"
__LOGGING_ACTIVE_DIR__ = __LOGGING_BASE_DIR__ + "/active"

def has_ros_params():
	has_params = raw_input("[PROMPT] : Will there be any additional rosparam values that need to be set (y or n)? ").upper() == 'Y'
	if(not has_params):
		return False
	
	param_file = open(__PROGRAM_DIR__ + "/rosparam.config", 'w')
	
	param_pair = raw_input("[PROMPT] : Input paramameter as \"parameter : value\" (\"DONE\" when finished) -> ")
	while(not param_pair.upper() == "DONE"):
		param_file.write(param_pair)
		param_pair = raw_input("[PROMPT] : Input paramameter as \"parameter : value\" (\"DONE\" when finished) -> ")

	param_file.close()
	return True
	
def uninstall():
	global __PROGRAM_DIR__
	global __LOGGING_BASE_DIR__
	
	if(os.path.isfile("/etc/systemd/system/custom_ros.service")):
		os.system("systemctl stop custom_ros.service")
		os.system("systemctl disable custom_ros.service")
		os.remove("/etc/systemd/system/custom_ros.service")
	if(os.path.exists(__LOGGING_BASE_DIR__)):
		shutil.rmtree(__LOGGING_BASE_DIR__)
	if(os.path.exists(__PROGRAM_DIR__)):
		shutil.rmtree(__PROGRAM_DIR__)

def create_setup_file():
	global __PROGRAM_DIR__
	global __LOGGING_ACTIVE_DIR__
	global __LOGGING_ARCHIVE_DIR__
	
	
	interface = raw_input("[PROMPT] : What networking interface is being used on this device? ")
	
	core_ip = raw_input("[PROMPT] : What is the ip address of the core (default:192.168.0.1)? ")
	if(not core_ip):
		core_ip = "192.168.0.1"
	
	core = raw_input("[PROMPT] : Will this instillation be running the roscore (y or n)? ").upper() == 'Y'		
	arduino_control = raw_input("[PROMPT] : Will this instillation be responsable for issuing joystick commands to arduino devices (y or n)? ").upper() == 'Y'
	sensor_manage = raw_input("[PROMPT] : Will this instillation be running the sensor management node (y or n)? ").upper() == 'Y'
	pi_camera = raw_input("[PROMPT] : Will this instillation be utilizing a Raspberry Pi Camera (y or n)? ").upper() == 'Y'
	
	command = "python " + __PROGRAM_DIR__ + "/run.py --logging_dir " + __LOGGING_ACTIVE_DIR__ + " "
	
	if(core):
		command = command + "--core "
	if(arduino_control):
		command = command + "--arduino_control "
	if(sensor_manage):
		command = command + "--sensing_manager "
	if(pi_camera):
		command = command + "--pi_camera "
	if(has_ros_params()):
		command = command + "--rosparams " + __PROGRAM_DIR__ + "/rosparam.config"
	
	print "[INFO] : Creating start script for service"
	
	setup_file = open(__PROGRAM_DIR__ + "/start.sh", 'w')
	
	setup_file.write("#!/bin/bash\n")
	
	setup_file.write("rm -r " + __LOGGING_ARCHIVE_DIR__ + "\n")
	setup_file.write("cp -r " + __LOGGING_ACTIVE_DIR__ + "/* " + __LOGGING_ARCHIVE_DIR__ + "\n")
	
	setup_file.write("ip route add 224.0.0.0/4 dev " + interface + "\n")
	if(core):
		setup_file.write("ifconfig " + interface + " down\n")
		setup_file.write("ifconfig " + interface + " " + core_ip + "\n")
		setup_file.write("ifconfig " + interface + " up\n")
		setup_file.write("ip_address=" + core_ip + "\n")
	else:
		setup_file.write("ip_address=$(ifconfig | grep " + interface + " -1 | cut -d: -f2 | cut -d' ' -f1)\n")
		setup_file.write("export ROS_MASTER_URI=http://" + core_ip + "::11311\n")	
	setup_file.write("export ROS_HOSTNAME=$ip_address\n")
	setup_file.write("export ROS_IP=$ip_address\n")
	
	setup_file.write(command + "\n")
	
	setup_file.close()
	
	print "[INFO] : Copying necessary instillation files"
	if os.path.exists(__PROGRAM_DIR__ + "/install"):
		shutil.rmtree(__PROGRAM_DIR__ + "/install")
	shutil.copytree("./resources/install", __PROGRAM_DIR__ + "/install", True)
	shutil.copy("./resources/run.py", __PROGRAM_DIR__ + "/run.py")
		
	os.system("chmod 755 " + __PROGRAM_DIR__ + "/start.sh")
	os.system("chmod 755 " + __PROGRAM_DIR__ + "/run.py")
	
def create_service_file():
	
	print "[INFO] : Creating service"
	
	service_file = open("/etc/systemd/system/custom_ros.service", 'w')
	
	service_file.write("[Unit]\n")
	service_file.write("Description=Service to start Senior Project at boot\n")
	service_file.write("[Service]\n")
	service_file.write("ExecStart=" + __PROGRAM_DIR__ + "/start.sh\n")
	service_file.write("[Install]\n")
	service_file.write("WantedBy=multi-user.target\n")
	
	service_file.close()
	
	print "[INFO] : Enabling service"	
	os.system("systemctl enable custom_ros.service")
	os.system("systemctl start custom_ros.service")
	
def install():
	uninstall()
	os.makedirs(__PROGRAM_DIR__)
	os.makedirs(__LOGGING_BASE_DIR__)
	os.makedirs(__LOGGING_ACTIVE_DIR__)
	os.makedirs(__LOGGING_ARCHIVE_DIR__)
	
	create_setup_file()
	create_service_file()
	
def main():
	global __args__
	
	if(not os.getuid() == 0):
		print "[ERROR] : To install this must be executed as the root user"
	else:
		parser = argparse.ArgumentParser(description='Senior Project Instillation')
		parser.add_argument('-u', '--uninstall', dest='uninstall', action="store_true", default=False,
						help='Use this flag to uninstall the program')
		parser.add_argument('-i', '--install', dest='install', action='store_true', default=False,
						help='Use this flag to install the program')

		__args__ = parser.parse_args()
		
		if(__args__.install):
			install()
		if(__args__.uninstall):
			uninstall()

if __name__ == "__main__":
	main()
