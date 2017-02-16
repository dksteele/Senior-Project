// Auto-generated. Do not edit!

// (in-package sensors.srv)


"use strict";

let _serializer = require('../base_serialize.js');
let _deserializer = require('../base_deserialize.js');
let _finder = require('../find.js');

//-----------------------------------------------------------


//-----------------------------------------------------------

class RegistrationServiceRequest {
  constructor() {
    this.platform_name = '';
    this.sensor_type = '';
  }

  static serialize(obj, bufferInfo) {
    // Serializes a message object of type RegistrationServiceRequest
    // Serialize message field [platform_name]
    bufferInfo = _serializer.string(obj.platform_name, bufferInfo);
    // Serialize message field [sensor_type]
    bufferInfo = _serializer.string(obj.sensor_type, bufferInfo);
    return bufferInfo;
  }

  static deserialize(buffer) {
    //deserializes a message object of type RegistrationServiceRequest
    let tmp;
    let len;
    let data = new RegistrationServiceRequest();
    // Deserialize message field [platform_name]
    tmp = _deserializer.string(buffer);
    data.platform_name = tmp.data;
    buffer = tmp.buffer;
    // Deserialize message field [sensor_type]
    tmp = _deserializer.string(buffer);
    data.sensor_type = tmp.data;
    buffer = tmp.buffer;
    return {
      data: data,
      buffer: buffer
    }
  }

  static datatype() {
    // Returns string type for a service object
    return 'sensors/RegistrationServiceRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ba03e6be1518decf9b0a19989136c24d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    string CAMERA=CAMERA
    string ANALOG=ANALOG
    string DIGITAL=DIGITAL
    
    
    string platform_name
    string sensor_type
    
    `;
  }

};

// Constants for message
RegistrationServiceRequest.Constants = {
  CAMERA: 'CAMERA',
  ANALOG: 'ANALOG',
  DIGITAL: 'DIGITAL',
}

class RegistrationServiceResponse {
  constructor() {
    this.topic = '';
  }

  static serialize(obj, bufferInfo) {
    // Serializes a message object of type RegistrationServiceResponse
    // Serialize message field [topic]
    bufferInfo = _serializer.string(obj.topic, bufferInfo);
    return bufferInfo;
  }

  static deserialize(buffer) {
    //deserializes a message object of type RegistrationServiceResponse
    let tmp;
    let len;
    let data = new RegistrationServiceResponse();
    // Deserialize message field [topic]
    tmp = _deserializer.string(buffer);
    data.topic = tmp.data;
    buffer = tmp.buffer;
    return {
      data: data,
      buffer: buffer
    }
  }

  static datatype() {
    // Returns string type for a service object
    return 'sensors/RegistrationServiceResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'd8f94bae31b356b24d0427f80426d0c3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string topic
    
    
    `;
  }

};

module.exports = {
  Request: RegistrationServiceRequest,
  Response: RegistrationServiceResponse
};
