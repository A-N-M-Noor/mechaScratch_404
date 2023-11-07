float targetThrottle = 0, throttle = 0;
float targetSteer = 0, steer = 0; // (-)Left, (+)Right
int pwmLimit = 200;
int steerAngle = 20;
int steerMultiplier = 1; // set it to -1 if the steer is reversed
int steerOffset = 7;

float throttleSmoothing = 0.3;
float steerSmoothing = 0.8;

float steerObstacle = 0;
float modAcrossX, modAcrossD;

int turnCount = 0;
int totalTurns = 12;
int scndLapTurns = 4;
bool uTurn = true;
bool makeUTurn = false;
bool passedLastObj = false;
long lastTurnTimer;
int lastTurnTime = 2200;
boolean finished = false;
boolean lastLine = false;
boolean received = false;

char fObj = 'N';
char history[] = {'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'};
long objPastTime = 0;

int ignoreD = 7;
int rDmin[] = {4, 4, 15, 8};    //Minimum distance range for {Side, Angle, Forward, Forward collision}
int rDmax[] = {110, 90, 80, 40}; //Maximum distance range for {Side, Angle, Forward, Forward speed}


TaskHandle_t handleSonar;

char objType = 'N'; // N = None, G = Green, R = Red
char lostObj = 'N';
char lastObj = 'N';
long lostTimer = 0;
int lostTime = 200;
float lastObjSteer = -10;

int objDist = 200;
int newObjDist = 200;
int objPos = 0;

int xRange[] = {30, 170};
float rangeAcrossX[] = {0.2, 0.85};
float fRangeAcrossX[] = { -0.6, 0.6};

int dRange[] = {10, 120};
int FDRange[] = {40, 200};
float rangeAcrossD[] = {1, 0.1};
//float fRangeAcrossD[] = {0, 1};

int followD = FDRange[0];
long turnTimer = 0;
long turnTime = 800;
// ---------------------------------- Sonar ---------------------------------- //
#define MAX_DISTANCE 150
int sPins[] = {32, 27, 26, 25, 33};
long dists[] = {0, 0, 0, 0, 0};
long sonarTimer;
// ---------------------------------- Sonar ---------------------------------- //
//                               ---------------                               //
// ---------------------------------- Motor ---------------------------------- //
#define motPWM 18
#define motA 4
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
#define btnPin 2
// ----------------------------------- Btn ----------------------------------- //
//                               ---------------                               //
// ----------------------------------- MPU ----------------------------------- //
#include <MPU6050_tockn.h>
#include <Wire.h>

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
int trackDir = 0; // -1: cw, +1: ccw
// ----------------------------------- COM ----------------------------------- //
//                               ---------------                               //
// -------------------------------- INDICATOR -------------------------------- //
#define buzz 13

long buzzTimer = 0;
long ledTimer = 0;

long dTmr = 0;
int dt = 1;
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

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(buzz, OUTPUT);


  Wire.begin();
  mpu.begin();
  Serial.println("Done!\n");
  digitalWrite(buzz, HIGH);
  delay(1000);
  digitalWrite(buzz, LOW);

  pinMode(btnPin, OUTPUT);
  digitalWrite(btnPin, HIGH);
  while (true) {
    if (received) {
      break;
    }
  }
  digitalWrite(btnPin, LOW);

  pinMode(btnPin, INPUT);
  while (digitalRead(btnPin) == 0) { } // wait untill the button is pressed
  delay(300);

  Serial2.print("S");
  serialTimer = millis();

  getMPU();
  lastAngle = currentAngle;

  pinMode(btnPin, OUTPUT);
  dTmr = millis();
}

void loop() {
  //getMPU

  dt = millis() - dTmr;
  dTmr = millis();
  if (millis() - buzzTimer < 200) {
    digitalWrite(buzz, HIGH);
  } else if (!finished) {
    digitalWrite(buzz, LOW);
  }
  if (millis() - ledTimer < 500 || history[1] == 'R') {
    digitalWrite(btnPin, HIGH);
  } else {
    digitalWrite(btnPin, LOW);
  }

  if (!finished && turnCount >= totalTurns) { // if the car finishes three laps
    finished = true;
    lastTurnTimer = millis();
    digitalWrite(buzz, HIGH);
  }

  if (turnCount == scndLapTurns && uTurn) {
    checkIfU(50);
  }

  setControls();
  modifyObs();

  whenLost();

  avoidCollision(rDmin, rDmax);

  targetThrottle = clamp(targetThrottle, -1, 1);
  targetSteer = clamp(targetSteer, -1, 1);

  handleScenarios();
  throttle = lerpF(throttle, targetThrottle, throttleSmoothing);
  steer = lerpF(steer, targetSteer, steerSmoothing);
  throttle = clamp(throttle, -1, 0.6);
  setThrottleSteer(throttle, steer);

  if (finished && millis() - lastTurnTimer > lastTurnTime) {
    for (float i = 0; i < 0.5; i += 0.1) {
      setThrottleSteer(-i, 0); // stop the car
      delay(1);
    }
    digitalWrite(buzz, LOW);
    setThrottleSteer(0, 0);

    delay(100);
    pinMode(btnPin, OUTPUT);
    pwmLimit = 0;
    while (true) {
      digitalWrite(btnPin, HIGH);
      delay(200);
      digitalWrite(btnPin, LOW);
      delay(200);
    }
  }
}

void loopB(void * param) {
  while (true) {
    getDistanceValues();
    //printDistanceValues();
    delay(10);
    getSerialInfo();
    printSerialInfo();
  }
}
