; Auto-generated. Do not edit!


(cl:in-package arduino_control-msg)


;//! \htmlinclude ArduinoControl.msg.html

(cl:defclass <ArduinoControl> (roslisp-msg-protocol:ros-message)
  ((dir
    :reader dir
    :initarg :dir
    :type cl:float
    :initform 0.0)
   (speed
    :reader speed
    :initarg :speed
    :type cl:float
    :initform 0.0))
)

(cl:defclass ArduinoControl (<ArduinoControl>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ArduinoControl>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ArduinoControl)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name arduino_control-msg:<ArduinoControl> is deprecated: use arduino_control-msg:ArduinoControl instead.")))

(cl:ensure-generic-function 'dir-val :lambda-list '(m))
(cl:defmethod dir-val ((m <ArduinoControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arduino_control-msg:dir-val is deprecated.  Use arduino_control-msg:dir instead.")
  (dir m))

(cl:ensure-generic-function 'speed-val :lambda-list '(m))
(cl:defmethod speed-val ((m <ArduinoControl>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader arduino_control-msg:speed-val is deprecated.  Use arduino_control-msg:speed instead.")
  (speed m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ArduinoControl>) ostream)
  "Serializes a message object of type '<ArduinoControl>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'dir))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'speed))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ArduinoControl>) istream)
  "Deserializes a message object of type '<ArduinoControl>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'dir) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'speed) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ArduinoControl>)))
  "Returns string type for a message object of type '<ArduinoControl>"
  "arduino_control/ArduinoControl")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ArduinoControl)))
  "Returns string type for a message object of type 'ArduinoControl"
  "arduino_control/ArduinoControl")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ArduinoControl>)))
  "Returns md5sum for a message object of type '<ArduinoControl>"
  "7528cb4c6fd33cf9e3157bf84136adec")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ArduinoControl)))
  "Returns md5sum for a message object of type 'ArduinoControl"
  "7528cb4c6fd33cf9e3157bf84136adec")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ArduinoControl>)))
  "Returns full string definition for message of type '<ArduinoControl>"
  (cl:format cl:nil "float64 dir			#Direction in degrees with 0 degrees being forward~%float64 speed			#Magnitude of direction -1 to 1~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ArduinoControl)))
  "Returns full string definition for message of type 'ArduinoControl"
  (cl:format cl:nil "float64 dir			#Direction in degrees with 0 degrees being forward~%float64 speed			#Magnitude of direction -1 to 1~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ArduinoControl>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ArduinoControl>))
  "Converts a ROS message object to a list"
  (cl:list 'ArduinoControl
    (cl:cons ':dir (dir msg))
    (cl:cons ':speed (speed msg))
))
