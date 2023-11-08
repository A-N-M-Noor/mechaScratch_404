void onTurn() {
  lostObj = 'N';
  ledTimer = millis();
  lastAngle = currentAngle;
  turnTimer = millis();
  //digitalWrite(buzz, HIGH);
  buzzTimer = millis();
}


//not used
void manualTurn() {
  if (millis() - turnTimer < turnTime) {
    if (objType == 'N') {
      targetThrottle = 0.3;
      targetSteer = trackDir * 1;
    }
    else {
      turnTimer -= (turnTime * dt) / 10;
    }
  } else {
    turnTimer = 0;
  }
}

// after passing an object, steer slightly the opposit way
void whenLost() {
  if (lostObj != 'N' && millis() - lostTimer > lostTime) {
    if(millis() - turnTimer < 400){ 
      if(trackDir == 1 && lostObj == 'G'){return;}
      if(trackDir == -1 && lostObj == 'R'){return;} 
    }
    long tmr = millis();
    tmr = millis();
    float _str = 0;
    int tm = (int)clamp(mapFC(lastObjSteer, 0, 800, 0, 1500), 400, 900) + 150;
    while (millis() - tmr > 75 && millis() - tmr < tm && objType == 'N' && turnTimer != 0) {
      if (lostObj == 'R') {
        _str = -0.65;
      } else if (lostObj == 'G') {
        _str = 0.65;
      }
      setThrottleSteer(0.3, _str);
      if (obstacleIn(10, _str)) {
        break;
      }
    }
    /*if (objType == 'N') {
      tmr = millis();
      while (millis() - tmr < (tm * 2) / 3 && objType == 'N') {
        setThrottleSteer(0.4, -_str / 2);
        if (obstacleIn(10, -_str)) {
          break;
        }
      }
    }*/
    lostObj = 'N';
    lastObjSteer = -10;
  }

}

void setControls() {
  float _thr = 1;
  float _steer = 0;

  if (dists[0] < rDmax[0]) {
    float vl = mapFC(dists[0], rDmin[0], rDmax[0], 0.8, 0);
    _steer += vl;
  }
  if (dists[1] < rDmax[1]) {
    float vl = mapFC(dists[1], rDmin[1], rDmax[1], 0.6, 0);
    _steer += vl;
  }

  if (dists[3] < rDmax[1]) {
    float vl = mapFC(dists[3], rDmin[1], rDmax[1], 0.6, 0);
    _steer -= vl;
  }
  if (dists[4] < rDmax[0]) {
    float vl = mapFC(dists[4], rDmin[0], rDmax[0], 0.8, 0);
    _steer -= vl;
  }



  if (dists[2] < rDmax[2]) {
    _thr -= mapFC(dists[2], rDmin[2], rDmax[2], 0.3, 0);
  }
  if (dists[2] < rDmax[3]) {
    _steer *= mapFC(dists[2], rDmin[2], rDmax[3], 2, 1);
  }

  targetThrottle = _thr;
  targetSteer = _steer;
}

void thrFromStr() {
  targetThrottle *= mapFC(abs(targetSteer), 0, 1, 1, 0.5);
}

void modifyObs() {
  for (int i = 0; i < 5; i++) {
    if (dists[i] < ignoreD && i != 2) {
      return;
    }
  }

  if (objType != 'N') {
    targetSteer *= 0.5; //0
    targetThrottle *= 0.6;
    if (objDist > followD) {  //follow object
      modAcrossD = 1;
      int cPos = scrPos(objType);
      modAcrossX = mapFC(objPos, max(-30, cPos - 100), min(230, cPos + 100), fRangeAcrossX[0], fRangeAcrossX[1]);

    }
    else { //avoid objects
      if (lastObjSteer < 0) {
        lastObjSteer = 0;
      }
      modAcrossD = mapFC(objDist, dRange[0], dRange[1], rangeAcrossD[0], rangeAcrossD[1]);
      if (objType == 'R') {
        modAcrossX = mapFC(objPos, xRange[0], xRange[1], rangeAcrossX[0], rangeAcrossX[1]);
      }
      if (objType == 'G') {
        modAcrossX = -mapFC(objPos, xRange[0], xRange[1], rangeAcrossX[1], rangeAcrossX[0]);
      }
      delay(2);
      lastObjSteer += (modAcrossX * modAcrossD) * targetThrottle * float(dt);
    }
  } else {
    digitalWrite(btnPin, LOW);
  }

  steerObstacle = modAcrossX * modAcrossD;
  targetSteer += steerObstacle;
}

void avoidCollision(int _rDmin[], int _rDmax[]) {
  if (dists[2] < _rDmin[3] /*|| dists[1] < _rDmin[1] || dists[3] < _rDmin[1] || (objDist < 12 && abs(objPos - 100) < 40)*/ ) {
    long _tmr = millis();
    float _str  = 0;
    //float _str  = trackDir;

    if ((objType == 'G' && objDist < 40) || (history[0] == 'R' && objType == 'N')) {
      _str = 0.75;
    }
    else if ((objType == 'R' && objDist < 40) || (history[1] == 'G' && objType == 'N')) {
      _str = -0.75;
    }
    while (millis() - _tmr < 700) {
      setThrottleSteer(-0.6, _str);
      getMPU();
    }
    setThrottleSteer(0, 0);
    delay(500);
  }
}

void setThrottleSteer(float _thr, float _str) {
  _thr = clamp(_thr, -1, 1);
  _str = clamp(_str, -1, 1);
  delay(2);
  if (_thr == 0) {
    digitalWrite(motA, LOW);
    digitalWrite(motB, LOW);
    digitalWrite(motPWM, LOW);
  }
  else if (_thr > 0) {
    digitalWrite(motA, HIGH);
    digitalWrite(motB, LOW);
    analogWrite(motPWM, int(_thr * pwmLimit));
  }
  else {
    digitalWrite(motA, LOW);
    digitalWrite(motB, HIGH);
    analogWrite(motPWM, int(-_thr * pwmLimit));
  }


  s.write(90 + _str * steerAngle * steerMultiplier + steerOffset);
}
