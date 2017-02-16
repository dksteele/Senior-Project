
(cl:in-package :asdf)

(defsystem "sensors-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "RegistrationService" :depends-on ("_package_RegistrationService"))
    (:file "_package_RegistrationService" :depends-on ("_package"))
  ))