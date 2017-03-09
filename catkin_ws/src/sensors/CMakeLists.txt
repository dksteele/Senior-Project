cmake_minimum_required(VERSION 2.8.3)
project(sensors)

find_package(catkin REQUIRED COMPONENTS rospy message_generation std_msgs sensor_msgs)
catkin_python_setup()

add_service_files(FILES RegistrationService.srv)
generate_messages(DEPENDENCIES std_msgs sensor_msgs)

catkin_package()

install(PROGRAMS nodes/pi_camera.py nodes/sensing_manager.py nodes/digital_tester.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY resource
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
