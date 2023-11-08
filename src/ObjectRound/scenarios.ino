void handleScenarios() {
  //  trackDir = -1;
  long current_time = millis();
  if (objType == 'N') {
    if (trackDir == -1) {
      if (current_time - turnTimer > 200 && current_time - turnTimer < 2200 && !obstacleIn(10,-trackDir) && current_time - objPastTime > 200) {

        //if (history[0] == 'G' && current_time - turnTimer > 150 && current_time - turnTimer < 3500) { // Scenario 1
        targetSteer = -trackDir * 0.7;
        targetThrottle = 0.4;
        //buzzTimer = millis();
      }
    }
    if (trackDir == 1) {
      if (current_time - turnTimer > 200 && current_time - turnTimer < 2200 && !obstacleIn(10,-trackDir) && current_time - objPastTime > 200) { // Scenario 1
        targetSteer = -trackDir * 0.7;
        targetThrottle = 0.4;
        //buzzTimer = millis();
      }
    }
  }
}

void checkIfU(int dst){
  long current_time = millis();
  if(!passedLastObj){
    if((current_time - turnTimer > 200 && current_time - turnTimer < 3000)){
      if(objType == 'R' && objDist < dst){ // if a red object is in the beginning of the section
        makeUTurn = true;
      }
      if(objType == 'G' && objDist < dst){
        uTurn = false;
      }
      if(objType != 'N' && objDist > dst){
        if(history[1] == 'R'){ //history[0] is the current object
          makeUTurn = true;
          passedLastObj = true;
        }
        if(history[1] == 'G'){
          uTurn = false;
        }
      }
    }
    if(makeUTurn && current_time - lostTimer > 200){
      passedLastObj = true;
      buzzTimer = millis() - 400;
    }
  }
  if(passedLastObj && current_time - turnTimer > 2000){
    doUTurn();
  }
}
