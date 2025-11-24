#include "DFRobotBLEGamepad.h"
#include <Wire.h>

#define header_H     0x3E 

#define V_CMD        0xA2 
#define PV_CMD       0xA4 

#define device1_Addr 0x01 
#define device2_Addr 0x02 

#define V_data_Length  0x04 
#define PV_data_Length  0x0C 

#define V_header_checksum1 0xE5 
#define V_header_checksum2 0xE6 
#define PV_header_checksum1 0xEF 
#define PV_header_checksum2 0xF0 

#define V_P90_1 0x28
#define V_P90_2 0x23 
#define V_P90_3 0x00 
#define V_P90_4 0x00 
#define V_P90_checksum 0x4B

#define V_N90_1 0xD8 
#define V_N90_2 0xDC 
#define V_N90_3 0xFF 
#define V_N90_4 0xFF 
#define V_N90_checksum 0xB2 

#define V_P75_1 0x4C 
#define V_P75_2 0x1D 
#define V_P75_3 0x00 
#define V_P75_4 0x00 
#define V_P75_checksum 0x69 

#define V_N75_1 0xB4 
#define V_N75_2 0xE2 
#define V_N75_3 0xFF 
#define V_N75_4 0xFF
#define V_N75_checksum 0x94 

#define V_P50_1 0x88 
#define V_P50_2 0x13
#define V_P50_3 0x00 
#define V_P50_4 0x00 
#define V_P50_checksum 0x9B

#define V_N50_1 0x78
#define V_N50_2 0xEC 
#define V_N50_3 0xFF 
#define V_N50_4 0xFF 
#define V_N50_checksum 0x62 

#define V_P20_1 0xD0 
#define V_P20_2 0x07 
#define V_P20_3 0x00 
#define V_P20_4 0x00 
#define V_P20_checksum 0xD7

#define V_N20_1 0x30
#define V_N20_2 0xF8 
#define V_N20_3 0xFF
#define V_N20_4 0xFF 
#define V_N20_checksum 0x26 

#define V_0_1 0x00 
#define V_0_2 0x00 
#define V_0_3 0x00 
#define V_0_4 0x00
#define V_0_checksum 0x00 

#define P_0_1 0x00
#define P_0_2 0x00 
#define P_0_3 0x00 
#define P_0_4 0x00 
#define P_0_5 0x00 
#define P_0_6 0x00 
#define P_0_7 0x00 
#define P_0_8 0x00
#define PV_0_0_20_checksum 0xD7 

#define P_360_1 0xA0 
#define P_360_2 0x8C 
#define P_360_3 0x00 
#define P_360_4 0x00 
#define P_360_5 0x00 
#define P_360_6 0x00 
#define P_360_7 0x00 
#define P_360_8 0x00 
#define PV_0_360_20_checksum 0x03 

#define P_300_1 0x30 
#define P_300_2 0x75 
#define P_300_3 0x00 
#define P_300_4 0x00
#define P_300_5 0x00 
#define P_300_6 0x00 
#define P_300_7 0x00 
#define P_300_8 0x00 
#define PV_0_300_20_checksum 0x7C 

unsigned char i=0;

unsigned char CMD1_V_P90[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                              V_P90_1,V_P90_2,V_P90_3,V_P90_4,V_P90_checksum}; 
                     
unsigned char CMD2_V_P90[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                              V_P90_1,V_P90_2,V_P90_3,V_P90_4,V_P90_checksum}; 

unsigned char CMD1_V_N90[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                              V_N90_1,V_N90_2,V_N90_3,V_N90_4,V_N90_checksum}; 

unsigned char CMD2_V_N90[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                              V_N90_1,V_N90_2,V_N90_3,V_N90_4,V_N90_checksum};
                              

unsigned char CMD1_V_P75[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                             V_P75_1,V_P75_2,V_P75_3,V_P75_4,V_P75_checksum}; 
                        
unsigned char CMD2_V_P75[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                             V_P75_1,V_P75_2,V_P75_3,V_P75_4,V_P75_checksum}; 

unsigned char CMD1_V_N75[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                             V_N75_1,V_N75_2,V_N75_3,V_N75_4,V_N75_checksum}; 

unsigned char CMD2_V_N75[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                             V_N75_1,V_N75_2,V_N75_3,V_N75_4,V_N75_checksum};
                             

unsigned char CMD1_V_P50[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                             V_P50_1,V_P50_2,V_P50_3,V_P50_4,V_P50_checksum}; 
                         
unsigned char CMD2_V_P50[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                             V_P50_1,V_P50_2,V_P50_3,V_P50_4,V_P50_checksum}; 

unsigned char CMD1_V_N50[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                             V_N50_1,V_N50_2,V_N50_3,V_N50_4,V_N50_checksum}; 

