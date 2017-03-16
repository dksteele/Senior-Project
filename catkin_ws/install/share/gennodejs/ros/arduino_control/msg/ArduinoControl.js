// Auto-generated. Do not edit!

// (in-package arduino_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class ArduinoControl {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.dir = null;
      this.speed = null;
    }
    else {
      if (initObj.hasOwnProperty('dir')) {
        this.dir = initObj.dir
      }
      else {
        this.dir = 0.0;
      }
      if (initObj.hasOwnProperty('speed')) {
        this.speed = initObj.speed
      }
      else {
        this.speed = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ArduinoControl
    // Serialize message field [dir]
    bufferOffset = _serializer.float64(obj.dir, buffer, bufferOffset);
    // Serialize message field [speed]
    bufferOffset = _serializer.float64(obj.speed, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ArduinoControl
    let len;
    let data = new ArduinoControl(null);
    // Deserialize message field [dir]
    data.dir = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [speed]
    data.speed = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'arduino_control/ArduinoControl';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7528cb4c6fd33cf9e3157bf84136adec';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 dir			#Direction in degrees with 0 degrees being forward
    float64 speed			#Magnitude of direction -1 to 1
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ArduinoControl(null);
    if (msg.dir !== undefined) {
      resolved.dir = msg.dir;
    }
    else {
      resolved.dir = 0.0
    }

    if (msg.speed !== undefined) {
      resolved.speed = msg.speed;
    }
    else {
      resolved.speed = 0.0
    }

    return resolved;
    }
};

module.exports = ArduinoControl;
