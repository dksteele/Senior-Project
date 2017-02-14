cmake_minimum_required(VERSION 2.8.3)
project(arduino_control)

find_package(catkin REQUIRED COMPONENTS roscpp message_generation std_msgs)

add_message_files(FILES ArduinoControl.msg)
generate_messages(DEPENDENCIES std_msgs)

catkin_package()

include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(arduino_control src/arduino_control.cpp)
target_link_libraries(arduino_control ${catkin_LIBRARIES})

install(TARGETS arduino_control
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
