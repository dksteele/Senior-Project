#include <ros/ros.h>
#include <sensor_msgs/Joy.h>
#include <arduino_control/ArduinoControl.h>

#include <math.h>

#define PI 3.14159265359

ros::Publisher controlPub;
double DEADZONE = 0;

int joyCallback(const sensor_msgs::Joy::ConstPtr& msg){
	arduino_control::ArduinoControl ac;
	
	ac.dir = atan2(-msg->axes[0], msg->axes[1]) * 180 / PI;		//Gets angle of the joystick in degrees with forward/top being 0 degrees
	
	ac.speed = sqrt(pow(msg->axes[1] , 2) + pow(msg->axes[0] , 2));	//Gets magnitude of the joystick movement
	
	if(fabs(msg->axes[0]) < DEADZONE && fabs(msg->axes[1]) < DEADZONE)	//Speed is 0 when within the deadzone of both axes
		ac.speed = 0;
	
	controlPub.publish(ac);
}

int main(int argc, char* argv[]){
	ros::init(argc, argv, "arduino_control");
	ros::NodeHandle nh;
	
	//Retrieve deadzone value from the ros params (defaults to .1) and then use the absalute value
	nh.param<double>("arduino_control/deadzone", DEADZONE, 0.1);
	DEADZONE = fabs(DEADZONE);
	
	//Create subscriber and publisher
	ros::Subscriber joySub = nh.subscribe<sensor_msgs::Joy>("joy", 1, joyCallback);
	controlPub = nh.advertise<arduino_control::ArduinoControl>("arduino_control", 10);
	
	ros::spin();
}
