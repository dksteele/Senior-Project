#include <ros.h>
#include <arduino_control/ArduinoControl.h>
#include <Ethernet.h>
#include <SPI.h>
#include <utility/w5100.h>

//Define Ports Used For Motor Control
#define RDIR 7
#define RPWM 9
#define LDIR 8
#define LPWM 3

// Needs to be only device with a MAC of this value per network
byte mac[] = {0x00, 0xAA, 0xBB, 0xCC, 0xDE, 0xFF};

//Multicasting IP, Port, and MAC are dependent upon the Multicast Group you are connecting to 
byte multicast_ip[] = {224,0,1,1};
byte multicast_mac[] = {0x01, 0x00, 0x5E, 0x00, 0x01, 0x01};
byte multicast_port = 1234;
int s = 0;

arduino_control::ArduinoControl ac;
EthernetUDP udp;
void setup(){
  Serial.begin(9600);
  
  //Setup Outputs For Motor Control
  pinMode(LDIR, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(RDIR, OUTPUT);
  pinMode(RPWM, OUTPUT);

  //Initialize Ethernet Chipset DHCP
  while(!Ethernet.begin(mac));

  //Setup socket s to utilize udp multicasting
  W5100.writeSnDIPR(s, multicast_ip);
  W5100.writeSnDPORT(s, multicast_port);
  W5100.writeSnDHAR(s, multicast_mac);
  W5100.writeSnMR(s, SnMR::UDP | SnMR::MULTI);
  W5100.execCmdSn(s, Sock_OPEN);
}

void loop(){
  //If data has been recieved begin processing, otherwise loop back and check again
  if(W5100.getRXReceivedSize(s) > 0){
    
    //Recieve the header information
    uint8_t packet_info[8];
    W5100.recv_data_processing(s, packet_info, 8);
    W5100.execCmdSn(s, Sock_RECV);
    
    //Recieve the data
    uint16_t packet_size = (packet_info[6] << 8) + packet_info[7];
    unsigned char msg_buf[packet_size];
    W5100.recv_data_processing(s, msg_buf, packet_size);
    W5100.execCmdSn(s, Sock_RECV);
    
    //Deserialize the data
    ac.deserialize(msg_buf);
        
    double lspeed = 255, rspeed = 255;
    
    lspeed = (ac.dir > 0 ? lspeed * fabs(cos(ac.dir * PI / 180)): lspeed) * ac.speed;
    rspeed = (ac.dir > 0 ? rspeed : rspeed * fabs(cos(ac.dir * PI / 180))) * ac.speed;

    int normalization_val = scale(fabs(ceil(lspeed)), fabs(ceil(rspeed)), 255);
    lspeed = ceil(lspeed) * normalization_val;
    rspeed = ceil(rspeed) * normalization_val;
    
    Serial.print("L : ");
    Serial.print(lspeed);
    Serial.print(" R: ");
    Serial.println(rspeed);
    
    setSpeed(lspeed, LPWM, LDIR);
    setSpeed(rspeed, RPWM, RDIR);
     
  }
}

//Return scal value to normalize values such that they are all below speedMax
int scale(int speed1, int speed2, int speedMax){
  if(speed1 <= speedMax && speed2 <= speedMax)
    return 1;
  
  return (speed1 > speed2) ? speedMax/speed1 : speedMax/speed2;
}

//Set speed and direction of motor attached to pwm_port ant dir_port
void setSpeed(int speed, int pwm_port, int dir_port){
  if(speed < 0)
    digitalWrite(dir_port, HIGH);
  else
    digitalWrite(dir_port, LOW);
  
  analogWrite(pwm_port, abs(speed));
}