unsigned char CMD2_V_N50[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                             V_N50_1,V_N50_2,V_N50_3,V_N50_4,V_N50_checksum};
                             

unsigned char CMD1_V_P20[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                             V_P20_1,V_P20_2,V_P20_3,V_P20_4,V_P20_checksum}; 
                        
unsigned char CMD2_V_P20[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                             V_P20_1,V_P20_2,V_P20_3,V_P20_4,V_P20_checksum}; 

unsigned char CMD1_V_N20[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                             V_N20_1,V_N20_2,V_N20_3,V_N20_4,V_N20_checksum}; 

unsigned char CMD2_V_N20[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                             V_N20_1,V_N20_2,V_N20_3,V_N20_4,V_N20_checksum};
                             

unsigned char CMD1_V_0[10]={header_H,V_CMD,device1_Addr,V_data_Length,V_header_checksum1,
                            V_0_1,V_0_2,V_0_3,V_0_4,V_0_checksum};

unsigned char CMD2_V_0[10]={header_H,V_CMD,device2_Addr,V_data_Length,V_header_checksum2,
                            V_0_1,V_0_2,V_0_3,V_0_4,V_0_checksum}; 
                            

unsigned char CMD1_PV_0_0_20[18]={header_H,PV_CMD,device1_Addr,PV_data_Length,PV_header_checksum1,
                                  P_0_1,P_0_2,P_0_3,P_0_4,P_0_5,P_0_6,P_0_7,P_0_8,V_P20_1,V_P20_2,V_P20_3,V_P20_4,PV_0_0_20_checksum};

unsigned char CMD2_PV_0_0_20[18]={header_H,PV_CMD,device2_Addr,PV_data_Length,PV_header_checksum2,
                                  P_0_1,P_0_2,P_0_3,P_0_4,P_0_5,P_0_6,P_0_7,P_0_8,V_P20_1,V_P20_2,V_P20_3,V_P20_4,PV_0_0_20_checksum};

unsigned char CMD1_PV_0_300_20[18]={header_H,PV_CMD,device1_Addr,PV_data_Length,PV_header_checksum1,
                                    P_300_1,P_300_2,P_300_3,P_300_4,P_300_5,P_300_6,P_300_7,P_300_8,V_P20_1,V_P20_2,V_P20_3,V_P20_4,PV_0_300_20_checksum};

unsigned char CMD1_Reset[5]={0x3E,0x19,0x01,0x00,0x58};

#define SWITCH_UP   0
#define SWITCH_DOWN   1
#define SWITCH_LEFT   2
#define SWITCH_RIGHT   3
#define SWITCH_LEFT_F1  4
#define SWITCH_LEFT_F2  5
#define SWITCH_LEFT_STICK  6

#define SWITCH_4   7
#define SWITCH_2   8
#define SWITCH_1   9
#define SWITCH_3   10
#define SWITCH_RIGHT_F1  11
#define SWITCH_RIGHT_F2  12
#define SWITCH_RIGHT_STICK  13

DFRobotBLEGamepad myDFRobotBLEGamepad;                      
int joystickRightX, joystickRightY;                 
int joystickLeftX, joystickLeftY;  
boolean buttonState[14];                                                        

bool begin_state = true;
bool SWITCH_UP_state = false;
bool SWITCH_DOWN_state = false;
bool SWITCH_LEFT_state = false;
bool SWITCH_RIGHT_state = false;
bool SWITCH_1_state = true;
bool SWITCH_2_state = false;
bool SWITCH_3_state = false;
bool SWITCH_4_state = false;
bool SWITCH_run_2_state = false;
bool SWITCH_run_3_state = false;
bool SWITCH_run_4_state = false;
bool joystickRightX_state = false;
bool joystickRightY_state = false;
bool joystick_state = false;
int last_joystickRightX = 127;
int last_joystickRightY = 127;
const int relay4 = 35;

void setup() {
  pinMode(relay4, OUTPUT);
  digitalWrite(relay4,LOW);
  Serial.begin(115200); 
  Serial1.begin(115200);
  Serial3.begin(115200);
  myDFRobotBLEGamepad.begin(Serial1);     

}

