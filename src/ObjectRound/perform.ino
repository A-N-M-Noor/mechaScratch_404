void doUTurn(bool goB){
  Serial2.print("B");
  digitalWrite(buzz, HIGH);
  long tmr = millis();
  while(millis() - tmr < 700){
    setThrottleSteer(-0.6, 1);
    if(obstacleIn(8, 5)){
      setThrottleSteer(-0.6, 0);
      tmr += 700;
    }
  }
  tmr = millis();
  while(millis() - tmr < 1700){
    setThrottleSteer(0.6, -1);
    if(obstacleIn(8, 5)){
      setThrottleSteer(-0.6, 0);
      tmr += 700;
      //delay(700);
    }
  }
  tmr = millis();
  /*while(millis() - tmr < 1000){
    setThrottleSteer(0.35, -1);
    if(obstacleIn(8, 5)){
      setThrottleSteer(-0.4, 0);
      tmr += 700;
      delay(700);
    }
  }*/

  tmr = millis();
  /*while(millis() - tmr < 1000){
    setThrottleSteer(0.35, -1);
    if(objType != 'N'){
      break;
    }
  }*/
  tmr = millis();
  while(millis() - tmr < 400){
    setThrottleSteer(-0.6, 0);
  }
  tmr = millis();
  uTurn = false;
  makeUTurn = false;
  passedLastObj = false;
  Serial2.print("U");
  trackDir *= -1;
  totalTurns = 4;
  turnCount = 0;
  while(millis() - tmr < 800){
    setThrottleSteer(0, 0);
  }
}

void followObj(char obj, int dst){
  while(objType == obj){
    float str = mapFC(objPos, 0, 200, fRangeAcrossX[0], fRangeAcrossX[1]);
    setThrottleSteer(0.6, str);
    if(objDist <= dst || dists[2] < dst || objType != obj){
      break;
    }
  }
}
