#!/usr/bin/env python

import argparse
import os
import shutil

__args__ = None
__PROGRAM_DIR__ = "/usr/share/custom_ros"
__LOGGING_DIR__ = "/var/log/custom_ros"

def uninstall():
	os.system("systemctl stop custom_ros.service")
	os.system("systemctl disable custom_ros.service")
	if os.path.exists(__LOGGING_DIR__):
		shutil.rmtree(__LOGGING_DIR__)
	if os.path.exists(__PROGRAM_DIR__):
		shutil.rmtree(__PROGRAM_DIR__)
	os.remove("/etc/systemd/system/custom_ros.service")
	
def create_setup_file():
	interface = raw_input("[PROMPT] : What networking interface is being used on this device?\t")
	core_ip = raw_input("[PROMPT] : What is the ip address of the core (default:192.168.0.1)?\t")
	print core_ip
	if(not core_ip):
		core_ip = "192.168.0.1"
	core = raw_input("[PROMPT] : Will this instillation be running the roscore (y or n)?\t").upper() == 'Y'		
	arduino_control = raw_input("[PROMPT] : Will this instillation be responsable for issuing joystick commands to arduino devices (y or n)?\t").upper() == 'Y'
	sensor_manage = raw_input("[PROMPT] : Will this instillation be running the sensor management node (y or n)?\t").upper() == 'Y'
	pi_camera = raw_input("[PROMPT] : Will this instillation be utilizing a Raspberry Pi Camera (y or n)?\t").upper() == 'Y'

	print "[INFO] : Creating start script for service"
	
	setup_file = open(__PROGRAM_DIR__ + "/start.sh", 'w')
	setup_file.write("#!/bin/bash\n")
	setup_file.write(". /opt/ros/kinetic/setup.sh\n")
	setup_file.write(". " + __PROGRAM_DIR__ + "/install/setup.sh\n")
	#setup_file.write("rosparam load " + __PROGRAM_DIR__ + "/rosparam.dump\n")
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
	
	if(core):
		setup_file.write("roscore > " + __LOGGING_DIR__ + "/roscore.log &\n")
	if(arduino_control):
		setup_file.write("rosrun arduino_control arduino_control > " + __LOGGING_DIR__ + "/arduino_control.log &\n")
		setup_file.write("rosrun bridge multicast_topic_bridge > " + __LOGGING_DIR__ + "/multicast_bridge.log &\n")
		setup_file.write("rosrun joy joy_node > " + __LOGGING_DIR__ + "/joy.log &\n")
	if(sensor_manage):
		setup_file.write("rosrun sensors sensing_manager.py > " + __LOGGING_DIR__ + "/sensor_manager.log &\n")
	if(pi_camera):
		setup_file.write("rosrun sensors pi_camera.py > " + __LOGGING_DIR__ + "/pi_camera.log &\n")
	
	setup_file.close()
	
	print "[INFO] : Copying necessary instillation files"
	if os.path.exists(__PROGRAM_DIR__ + "/install"):
		shutil.rmtree(__PROGRAM_DIR__ + "/install")
	shutil.copytree("./resources/install", __PROGRAM_DIR__ + "/install", True)
	
	os.system("chmod 755 " + __PROGRAM_DIR__ + "/start.sh")
	
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
	try:
		os.makedirs(__PROGRAM_DIR__)
	except:
		pass
		
	try:
		os.makedirs(__LOGGING_DIR__)
	except:
		pass
	
	create_setup_file()
	create_service_file()
	
def main():
	global __args__
	
	parser = argparse.ArgumentParser(description='Senior Project Instillation')
	parser.add_argument('-u', '--uninstall', dest='uninstall', action="store_true", default=False,
                    help='Use this flag to uninstall the program')
	parser.add_argument('-i', '--install', dest='install', action='store_true', default=False,
                    help='Use this flag to install the program')

	__args__ = parser.parse_args()
	
	if __args__.install:
		install()
	if __args__.uninstall:
		uninstall()

if __name__ == "__main__":
	main()
