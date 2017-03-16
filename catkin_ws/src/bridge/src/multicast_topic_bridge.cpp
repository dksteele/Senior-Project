#include <arpa/inet.h>
#include <netinet/in.h>
#include <pthread.h>
#include <signal.h>
#include <sys/socket.h>
#include <unistd.h>

#include <boost/date_time/posix_time/posix_time.hpp>

#include <topic_tools/shape_shifter.h>

#include <ros/ros.h>
#include <ros/console.h>

//Struct for handeling data that both the master and a thread or both threads need acccess to
struct shared_program_data
{
	// Data, New Data Flag, and Mutex
	unsigned char* data;
	int data_size;
	bool new_msg;
	pthread_mutex_t modifying_msg;
	
	int s; // Multicasting Socket
	
	bool stop;	//Stop Command To Cleanly Exit Program
	
	//Parameters
	std::string MULTICAST_GROUP_ADDRESS;
	int SENDING_PORT;
	int FREQUENCY;
};

// Thread for handling the ros multicasting functions
pthread_t multicasting_thread;

shared_program_data data;

void output_debug_message(std::string s){
	boost::posix_time::ptime time = boost::posix_time::second_clock::local_time();
	printf("%s\t: %s\n", boost::posix_time::to_simple_string(time).c_str(), s.c_str());
}

/*
 * Callback for the subscriber function
*/
void topic_callback(const boost::shared_ptr<topic_tools::ShapeShifter const>& msg){
	//Make a buffer to hold the serialized data
	data.data_size = ros::serialization::serializationLength(*msg);
    std::vector<uint8_t> buffer(data.data_size);
 
    
    //Stram the serialized data into the buffer
    ros::serialization::OStream os(&buffer[0], data.data_size);
    ros::serialization::Serializer<topic_tools::ShapeShifter>::write(os, *msg);
	

	//Put the new message into the structure and set the new message flag
	pthread_mutex_lock(&(data.modifying_msg));
	data.data = (unsigned char*) malloc((sizeof(unsigned char) * data.data_size));
	memcpy(data.data, &buffer[0], data.data_size);
	data.new_msg = true;
	pthread_mutex_unlock(&(data.modifying_msg));
}

/*
 * This function is a thread to manage incrmental sending of the information recieved over the desigated topic
 * The increment at which the sending is preformed is defined through parameters  
*/
void* multicasting_socket(void* argv){
	shared_program_data* args = (shared_program_data*) argv;
	
	// Addressing Information For Sending Multicast Data
	struct sockaddr_in addr;
	
	output_debug_message("[ INFO ] : Creating Socket...");
	
	//Create The Socket
	args->s = socket(AF_INET,SOCK_DGRAM,0);
	if(args->s < 0){
		output_debug_message("[ ERROR ] : Socket Error Creation Error]");
		perror("SOCKET");
		return 0;
	}

	//Populate Addressing Information
	memset(&addr,0,sizeof(addr));
	addr.sin_family=AF_INET;
	addr.sin_addr.s_addr=inet_addr(args->MULTICAST_GROUP_ADDRESS.c_str());
	addr.sin_port=htons(args->SENDING_PORT);
	
	//Print Multicasting Information To User
	output_debug_message("[ INFO ] : Socket Creation Completed Successfully");

	char buff[80];
	sprintf(buff, "[ INFO ] : Sending To -> %s:%d", args->MULTICAST_GROUP_ADDRESS.c_str(), args->SENDING_PORT);
	output_debug_message(buff);
	
	if(args->FREQUENCY == 0)
		sprintf(buff, "[ INFO ] : A New Message Will Be Sent When Available");
	else
		sprintf(buff, "[ INFO ] : A New Message Will Be Sent %d Times A Second If Available", args->FREQUENCY);
	output_debug_message(buff);
	
	while(!args->stop){
		//Check For New Message And Send If Available Then Wait Till Next Check Is Needed
		
		pthread_mutex_lock(&(args->modifying_msg));
		if(args->new_msg){
			if(sendto(args->s, args->data, args->data_size, 0, (struct sockaddr *) &addr, sizeof(addr)) < 0)
				output_debug_message("[ ERROR ] : Failed To Send Message");
			else
				args->new_msg = false;			
		}
		pthread_mutex_unlock(&(args->modifying_msg));
		
		if(args->FREQUENCY != 0)
			usleep(1000000 / args->FREQUENCY);
	}
}

void close_program(int error_id){	
	output_debug_message("[ INFO ] : Shutting Down");
	
	//Set Flag And Wait For Thread To Complete
	data.stop = true;
	pthread_join(multicasting_thread, NULL);
	
	if(data.s >= 0){
		// Handle Closing The Socket And Sending Any Termination Information
		close(data.s);
	}
	
	//Exit Program
	exit(1);
}

int main(int argc, char* argv[])
{	
	//Signal Handler For Interupt Such As Ctl-C
	signal(SIGINT, close_program);	
	
	//Initialize The ROS NodeHandle
	ros::init(argc, argv, "multicast_topic_bridge", ros::init_options::NoSigintHandler);
	ros::NodeHandle nh;
	
	//Retrieve all parameters
	std::string topic_name;	
	nh.param<std::string>("multicast_topic_bridge/topic", topic_name, "multicast_topic");
	nh.param<std::string>("multicast_topic_bridge/multicating_group_addr", data.MULTICAST_GROUP_ADDRESS, "224.0.1.1");
	nh.param<int>("multicast_topic_bridge/sending_port", data.SENDING_PORT, 12345);
	nh.param<int>("multicast_topic_bridge/frequency", data.FREQUENCY, 1);
	
	//Subscribe to parameter for topic_name
	ros::Subscriber sub = nh.subscribe<topic_tools::ShapeShifter>(topic_name, 1, topic_callback);
	output_debug_message("[ INFO ] : Subscribed To : " + topic_name);
	
	//Create thread for multicasting new message at the speed of the frequency parameter
	pthread_create(&multicasting_thread, NULL, multicasting_socket, &data);
	
	//Spin ROS Subscriber For New Data
	ros::spin();
}
