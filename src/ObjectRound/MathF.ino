
float mapF(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float mapFC(float x, float in_min, float in_max, float out_min, float out_max) {
  return clamp( mapF(x, in_min, in_max, out_min, out_max), out_min, out_max);
}

float clamp(float val, float mini, float maxi) {
  float tMin = mini;
  float tMax = maxi;
  if (mini > maxi) {
    tMin = maxi;
    tMax = mini;
  }
  if (val < tMin) {
    return tMin;
  }
  if (val > tMax) {
    return tMax;
  }
  return val;
}

float lerpF(float a, float b, float t)
{
  return a + t * (b - a);
}

int scrPos(char ob){
  if(ob == 'G'){ // remove trcdir
    if(trackDir == -1){
      return(170);
    }
    return 100;
  }
  if(ob == 'R'){
    if(trackDir == 1){
      return(30);
    }
    return(100);
  }
  return(100);
}
