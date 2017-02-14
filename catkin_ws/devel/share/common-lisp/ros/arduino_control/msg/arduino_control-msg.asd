
(cl:in-package :asdf)

(defsystem "arduino_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ArduinoControl" :depends-on ("_package_ArduinoControl"))
    (:file "_package_ArduinoControl" :depends-on ("_package"))
  ))