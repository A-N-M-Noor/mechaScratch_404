void getDistanceValues() {
  long sonarTimer = millis();
  for (int i = 0; i < 5; i++) {
    dists[i] = getDistS(sPins[i]);
  }
  while (millis() - sonarTimer < 15) { }
}

void printDistanceValues(){
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


void getSerialInfo(){
  if(millis() - serialTimer > 15){
    //Serial.println("SendingData");
    Serial2.print("D");
    serialTimer = millis();
  }
  
  while (Serial2.available()) {
    int val = Serial2.read();
    if(val < 50){
      key = val;
    }else{
      switch(key){
        case 8:
          if(val-50 != turnCount){
            buzzTimer = millis();
          }
          turnCount = val-50;
          break;
        case 9:
          lineAng = val-150;
          break;
        case 10:
          trackDir = val-150;
          break;
      }
    }
  }
}

void printSerialInfo(){
  Serial.print("turnCount: ");
  Serial.print(turnCount);
  Serial.print(" - lineAng: ");
  Serial.print(lineAng);
  Serial.print(" - trackDir: ");
  Serial.println(trackDir);
}

void getMPU(){
  mpu.update();
  currentAngle = mpu.getAngleZ();
}
