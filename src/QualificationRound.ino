float throttle = 0;
float steer = 0;
float throttleMult = 1;
int steerAngle = 30;
int steerMultiplier = 1; // set it to -1 if the steer is reversed
int steerOffset = 5;

float throttleSmoothing = 0.6;
float steerSmoothing = 0.5;

int turnCount = 0;
int totalTurns = 12;
long lastTurnTimer;
int lastTurnTime = 6000;
boolean finished = false;

long rDmin[] = {2, 2, 2};    //Minimum distance range for {Side, Angle, Forward}
long rDmax[] = {60, 70, 60}; //Maximum distance range for {Side, Angle, Forward}

TaskHandle_t handleSonar;

// ---------------------------------- Sonar ---------------------------------- //
#include <NewPing.h>

#define MAX_DISTANCE 120

NewPing sonars[] = {
  NewPing(26, 26, MAX_DISTANCE),
  NewPing(27, 27, MAX_DISTANCE),
  NewPing(32, 32, MAX_DISTANCE),
  NewPing(33, 33, MAX_DISTANCE),
  NewPing(25, 25, MAX_DISTANCE)
};

long dists[] = {0, 0, 0, 0, 0};
// ---------------------------------- Sonar ---------------------------------- //
//                               ---------------                               //
// ---------------------------------- Motor ---------------------------------- //
#define motPWM 4
#define motA 17
#define motB 16
// ---------------------------------- Motor ---------------------------------- //
//                               ---------------                               //
// ---------------------------------- Servo ---------------------------------- //
#include <ESP32Servo.h>

Servo s;
#define servoPin 18
// ---------------------------------- Servo ---------------------------------- //
//                               ---------------                               //
// ----------------------------------- Btn ----------------------------------- //
#define btnPin 19
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
// -------------------------------- INDICATOR -------------------------------- //
#define RED 15
#define GREEN 2

void setup() {
  Serial.begin(115200);

  xTaskCreatePinnedToCore(loopB,    "secondJob", 4096,   NULL,      1,        &handleSonar,            0);
  //                     (function, task name,   memory, parameter, priority, task reference,          core)

  pinMode(motPWM, OUTPUT);
  pinMode(motA, OUTPUT);
  pinMode(motB, OUTPUT);

  s.attach(servoPin);
  setThrottleSteer(0, 0);

  pinMode(btnPin, INPUT);

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);

  //Wire.begin();
  //byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  //Serial.println(status);
  //while(status!=0){ }
  digitalWrite(GREEN, HIGH);

  Serial.println(F("Calculating offsets"));
  // mpu.upsideDownMounting = true;
  //mpu.calcOffsets();
  Serial.println("Done!\n");
  while (digitalRead(btnPin) == 0) { } // wait untill the button is pressed
  delay(1000);
  digitalWrite(GREEN, LOW);

  //currentAngle = mpu.getAngleZ();
  lastAngle = currentAngle;
}

void loop() {
  //mpu.update();
  //currentAngle = mpu.getAngleZ();
  if (abs(lastAngle - currentAngle) > 90) {
    turnCount ++;
    lastAngle = currentAngle;
  }
  if (!finished && turnCount >= totalTurns) { // if the car finishes three laps
    finished = true;
    lastTurnTimer = millis();
  }

  setControls();
  throttle = clamp(throttle, 0, 1);
  steer = clamp(steer, -1, 1);

  thrFromStr();
  setThrottleSteer(throttle, steer);

  if (finished && millis() - lastTurnTimer > lastTurnTime) { // Run another <lastTurnTime> milliseconds
    setThrottleSteer(0, 0); // stop the car
    digitalWrite(GREEN, HIGH);
    while (digitalRead(btnPin) == 0) { } // wait untill the button is pressed
    delay(1000);

    currentAngle = mpu.getAngleZ();
    lastAngle = currentAngle;
    turnCount = 0;
    finished = false;
  }
}

void loopB(void * param) {
  while (true) {
    getDistanceValues();
  }
}


void setControls() {
  float _thr = 1;
  float _steer = 0;

  if (dists[0] < rDmax[0]) {
    float vl = mapFC(dists[0], rDmin[0], rDmax[0], 0.4, 0);
    _steer -= vl * vl;
  }
  if (dists[1] < rDmax[1]) {
    float vl = mapFC(dists[1], rDmin[1], rDmax[1], 0.6, 0);
    _steer -= vl * vl;
  }

  if (dists[3] < rDmax[1]) {
    float vl = mapFC(dists[3], rDmin[1], rDmax[1], 0.6, 0);
    _steer += vl * vl;
  }
  if (dists[4] < rDmax[0]) {
    float vl = mapFC(dists[4], rDmin[0], rDmax[0], 0.4, 0);
    _steer += vl * vl;
  }


  if (dists[2] < rDmax[2]) {
    _thr -= mapFC(dists[2], rDmin[2], rDmax[2], 1, 0);
    _steer *= mapFC(dists[2], rDmin[2], rDmax[2]*3, 3.5, 1);
  }
  throttle = lerpF(throttle, _thr, throttleSmoothing);
  steer = lerpF(steer, _steer, steerSmoothing);
}

void thrFromStr(){
  throttle *= mapFC(abs(steer), 0, 1, 1, 0.6);
}

void getDistanceValues() {
  long sonarTimer = millis();
  Serial.print("Sonar Values: ");
  for (int i = 0; i < 5; i++) {
    dists[i] = sonars[i].ping_cm();
    if (dists[i] == 0) {
      dists[i] = MAX_DISTANCE;
    }
    Serial.print(dists[i]);
    Serial.print(" - ");
  }
  Serial.println(" | ");
  delay(10);
  while (millis() - sonarTimer < 15) { } // ensures a 30ms delay between pings per sonar
}

void setThrottleSteer(float _thr, float _str) {
  _thr *= throttleMult;
  Serial.println(int(_thr * 255));
  if (_thr == 0) {
    digitalWrite(motA, LOW);
    digitalWrite(motB, LOW);
  }
  else if (_thr > 0) {
    digitalWrite(motA, HIGH);
    digitalWrite(motB, LOW);
    analogWrite(motPWM, int(_thr * 255));
  }
  else {
    digitalWrite(motA, LOW);
    digitalWrite(motB, HIGH);
    analogWrite(motPWM, int(-_thr * 255));
  }

  s.write(90 + _str * steerAngle * steerMultiplier + steerOffset);
}

float mapF(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float mapFC(float x, float in_min, float in_max, float out_min, float out_max) {
  return clamp( mapF(x, in_min, in_max, out_min, out_max), out_min, out_max);
}

float clamp(float val, float mini, float maxi) {
  if (val < mini) {
    return mini;
  }
  if (val > maxi) {
    return maxi;
  }
  return val;
}

float lerpF(float a, float b, float t)
{
  return a + t * (b - a);
}
