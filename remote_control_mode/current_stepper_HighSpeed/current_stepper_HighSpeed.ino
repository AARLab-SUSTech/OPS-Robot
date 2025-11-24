#include <Wire.h>
#include "DFRobot_INA219.h"
#include <AccelStepper.h>  

/* INA219_I2C_ADDRESS3  0x44   A0 = 0  A1 = 1
   INA219_I2C_ADDRESS4  0x45   A0 = 1  A1 = 1

   Serial2 MAC:0x78DB2FCDD56B

*/
DFRobot_INA219_IIC     ina219_1(&Wire, INA219_I2C_ADDRESS4);
DFRobot_INA219_IIC     ina219_2(&Wire, INA219_I2C_ADDRESS3);

float ina219Reading_mA = 1000;
float extMeterReading_mA = 1000;


const int xdirPin = 5;     
const int xstepPin = 2;    
const int switchEnd = A1;
const int relay1 = 8;
const int relay2 = 48;
const int relay3 = 49;
const int relay4 = 53;
const int switch1 = 47;
const long range = 200LL * 150;    
const long moveSteps = 500LL;      
const int MaxSpeed = 16000;    

int val;                  
long aimPosition = moveSteps;         
long currentPositon;

bool state1 = false;
bool state2 = false;
bool state3 = false;

AccelStepper stepper1(1, xstepPin, xdirPin); 

char comchar = "";
char comchar1 = "";
float c1,c2;
void setup(void)
{
  pinMode(xstepPin, OUTPUT);
  pinMode(xdirPin, OUTPUT);
  pinMode(switchEnd, INPUT);
  pinMode(relay1, OUTPUT);
  pinMode(relay2, OUTPUT);
  pinMode(relay3, OUTPUT);
  pinMode(relay4, OUTPUT);
  digitalWrite(relay1,LOW);
  digitalWrite(relay2,LOW);
  digitalWrite(relay3,LOW);
  digitalWrite(relay4,LOW);
  pinMode(switch1, INPUT);
  
  stepper1.setMaxSpeed(80000);     
  stepper1.setAcceleration(10000); 
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial2.begin(115200);
  Serial3.begin(115200);

  ina219_1.begin();
  delay(200);
  ina219_2.begin();
  delay(200);
  ina219_1.linearCalibrate(ina219Reading_mA, extMeterReading_mA);
  ina219_2.linearCalibrate(ina219Reading_mA, extMeterReading_mA);
  delay(200);
  digitalWrite(relay4, HIGH);
  delay(4000);
  digitalWrite(relay4, LOW);
}

void loop(void)
{ 
  c1 = ina219_1.getCurrent_mA();
  c2 = ina219_2.getCurrent_mA();
  if(c1 > 6 || c2 > 6)
  {
     Serial1.print("s");
     delay(20);
  }
  if(c1 > 15 || c2 > 15)
  {
     Serial1.print("t");
     delay(20);
  }
  if(c1 > 30 || c2 > 30)
  {
     Serial1.print("r");
     delay(20);
  }
  while (Serial2.available() > 0) {
    comchar1 = Serial2.read();
    //Serial.print("Serial.read: ");
    //Serial.println(comchar);
    delay(20);
  }
  
  while (Serial3.available() > 0) {
    comchar = Serial3.read();
    //Serial.print("Serial.read: ");
    //Serial.println(comchar);
    delay(20);
  }
  
  if (comchar == 'a') 
  {
      val = analogRead(switchEnd);   
      if(val > 1000)
      {
        stepper1.runToNewPosition(aimPosition);   
        aimPosition = aimPosition + moveSteps;
      }
      else
      {
        stepper1.setCurrentPosition(200LL * 150); 
        Serial1.print("a");
        delay(100);
        comchar = "";
      }
  }
  
  if (comchar == 'b')
  {
    Serial1.print("b");
    delay(100);
    stepper1.runToNewPosition(200LL * 100); 
    Serial1.print("m");
    delay(100);
    state1 = true;
    currentPositon = 200LL * 100;
    comchar = "";
  }
  
  if (comchar == 'c')
  {
    state1 = false;
    Serial1.print("c");
    delay(100);
    stepper1.runToNewPosition(200LL * 150); 
    Serial1.print("d");
    delay(200);
    state2 = true;
    comchar = "";
  }

  if (comchar == 'f' && state1)
  {
    currentPositon = currentPositon + 50LL;
    stepper1.runToNewPosition(currentPositon);
    comchar = "";
  }

  if (comchar == 'e' && state1)
  {
    currentPositon = currentPositon - 50LL;
    stepper1.runToNewPosition(currentPositon);
    comchar = "";
  }

  if (comchar == 'f' && state2)
  {
    currentPositon = currentPositon + 200LL;
    stepper1.runToNewPosition(currentPositon);
    comchar = "";
  }

  if (comchar == 'e' && state2)
  {
    currentPositon = currentPositon - 200LL;
    stepper1.runToNewPosition(currentPositon);
    comchar = "";
  }

  if (comchar == 'n')
  {
    currentPositon = currentPositon + 200LL;
    stepper1.runToNewPosition(currentPositon);
    comchar = "";
  }

  if (comchar == 'm')
  {
    currentPositon = currentPositon - 200LL;
    stepper1.runToNewPosition(currentPositon);
    comchar = "";
  }
  
  while (Serial2.available() > 0) {
    comchar1 = Serial2.read();
    //Serial.print("Serial.read: ");
    //Serial.println(comchar);
    delay(20);
  }
  
  if (digitalRead(switch1) == 1 || comchar1 == 'y')
  {
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, HIGH);
    digitalWrite(relay3, HIGH);
    delay(20);
    Serial1.print("h");
    delay(1000);
    state3 = true;
    comchar1 = "";
  }

  while (Serial2.available() > 0) {
    comchar1 = Serial2.read();
    //Serial.print("Serial.read: ");
    //Serial.println(comchar);
    delay(20);
  }
  
  if(digitalRead(switch1) == 0 && state3 == true && comchar1 == 'z')
    {
      //stepper1.setCurrentPosition(200LL * 150); 
      //Serial1.print("a");
      //delay(100);
      digitalWrite(relay1, LOW);
      digitalWrite(relay2, LOW);
      digitalWrite(relay3, LOW);
      state3 = false;
      comchar1 = "";
    }

}
