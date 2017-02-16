#ifndef _ROS_arduino_control_ArduinoControl_h
#define _ROS_arduino_control_ArduinoControl_h

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace arduino_control
{

  class ArduinoControl : public ros::Msg
  {
    public:
      typedef float _dir_type;
      _dir_type dir;
      typedef float _speed_type;
      _speed_type speed;

    ArduinoControl():
      dir(0),
      speed(0)
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      offset += serializeAvrFloat64(outbuffer + offset, this->dir);
      offset += serializeAvrFloat64(outbuffer + offset, this->speed);
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      offset += deserializeAvrFloat64(inbuffer + offset, &(this->dir));
      offset += deserializeAvrFloat64(inbuffer + offset, &(this->speed));
     return offset;
    }

    const char * getType(){ return "arduino_control/ArduinoControl"; };
    const char * getMD5(){ return "7528cb4c6fd33cf9e3157bf84136adec"; };

  };

}
#endif