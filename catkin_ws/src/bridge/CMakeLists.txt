cmake_minimum_required(VERSION 2.8.3)
project(bridge)

find_package(catkin REQUIRED COMPONENTS roscpp rosconsole topic_tools)

catkin_package()

include_directories(include ${catkin_INCLUDE_DIRS})

add_executable(multicast_topic_bridge src/multicast_topic_bridge.cpp)
target_link_libraries(multicast_topic_bridge ${catkin_LIBRARIES})

install(TARGETS multicast_topic_bridge
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
