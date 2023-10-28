float targetThrottle = 0, throttle = 0;
int pwmVal = 0;
float targetSteer = 0, steer = 0;
float throttleMult = 0.7;
int steerAngle = 20;
int steerMultiplier = 1; // set it to -1 if the steer is reversed
int steerOffset = 7;

float throttleSmoothing = 0.6;
float steerSmoothing = 1;

int turnCount = 0;
int totalTurns = 2;
long lastTurnTimer;
int lastTurnTime = 1300;
boolean finished = false;

int rDmin[] = {4, 4, 15};    //Minimum distance range for {Side, Angle, Forward}
int rDmax[] = {90, 110, 80, 30}; //Maximum distance range for {Side, Angle, Forward}
int reactionDist = 10;

TaskHandle_t handleSonar;

// ---------------------------------- Sonar ---------------------------------- //
#include <NewPing.h>

#define MAX_DISTANCE 120
int sPins[] = {32, 27, 26, 25, 33};
long dists[] = {0, 0, 0, 0, 0};
// ---------------------------------- Sonar ---------------------------------- //
//                               ---------------                               //
// ---------------------------------- Motor ---------------------------------- //
#define motPWM 18
#define motA 21
#define motB 19
// ---------------------------------- Motor ---------------------------------- //
//                               ---------------                               //
// ---------------------------------- Servo ---------------------------------- //
#include <ESP32Servo.h>

Servo s;
#define servoPin 23
// ---------------------------------- Servo ---------------------------------- //
//                               ---------------                               //
// ----------------------------------- Btn ----------------------------------- //
#define btnPin 4
// ----------------------------------- Btn ----------------------------------- //
//                               ---------------                               //
// ----------------------------------- MPU ----------------------------------- //
#include "Wire.h"
#include <MPU6050_light.h>

MPU6050 mpu(Wire);
long lastAngle;
long currentAngle;
// ----------------------------------- MPU ----------------------------------- //
//                               ---------------                               //
// ----------------------------------- COM ----------------------------------- //
#define RXD2 16
#define TXD2 17

long serialTimer;
int key = 0;

int lineAng = 0;
int trackDir = 0;
// ----------------------------------- COM ----------------------------------- //
//                               ---------------                               //
// -------------------------------- INDICATOR -------------------------------- //
#define RED 15
#define GREEN 2
#define buzz 13

long buzzTimer = 0;

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);
  
  xTaskCreatePinnedToCore(loopB,    "secondJob", 4096,   NULL,      1,        &handleSonar,            0);
  //                     (function, task name,   memory, parameter, priority, task reference,          core)

  Serial2.print("S");
  pinMode(motPWM, OUTPUT);
  pinMode(motA, OUTPUT);
  pinMode(motB, OUTPUT);

  s.attach(servoPin);
  setThrottleSteer(0, 0);

  pinMode(btnPin, INPUT);

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(buzz, OUTPUT);


  Wire.begin();
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  //while(status!=0){ }
  //digitalWrite(GREEN, HIGH);
  Serial.println(F("Calculating offsets"));
  // mpu.upsideDownMounting = true;
  //mpu.calcOffsets();
  Serial.println("Done!\n");

  
  while (digitalRead(btnPin) == 0) { } // wait untill the button is pressed
  delay(300);
  digitalWrite(GREEN, LOW);

  Serial2.print("S");
  serialTimer = millis();
    
  //currentAngle = mpu.getAngleZ();
  lastAngle = currentAngle;
}

void loop() {
  //getMPU();
  if(millis() - buzzTimer < 200){
    digitalWrite(buzz, HIGH);
  }else if(!finished){
    digitalWrite(buzz, LOW);
  }
  
  if (!finished && turnCount >= totalTurns) { // if the car finishes three laps
    finished = true;
    lastTurnTimer = millis();
    digitalWrite(buzz, HIGH);
  }

  setControls();
  thrFromStr();

  targetThrottle = clamp(targetThrottle, 0, 1);
  targetSteer = clamp(targetSteer, -1, 1);
  
  throttle = lerpF(throttle, targetThrottle, throttleSmoothing);
  steer = lerpF(steer, targetSteer, steerSmoothing);
  
  setThrottleSteer(throttle, steer);

  if (finished && millis() - lastTurnTimer > lastTurnTime) { // Run another <lastTurnTime> milliseconds
    digitalWrite(GREEN, HIGH);
    digitalWrite(buzz, LOW);
    setThrottleSteer(0, 0);
    delay(50);
    exit(0);
  }
}

void loopB(void * param) {
  while (true) {
    getDistanceValues();
    printDistanceValues();
    delay(10);
    getSerialInfo();
    printSerialInfo();
  }
}
