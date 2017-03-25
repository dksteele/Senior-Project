#Senior-Project/catkin_ws#

##Package Descriptions##

* ###Arduino Control###
    * ####Description :####
        * Translates joy messages such as those generated with joy_node to arduino_control messages that can be sent to control the arduino
        * The outputed message is composed of the direction and angle of magnitude with forward being 0&deg;
    * ####ROS Parameters :####
        * arduino_control/deadzone : Value of either axis at which to begin sending data. This allows the user to comensate for a non-zero'd axis

* ###Sensors###
    * ####Description :####
        * Management utility for multiple sensor stream
        * Implemented Sensors :
            * Raspberry Pi Camera
            * Digital Testing Utility
    * ####ROS Parameters :####
        * All Sensors :
            * node/platform_name : Designation of platform containing sensors
        * Pi Camera :
            * [plaform_name]-pi_camera/vflip : Raspery Pi Camera Vertical Flip
            * [plaform_name]-pi_camera/hflip : Raspery Pi Camera Horizontal Flip

* ###Bridge###
    * ####Description :####
        * Utility for sending serialized ros messages over a multicast channel
    * ####ROS Parameters :####
        * multicast_topic_bridge/topic : Topic to send over multicast
        * multicast_topic_bridge/mulicast_group_addr : Multicast group address to send to
        * multicast_topic_bridge/sending_port : Port to send on
        * multicast_topic_bridge/frequency : How often to send an updated message (Hz)
