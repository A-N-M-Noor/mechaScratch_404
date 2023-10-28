
void setControls() {
  float _thr = 1;
  float _steer = 0;

  if (dists[0] < rDmax[0]) {
    float vl = mapFC(dists[0], rDmin[0], rDmax[0], 0.55, 0);
    _steer += vl;
  }
  if (dists[1] < rDmax[1]) {
    float vl = mapFC(dists[1], rDmin[1], rDmax[1], 0.45, 0);
    _steer += vl;
  }

  if (dists[3] < rDmax[1]) {
    float vl = mapFC(dists[3], rDmin[1], rDmax[1], 0.45, 0);
    _steer -= vl;
  }
  if (dists[4] < rDmax[0]) {
    float vl = mapFC(dists[4], rDmin[0], rDmax[0], 0.55, 0);
    _steer -= vl;
  }

  

  if (dists[2] < rDmax[2]) {
    _thr -= mapFC(dists[2], rDmin[2], rDmax[2], 0.6, 0);
  }
  if(dists[2] < rDmax[3]){
    _steer *= mapFC(dists[2], rDmin[2], rDmax[3], 2, 1);
  }
  
  targetThrottle = _thr;
  targetSteer = _steer;
}

/*
void setControls() {
  float _thr = 1;
  float _steer = 0;

  int dS = dists[0] - dists[4];
  float dsS = mapFC(abs(dS), 0, rDdelta[0], 0.5, 0);
  _steer += dsS * (dS/abs(dS));

  dS = dists[1] - dists[3];
  dsS = mapFC(abs(dS), 0, rDdelta[1], 0.7, 0);
  _steer += dsS * (dS/abs(dS));

  if (dists[2] < rDmax[2]) {
    _thr -= mapFC(dists[2], rDmin[2], rDmax[2], 1, 0);
    _steer *= mapFC(dists[2], rDmin[2], rDmax[2]*3, 3.5, 1);
  }
  throttle = lerpF(throttle, _thr, throttleSmoothing);
  steer = lerpF(steer, _steer, steerSmoothing);
}
*/
void thrFromStr(){
  targetThrottle *= mapFC(abs(targetSteer), 0, 1, 1, 0.6);
}


void setThrottleSteer(float _thr, float _str) {
  if (_thr == 0) {
    digitalWrite(motA, LOW);
    digitalWrite(motB, LOW);
  }
  else{
  _thr = _thr * throttleMult;
  pwmVal = int(_thr * 255);
  //Serial.println(pwmVal);
  }
  
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

  s.write(90 + _str * steerAngle * steerMultiplier + steerOffset);
}
