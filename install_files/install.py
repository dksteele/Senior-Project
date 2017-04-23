#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess

__args__ = None
__PROGRAM_DIR__ = "/opt/custom_ros"
__LOGGING_BASE_DIR__ = "/var/log/custom_ros"
__LOGGING_ARCHIVE_DIR__ = __LOGGING_BASE_DIR__ + "/archive"
__LOGGING_ACTIVE_DIR__ = __LOGGING_BASE_DIR__ + "/active"
__HAS_GUI_APP__ = False
__DEFAULT_ROS_PARAMS__ = ""

# Prompts the user for any rosparam values that should be set at startup and  that corispond to the platform being setup.
# Returns a boolean value reperesenting if any ros params are provided
def has_ros_params():
	global __PROGRAM_DIR__
	global __DEFAULT_ROS_PARAMS__
	
	has_params = raw_input("[PROMPT] : Will there be any additional rosparam values that need to be set (y or n)? ").upper() == 'Y'
	if(not has_params and __DEFAULT_ROS_PARAMS__ == ""):
		return False
	
	param_file = open(__PROGRAM_DIR__ + "/rosparam.config", 'w')
	
	if(not __DEFAULT_ROS_PARAMS__ == ""):
		param_file.write(__DEFAULT_ROS_PARAMS__);
		
	if(has_params):
		param_pair = raw_input("[PROMPT] : Input paramameter as \"parameter : value\" (\"DONE\" when finished) -> ")
		while(not param_pair.upper() == "DONE"):
			param_file.write(param_pair + "\n")
			param_pair = raw_input("[PROMPT] : Input paramameter as \"parameter : value\" (\"DONE\" when finished) -> ")

	param_file.close()
	return True

# Prompts the user to determine if they are using the raspberry pi camera or not
# If used it will prompt for if a classifier should be used
# Returns a boolean value representing wheather or not the pi camera is used
def user_pi_camera(platform):
	global __DEFAULT_ROS_PARAMS__
	
	pi_camera = raw_input("[PROMPT] : Will this instillation be utilizing a Raspberry Pi Camera (y or n)? ").upper() == 'Y'
	
	if pi_camera:
		if raw_input("[PROMT] : Will you be using a classifier (y or n)? ").upper() == 'Y':
			__DEFAULT_ROS_PARAMS__ += platform + "-pi_camera/classifier : " + raw_input("[PROMPT]  : Where is the classifier stored? ") + "\n"
			if raw_input("[PROMT] : Does the classifier require a grayscale image (y or n)? ").upper() == 'Y':
				__DEFAULT_ROS_PARAMS__ += platform + "-pi_camera/classify_gray : True\n"
	
	return pi_camera
	
def create_start_files():
	global __PROGRAM_DIR__
	global __LOGGING_ACTIVE_DIR__
	global __LOGGING_ARCHIVE_DIR__
	global __HAS_GUI_APP__
	global __DEFAULT_ROS_PARAMS__
	
	#Prompt the user for configuration
	platform_name = raw_input("[PROMPT] : What is the name of this platform? ")
	interface = raw_input("[PROMPT] : What networking interface is being used on this device? ")
	
	core_ip = raw_input("[PROMPT] : What is the ip address of the core (default:192.168.1.1)? ")
	if(not core_ip):
		core_ip = "192.168.1.1"
	
	core = raw_input("[PROMPT] : Will this instillation be running the roscore (y or n)? ").upper() == 'Y'		
	arduino_control = raw_input("[PROMPT] : Will this instillation be responsable for issuing joystick commands to arduino devices (y or n)? ").upper() == 'Y'
	sensor_manager = raw_input("[PROMPT] : Will this instillation be running the sensor management node (y or n)? ").upper() == 'Y'
	
	command = "python " + __PROGRAM_DIR__ + "/run.py --logging_dir " + __LOGGING_ACTIVE_DIR__ + " "
	
	if(core):
		command = command + "--core "
	if(arduino_control):
		command = command + "--arduino_control "
		__DEFAULT_ROS_PARAMS__ += "multicast_topic_bridge/topic : arduino_control\n"
	if(use_pi_camera(platform_name)):
		command = command + "--pi_camera "
	if(has_ros_params()):
		command = command + "--rosparams " + __PROGRAM_DIR__ + "/rosparam.config"
	
	#Write the scripts for running at startup and for gui start
	if(sensor_manager):
		__HAS_GUI_APP__ = True
		gui_start_file = open(__PROGRAM_DIR__ + "/start_gui.sh", 'w')
		gui_start_file.write("#!/bin/bash\n")
		gui_start_file.write("ip_address=$(ifconfig | grep " + interface + " -1 | tail -n 1 | cut -d: -f2 | cut -d' ' -f1)\n")
		gui_start_file.write("export ROS_MASTER_URI=http://" + core_ip + ":11311/\n")
		gui_start_file.write("export ROS_HOSTNAME=$ip_address\n")
		gui_start_file.write("export ROS_IP=$ip_address\n")
		gui_start_file.write("export PLATFORM_NAME=" +  platform_name + "\n")
		gui_start_file.write("python " + __PROGRAM_DIR__ + "/run.py --logging_dir " + __LOGGING_ACTIVE_DIR__ + " --sensing_manager\n")
		gui_start_file.close()
	
	print "[INFO] : Creating start script for service"
	
	service_start_file = open(__PROGRAM_DIR__ + "/start_service.sh", 'w')
	
	service_start_file.write("#!/bin/bash\n")
	service_start_file.write("rm -r " + __LOGGING_ARCHIVE_DIR__ + "\n")
	service_start_file.write("cp -r " + __LOGGING_ACTIVE_DIR__ + " " +  __LOGGING_ARCHIVE_DIR__ + "\n")
	service_start_file.write("rm -r " + __LOGGING_ACTIVE_DIR__ + "/*\n")
	
	if(core):
		service_start_file.write("ifconfig " + interface + " down\n")
		service_start_file.write("ifconfig " + interface + " " + core_ip + "\n")
		service_start_file.write("ifconfig " + interface + " up\n")
		service_start_file.write("ip_address=" + core_ip + "\n")
	else:
		service_start_file.write("ip_address=$(ifconfig | grep " + interface + " -1 | tail -n 1 | cut -d: -f2 | cut -d' ' -f1)\n")
	service_start_file.write("export ROS_MASTER_URI=http://" + core_ip + ":11311/\n")
	service_start_file.write("export ROS_HOSTNAME=$ip_address\n")
	service_start_file.write("export ROS_IP=$ip_address\n")
	service_start_file.write("export PLATFORM_NAME=" +  platform_name + "\n")
	service_start_file.write("env | grep ROS\n");
	service_start_file.write("ip route add 224.0.0.0/4 dev " + interface + "\n")
	service_start_file.write(command + "\n")
	service_start_file.close()

	os.system("chmod 755 " + __PROGRAM_DIR__ + "/start_service.sh")

	if (sensor_manager):
		os.system("chmod 755 " + __PROGRAM_DIR__ + "/start_gui.sh")
		os.system("chmod 755 " + os.getenv("HOME") + "/.config/autostart")
		os.system("chmod -R 777 " + __LOGGING_ACTIVE_DIR__)

