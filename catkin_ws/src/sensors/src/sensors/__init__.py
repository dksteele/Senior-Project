import sys
import os

#Import extra files for the sensing_manager to be able to access
if os.path.basename(sys.argv[0]) == "sensing_manager.py":
	from sensing_register import *
	from sensing_subscriber import *
