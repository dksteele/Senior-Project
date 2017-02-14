; Auto-generated. Do not edit!


(cl:in-package sensors-srv)


;//! \htmlinclude RegistrationService-request.msg.html

(cl:defclass <RegistrationService-request> (roslisp-msg-protocol:ros-message)
  ((platform_name
    :reader platform_name
    :initarg :platform_name
    :type cl:string
    :initform "")
   (sensor_type
    :reader sensor_type
    :initarg :sensor_type
    :type cl:string
    :initform ""))
)

(cl:defclass RegistrationService-request (<RegistrationService-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RegistrationService-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RegistrationService-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensors-srv:<RegistrationService-request> is deprecated: use sensors-srv:RegistrationService-request instead.")))

(cl:ensure-generic-function 'platform_name-val :lambda-list '(m))
(cl:defmethod platform_name-val ((m <RegistrationService-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensors-srv:platform_name-val is deprecated.  Use sensors-srv:platform_name instead.")
  (platform_name m))

(cl:ensure-generic-function 'sensor_type-val :lambda-list '(m))
(cl:defmethod sensor_type-val ((m <RegistrationService-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensors-srv:sensor_type-val is deprecated.  Use sensors-srv:sensor_type instead.")
  (sensor_type m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<RegistrationService-request>)))
    "Constants for message type '<RegistrationService-request>"
  '((:CAMERA . CAMERA)
    (:ANALOG . ANALOG)
    (:DIGITAL . DIGITAL))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'RegistrationService-request)))
    "Constants for message type 'RegistrationService-request"
  '((:CAMERA . CAMERA)
    (:ANALOG . ANALOG)
    (:DIGITAL . DIGITAL))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RegistrationService-request>) ostream)
  "Serializes a message object of type '<RegistrationService-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'platform_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'platform_name))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'sensor_type))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'sensor_type))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RegistrationService-request>) istream)
  "Deserializes a message object of type '<RegistrationService-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'platform_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'platform_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'sensor_type) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'sensor_type) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RegistrationService-request>)))
  "Returns string type for a service object of type '<RegistrationService-request>"
  "sensors/RegistrationServiceRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RegistrationService-request)))
  "Returns string type for a service object of type 'RegistrationService-request"
  "sensors/RegistrationServiceRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RegistrationService-request>)))
  "Returns md5sum for a message object of type '<RegistrationService-request>"
  "8c8e7f7b21963192fb9e2b408247fa79")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RegistrationService-request)))
  "Returns md5sum for a message object of type 'RegistrationService-request"
  "8c8e7f7b21963192fb9e2b408247fa79")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RegistrationService-request>)))
  "Returns full string definition for message of type '<RegistrationService-request>"
  (cl:format cl:nil "~%string CAMERA=CAMERA~%string ANALOG=ANALOG~%string DIGITAL=DIGITAL~%~%~%string platform_name~%string sensor_type~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RegistrationService-request)))
  "Returns full string definition for message of type 'RegistrationService-request"
  (cl:format cl:nil "~%string CAMERA=CAMERA~%string ANALOG=ANALOG~%string DIGITAL=DIGITAL~%~%~%string platform_name~%string sensor_type~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RegistrationService-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'platform_name))
     4 (cl:length (cl:slot-value msg 'sensor_type))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RegistrationService-request>))
  "Converts a ROS message object to a list"
  (cl:list 'RegistrationService-request
    (cl:cons ':platform_name (platform_name msg))
    (cl:cons ':sensor_type (sensor_type msg))
))
;//! \htmlinclude RegistrationService-response.msg.html

(cl:defclass <RegistrationService-response> (roslisp-msg-protocol:ros-message)
  ((topic
    :reader topic
    :initarg :topic
    :type cl:string
    :initform ""))
)

(cl:defclass RegistrationService-response (<RegistrationService-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RegistrationService-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RegistrationService-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensors-srv:<RegistrationService-response> is deprecated: use sensors-srv:RegistrationService-response instead.")))

(cl:ensure-generic-function 'topic-val :lambda-list '(m))
(cl:defmethod topic-val ((m <RegistrationService-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensors-srv:topic-val is deprecated.  Use sensors-srv:topic instead.")
  (topic m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RegistrationService-response>) ostream)
  "Serializes a message object of type '<RegistrationService-response>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'topic))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'topic))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RegistrationService-response>) istream)
  "Deserializes a message object of type '<RegistrationService-response>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'topic) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'topic) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RegistrationService-response>)))
  "Returns string type for a service object of type '<RegistrationService-response>"
  "sensors/RegistrationServiceResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RegistrationService-response)))
  "Returns string type for a service object of type 'RegistrationService-response"
  "sensors/RegistrationServiceResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RegistrationService-response>)))
  "Returns md5sum for a message object of type '<RegistrationService-response>"
  "8c8e7f7b21963192fb9e2b408247fa79")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RegistrationService-response)))
  "Returns md5sum for a message object of type 'RegistrationService-response"
  "8c8e7f7b21963192fb9e2b408247fa79")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RegistrationService-response>)))
  "Returns full string definition for message of type '<RegistrationService-response>"
  (cl:format cl:nil "string topic~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RegistrationService-response)))
  "Returns full string definition for message of type 'RegistrationService-response"
  (cl:format cl:nil "string topic~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RegistrationService-response>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'topic))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RegistrationService-response>))
  "Converts a ROS message object to a list"
  (cl:list 'RegistrationService-response
    (cl:cons ':topic (topic msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'RegistrationService)))
  'RegistrationService-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'RegistrationService)))
  'RegistrationService-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RegistrationService)))
  "Returns string type for a service object of type '<RegistrationService>"
  "sensors/RegistrationService")