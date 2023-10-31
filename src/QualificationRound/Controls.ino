void onTurn() {
  buzzTimer = millis();
  lastAngle = currentAngle;
}


void setControls() {
  float _thr = 1;
  float _steer = 0;

  if (dists[0] < rDmax[0]) {
    float vl = mapFC(dists[0], rDmin[0], rDmax[0], 0.65, 0);
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
    float vl = mapFC(dists[4], rDmin[0], rDmax[0], 0.65, 0);
    _steer -= vl;
  }



  if (dists[2] < rDmax[2]) {
    _thr -= mapFC(dists[2], rDmin[2], rDmax[2], 0.6, 0);
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


void setThrottleSteer(float _thr, float _str) {
  if (_thr == 0) {
    digitalWrite(motA, LOW);
    digitalWrite(motB, LOW);
    digitalWrite(motPWM, LOW);
  }
  else {
    pwmVal = int(_thr * pwmLimit);
    //Serial.println(pwmVal);
  

    delay(2);
  
    if (_thr > 0) {
      digitalWrite(motA, HIGH);
      digitalWrite(motB, LOW);
      analogWrite(motPWM, pwmVal);
    }
    else if (_thr < 0) {
      digitalWrite(motA, LOW);
      digitalWrite(motB, HIGH);
      analogWrite(motPWM, -pwmVal);
    }
  }

  s.write(90 + _str * steerAngle * steerMultiplier + steerOffset);
}
