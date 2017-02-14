// Auto-generated. Do not edit!

// (in-package arduino_control.msg)


"use strict";

let _serializer = require('../base_serialize.js');
let _deserializer = require('../base_deserialize.js');
let _finder = require('../find.js');

//-----------------------------------------------------------

class ArduinoControl {
  constructor() {
    this.dir = 0.0;
    this.speed = 0.0;
  }

  static serialize(obj, bufferInfo) {
    // Serializes a message object of type ArduinoControl
    // Serialize message field [dir]
    bufferInfo = _serializer.float64(obj.dir, bufferInfo);
    // Serialize message field [speed]
    bufferInfo = _serializer.float64(obj.speed, bufferInfo);
    return bufferInfo;
  }

  static deserialize(buffer) {
    //deserializes a message object of type ArduinoControl
    let tmp;
    let len;
    let data = new ArduinoControl();
    // Deserialize message field [dir]
    tmp = _deserializer.float64(buffer);
    data.dir = tmp.data;
    buffer = tmp.buffer;
    // Deserialize message field [speed]
    tmp = _deserializer.float64(buffer);
    data.speed = tmp.data;
    buffer = tmp.buffer;
    return {
      data: data,
      buffer: buffer
    }
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
    float64 speed		#Magnitude of direction -1 to 1
    
    `;
  }

};

module.exports = ArduinoControl;
