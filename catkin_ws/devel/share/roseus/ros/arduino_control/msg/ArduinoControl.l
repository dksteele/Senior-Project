;; Auto-generated. Do not edit!


(when (boundp 'arduino_control::ArduinoControl)
  (if (not (find-package "ARDUINO_CONTROL"))
    (make-package "ARDUINO_CONTROL"))
  (shadow 'ArduinoControl (find-package "ARDUINO_CONTROL")))
(unless (find-package "ARDUINO_CONTROL::ARDUINOCONTROL")
  (make-package "ARDUINO_CONTROL::ARDUINOCONTROL"))

(in-package "ROS")
;;//! \htmlinclude ArduinoControl.msg.html


(defclass arduino_control::ArduinoControl
  :super ros::object
  :slots (_dir _speed ))

(defmethod arduino_control::ArduinoControl
  (:init
   (&key
    ((:dir __dir) 0.0)
    ((:speed __speed) 0.0)
    )
   (send-super :init)
   (setq _dir (float __dir))
   (setq _speed (float __speed))
   self)
  (:dir
   (&optional __dir)
   (if __dir (setq _dir __dir)) _dir)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:serialization-length
   ()
   (+
    ;; float64 _dir
    8
    ;; float64 _speed
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _dir
       (sys::poke _dir (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _dir
     (setq _dir (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _speed
     (setq _speed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get arduino_control::ArduinoControl :md5sum-) "7528cb4c6fd33cf9e3157bf84136adec")
(setf (get arduino_control::ArduinoControl :datatype-) "arduino_control/ArduinoControl")
(setf (get arduino_control::ArduinoControl :definition-)
      "float64 dir			#Direction in degrees with 0 degrees being forward
float64 speed			#Magnitude of direction -1 to 1

")



(provide :arduino_control/ArduinoControl "7528cb4c6fd33cf9e3157bf84136adec")


