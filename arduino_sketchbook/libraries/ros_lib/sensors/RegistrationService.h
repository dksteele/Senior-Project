#ifndef _ROS_SERVICE_RegistrationService_h
#define _ROS_SERVICE_RegistrationService_h
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include "ros/msg.h"

namespace sensors
{

static const char REGISTRATIONSERVICE[] = "sensors/RegistrationService";

  class RegistrationServiceRequest : public ros::Msg
  {
    public:
      typedef const char* _platform_name_type;
      _platform_name_type platform_name;
      typedef const char* _sensor_type_type;
      _sensor_type_type sensor_type;
      enum { CAMERA = CAMERA };
      enum { ANALOG = ANALOG };
      enum { DIGITAL = DIGITAL };

    RegistrationServiceRequest():
      platform_name(""),
      sensor_type("")
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t length_platform_name = strlen(this->platform_name);
      varToArr(outbuffer + offset, length_platform_name);
      offset += 4;
      memcpy(outbuffer + offset, this->platform_name, length_platform_name);
      offset += length_platform_name;
      uint32_t length_sensor_type = strlen(this->sensor_type);
      varToArr(outbuffer + offset, length_sensor_type);
      offset += 4;
      memcpy(outbuffer + offset, this->sensor_type, length_sensor_type);
      offset += length_sensor_type;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_platform_name;
      arrToVar(length_platform_name, (inbuffer + offset));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_platform_name; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_platform_name-1]=0;
      this->platform_name = (char *)(inbuffer + offset-1);
      offset += length_platform_name;
      uint32_t length_sensor_type;
      arrToVar(length_sensor_type, (inbuffer + offset));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_sensor_type; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_sensor_type-1]=0;
      this->sensor_type = (char *)(inbuffer + offset-1);
      offset += length_sensor_type;
     return offset;
    }

    const char * getType(){ return REGISTRATIONSERVICE; };
    const char * getMD5(){ return "ba03e6be1518decf9b0a19989136c24d"; };

  };

  class RegistrationServiceResponse : public ros::Msg
  {
    public:
      typedef const char* _topic_type;
      _topic_type topic;

    RegistrationServiceResponse():
      topic("")
    {
    }

    virtual int serialize(unsigned char *outbuffer) const
    {
      int offset = 0;
      uint32_t length_topic = strlen(this->topic);
      varToArr(outbuffer + offset, length_topic);
      offset += 4;
      memcpy(outbuffer + offset, this->topic, length_topic);
      offset += length_topic;
      return offset;
    }

    virtual int deserialize(unsigned char *inbuffer)
    {
      int offset = 0;
      uint32_t length_topic;
      arrToVar(length_topic, (inbuffer + offset));
      offset += 4;
      for(unsigned int k= offset; k< offset+length_topic; ++k){
          inbuffer[k-1]=inbuffer[k];
      }
      inbuffer[offset+length_topic-1]=0;
      this->topic = (char *)(inbuffer + offset-1);
      offset += length_topic;
     return offset;
    }

    const char * getType(){ return REGISTRATIONSERVICE; };
    const char * getMD5(){ return "d8f94bae31b356b24d0427f80426d0c3"; };

  };

  class RegistrationService {
    public:
    typedef RegistrationServiceRequest Request;
    typedef RegistrationServiceResponse Response;
  };

}
#endif
