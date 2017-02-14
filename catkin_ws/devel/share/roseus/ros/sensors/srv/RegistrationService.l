;; Auto-generated. Do not edit!


(when (boundp 'sensors::RegistrationService)
  (if (not (find-package "SENSORS"))
    (make-package "SENSORS"))
  (shadow 'RegistrationService (find-package "SENSORS")))
(unless (find-package "SENSORS::REGISTRATIONSERVICE")
  (make-package "SENSORS::REGISTRATIONSERVICE"))
(unless (find-package "SENSORS::REGISTRATIONSERVICEREQUEST")
  (make-package "SENSORS::REGISTRATIONSERVICEREQUEST"))
(unless (find-package "SENSORS::REGISTRATIONSERVICERESPONSE")
  (make-package "SENSORS::REGISTRATIONSERVICERESPONSE"))

(in-package "ROS")





(intern "*CAMERA*" (find-package "SENSORS::REGISTRATIONSERVICEREQUEST"))
(shadow '*CAMERA* (find-package "SENSORS::REGISTRATIONSERVICEREQUEST"))
(defconstant sensors::RegistrationServiceRequest::*CAMERA* "CAMERA")
(intern "*ANALOG*" (find-package "SENSORS::REGISTRATIONSERVICEREQUEST"))
(shadow '*ANALOG* (find-package "SENSORS::REGISTRATIONSERVICEREQUEST"))
(defconstant sensors::RegistrationServiceRequest::*ANALOG* "ANALOG")
(intern "*DIGITAL*" (find-package "SENSORS::REGISTRATIONSERVICEREQUEST"))
(shadow '*DIGITAL* (find-package "SENSORS::REGISTRATIONSERVICEREQUEST"))
(defconstant sensors::RegistrationServiceRequest::*DIGITAL* "DIGITAL")
(defclass sensors::RegistrationServiceRequest
  :super ros::object
  :slots (_platform_name _sensor_type ))

(defmethod sensors::RegistrationServiceRequest
  (:init
   (&key
    ((:platform_name __platform_name) "")
    ((:sensor_type __sensor_type) "")
    )
   (send-super :init)
   (setq _platform_name (string __platform_name))
   (setq _sensor_type (string __sensor_type))
   self)
  (:platform_name
   (&optional __platform_name)
   (if __platform_name (setq _platform_name __platform_name)) _platform_name)
  (:sensor_type
   (&optional __sensor_type)
   (if __sensor_type (setq _sensor_type __sensor_type)) _sensor_type)
  (:serialization-length
   ()
   (+
    ;; string _platform_name
    4 (length _platform_name)
    ;; string _sensor_type
    4 (length _sensor_type)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _platform_name
       (write-long (length _platform_name) s) (princ _platform_name s)
     ;; string _sensor_type
       (write-long (length _sensor_type) s) (princ _sensor_type s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _platform_name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _platform_name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _sensor_type
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _sensor_type (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass sensors::RegistrationServiceResponse
  :super ros::object
  :slots (_topic ))

(defmethod sensors::RegistrationServiceResponse
  (:init
   (&key
    ((:topic __topic) "")
    )
   (send-super :init)
   (setq _topic (string __topic))
   self)
  (:topic
   (&optional __topic)
   (if __topic (setq _topic __topic)) _topic)
  (:serialization-length
   ()
   (+
    ;; string _topic
    4 (length _topic)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _topic
       (write-long (length _topic) s) (princ _topic s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _topic
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _topic (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass sensors::RegistrationService
  :super ros::object
  :slots ())

(setf (get sensors::RegistrationService :md5sum-) "8c8e7f7b21963192fb9e2b408247fa79")
(setf (get sensors::RegistrationService :datatype-) "sensors/RegistrationService")
(setf (get sensors::RegistrationService :request) sensors::RegistrationServiceRequest)
(setf (get sensors::RegistrationService :response) sensors::RegistrationServiceResponse)

(defmethod sensors::RegistrationServiceRequest
  (:response () (instance sensors::RegistrationServiceResponse :init)))

(setf (get sensors::RegistrationServiceRequest :md5sum-) "8c8e7f7b21963192fb9e2b408247fa79")
(setf (get sensors::RegistrationServiceRequest :datatype-) "sensors/RegistrationServiceRequest")
(setf (get sensors::RegistrationServiceRequest :definition-)
      "
string CAMERA=CAMERA
string ANALOG=ANALOG
string DIGITAL=DIGITAL


string platform_name
string sensor_type
---
string topic

")

(setf (get sensors::RegistrationServiceResponse :md5sum-) "8c8e7f7b21963192fb9e2b408247fa79")
(setf (get sensors::RegistrationServiceResponse :datatype-) "sensors/RegistrationServiceResponse")
(setf (get sensors::RegistrationServiceResponse :definition-)
      "
string CAMERA=CAMERA
string ANALOG=ANALOG
string DIGITAL=DIGITAL


string platform_name
string sensor_type
---
string topic

")



(provide :sensors/RegistrationService "8c8e7f7b21963192fb9e2b408247fa79")


