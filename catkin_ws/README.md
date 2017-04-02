# Senior-Project/catkin_ws

## Package Descriptions 

* ### Arduino Control
    * #### Description :
        * Translates joy messages such as those generated with joy_node to arduino_control messages that can be sent to control the arduino
        * The outputted message is composed of the direction and angle of magnitude with forward being 0&deg;
    * #### ROS Parameters :
        * arduino_control/deadzone : Value of either axis at which to begin sending data. This allows the user to compensate for a non-zeroed axis (Default : 0.1)

* ### Sensors
    * #### Description :
        * Management utility for multiple sensor stream
        * Implemented Sensors :
            * Raspberry Pi Camera
            * Digital Testing Utility
    * #### Enviroment Parameters :
        * All Sensors :
            * PLATFORM_NAME : Designation of platform containing sensors
    * #### ROS Parameters :
        * Pi Camera :
            * [plaform_name]-pi_camera/vflip : Raspery Pi Camera Vertical Flip (Default : False)
            * [plaform_name]-pi_camera/hflip : Raspery Pi Camera Horizontal Flip (Default : False)

* ### Bridge
    * #### Description :
        * Utility for sending serialized ros messages over a multicast channel
    * #### ROS Parameters :
        * multicast_topic_bridge/topic : Topic to send over multicast (Default : multicast_topic)
        * multicast_topic_bridge/mulicast_group_addr : Multicast group address to send to (Default : 224.0.1.1)
        * multicast_topic_bridge/sending_port : Port to send on (Default : 12345)
        * multicast_topic_bridge/frequency : How often to send an updated message (Hz) (Default : 1)