void loop() {

 while(begin_state == true) 
    {
       for(i=0;i<10;i++)
       {
          Serial.write(CMD1_V_0[i]);
        }
       delay(100);
       for(i=0;i<10;i++)
       {
          Serial.write(CMD2_V_0[i]);
        }
       begin_state = false;
    }
  
 if ( myDFRobotBLEGamepad.available() ) {

    //get the joystick value
    joystickRightX = myDFRobotBLEGamepad.readJoystickRightX();                   
    joystickRightY = myDFRobotBLEGamepad.readJoystickRightY();                   
    joystickLeftX = myDFRobotBLEGamepad.readJoystickLeftX();                     
    joystickLeftY = myDFRobotBLEGamepad.readJoystickLeftY();

    //read button state when there's valid command from bluetooth
    buttonState[SWITCH_UP] = myDFRobotBLEGamepad.readSwitchUp();
    buttonState[SWITCH_DOWN] = myDFRobotBLEGamepad.readSwitchDown();
    buttonState[SWITCH_LEFT] = myDFRobotBLEGamepad.readSwitchLeft();
    buttonState[SWITCH_RIGHT] = myDFRobotBLEGamepad.readSwitchRight();
    buttonState[SWITCH_LEFT_F1] = myDFRobotBLEGamepad.readSwitchLeftF1();
    buttonState[SWITCH_LEFT_F2] = myDFRobotBLEGamepad.readSwitchLeftF2();
    buttonState[SWITCH_LEFT_STICK] = myDFRobotBLEGamepad.readSwitchLeftStick();

    buttonState[SWITCH_1] = myDFRobotBLEGamepad.readSwitch1();
    buttonState[SWITCH_2] = myDFRobotBLEGamepad.readSwitch2();
    buttonState[SWITCH_3] = myDFRobotBLEGamepad.readSwitch3();
    buttonState[SWITCH_4] = myDFRobotBLEGamepad.readSwitch4();
    buttonState[SWITCH_RIGHT_F1] = myDFRobotBLEGamepad.readSwitchRightF1();
    buttonState[SWITCH_RIGHT_F2] = myDFRobotBLEGamepad.readSwitchRightF2();
    buttonState[SWITCH_RIGHT_STICK] = myDFRobotBLEGamepad.readSwitchRightStick();
    /**
    Serial.print( "Joystick Left Value: " );                                     //debug bluetooth data received
    Serial.print( joystickLeftX );
    Serial.print("  ");
    Serial.println( joystickLeftY );

    Serial.print( "Joystick Right Value: " );                                    //debug bluetooth data received
    Serial.print( joystickRightX );
    Serial.print("  ");
    Serial.println( joystickRightY );
    **/
    /************************************************************/
    /*
     * 
     */
    if (buttonState[SWITCH_UP] == PRESSED) 
    {
      if(SWITCH_UP_state == true)
      {
        for(i=0;i<10;i++)
        {
          Serial.write(CMD1_V_N75[i]);
         }
        SWITCH_UP_state = false;
      }
    }   
    if (buttonState[SWITCH_DOWN] == PRESSED) 
    {
      if(SWITCH_DOWN_state == true)
      {
        for(i=0;i<10;i++)
        {
          Serial.write(CMD1_V_P75[i]);
         }
        SWITCH_DOWN_state = false;
      }
    }
    if (buttonState[SWITCH_LEFT] == PRESSED) 
    {
      if(SWITCH_LEFT_state == true)
      {
        for(i=0;i<10;i++)
        {
          Serial.write(CMD2_V_N75[i]);
         }
        SWITCH_LEFT_state = false;
      }
    }
    if (buttonState[SWITCH_RIGHT] == PRESSED) 
    {
      if(SWITCH_RIGHT_state == true)
      {
        for(i=0;i<10;i++)
        {
          Serial.write(CMD2_V_P75[i]);
         }
       SWITCH_RIGHT_state = false;
      }
    }
   
    /************************************************************/
    
    /************************************************************/   
    /*
     * Step1:
     */
    if (buttonState[SWITCH_1] == PRESSED) 
    {
      if(SWITCH_1_state == true)
      {
          for(i=0;i<18;i++)
          {
             Serial.write(CMD1_PV_0_0_20[i]); 
          }
          delay(100);
          for(i=0;i<18;i++)
          {
             Serial.write(CMD2_PV_0_0_20[i]); 
          }
          delay(1000);
          
          Serial3.print("a");
          delay(100);

          
          /*for(i=0;i<10;i++)
          {
             Serial.write(CMD1_V_N5[i]); 
          }
          delay(4000);
          for(i=0;i<10;i++)
          {
             Serial.write(CMD1_V_0[i]);
          }
          delay(100);*/
          SWITCH_2_state = true;
      }
      SWITCH_1_state = false;
    }
    /************************************************************/
    /*
     * Step2:
     */
     if (buttonState[SWITCH_2] == PRESSED) 
    {
      if(SWITCH_2_state == true)
      {
          for(i=0;i<18;i++)
          {
             Serial.write(CMD1_PV_0_0_20[i]); 
          }
          delay(500);

          Serial3.print("b");
          delay(100);
          SWITCH_3_state = true;
      }
      SWITCH_2_state = false; 
      
    }
    /************************************************************/
    /*
     * Step3:
     */
     if (buttonState[SWITCH_3] == PRESSED) 
    {
      if(SWITCH_3_state == true)
      {
          for(i=0;i<18;i++)
          {
             Serial.write(CMD1_PV_0_0_20[i]); 
          }
          delay(100);
          for(i=0;i<18;i++)
          {
             Serial.write(CMD2_PV_0_0_20[i]); 
          }
          delay(1000);
          /*for(i=0;i<10;i++)
          {
             Serial.write(CMD1_V_P5[i]); 
          }
          delay(1000);
          for(i=0;i<10;i++)
          {
             Serial.write(CMD1_V_0[i]);
          }
          delay(1000);*/
          Serial3.print("c");
      }
      SWITCH_3_state = false; 
      SWITCH_1_state = true; 
    }
    /*****************************************************/
    /*
                  UP: joystickLeftY = 255
     LEFT:  joystickLeftX = 255      RIGHT:  joystickLeftX = 0
                 DOWN: joystickLeftY = 0
     
       1-28,  29-57,  58-85, 86-113,114-141,142-169,170-197,198-225,226-255
     352.88°,354.66°,356.44°,358.22°,  0°,   1.78°,  3.56°,  5.34°,  7.12°
     */
    if (buttonState[SWITCH_LEFT_F2] == PRESSED && (joystickRightX > 135 || (joystickRightX < 120 && joystickRightX > 0)))
    {
          if(joystickRightX - last_joystickRightX >= 10)
          {
              for(i=0;i<10;i++)
              {
                 Serial.write(CMD2_V_N75[i]); 
              }
              delay(50);
              last_joystickRightX = joystickRightX;
              joystickRightX_state = true;
          }
          delay(20);
          if(last_joystickRightX - joystickRightX >= 10 )
          {
                for(i=0;i<10;i++)
              {
                 Serial.write(CMD2_V_P75[i]); 
              }
              delay(50);
              last_joystickRightX = joystickRightX;
              joystickRightX_state = true;  
          }
    }
    
    if ( buttonState[SWITCH_LEFT_F2] == RELEASED)    
    {
        if(joystickRightY_state == true && joystickRightX_state == true)
        {
            for(i=0;i<10;i++)
            {
               Serial.write(CMD2_V_0[i]); 
            }
            delay(50);
              for(i=0;i<10;i++)
            {
               Serial.write(CMD1_V_0[i]); 
            }
            delay(50);
            joystickRightY_state = false;
            joystickRightX_state = false;
        }
    }

    if (buttonState[SWITCH_LEFT_F2] == PRESSED && (joystickRightY > 135 || (joystickRightY < 120 && joystickRightY > 0)))
    {
        if(joystickRightY - last_joystickRightY >= 10)
        {
            for(i=0;i<10;i++)
            {
               Serial.write(CMD1_V_N75[i]); 
            }
            delay(50);
            last_joystickRightY = joystickRightY;
            joystickRightY_state = true;
        }
        delay(20);
        if(last_joystickRightY - joystickRightY >= 10)
        {
            for(i=0;i<10;i++)
            {
               Serial.write(CMD1_V_P75[i]); 
            }
            delay(50);
            last_joystickRightY = joystickRightY;
            joystickRightY_state = true;   
        }
    }

    if (joystickLeftY > 135 && buttonState[SWITCH_LEFT_F1] == RELEASED)
    {
        Serial3.print("e");  
    }

    if (joystickLeftY > 0 && joystickLeftY < 120 && buttonState[SWITCH_LEFT_F1] == RELEASED)
    {
        Serial3.print("f");  
    }

    if (joystickLeftY > 135 && buttonState[SWITCH_LEFT_F1] == PRESSED)
    {
        Serial3.print("m");  
    }

    if (joystickLeftY > 0 && joystickLeftY < 120 && buttonState[SWITCH_LEFT_F1] == PRESSED)
    {
        Serial3.print("n");  
    }
    if (buttonState[SWITCH_RIGHT_F2] == PRESSED)
    {
        Serial3.print("y"); 
    }
    if (buttonState[SWITCH_RIGHT] == RELEASED && buttonState[SWITCH_LEFT] == RELEASED )
    {
      if(SWITCH_RIGHT_state == false || SWITCH_LEFT_state == false)
      {
        for(i=0;i<10;i++)
        {
          Serial.write(CMD2_V_0[i]);
         }
        delay(20);        
        SWITCH_RIGHT_state = true;
        SWITCH_LEFT_state = true;
        last_joystickRightX = 127;
        joystickRightX_state = false;
      }
    }  
    if (buttonState[SWITCH_UP] == RELEASED && buttonState[SWITCH_DOWN] == RELEASED )
    {
      if(SWITCH_UP_state == false || SWITCH_DOWN_state == false)
      {
        for(i=0;i<10;i++)
        {
          Serial.write(CMD1_V_0[i]);
         }
        delay(20);
        SWITCH_UP_state = true;
        SWITCH_DOWN_state = true;
        last_joystickRightY = 127;
        joystickRightY_state = false;
      }
    }
    /************************************************************/ 
  }


}