# Copies required package files for installign components
def install_packages():
	global __PROGRAM_DIR__
	
	print "[INFO] : Copying necessary instillation files"
	if os.path.exists(__PROGRAM_DIR__ + "/install"):
		shutil.rmtree(__PROGRAM_DIR__ + "/install")
	shutil.copytree("./resources/install", __PROGRAM_DIR__ + "/install", True)
	shutil.copy("./resources/run.py", __PROGRAM_DIR__ + "/run.py")
		
	os.system("chmod 755 " + __PROGRAM_DIR__ + "/run.py")

	
# Creates the startup service definition file
def create_service_file():
	global __PROGRAM_DIR__
	
	print "[INFO] : Creating service"
	
	service_file = open("/etc/systemd/system/custom_ros.service", 'w')
	service_file.write("[Unit]\n")
	service_file.write("Description=Service to start Senior Project at boot\n")
	service_file.write("After=networking.service\n")
	service_file.write("[Service]\n")
	service_file.write("ExecStart=" + __PROGRAM_DIR__ + "/start_service.sh\n")
	service_file.write("[Install]\n")
	service_file.write("WantedBy=multi-user.target\n")
	service_file.close()
	
	print "[INFO] : Enabling service"	
	os.system("systemctl enable custom_ros.service")
	os.system("systemctl start custom_ros.service")

# Creates the GUI autostart file
def create_gui_autostart():
	global __HAS_GUI_APP__
	global __PROGRAM_DIR__
	
	if(__HAS_GUI_APP__):
		print "[INFO] : Creating GUI autostart"
		
		if( not os.path.exists(os.getenv("HOME") + "/.config/autostart") ):
			os.makedirs(os.getenv("HOME") + "/.config/autostart")
		
		autostart_file = open(os.getenv("HOME") + "/.config/autostart/custom_ros.desktop", 'w')
		
		autostart_file.write("[Desktop Entry]\n")
		autostart_file.write("Type=Application\n")
		autostart_file.write("Name=Custom ROS GUI\n")
		autostart_file.write("Hidden=false\n")
		autostart_file.write("NoDisplay=false\n")
		autostart_file.write("Exec=" + __PROGRAM_DIR__ + "/start_gui.sh\n")
		autostart_file.write("X-GNOME-Autostart-enabled=true\n")
			
		os.system("chmod 755 " + os.getenv("HOME") + "/.config/autostart/custom_ros.desktop")
		os.system("chown -R " + os.getenv("USER") + ":" + os.getenv("USER") + " " + os.getenv("HOME") + "/.config/autostart")
		os.system("chmod 777 " + __LOGGING_BASE_DIR__)
		
def install():
	global __PROGRAM_DIR__
	global __LOGGING_BASE_DIR__
	global __LOGGING_ARCHIVE_DIR__
	global __LOGGING_ARCHIVE_DIR__
	
	uninstall()
	os.makedirs(__PROGRAM_DIR__)
	os.makedirs(__LOGGING_BASE_DIR__)
	os.makedirs(__LOGGING_ACTIVE_DIR__)
	os.makedirs(__LOGGING_ARCHIVE_DIR__)
	
	create_start_files()
	install_packages()
	create_service_file()
	create_gui_autostart()
	
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
	if(os.path.exists(os.getenv("HOME") + "/.config/autostart/custom_ros.desktop")):
		os.remove(os.getenv("HOME") + "/.config/autostart/custom_ros.desktop")

def main():
	global __args__
	
	if(not os.getuid() == 0):
		print "[ERROR] : To utilize this utility is must be executed as the root user (ex. sudo python install.py <arguments>)"
	else:
		parser = argparse.ArgumentParser(description='Senior Project Instillation')
		parser.add_argument('-u', '--uninstall', dest='uninstall', action="store_true", default=False,
						help='Use this flag to uninstall the program, the default is to install')

		__args__ = parser.parse_args()
		
		if(__args__.uninstall):
			uninstall()
		else:
			install()

if __name__ == "__main__":
	main()
