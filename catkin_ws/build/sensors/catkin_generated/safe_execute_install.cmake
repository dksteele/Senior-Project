execute_process(COMMAND "/home/daniel/Documents/catkin_ws/build/sensors/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/daniel/Documents/catkin_ws/build/sensors/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
