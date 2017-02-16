# Senior-Project/install-files

[ INSTALLING PACKAGES ]

Prerequisites: ROS Kinetic Instaillation
               Python

Steps:
    1- Before attempting to install run "catkin_make install"(make sure to source ROS for the catkin package) in Senior-Project/catkin_ws
    2- Run "sudo python install.py -i" and follow the prompts

Information:
    After running the install script a service will be installed on the system that will start at boot, this service will start the ros commponents outputing their stdout to a file located in /var/log/custom-ros
    The instillation is self contained in /usr/share/custom-ros and the Senior-Project repository can be removed at any time after the install.py script is run

