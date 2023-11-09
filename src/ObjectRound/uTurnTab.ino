void checkFU() {
  if (turnCount == 8) {
    if (objType == 'G' && objDist < 65) {
      uTurn = false;
    }
    if (objType == 'R' && objDist < 65) {
      makeUTurn = true;
      uTurn = false;
      uTurnTimer = millis();
    }
    if(objType != 'N' && objDist > 65){
      if(lstObj7 == 'R'){
        makeUTurn = true;
        uTurn = false;
        uTurnTimer = millis();
      }
    }
  }
  if (turnCount == 7) {
    Serial2.print("L");
  }
}
