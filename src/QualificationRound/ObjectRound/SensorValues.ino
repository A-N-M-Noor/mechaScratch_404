void getDistanceValues() {
  if (millis() - sonarTimer > 15) {
    for (int i = 0; i < 5; i++) {
      dists[i] = getDistS(sPins[i]);
    }
  }
}

void printDistanceValues() {
  Serial.print("Sonar Values: ");
  for (int i = 0; i < 5; i++) {
    Serial.print(dists[i]);
    Serial.print(" - ");
  }
  Serial.println(" | ");
}

int getDistS(int te) {
  pinMode(te, OUTPUT);

  digitalWrite(te, LOW);
  delayMicroseconds(2);
  digitalWrite(te, HIGH);
  delayMicroseconds(10);
  digitalWrite(te, LOW);

  pinMode(te, INPUT);

  long dur = pulseIn(te, HIGH, MAX_DISTANCE * 60);
  int dst = dur / 58.8;
  if (dst <= 1) dst = MAX_DISTANCE;
  return (dst);
}


void getSerialInfo() {
  if (millis() - serialTimer > 15) {
    Serial2.print("D");
    serialTimer = millis();
  }

  char thisObj = 'N';
  bool newObj = false;
  while (Serial2.available()) {
    int val = Serial2.read();
    received = true;
    if (val < 50) {
      key = val;
    }

    else {
      switch (key) {
        case 5:
          if (val == 51) {
            thisObj = 'R';
            objPastTime = millis();
          }
          if (val == 52) {
            thisObj = 'N';
          }
          if (val == 53) {
            thisObj = 'G';
            objPastTime = millis();
          }
          if (objType != thisObj) {
            if (thisObj == 'N') {
              if (objType == 'R') {
                lostObj = 'R';
                lostTimer = millis();
              } else if (objType == 'G') {
                lostObj = 'G';
                lostTimer = millis();
              }
            } else {
              newObj = true;
              lastObjSteer = -10;
            }
            objType = thisObj;
          }
          else if (objType == thisObj and objType != 'N') {
            lostObj = 'N';
          }
          break;
        case 6:
          objPos = val - 50;
          break;
        case 7:
          newObjDist = val - 50;
          break;
        case 8:
          if (val - 50 != turnCount) {
            onTurn();
          }

          turnCount = val - 50;
          break;

        case 10:
          trackDir = val - 150;
          break;
        case 11:
          if (val > 55) {
            lastLine = true;
          }
          else {
            lastLine = false;
          }
          break;
      }
    }
  }
  if (newObj || newObjDist > objDist + 15) {
    addHistory(thisObj);
    lostTimer = millis();
    if (objDist < followD) {
      lastObj = thisObj;
    }
  }
  objDist = newObjDist;
}

bool obstacleIn(int dist, float _str) {
  if(_str > 2){
    for(int i = 1; i < 5; i++){
      if(dists[i] < dist){
        return true;
      }
    }
  }
  if (_str < -0.2) {
    if (dists[0] < dist || dists[1] < dist) {
      return true;
    }
  }
  if (_str > 0.2) {
    if (dists[2] < dist || dists[3] < dist) {
      return true;
    }
  }
  for (int i = 1; i < 4; i++) {
    if (dists[i] < dist) {
      return true;
    }
  }
  return false;
}

void printSerialInfo() {
  Serial.print("turnCount: ");
  Serial.print(trackDir);
  Serial.print(".");
  Serial.print(turnCount);
  Serial.print(" - Obj: ");
  Serial.print(String(history[0]) + String(objType) + String(fObj));
  Serial.print(" | ");
  Serial.print(objPos);
  Serial.print(" | ");
  Serial.print(objDist);
  Serial.print("||Mod");
  Serial.print(modAcrossX);
  Serial.print(":");
  Serial.print(modAcrossD);
  Serial.print(":");
  Serial.println(steerObstacle);
}

void sendDelay(int del) {
  Serial1.print("<" + String(del) + ">");
}
void getMPU() {
  mpu.update();
  currentAngle = mpu.getGyroAngleY();
}


void addHistory(char ob) {
  if (ob != 'N') {
    for (int i = 7; i > 0; i--) {
      history[i] = history[i - 1];
    }
    history[0] = ob;
  }
}
